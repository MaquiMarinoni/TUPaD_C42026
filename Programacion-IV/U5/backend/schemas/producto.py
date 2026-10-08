from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductoBase(BaseModel):
    nombre: str = Field(..., json_schema_extra={"example": "Silla de Oficina"})
    categoria: str = Field(
        ...,
        pattern=r"^[A-Z]{3}-\d{2}$",
        json_schema_extra={"example": "MUE-01"},
    )
    precio: float = Field(gt=0, json_schema_extra={"example": 150.50})
    stock: int = Field(ge=0, json_schema_extra={"example": 20})
    stock_minimo: int = Field(ge=0, json_schema_extra={"example": 5})
    activo: bool = True


class ProductoCreate(ProductoBase):
    pass  # Exige todos los campos obligatorios de Base


class ProductoUpdate(BaseModel):
    # Se utiliza para actualización parcial (PATCH) si se requiere
    nombre: Optional[str] = None
    categoria: Optional[str] = Field(None, pattern=r"^[A-Z]{3}-\d{2}$")
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None


class ProductoRead(ProductoBase):
    id: int  # Contrato de salida: siempre incluye el ID generado por PostgreSQL

    model_config = ConfigDict(from_attributes=True)


class ProductoStockResponse(BaseModel):
    stock: int
    bajo_stock_minimo: bool
    activo: bool