from typing import Optional
from sqlmodel import Session, select
from app.core.repository import BaseRepository
from app.pedidos.models import DetallePedido, Pedido
from app.producto.model import Producto


class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session):
        super().__init__(session, Pedido)


class DetallePedidoRepository:
    """Repositorio para DetallePedido (clave primaria compuesta pedido_id + producto_id)."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, detalle: DetallePedido) -> DetallePedido:
        self.session.add(detalle)
        self.session.flush()
        self.session.refresh(detalle)
        return detalle

    def get_by_pedido_id(self, pedido_id: int) -> list[DetallePedido]:
        statement = select(DetallePedido).where(DetallePedido.pedido_id == pedido_id)
        return list(self.session.exec(statement).all())


class ProductoLookupRepository(BaseRepository[Producto]):
    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        return super().get_by_id(producto_id)
