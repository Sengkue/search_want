from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import case
from sqlalchemy.orm import Session, joinedload

from app.core.deps import require_admin
from app.db.database import get_db
from app.db.models import ApprovalLog, Notification, Shop, User
from app.schemas.schemas import AdminDecisionRequest, AdminStatsOut, ApprovalLogOut, ShopOut
from app.services.serializer import shop_to_out

router = APIRouter(prefix="/api/admin", tags=["Admin Moderation"])


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

