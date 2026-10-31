from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.permissions import ADMIN_ROLES, ROLE_SUPER_ADMIN
from app.core.security import decode_access_token
from app.db.database import get_db
from app.db.models import User

bearer_scheme = HTTPBearer(auto_error=False)


def _lookup_token_user(
    credentials: HTTPAuthorizationCredentials | None,
    db: Session,
) -> tuple[User | None, bool]:
    """Return `(user, is_suspended)` after verifying JWT signature, expiry, and `token_version`."""
    if not credentials or not credentials.credentials:
        return None, False
    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload:
        return None, False
    try:
        user_id = int(payload["sub"])
        token_ver = int(payload.get("ver", 1))
    except (TypeError, ValueError):
        return None, False

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None, False

    # Reject revoked tokens (role change, account suspension, or password rotation increments token_version)
    if (user.token_version or 1) != token_ver:
        return None, False

    if not user.is_active:
        return None, True

    return user, False


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    user, _suspended = _lookup_token_user(credentials, db)
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    user, is_suspended = _lookup_token_user(credentials, db)
    if is_suspended:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ບັນຊີຂອງທ່ານຖືກລະງັບການໃຊ້ງານຊົ່ວຄາວ. ກະລຸນາຕິດຕໍ່ຜູ້ບໍລິຫານລະບົບ.",
        )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ຕ້ອງເຂົ້າສູ່ລະບົບກ່ອນ ຫຼື ເຊດຊັນໝົດອາຍຸແລ້ວ.",
        )
    return user


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Allows both `ADMIN` (Shop Moderator) and `SUPER_ADMIN` (System Owner)."""
    if current_user.role not in ADMIN_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ຕ້ອງໃຊ້ສິດຂອງຜູ້ດູແລລະບົບ (Admin) ຂຶ້ນໄປ.",
        )
    return current_user


def require_super_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Strictly restricts critical production settings (AdSense, User Roles, Security) to `SUPER_ADMIN`."""
    if current_user.role != ROLE_SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ສະເພາະຜູ້ບໍລິຫານສູງສຸດ (Super Admin) ເທົ່ານັ້ນທີ່ມີສິດຈັດການສ່ວນນີ້.",
        )
    return current_user
