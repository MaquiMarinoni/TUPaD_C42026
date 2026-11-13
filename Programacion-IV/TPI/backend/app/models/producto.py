from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.categoria import Categoria
    from app.models.detalle_pedido import DetallePedido


class Producto(SQLModel, table=True):
    __tablename__ = "productos"
    __table_args__ = (
        CheckConstraint("precio_base >= 0", name="ck_producto_precio"),
        CheckConstraint("stock >= 0", name="ck_producto_stock"),
    )

    id: int | None = Field(default=None, primary_key=True)
    categoria_id: int = Field(foreign_key="categorias.id", index=True)
    nombre: str = Field(max_length=150)
    descripcion: str | None = Field(default=None)
    precio_base: float = Field(ge=0)
    imagen_url: str | None = Field(default=None)
    stock: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)
    activo: bool = Field(default=True)

    categoria: "Categoria" = Relationship(back_populates="productos")
    detalles: list["DetallePedido"] = Relationship(back_populates="producto")
