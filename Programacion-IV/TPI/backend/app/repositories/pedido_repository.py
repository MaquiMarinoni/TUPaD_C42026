from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload
from sqlmodel import select

from app.models.pedido import Pedido
from app.repositories.base import BaseRepository


class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session):
        super().__init__(session, Pedido)

    def get_by_id_con_items(self, pedido_id: int) -> Pedido | None:
        statement = (
            select(Pedido)
            .options(selectinload(Pedido.items))
            .where(Pedido.id == pedido_id)
        )
        return self.session.scalars(statement).first()

    def get_for_update(self, pedido_id: int) -> Pedido | None:
        statement = (
            select(Pedido)
            .where(Pedido.id == pedido_id)
            .with_for_update()
        )
        return self.session.scalars(statement).first()

    def buscar(
        self,
        skip: int = 0,
        limit: int = 20,
        usuario_id: int | None = None,
        estado: str | None = None,
    ) -> tuple[int, list[Pedido]]:
        condiciones = []

        if usuario_id is not None:
            condiciones.append(Pedido.usuario_id == usuario_id)

        if estado is not None:
            condiciones.append(Pedido.estado == estado)

        total = self.session.scalar(
            select(func.count())
            .select_from(Pedido)
            .where(*condiciones)
        ) or 0

        statement = (
            select(Pedido)
            .options(selectinload(Pedido.items))
            .where(*condiciones)
            .order_by(Pedido.created_at.desc(), Pedido.id.desc())
            .offset(skip)
            .limit(limit)
        )

        pedidos = list(self.session.scalars(statement).all())
        return total, pedidos

    def get_by_usuario(self, usuario_id: int) -> list[Pedido]:
        return list(
            self.session.scalars(
                select(Pedido).where(Pedido.usuario_id == usuario_id)
            ).all()
        )

    def get_by_estado(self, estado: str) -> list[Pedido]:
        return list(
            self.session.scalars(
                select(Pedido).where(Pedido.estado == estado)
            ).all()
        )
