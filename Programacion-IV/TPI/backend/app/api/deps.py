from collections.abc import Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token
from app.models.usuario import Usuario
from app.uow.unit_of_work import UnitOfWork


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    auto_error=False,
)


def get_current_user(
    request: Request,
) -> Usuario:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
        )

    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesion invalida o vencida",
        )

    with UnitOfWork() as uow:
        usuario = uow.usuarios.get_by_id(user_id)

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario inexistente",
            )

        # El objeto se utiliza despues de cerrar la sesion.
        uow.session.expunge(usuario)
        return usuario


def get_current_active_user(
    usuario: Usuario = Depends(get_current_user),
) -> Usuario:
    if usuario.disabled:
        raise HTTPException(
            status_code=400,
            detail="La cuenta esta desactivada",
        )
    return usuario


def require_role(*roles: str) -> Callable:
    def verificar_rol(
        usuario: Usuario = Depends(get_current_active_user),
    ) -> Usuario:
        if usuario.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes",
            )
        return usuario

    return verificar_rol
