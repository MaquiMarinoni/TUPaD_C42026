from sqlalchemy import func, or_
from sqlalchemy.orm import Session, selectinload
from sqlmodel import select

from app.models.categoria import Categoria
from app.models.producto import Producto
from app.repositories.base import BaseRepository


class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def get_by_id_con_categoria(self, producto_id: int) -> Producto | None:
        statement = (
            select(Producto)
            .options(selectinload(Producto.categoria))
            .where(Producto.id == producto_id)
        )
        return self.session.scalars(statement).first()

    def buscar(
        self,
        skip: int = 0,
        limit: int = 20,
        buscar: str | None = None,
        categoria_id: int | None = None,
        disponible: bool | None = None,
        solo_activos: bool = True,
    ) -> tuple[int, list[Producto]]:
        condiciones = []

        if solo_activos:
            condiciones.extend([
                Producto.activo.is_(True),
                Categoria.activo.is_(True),
            ])

        if buscar:
            condiciones.append(
                Producto.nombre.ilike(f"%{buscar.strip()}%")
            )

        if categoria_id is not None:
            condiciones.append(Producto.categoria_id == categoria_id)

        if disponible is not None:
            condiciones.append(Producto.disponible == disponible)

        base = (
            select(Producto)
            .join(Categoria, Producto.categoria_id == Categoria.id)
            .where(*condiciones)
        )

        total = self.session.scalar(
            select(func.count())
            .select_from(Producto)
            .join(Categoria, Producto.categoria_id == Categoria.id)
            .where(*condiciones)
        ) or 0

        statement = (
            base
            .options(selectinload(Producto.categoria))
            .order_by(Producto.id)
            .offset(skip)
            .limit(limit)
        )

        items = list(self.session.scalars(statement).all())
        return total, items

    def get_activos(self) -> list[Producto]:
        return list(
            self.session.scalars(
                select(Producto).where(Producto.activo.is_(True))
            ).all()
        )

    def get_by_categoria(self, categoria_id: int) -> list[Producto]:
        return list(
            self.session.scalars(
                select(Producto).where(
                    Producto.categoria_id == categoria_id,
                    Producto.activo.is_(True),
                )
            ).all()
        )

    def get_for_update(self, producto_id: int) -> Producto | None:
        statement = (
            select(Producto)
            .where(Producto.id == producto_id)
            .with_for_update()
        )
        return self.session.scalars(statement).first()
