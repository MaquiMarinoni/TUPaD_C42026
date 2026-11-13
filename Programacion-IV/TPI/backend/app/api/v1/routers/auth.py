from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_current_active_user
from app.core.config import settings
from app.models.usuario import Usuario
from app.schemas.auth import Mensaje, UsuarioLectura, UsuarioRegistro
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post(
    "/register",
    response_model=UsuarioLectura,
    status_code=status.HTTP_201_CREATED,
)
def register(data: UsuarioRegistro):
    return AuthService().register(data)


@router.post("/token", response_model=Mensaje)
def login(
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
):
    token = AuthService().authenticate(
        form.username,
        form.password,
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Desarrollo local HTTP; True en HTTPS.
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )

    return {"message": "Inicio de sesion correcto"}


@router.get("/me", response_model=UsuarioLectura)
def me(usuario: Usuario = Depends(get_current_active_user)):
    return UsuarioLectura.model_validate(usuario)


@router.post("/logout", response_model=Mensaje)
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        samesite="lax",
    )
    return {"message": "Sesion cerrada"}
