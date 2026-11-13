from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_current_active_user, require_role
from app.models.usuario import Usuario
from app.schemas.pedido import (
    EstadoPedido,
    PedidoCrear,
    PedidoEstadoActualizar,
    PedidoLectura,
    PedidosPaginados,
    PedidoResumen,
)
from app.services.pedido_service import PedidoService


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post(
    "",
    response_model=PedidoLectura,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    data: PedidoCrear,
    usuario: Usuario = Depends(get_current_active_user),
):
    return PedidoService().crear(data, usuario.id)


@router.get("", response_model=PedidosPaginados)
def listar(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    estado: EstadoPedido | None = None,
    usuario: Usuario = Depends(get_current_active_user),
):
    usuario_id = None if usuario.role == "admin" else usuario.id
    return PedidoService().listar(usuario_id, skip, limit, estado)


@router.get("/resumen", response_model=PedidoResumen)
def resumen(
    admin: Usuario = Depends(require_role("admin")),
):
    return PedidoService().resumen()


@router.get("/{pedido_id}", response_model=PedidoLectura)
def obtener(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_active_user),
):
    return PedidoService().obtener(
        pedido_id,
        usuario.id,
        usuario.role == "admin",
    )


@router.patch("/{pedido_id}/estado", response_model=PedidoLectura)
def cambiar_estado(
    pedido_id: int,
    data: PedidoEstadoActualizar,
    admin: Usuario = Depends(require_role("admin")),
):
    return PedidoService().cambiar_estado(pedido_id, data.estado)


@router.patch("/{pedido_id}/cancelar", response_model=PedidoLectura)
def cancelar(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_active_user),
):
    return PedidoService().cancelar(pedido_id, usuario.id)
