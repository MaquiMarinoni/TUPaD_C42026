from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.core.config import settings
from app.core.database import get_session
from app.core.deps import get_current_active_user, require_role
from app.core.security import create_access_token
from app.modules.usuarios.model import Rol
from app.modules.usuarios.schema import UserCreate, UserPublic
from app.modules.usuarios.service import UsuarioService

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])
roles_router = APIRouter(
    prefix="/roles", tags=["Roles"], dependencies=[Depends(get_current_active_user)]
)


@router.post("/register", response_model=UserPublic, status_code=201)
def register(data: UserCreate, session: Session = Depends(get_session)):
    return UsuarioService(session).register(data)


@router.post("/token")
def login(
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = UsuarioService(session).authenticate(form.username, form.password)
    response.set_cookie(
        "access_token",
        create_access_token(user.id),
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        path="/",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"mensaje": "Sesión iniciada"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        "access_token", httponly=True, secure=settings.COOKIE_SECURE, samesite="lax", path="/"
    )
    return {"mensaje": "Sesión cerrada"}


@router.get("/me", response_model=UserPublic)
def me(user: UserPublic = Depends(get_current_active_user)):
    return user


@router.get(
    "/admin/usuarios",
    response_model=list[UserPublic],
    dependencies=[Depends(require_role(["admin"]))],
)
def users(session: Session = Depends(get_session)):
    return UsuarioService(session).list_all()


@router.post(
    "/admin/usuarios/{user_id}/activar",
    response_model=UserPublic,
    dependencies=[Depends(require_role(["admin"]))],
)
def activate(user_id: int, session: Session = Depends(get_session)):
    return UsuarioService(session).set_active(user_id, True)


@router.post(
    "/admin/usuarios/{user_id}/desactivar",
    response_model=UserPublic,
    dependencies=[Depends(require_role(["admin"]))],
)
def deactivate(user_id: int, session: Session = Depends(get_session)):
    return UsuarioService(session).set_active(user_id, False)


@roles_router.get("", response_model=list[Rol])
def roles(session: Session = Depends(get_session)):
    return session.exec(select(Rol).order_by(Rol.id)).all()
