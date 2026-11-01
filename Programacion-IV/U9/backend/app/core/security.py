"""bcrypt para contraseñas y JWT firmado; el token solo viaja en la cookie."""
from datetime import datetime, timedelta, timezone
import bcrypt
from jose import JWTError, jwt
from app.core.config import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    if len(password.encode()) > 72:
        return False
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    expiry = datetime.now(timezone.utc) + (expires_delta if expires_delta is not None else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return jwt.encode({"sub": str(user_id), "exp": expiry, "type": "access"}, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict | None:
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"require_exp": True, "require_sub": True})
        return data if data.get("type") == "access" else None
    except JWTError:
        return None
