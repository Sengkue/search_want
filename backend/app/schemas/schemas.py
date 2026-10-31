from datetime import datetime
import re
from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserRegister(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=6, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=150)
    phone: str | None = Field(default=None, max_length=60)


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    phone: str | None = None
    role: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ProblemKeywordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    keyword: str
    symptom_label: str
    advice_hint: str


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    icon: str
    color: str
    description: str
    shop_count: int = 0


class ShopCreate(BaseModel):
    category_id: int
    name: str = Field(..., min_length=2, max_length=160)
    description: str = Field(..., min_length=5, max_length=2000)
    problem_tags: str = Field(default="", max_length=600)
    phone: str = Field(..., min_length=3, max_length=60)
    address: str = Field(..., min_length=3, max_length=350)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    opening_hours: str = Field(default="08:00 - 18:00", max_length=120)
    is_emergency_24h: bool = False


class ShopUpdate(ShopCreate):
    pass


class ApprovalLogOut(BaseModel):
    id: int
    shop_id: int
    admin_id: int
    admin_name: str
    action: str
    note: str | None = None
    created_at: datetime


class ShopOut(BaseModel):
    id: int
    owner_id: int
    owner_name: str
    owner_email: str | None = None
    category_id: int
    category_name: str
    category_slug: str
    category_icon: str
    category_color: str
    name: str
    description: str
    problem_tags: str
    phone: str
    address: str
    latitude: float
    longitude: float
    opening_hours: str
    is_emergency_24h: bool
    status: str
    rejection_reason: str | None = None
    distance_km: float | None = None
    match_score: int = 0
    matched_reasons: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class DiagnosisResult(BaseModel):
    query: str
    matched_categories: list[CategoryOut] = Field(default_factory=list)
    symptom_labels: list[str] = Field(default_factory=list)
    advice_hints: list[str] = Field(default_factory=list)
    notification_summary: str


class NearbySearchResponse(BaseModel):
    diagnosis: DiagnosisResult
    total_found: int
    radius_km: float | None = None
    user_lat: float | None = None
    user_lng: float | None = None
    shops: list[ShopOut]


class AdminDecisionRequest(BaseModel):
    action: str = Field(..., pattern="^(APPROVE|REJECT|SUSPEND)$")
    note: str | None = Field(default=None, max_length=1000)


class AdminStatsOut(BaseModel):
    pending_count: int
    approved_count: int
    rejected_count: int
    suspended_count: int
    total_users: int


class SeedNearbyRequest(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    area_name: str = Field(default="Your Area", max_length=120)


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    message: str
    notif_type: str
    link_url: str | None = None
    is_read: bool
    created_at: datetime


_ADSENSE_PUB_RE = re.compile(r"^ca-pub-\d{16}$")
_ADSENSE_SHORT_PUB_RE = re.compile(r"^pub-\d{16}$")
_ADSENSE_SLOT_RE = re.compile(r"^\d{6,20}$")


class AdSenseConfigUpdate(BaseModel):
    enabled: bool = True
    client_id: str = Field(default="", max_length=64)
    slot_infeed: str = Field(default="", max_length=64)
    slot_banner: str = Field(default="", max_length=64)
    auto_ads: bool = True
    test_mode: bool = True

    @field_validator("client_id")
    @classmethod
    def validate_client_id(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            return ""
        if _ADSENSE_SHORT_PUB_RE.match(cleaned):
            cleaned = f"ca-{cleaned}"
        if not _ADSENSE_PUB_RE.match(cleaned):
            raise ValueError(
                "ລະຫັດ Publisher ID ຕ້ອງເປັນຮູບແບບ ca-pub-1234567890123456 (ຕົວເລກ 16 ຫຼັກ)"
            )
        return cleaned

    @field_validator("slot_infeed", "slot_banner")
    @classmethod
    def validate_slot_id(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            return ""
        if not _ADSENSE_SLOT_RE.match(cleaned):
            raise ValueError(
                "ລະຫັດ Ad Slot ID ຕ້ອງເປັນຕົວເລກ 6-20 ຫຼັກ (ຫຼື ປະວ່າງໄວ້)"
            )
        return cleaned


class AdSenseConfigOut(BaseModel):
    enabled: bool
    client_id: str
    publisher_id: str
    slot_infeed: str
    slot_banner: str
    auto_ads: bool
    test_mode: bool
    ads_txt_line: str
    updated_at: datetime


