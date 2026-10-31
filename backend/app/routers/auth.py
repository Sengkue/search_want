from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.database import get_db
from app.db.models import Notification, User
from app.schemas.schemas import TokenResponse, UserLogin, UserOut, UserRegister

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegister, db: Session = Depends(get_db)) -> TokenResponse:
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

    user = User(
        email=norm_email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name.strip(),
        phone=payload.phone.strip() if payload.phone else None,
        role="USER",
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

    token = create_access_token(user_id=user.id, role=user.role)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    norm_email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == norm_email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ອີເມວ ຫຼື ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ.",
        )

    token = create_access_token(user_id=user.id, role=user.role)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(current_user)

