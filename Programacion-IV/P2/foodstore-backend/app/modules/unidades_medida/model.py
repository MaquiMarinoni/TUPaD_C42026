
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.productos.model import Producto


class TipoUnidad(str, Enum):
    peso = "peso"
    volumen = "volumen"
    contable = "contable"


class UnidadMedida(SQLModel, table=True):
    __tablename__ = "unidades_medida"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, nullable=False)
    simbolo: str = Field(unique=True, nullable=False)
    tipo: TipoUnidad

    productos: list["Producto"] = Relationship(
        back_populates="unidad_venta"
    )
