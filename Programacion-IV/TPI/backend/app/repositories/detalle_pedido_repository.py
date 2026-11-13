from sqlalchemy.orm import Session
from sqlmodel import select

from app.models.detalle_pedido import DetallePedido
from app.repositories.base import BaseRepository


class DetallePedidoRepository(BaseRepository[DetallePedido]):
    def __init__(self, session: Session):
        super().__init__(session, DetallePedido)

    def get_by_pedido(self, pedido_id: int) -> list[DetallePedido]:
        return list(
            self.session.scalars(
                select(DetallePedido).where(
                    DetallePedido.pedido_id == pedido_id
                )
            ).all()
        )
