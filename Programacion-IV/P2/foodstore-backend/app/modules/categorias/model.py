
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from app.modules.productos.link_model import ProductoCategoria

if TYPE_CHECKING:
    from app.modules.productos.model import Producto


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: int | None = Field(default=None, primary_key=True)

    nombre: str = Field(min_length=3, index=True)
    descripcion: str | None = Field(default=None)

    activo: bool = Field(default=True, nullable=False)
    anulado_at: datetime | None = Field(default=None)

    productos: list["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoria
    )
