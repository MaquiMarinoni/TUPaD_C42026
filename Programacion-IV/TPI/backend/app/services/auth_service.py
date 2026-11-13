from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.usuario import Usuario
from app.schemas.auth import UsuarioLectura, UsuarioRegistro
from app.uow.unit_of_work import UnitOfWork


class AuthService:
    def register(self, data: UsuarioRegistro) -> UsuarioLectura:
        try:
            with UnitOfWork() as uow:
                if uow.usuarios.get_by_username(data.username):
                    raise HTTPException(
                        status_code=409,
                        detail="El nombre de usuario ya existe",
                    )

                if uow.usuarios.get_by_email(str(data.email)):
                    raise HTTPException(
                        status_code=409,
                        detail="El correo electronico ya existe",
                    )

                usuario = Usuario(
                    username=data.username,
                    full_name=data.full_name.strip(),
                    email=str(data.email),
                    hashed_password=hash_password(data.password),
                    role="user",
                    disabled=False,
                )
                uow.usuarios.add(usuario)
                resultado = UsuarioLectura.model_validate(usuario)

            return resultado
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="El usuario o correo electronico ya existe",
            ) from None

    def authenticate(self, username: str, password: str) -> str:
        with UnitOfWork() as uow:
            usuario = uow.usuarios.get_by_username(username)

            if usuario is None or not verify_password(
                password, usuario.hashed_password
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales incorrectas",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if usuario.disabled:
                raise HTTPException(
                    status_code=400,
                    detail="La cuenta esta desactivada",
                )

            if usuario.id is None:
                raise HTTPException(status_code=500, detail="Usuario sin ID")

            return create_access_token(usuario.id)

    def get_user(self, user_id: int) -> UsuarioLectura:
        with UnitOfWork() as uow:
            usuario = uow.usuarios.get_by_id(user_id)
            if usuario is None:
                raise HTTPException(status_code=404, detail="Usuario inexistente")
            return UsuarioLectura.model_validate(usuario)
