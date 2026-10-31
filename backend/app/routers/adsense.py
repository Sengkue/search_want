from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import require_admin
from app.db.database import get_db
from app.db.models import AdSenseSetting, User, utc_now
from app.schemas.schemas import AdSenseConfigOut, AdSenseConfigUpdate

router = APIRouter(tags=["Google AdSense"])

_GOOGLE_TAG_AUTHORITY_ID = "f08c47fec0942fa0"


def get_or_create_adsense_setting(db: Session) -> AdSenseSetting:
    bind = db.get_bind()
    AdSenseSetting.__table__.create(bind=bind, checkfirst=True)
    row = db.query(AdSenseSetting).order_by(AdSenseSetting.id.asc()).first()
    if row is None:
        raw_client = settings.ADSENSE_CLIENT_ID.strip()
        if raw_client.startswith("pub-") and len(raw_client) == 20:
            raw_client = f"ca-{raw_client}"
        row = AdSenseSetting(
            enabled=True,
            client_id=raw_client,
            slot_infeed=settings.ADSENSE_SLOT_INFEED.strip(),
            slot_banner=settings.ADSENSE_SLOT_BANNER.strip(),
            auto_ads=True,
            test_mode=not bool(raw_client),
        )
        db.add(row)
        db.commit()
        db.refresh(row)
    return row


def serialize_adsense_setting(row: AdSenseSetting) -> AdSenseConfigOut:
    publisher_id = (
        row.client_id.removeprefix("ca-")
        if row.client_id and row.client_id.startswith("ca-pub-")
        else ""
    )
    ads_txt_line = (
        f"google.com, {publisher_id}, DIRECT, {_GOOGLE_TAG_AUTHORITY_ID}"
        if publisher_id
        else "# Configure Google AdSense Publisher ID (ca-pub-XXXXXXXXXXXXXXXX) in Search-Want Admin Console"
    )
    return AdSenseConfigOut(
        enabled=row.enabled,
        client_id=row.client_id,
        publisher_id=publisher_id,
        slot_infeed=row.slot_infeed,
        slot_banner=row.slot_banner,
        auto_ads=row.auto_ads,
        test_mode=row.test_mode,
        ads_txt_line=ads_txt_line,
        updated_at=row.updated_at,
    )


@router.get("/api/adsense/config", response_model=AdSenseConfigOut)
def get_adsense_config(db: Session = Depends(get_db)) -> AdSenseConfigOut:
    row = get_or_create_adsense_setting(db)
    return serialize_adsense_setting(row)


@router.put("/api/admin/adsense", response_model=AdSenseConfigOut)
def update_adsense_config(
    payload: AdSenseConfigUpdate,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> AdSenseConfigOut:
    row = get_or_create_adsense_setting(db)
    row.enabled = payload.enabled
    row.client_id = payload.client_id
    row.slot_infeed = payload.slot_infeed
    row.slot_banner = payload.slot_banner
    row.auto_ads = payload.auto_ads
    row.test_mode = payload.test_mode
    row.updated_at = utc_now()
    db.commit()
    db.refresh(row)
    return serialize_adsense_setting(row)


@router.get("/ads.txt", response_class=PlainTextResponse)
def get_ads_txt(db: Session = Depends(get_db)) -> PlainTextResponse:
    row = get_or_create_adsense_setting(db)
    cfg = serialize_adsense_setting(row)
    return PlainTextResponse(content=f"{cfg.ads_txt_line}\n", media_type="text/plain; charset=utf-8")
