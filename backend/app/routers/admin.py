from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import case, func, or_
from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.core.deps import require_admin, require_super_admin
from app.core.permissions import ROLE_ADMIN, ROLE_SHOP_OWNER, ROLE_SUPER_ADMIN, ROLE_USER
from app.db.database import get_db
from app.db.models import ApprovalLog, Notification, Shop, User
from app.db.seed import count_active_weak_demo_accounts, disable_weak_demo_accounts, is_demo_email
from app.routers.adsense import get_or_create_adsense_setting
from app.schemas.schemas import (
    AdminDecisionRequest,
    AdminRoleUpdateRequest,
    AdminStatsOut,
    AdminStatusUpdateRequest,
    AdminUserOut,
    ApprovalLogOut,
    SecurityAuditOut,
    SecurityCheckItem,
    ShopOut,
)
from app.services.serializer import shop_to_out

router = APIRouter(prefix="/api/admin", tags=["Admin Moderation & RBAC"])

_ROLE_LABELS_LAO: dict[str, str] = {
    ROLE_USER: "ຜູ້ໃຊ້ທົ່ວໄປ",
    ROLE_SHOP_OWNER: "ເຈົ້າຂອງຮ້ານ",
    ROLE_ADMIN: "ຜູ້ດູແລອະນຸມັດຮ້ານ",
    ROLE_SUPER_ADMIN: "ຜູ້ບໍລິຫານສູງສຸດ",
}


@router.get("/stats", response_model=AdminStatsOut)
def get_admin_stats(
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> AdminStatsOut:
    return AdminStatsOut(
        pending_count=db.query(Shop).filter(Shop.status == "PENDING").count(),
        approved_count=db.query(Shop).filter(Shop.status == "APPROVED").count(),
        rejected_count=db.query(Shop).filter(Shop.status == "REJECTED").count(),
        suspended_count=db.query(Shop).filter(Shop.status == "SUSPENDED").count(),
        total_users=db.query(User).count(),
    )


@router.get("/shops", response_model=list[ShopOut])
def list_shops_for_moderation(
    status_filter: str | None = Query(default=None, alias="status"),
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> list[ShopOut]:
    query = db.query(Shop).options(joinedload(Shop.category), joinedload(Shop.owner))
    if status_filter and status_filter.upper() != "ALL":
        query = query.filter(Shop.status == status_filter.upper())

    priority_order = case(
        (Shop.status == "PENDING", 0),
        (Shop.status == "REJECTED", 1),
        (Shop.status == "APPROVED", 2),
        else_=3,
    )
    shops = query.order_by(priority_order, Shop.created_at.desc()).all()
    return [shop_to_out(s, include_owner_email=True) for s in shops]


@router.post("/shops/{shop_id}/decision", response_model=ShopOut)
def review_shop_submission(
    shop_id: int,
    payload: AdminDecisionRequest,
    admin_user: User = Depends(require_admin),
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

    action = payload.action.upper()
    note = payload.note.strip() if payload.note else None

    if action == "APPROVE":
        shop.status = "APPROVED"
        shop.rejection_reason = None
        log_action = "APPROVED"
        notif_title = f"ຮ້ານໄດ້ຮັບການອະນຸມັດ: {shop.name}"
        notif_msg = (
            f"ຂ່າວດີ! ຜູ້ດູແລລະບົບໄດ້ອະນຸມັດ '{shop.name}' ແລ້ວ. "
            "ຕຳແໜ່ງຮ້ານຂອງທ່ານເປີດສະແດງຢູ່ເທິງແຜນທີ່ໃຫ້ລູກຄ້າໃກ້ຄຽງເຫັນແລ້ວ!"
        )
        notif_type = "SHOP_APPROVED"
    elif action == "REJECT":
        shop.status = "REJECTED"
        shop.rejection_reason = note or "ກະລຸນາແກ້ໄຂລາຍລະອຽດຮ້ານ ແລະ ກວດສອບຈຸດປັກໝຸດຢູ່ແຜນທີ່."
        log_action = "REJECTED"
        notif_title = f"ຮ້ານຕ້ອງແກ້ໄຂ: {shop.name}"
        notif_msg = f"ຜູ້ດູແລລະບົບໄດ້ກວດສອບ '{shop.name}' ແລະ ຂໍໃຫ້ແກ້ໄຂ: {shop.rejection_reason}"
        notif_type = "SHOP_REJECTED"
    else:
        shop.status = "SUSPENDED"
        shop.rejection_reason = note or "ຜູ້ດູແລລະບົບໄດ້ຢຸດການສະແດງຮ້ານຊົ່ວຄາວ."
        log_action = "SUSPENDED"
        notif_title = f"ຮ້ານຖືກຢຸດຊົ່ວຄາວ: {shop.name}"
        notif_msg = f"ຜູ້ດູແລລະບົບໄດ້ຢຸດການສະແດງ '{shop.name}' ຊົ່ວຄາວ. ເຫດຜົນ: {shop.rejection_reason}"
        notif_type = "SHOP_REJECTED"

    shop.reviewed_by_id = admin_user.id
    shop.reviewed_at = datetime.now(timezone.utc)

    db.add(
        ApprovalLog(
            shop_id=shop.id,
            admin_id=admin_user.id,
            action=log_action,
            note=note,
        )
    )

    db.add(
        Notification(
            user_id=shop.owner_id,
            title=notif_title,
            message=notif_msg,
            notif_type=notif_type,
            link_url="/shops/mine",
        )
    )

    db.commit()
    db.refresh(shop)
    return shop_to_out(shop, include_owner_email=True)


@router.get("/logs", response_model=list[ApprovalLogOut])
def list_approval_logs(
    limit: int = Query(default=30, ge=1, le=200),
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> list[ApprovalLogOut]:
    logs = (
        db.query(ApprovalLog)
        .options(joinedload(ApprovalLog.admin))
        .order_by(ApprovalLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        ApprovalLogOut(
            id=lg.id,
            shop_id=lg.shop_id,
            admin_id=lg.admin_id,
            admin_name=lg.admin.full_name if lg.admin else "Admin",
            action=lg.action,
            note=lg.note,
            created_at=lg.created_at,
        )
        for lg in logs
    ]


# ==============================================================================
# SUPER ADMIN ONLY: High-Level User Role Management (RBAC) & Production Security
# ==============================================================================


def _serialize_admin_user(user: User, shops_count: int = 0) -> AdminUserOut:
    return AdminUserOut(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        role=user.role,
        is_active=user.is_active,
        shops_count=shops_count,
        is_demo_account=is_demo_email(user.email),
        created_at=user.created_at,
    )


@router.get("/users", response_model=list[AdminUserOut])
def list_users_for_rbac(
    q: str | None = Query(default=None, max_length=120),
    role: str | None = Query(default=None, max_length=30),
    _super_admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
) -> list[AdminUserOut]:
    shop_counts = dict(
        db.query(Shop.owner_id, func.count(Shop.id)).group_by(Shop.owner_id).all()
    )

    query = db.query(User)
    if q and q.strip():
        pattern = f"%{q.strip()}%"
        query = query.filter(
            or_(
                User.email.ilike(pattern),
                User.full_name.ilike(pattern),
            )
        )
    if role and role.upper() != "ALL":
        query = query.filter(User.role == role.upper())

    role_order = case(
        (User.role == ROLE_SUPER_ADMIN, 0),
        (User.role == ROLE_ADMIN, 1),
        (User.role == ROLE_SHOP_OWNER, 2),
        else_=3,
    )
    users = query.order_by(role_order, User.created_at.desc()).all()
    return [_serialize_admin_user(u, shop_counts.get(u.id, 0)) for u in users]


@router.patch("/users/{user_id}/role", response_model=AdminUserOut)
def update_user_role(
    user_id: int,
    payload: AdminRoleUpdateRequest,
    super_admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
) -> AdminUserOut:
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ບໍ່ພົບຜູ້ໃຊ້ນີ້.")

    new_role = payload.role.upper()
    if target.id == super_admin.id and new_role != ROLE_SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ບໍ່ສາມາດຫຼຸດລະດັບສິດຂອງບັນຊີຕົນເອງໄດ້ ເພື່ອປ້ອງກັນການລັອກອອກຈາກລະບົບ.",
        )

    if target.role == ROLE_SUPER_ADMIN and new_role != ROLE_SUPER_ADMIN:
        active_supers = (
            db.query(User)
            .filter(User.role == ROLE_SUPER_ADMIN, User.is_active.is_(True))
            .count()
        )
        if active_supers <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ຕ້ອງມີຜູ້ບໍລິຫານສູງສຸດ (Super Admin) ທີ່ເປີດໃຊ້ງານຢ່າງໜ້ອຍ 1 ບັນຊີສະເໝີ.",
            )

    if target.role != new_role:
        old_label = _ROLE_LABELS_LAO.get(target.role, target.role)
        new_label = _ROLE_LABELS_LAO.get(new_role, new_role)
        target.role = new_role
        # Increment token_version so old JWTs with previous role claims are invalidated immediately
        target.token_version = (target.token_version or 1) + 1

        db.add(
            Notification(
                user_id=target.id,
                title=f"ອັບເດດລະດັບສິດບັນຊີ: {new_label}",
                message=f"ຜູ້ບໍລິຫານສູງສຸດໄດ້ປ່ຽນສິດບັນຊີຂອງທ່ານຈາກ '{old_label}' ເປັນ '{new_label}'.",
                notif_type="INFO",
                link_url="/",
            )
        )
        db.commit()
        db.refresh(target)

    shops_count = db.query(Shop).filter(Shop.owner_id == target.id).count()
    return _serialize_admin_user(target, shops_count)


@router.patch("/users/{user_id}/status", response_model=AdminUserOut)
def update_user_active_status(
    user_id: int,
    payload: AdminStatusUpdateRequest,
    super_admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
) -> AdminUserOut:
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ບໍ່ພົບຜູ້ໃຊ້ນີ້.")

    if target.id == super_admin.id and not payload.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ບໍ່ສາມາດລະງັບບັນຊີຂອງຕົນເອງໄດ້.",
        )

    if target.role == ROLE_SUPER_ADMIN and not payload.is_active:
        active_supers = (
            db.query(User)
            .filter(User.role == ROLE_SUPER_ADMIN, User.is_active.is_(True))
            .count()
        )
        if active_supers <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ບໍ່ສາມາດລະງັບຜູ້ບໍລິຫານສູງສຸດຄົນສຸດທ້າຍຂອງລະບົບໄດ້.",
            )

    target.is_active = payload.is_active
    # Revoke any active sessions immediately
    target.token_version = (target.token_version or 1) + 1
    db.commit()
    db.refresh(target)

    shops_count = db.query(Shop).filter(Shop.owner_id == target.id).count()
    return _serialize_admin_user(target, shops_count)


@router.get("/security-audit", response_model=SecurityAuditOut)
def get_production_security_audit(
    _super_admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
) -> SecurityAuditOut:
    adsense_row = get_or_create_adsense_setting(db)
    adsense_live = bool(
        adsense_row.enabled and adsense_row.client_id and not adsense_row.test_mode
    )
    strong_secret = settings.has_strong_secret_key()
    cors_restricted = settings.is_cors_restricted()
    weak_demos = count_active_weak_demo_accounts(db)

    super_count = db.query(User).filter(User.role == ROLE_SUPER_ADMIN, User.is_active.is_(True)).count()
    admin_count = db.query(User).filter(User.role == ROLE_ADMIN, User.is_active.is_(True)).count()
    owner_count = db.query(User).filter(User.role == ROLE_SHOP_OWNER, User.is_active.is_(True)).count()
    user_count = db.query(User).filter(User.role == ROLE_USER, User.is_active.is_(True)).count()

    checks = [
        SecurityCheckItem(
            key="app_env",
            label="ໂໝດເຊີບເວີ Production (SEARCH_WANT_ENV=production)",
            passed=settings.IS_PRODUCTION,
            severity="warning",
            recommendation="ເມື່ອນຳຂຶ້ນເຊີບເວີຈິງ ໃຫ້ຕັ້ງ SEARCH_WANT_ENV=production ໃນໄຟລ໌ .env",
        ),
        SecurityCheckItem(
            key="strong_secret",
            label="ລະຫັດລັບເຊັນ JWT Token ປອດໄພ (SEARCH_WANT_SECRET_KEY >= 32 ຕົວອັກສອນ)",
            passed=strong_secret,
            severity="critical",
            recommendation="ຕັ້ງ SEARCH_WANT_SECRET_KEY ເປັນລະຫັດສຸ່ມຍາວຢ່າງໜ້ອຍ 32 ຕົວອັກສອນ ກ່ອນຂຶ້ນ Production",
        ),
        SecurityCheckItem(
            key="demo_mode_off",
            label="ປິດປຸ່ມລ໊ອກອິນທົດລອງ 1 ຄລິກ & ປິດສ້າງຮ້ານທົດລອງ (DEMO_MODE=false)",
            passed=not settings.DEMO_MODE,
            severity="critical",
            recommendation="ລະບົບຈະປິດອັດຕະໂນມັດທັນທີເມື່ອຕັ້ງ SEARCH_WANT_ENV=production (ຫຼື SEARCH_WANT_DEMO_MODE=false)",
        ),
        SecurityCheckItem(
            key="weak_demo_accounts",
            label="ບໍ່ມີບັນຊີທົດລອງທີ່ໃຊ້ລະຫັດຜ່ານເລີ່ມຕົ້ນ (admin123 / owner123 / user123)",
            passed=weak_demos == 0,
            severity="critical",
            recommendation="ປ່ຽນລະຫັດຜ່ານຜູ້ບໍລິຫານ ແລະ ກົດປຸ່ມ 'ລະງັບບັນຊີທົດລອງ' (ຫຼື ຕັ້ງ SEARCH_WANT_ENV=production ເພື່ອປິດອັດຕະໂນມັດ)",
        ),
        SecurityCheckItem(
            key="docs_disabled",
            label="ເຊື່ອງໜ້າເອກະສານ API (/docs & /openapi.json) ຈາກສາທາລະນະ",
            passed=not settings.ENABLE_DOCS,
            severity="warning",
            recommendation="ລະບົບຈະປິດ /docs ອັດຕະໂນມັດເມື່ອຕັ້ງ SEARCH_WANT_ENV=production",
        ),
        SecurityCheckItem(
            key="cors_restricted",
            label="ຈຳກັດໂດເມນ CORS ສະເພາະເວັບໄຊຈິງ (SEARCH_WANT_CORS_ORIGINS)",
            passed=cors_restricted,
            severity="warning",
            recommendation="ຕັ້ງ SEARCH_WANT_CORS_ORIGINS=https://your-domain.la ໃນ Production",
        ),
        SecurityCheckItem(
            key="adsense_live",
            label="Google AdSense ພ້ອມຮັບໂຄສະນາຈິງ (ປິດໂໝດທົດລອງ Preview Mode)",
            passed=adsense_live,
            severity="info",
            recommendation="ເມື່ອ Google ອະນຸມັດໂດເມນເປັນ Ready ແລ້ວ ໃຫ້ປິດ 'ໂໝດທົດລອງ' ໃນແຖບ ໂຄສະນາ AdSense",
        ),
    ]

    return SecurityAuditOut(
        app_env=settings.APP_ENV,
        is_production=settings.IS_PRODUCTION,
        demo_mode=settings.DEMO_MODE,
        enable_docs=settings.ENABLE_DOCS,
        strong_secret_key=strong_secret,
        cors_restricted=cors_restricted,
        adsense_live_mode=adsense_live,
        weak_demo_accounts_count=weak_demos,
        super_admin_count=super_count,
        admin_count=admin_count,
        shop_owner_count=owner_count,
        user_count=user_count,
        checks=checks,
    )


@router.post("/security/disable-demo-accounts")
def disable_demo_accounts_now(
    super_admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
) -> dict[str, int | str]:
    disabled = disable_weak_demo_accounts(db, exclude_user_id=super_admin.id)
    return {
        "disabled_count": disabled,
        "message": (
            f"ລະງັບບັນຊີທົດລອງທີ່ໃຊ້ລະຫັດຜ່ານເລີ່ມຕົ້ນຈຳນວນ {disabled} ບັນຊີແລ້ວ (ຍົກເວັ້ນບັນຊີທີ່ທ່ານກຳລັງໃຊ້ງານຢູ່)."
            if disabled > 0
            else "ບໍ່ພົບບັນຊີທົດລອງອື່ນທີ່ຍັງເປີດໃຊ້ງານດ້ວຍລະຫັດຜ່ານເລີ່ມຕົ້ນ."
        ),
    }
