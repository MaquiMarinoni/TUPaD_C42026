from sqlalchemy.orm import Session
from sqlmodel import select

from app.models.categoria import Categoria
from app.repositories.base import BaseRepository


class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session):
        super().__init__(session, Categoria)

    def get_by_nombre(self, nombre: str) -> Categoria | None:
        return self.session.scalars(
            select(Categoria).where(Categoria.nombre == nombre)
        ).first()

    def get_activas(self) -> list[Categoria]:
        return list(
            self.session.scalars(
                select(Categoria).where(Categoria.activo.is_(True))
            ).all()
        )
