
from datetime import datetime
from decimal import Decimal

from sqlmodel import SQLModel, Field, Relationship

from app.modules.unidades_medida.model import UnidadMedida
from app.modules.categorias.model import Categoria
from app.modules.productos.link_model import ProductoCategoria


class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: int | None = Field(default=None, primary_key=True)

    unidad_venta_id: int = Field(
        foreign_key="unidades_medida.id",
        nullable=False
    )

    nombre: str = Field(min_length=3, index=True)
    descripcion: str | None = Field(default=None)

    precio_base: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        ge=0
    )

    stock_cantidad: Decimal = Field(
        default=Decimal("0.000"),
        max_digits=12,
        decimal_places=3,
        ge=0
    )

    disponible: bool = Field(default=True, nullable=False)
    activo: bool = Field(default=True, nullable=False)
    anulado_at: datetime | None = Field(default=None)

    unidad_venta: UnidadMedida = Relationship(
        back_populates="productos"
    )

    categorias: list[Categoria] = Relationship(
        back_populates="productos",
        link_model=ProductoCategoria
    )
