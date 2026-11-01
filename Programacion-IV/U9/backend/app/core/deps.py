from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import decode_access_token
from app.modules.usuarios.schema import UserPublic
from app.modules.usuarios.service import UsuarioService


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(401, "No autenticado", headers={"WWW-Authenticate": "Bearer"})
        return token


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> UserPublic:
    payload = decode_access_token(token)
    try:
        user_id = int(payload["sub"]) if payload else None
    except (ValueError, TypeError, KeyError):
        user_id = None
    service = UsuarioService(session)
    user = service.repo.get_by_id(user_id) if user_id is not None else None
    if user is None:
        raise HTTPException(
            401, "Credenciales inválidas o token expirado", headers={"WWW-Authenticate": "Bearer"}
        )
    # Los permisos se leen de la base en cada petición, nunca del JWT.
    return service.public(user)


def get_current_active_user(user: UserPublic = Depends(get_current_user)) -> UserPublic:
    if user.deleted_at is not None:
        raise HTTPException(400, "Cuenta de usuario desactivada")
    return user


def require_role(roles: list[str]):
    def check(user: UserPublic = Depends(get_current_active_user)) -> UserPublic:
        if not set(roles).intersection(user.roles):
            raise HTTPException(403, "Permisos insuficientes")
        return user

    return check


def catalog_access(
    request: Request, user: UserPublic = Depends(get_current_active_user)
) -> UserPublic:
    # Una misma regla protege todos los métodos de los CRUD heredados de U8.
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        return require_role(["admin"])(user)
    return user
