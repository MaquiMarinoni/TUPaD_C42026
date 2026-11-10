
from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from app.modules.categorias.schema import CategoriaPublic
from app.modules.unidades_medida.schema import UnidadMedidaPublic


NombreProducto = Annotated[str, Field(min_length=3)]
Precio = Annotated[Decimal, Field(ge=0, max_digits=12, decimal_places=2)]
Stock = Annotated[Decimal, Field(ge=0, max_digits=12, decimal_places=3)]


class ProductoBase(BaseModel):
    nombre: NombreProducto
    descripcion: str | None = None
    precio_base: Precio
    unidad_venta_id: int
    stock_cantidad: Stock = Decimal("0.000")
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class CategoriaProductoPublic(CategoriaPublic):
    es_principal: bool = False


class ProductoPublic(ProductoBase):
    id: int
    activo: bool
    anulado_at: datetime | None = None
    unidad_venta: UnidadMedidaPublic
    categorias: list[CategoriaProductoPublic] = Field(default_factory=list)
    hay_stock: bool

    model_config = ConfigDict(from_attributes=True)


class ProductoCategoriaCreate(BaseModel):
    categoria_id: int
    es_principal: bool = False
