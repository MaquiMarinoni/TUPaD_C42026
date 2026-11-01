from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.deps import get_current_active_user, require_role
from app.modules.usuarios.schema import UserPublic
from app.pedidos.models import EstadoPedido, FormaPago
from app.pedidos.schemas import PedidoCreate, PedidoRead, PedidoUpdate
from app.pedidos.service import PedidoService

router = APIRouter(tags=["Pedidos"], dependencies=[Depends(get_current_active_user)])


@router.get("/pedidos", response_model=list[PedidoRead])
def listar():
    return PedidoService().listar()


@router.get("/pedidos/{pedido_id}", response_model=PedidoRead)
def obtener(pedido_id: int):
    return PedidoService().obtener(pedido_id)


@router.post("/pedidos", response_model=PedidoRead, status_code=201)
def crear(data: PedidoCreate, user: UserPublic = Depends(require_role(["user", "admin"]))):
    return PedidoService().crear(data, user.id)


@router.put("/pedidos/{pedido_id}", response_model=PedidoRead)
def actualizar(pedido_id: int, data: PedidoUpdate, user: UserPublic = Depends(require_role(["admin"]))):
    return PedidoService().actualizar_estado(pedido_id, data, user.id)


@router.delete("/pedidos/{pedido_id}", status_code=204, dependencies=[Depends(require_role(["admin"]))])
def eliminar(pedido_id: int):
    PedidoService().eliminar(pedido_id)


@router.get("/estados-pedido", response_model=list[EstadoPedido])
def estados(session: Session = Depends(get_session)):
    return session.exec(select(EstadoPedido).order_by(EstadoPedido.orden)).all()


@router.get("/formas-pago", response_model=list[FormaPago])
def formas_pago(session: Session = Depends(get_session)):
    return session.exec(select(FormaPago)).all()
