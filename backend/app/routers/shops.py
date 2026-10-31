from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.core.deps import get_current_user, get_optional_user
from app.db.database import get_db
from app.db.models import ApprovalLog, Category, Notification, Shop, User
from app.db.seed import seed_shops_around_coordinates
from app.schemas.schemas import (
    NearbySearchResponse,
    SeedNearbyRequest,
    ShopCreate,
    ShopOut,
    ShopUpdate,
)
from app.services.geo import bounding_box, haversine_km
from app.services.matcher import diagnose_problem, score_shop_for_problem
from app.services.serializer import shop_to_out

router = APIRouter(prefix="/api/shops", tags=["Shops & Nearby Discovery"])


@router.get("/nearby", response_model=NearbySearchResponse)
def search_nearby_shops(
    problem: str = Query(default="", max_length=300),
    lat: float | None = Query(default=None, ge=-90.0, le=90.0),
    lng: float | None = Query(default=None, ge=-180.0, le=180.0),
    radius_km: float | None = Query(default=None, ge=0.0, le=25000.0),
    category_id: int | None = Query(default=None),
    emergency_only: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> NearbySearchResponse:
    diagnosis, category_weights, tokens = diagnose_problem(db, problem, category_id)

    query = (
        db.query(Shop)
        .options(joinedload(Shop.category), joinedload(Shop.owner))
        .filter(Shop.status == "APPROVED")
    )

    if category_id is not None:
        query = query.filter(Shop.category_id == category_id)

    if emergency_only:
        query = query.filter(Shop.is_emergency_24h.is_(True))

    effective_radius = radius_km if (radius_km is not None and radius_km > 0) else None
    has_gps = lat is not None and lng is not None

    if has_gps and effective_radius is not None:
        min_lat, max_lat, min_lng, max_lng = bounding_box(lat, lng, effective_radius)
        query = query.filter(
            Shop.latitude >= min_lat,
            Shop.latitude <= max_lat,
            Shop.longitude >= min_lng,
            Shop.longitude <= max_lng,
        )

    candidate_shops = query.all()
    results: list[ShopOut] = []

    for shop in candidate_shops:
        dist: float | None = None
        if has_gps and lat is not None and lng is not None:
            dist = haversine_km(lat, lng, shop.latitude, shop.longitude)
            if effective_radius is not None and dist > effective_radius:
                continue

        score, reasons = score_shop_for_problem(shop, problem, category_weights, tokens)
        if problem.strip() and score <= 0:
            continue

        results.append(
            shop_to_out(
                shop=shop,
                distance_km=dist,
                match_score=score,
                matched_reasons=reasons,
            )
        )

    if has_gps:
        results.sort(
            key=lambda s: (
                0 if s.match_score >= 30 else 1,
                s.distance_km if s.distance_km is not None else 999999.0,
                -s.match_score,
            )
        )
    else:
        results.sort(key=lambda s: (-s.match_score, -s.id))

    if results:
        if has_gps and results[0].distance_km is not None:
            nearest = results[0]
            diagnosis.notification_summary = (
                f"ພົບ {len(results)} ຮ້ານທີ່ກົງກັບບັນຫາໃກ້ທ່ານ! "
                f"ໃກ້ທີ່ສຸດ: {nearest.name} (ຫ່າງ {nearest.distance_km} ກມ.)"
            )
        else:
            diagnosis.notification_summary = (
                f"ພົບ {len(results)} ຮ້ານທີ່ກົງກັບບັນຫາ. "
                "ເປີດ GPS ເພື່ອເບິ່ງໄລຍະທາງທີ່ແນ່ນອນຈາກທ່ານ."
            )
    else:
        if has_gps and effective_radius is not None:
            diagnosis.notification_summary = (
                f"ບໍ່ພົບຮ້ານທີ່ອະນຸມັດແລ້ວ ແລະ ກົງກັບບັນຫາພາຍໃນ {effective_radius:g} ກມ. "
                "ລອງຂະຫຍາຍໄລຍະທາງ ຫຼື ກົດ 'ສ້າງຮ້ານທົດລອງໃກ້ຂ້ອຍ' ເພື່ອທົດສອບໃນພື້ນທີ່ຂອງທ່ານ."
            )
        else:
            diagnosis.notification_summary = (
                "ຍັງບໍ່ພົບຮ້ານທີ່ອະນຸມັດແລ້ວ ແລະ ກົງກັບເງື່ອນໄຂນີ້. ລອງໃຊ້ຄຳຄົ້ນຫາທີ່ກວ້າງຂຶ້ນ ຫຼື ເລືອກໝວດໝູ່ອື່ນ."
            )

    return NearbySearchResponse(
        diagnosis=diagnosis,
        total_found=len(results),
        radius_km=effective_radius,
        user_lat=lat,
        user_lng=lng,
        shops=results,
    )


@router.get("/mine", response_model=list[ShopOut])
def list_my_shops(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ShopOut]:
    shops = (
        db.query(Shop)
        .options(joinedload(Shop.category), joinedload(Shop.owner))
        .filter(Shop.owner_id == current_user.id)
        .order_by(Shop.created_at.desc())
        .all()
    )
    return [shop_to_out(s) for s in shops]


@router.post("", response_model=ShopOut, status_code=status.HTTP_201_CREATED)
def submit_new_shop(
    payload: ShopCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ShopOut:
    category = db.query(Category).filter(Category.id == payload.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ບໍ່ພົບໝວດໝູ່ຮ້ານທີ່ເລືອກ.",
        )

    shop = Shop(
        owner_id=current_user.id,
        category_id=payload.category_id,
        name=payload.name.strip(),
        description=payload.description.strip(),
        problem_tags=payload.problem_tags.strip(),
        phone=payload.phone.strip(),
        address=payload.address.strip(),
        latitude=round(payload.latitude, 6),
        longitude=round(payload.longitude, 6),
        opening_hours=payload.opening_hours.strip(),
        is_emergency_24h=payload.is_emergency_24h,
        status="PENDING",
    )
    db.add(shop)

    if current_user.role == "USER":
        current_user.role = "SHOP_OWNER"

    # Notify all Admins to review & approve
    admins = db.query(User).filter(User.role == "ADMIN").all()
    for admin in admins:
        db.add(
            Notification(
                user_id=admin.id,
                title=f"ມີຮ້ານໃໝ່ລໍຖ້າການອະນຸມັດ: {shop.name}",
                message=f"{current_user.full_name} ໄດ້ປັກໝຸດ '{shop.name}' ({category.name}) ທີ່ {shop.address}. ກະລຸນາກວດສອບ ແລະ ອະນຸມັດ.",
                notif_type="SHOP_PENDING",
                link_url="/admin/approvals",
            )
        )

    # Confirmation notification for owner
    db.add(
        Notification(
            user_id=current_user.id,
            title=f"ສົ່ງຮ້ານແລ້ວ: {shop.name}",
            message="ຕຳແໜ່ງຮ້ານຂອງທ່ານກຳລັງລໍຖ້າການອະນຸມັດຈາກຜູ້ດູແລລະບົບ. ທ່ານຈະໄດ້ຮັບແຈ້ງເຕືອນທັນທີທີ່ຮ້ານເປີດສະແດງ!",
            notif_type="INFO",
            link_url="/shops/mine",
        )
    )

    db.commit()
    db.refresh(shop)
    return shop_to_out(shop)


@router.put("/{shop_id}", response_model=ShopOut)
def update_my_shop(
    shop_id: int,
    payload: ShopUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ShopOut:
    shop = (
        db.query(Shop)
        .options(joinedload(Shop.category), joinedload(Shop.owner))
        .filter(Shop.id == shop_id)
        .first()
    )
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ບໍ່ພົບຮ້ານນີ້.")

    if shop.owner_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ທ່ານແກ້ໄຂໄດ້ສະເພາະຮ້ານຂອງທ່ານເອງ.",
        )

    category = db.query(Category).filter(Category.id == payload.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ບໍ່ພົບໝວດໝູ່ຮ້ານທີ່ເລືອກ.",
        )

    shop.category_id = payload.category_id
    shop.name = payload.name.strip()
    shop.description = payload.description.strip()
    shop.problem_tags = payload.problem_tags.strip()
    shop.phone = payload.phone.strip()
    shop.address = payload.address.strip()
    shop.latitude = round(payload.latitude, 6)
    shop.longitude = round(payload.longitude, 6)
    shop.opening_hours = payload.opening_hours.strip()
    shop.is_emergency_24h = payload.is_emergency_24h

    if current_user.role != "ADMIN":
        shop.status = "PENDING"
        shop.rejection_reason = None

        db.add(
            ApprovalLog(
                shop_id=shop.id,
                admin_id=current_user.id,
                action="RESUBMITTED",
                note="ເຈົ້າຂອງຮ້ານໄດ້ແກ້ໄຂລາຍລະອຽດ/ຕຳແໜ່ງຮ້ານ ແລະ ສົ່ງຂໍອະນຸມັດໃໝ່.",
            )
        )
        admins = db.query(User).filter(User.role == "ADMIN").all()
        for admin in admins:
            db.add(
                Notification(
                    user_id=admin.id,
                    title=f"ຮ້ານຖືກສົ່ງຂໍອະນຸມັດໃໝ່: {shop.name}",
                    message=f"{current_user.full_name} ໄດ້ແກ້ໄຂ '{shop.name}' ແລະ ສົ່ງຂໍການອະນຸມັດໃໝ່.",
                    notif_type="SHOP_PENDING",
                    link_url="/admin/approvals",
                )
            )

    db.commit()
    db.refresh(shop)
    return shop_to_out(shop)


@router.post("/seed-nearby")
def seed_demo_shops_near_user(
    payload: SeedNearbyRequest,
    db: Session = Depends(get_db),
) -> dict[str, int | str]:
    owner = db.query(User).filter(User.email == "owner@searchwant.com").first()
    admin = db.query(User).filter(User.role == "ADMIN").first()
    if not owner:
        raise HTTPException(status_code=500, detail="ບໍ່ພົບບັນຊີເຈົ້າຂອງຮ້ານທົດລອງ.")

    area_tag = f"{payload.area_name.strip()} {round(payload.latitude, 2)},{round(payload.longitude, 2)}"
    created = seed_shops_around_coordinates(
        db=db,
        center_lat=payload.latitude,
        center_lng=payload.longitude,
        area_name=area_tag,
        owner=owner,
        admin=admin,
    )
    return {
        "created_count": created,
        "message": (
            f"ສ້າງຮ້ານທົດລອງ {created} ຮ້ານ (ອະນຸມັດແລ້ວ 7 ຮ້ານ + ລໍຖ້າການອະນຸມັດ 2 ຮ້ານ) ອ້ອມຮອບຕຳແໜ່ງຂອງທ່ານແລ້ວ!"
            if created > 0
            else "ມີຮ້ານທົດລອງອ້ອມຮອບພິກັດນີ້ຢູ່ແລ້ວ!"
        ),
    }


@router.get("/{shop_id}", response_model=ShopOut)
def get_shop_detail(
    shop_id: int,
    current_user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> ShopOut:
    shop = (
        db.query(Shop)
        .options(joinedload(Shop.category), joinedload(Shop.owner))
        .filter(Shop.id == shop_id)
        .first()
    )
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ບໍ່ພົບຮ້ານນີ້.")

    if shop.status != "APPROVED":
        if not current_user or (current_user.id != shop.owner_id and current_user.role != "ADMIN"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ຮ້ານນີ້ກຳລັງລໍຖ້າການອະນຸມັດຈາກຜູ້ດູແລລະບົບ.",
            )

    return shop_to_out(shop)

