from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.permissions import ROLE_USER
from app.core.ratelimit import clear_rate_limit_key, enforce_rate_limit, get_client_ip
from app.core.security import create_access_token, hash_password, verify_password
from app.db.database import get_db
from app.db.models import Notification, User
from app.db.seed import DEMO_ACCOUNT_DEFAULTS
from app.schemas.schemas import (
    PasswordChangeRequest,
    PublicSecurityConfigOut,
    TokenResponse,
    UserLogin,
    UserOut,
    UserRegister,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.get("/public-config", response_model=PublicSecurityConfigOut)
def get_public_security_config() -> PublicSecurityConfigOut:
    return PublicSecurityConfigOut(
        app_env=settings.APP_ENV,
        is_production=settings.IS_PRODUCTION,
        demo_mode=settings.DEMO_MODE,
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    payload: UserRegister,
    request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    client_ip = get_client_ip(request)
    enforce_rate_limit(
        bucket="auth_register",
        key=client_ip,
        max_requests=15,
        window_seconds=600,
        detail="ມີການສ້າງບັນຊີຫຼາຍເກີນໄປຈາກເຄືອຂ່າຍນີ້ ກະລຸນາລໍຖ້າສັກຄູ່.",
    )

    norm_email = payload.email.strip().lower()
    if "@" not in norm_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ກະລຸນາໃສ່ອີເມວທີ່ຖືກຕ້ອງ.",
        )

    existing = db.query(User).filter(User.email == norm_email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ມີບັນຊີທີ່ໃຊ້ອີເມວນີ້ແລ້ວ.",
        )

    # Self-registration is ALWAYS locked to the lowest privilege role ("USER")
    user = User(
        email=norm_email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name.strip(),
        phone=payload.phone.strip() if payload.phone else None,
        role=ROLE_USER,
        is_active=True,
        token_version=1,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    db.add(
        Notification(
            user_id=user.id,
            title="ຍິນດີຕ້ອນຮັບສູ່ Search-Want!",
            message="ບອກບັນຫາຂອງທ່ານເພື່ອຄົ້ນຫາຮ້ານທີ່ອະນຸມັດແລ້ວໃກ້ຄຽງ ຫຼື ປັກໝຸດຮ້ານຂອງທ່ານເພື່ອລໍຖ້າການອະນຸມັດຈາກຜູ້ດູແລລະບົບ.",
            notif_type="INFO",
            link_url="/",
        )
    )
    db.commit()

    token = create_access_token(
        user_id=user.id,
        role=user.role,
        token_version=user.token_version,
    )
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login_user(
    payload: UserLogin,
    request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    norm_email = payload.email.strip().lower()
    fail_key = f"{get_client_ip(request)}:{norm_email}"

    user = db.query(User).filter(User.email == norm_email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        enforce_rate_limit(
            bucket="auth_login_fail",
            key=fail_key,
            max_requests=10,
            window_seconds=300,
            detail="ພະຍາຍາມເຂົ້າສູ່ລະບົບຜິດຫຼາຍຄັ້ງເກີນໄປ ກະລຸນາລໍຖ້າ 5 ນາທີແລ້ວລອງໃໝ່.",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ອີເມວ ຫຼື ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ.",
        )

    # Block known weak demo passwords in Production even if DB rows exist
    if (
        settings.IS_PRODUCTION
        and not settings.DEMO_MODE
        and norm_email in DEMO_ACCOUNT_DEFAULTS
        and payload.password == DEMO_ACCOUNT_DEFAULTS[norm_email][0]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ບັນຊີທົດລອງຖືກປິດໃຊ້ງານໃນໂໝດ Production ເພື່ອຄວາມປອດໄພ.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ບັນຊີນີ້ຖືກລະງັບການໃຊ້ງານຊົ່ວຄາວ. ກະລຸນາຕິດຕໍ່ຜູ້ບໍລິຫານລະບົບ.",
        )

    clear_rate_limit_key("auth_login_fail", fail_key)
    token = create_access_token(
        user_id=user.id,
        role=user.role,
        token_version=user.token_version or 1,
    )
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(current_user)


@router.post("/change-password", response_model=TokenResponse)
def change_my_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TokenResponse:
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ລະຫັດຜ່ານປັດຈຸບັນບໍ່ຖືກຕ້ອງ.",
        )
    if payload.new_password == payload.current_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ລະຫັດຜ່ານໃໝ່ຕ້ອງບໍ່ຊ້ຳກັບລະຫັດຜ່ານເກົ່າ.",
        )

    current_user.password_hash = hash_password(payload.new_password)
    # Increment token_version so any older JWT tokens on other devices expire immediately
    current_user.token_version = (current_user.token_version or 1) + 1
    db.commit()
    db.refresh(current_user)

    fresh_token = create_access_token(
        user_id=current_user.id,
        role=current_user.role,
        token_version=current_user.token_version,
    )
    return TokenResponse(access_token=fresh_token, user=UserOut.model_validate(current_user))
