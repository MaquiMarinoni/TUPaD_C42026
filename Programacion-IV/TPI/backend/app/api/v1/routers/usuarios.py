from fastapi import APIRouter, Depends

from app.api.deps import require_role
from app.models.usuario import Usuario
from app.schemas.auth import UsuarioEstado, UsuarioLectura
from app.services.usuario_service import UsuarioService


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=list[UsuarioLectura])
def listar_usuarios(
    admin: Usuario = Depends(require_role("admin")),
):
    return UsuarioService().listar()


@router.patch("/{usuario_id}/estado", response_model=UsuarioLectura)
def cambiar_estado(
    usuario_id: int,
    data: UsuarioEstado,
    admin: Usuario = Depends(require_role("admin")),
):
    return UsuarioService().cambiar_estado(
        usuario_id=usuario_id,
        disabled=data.disabled,
        admin_id=admin.id,
    )
