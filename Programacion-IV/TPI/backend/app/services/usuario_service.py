from fastapi import HTTPException

from app.schemas.auth import UsuarioLectura
from app.uow.unit_of_work import UnitOfWork


class UsuarioService:
    def listar(self) -> list[UsuarioLectura]:
        with UnitOfWork() as uow:
            return [
                UsuarioLectura.model_validate(usuario)
                for usuario in uow.usuarios.get_all()
            ]

    def cambiar_estado(
        self,
        usuario_id: int,
        disabled: bool,
        admin_id: int,
    ) -> UsuarioLectura:
        with UnitOfWork() as uow:
            usuario = uow.usuarios.get_by_id(usuario_id)

            if usuario is None:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario inexistente",
                )

            if usuario_id == admin_id and disabled:
                raise HTTPException(
                    status_code=400,
                    detail="Un administrador no puede desactivarse a si mismo",
                )

            usuario.disabled = disabled
            uow.session.flush()
            return UsuarioLectura.model_validate(usuario)
