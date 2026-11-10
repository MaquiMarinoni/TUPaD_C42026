from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

EstadoPedidoLiteral = Literal["PENDIENTE", "CONFIRMADO", "EN_PREP", "EN_CAMINO", "ENTREGADO", "CANCELADO"]


class DetallePedidoCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    producto_id: int = Field(gt=0)
    cantidad: int = Field(ge=1, le=32767)


class PedidoCreate(BaseModel):
    # Rechaza usuario_id y precios enviados por el cliente: se toman de sesión y catálogo.
    model_config = ConfigDict(extra="forbid")
    detalles: list[DetallePedidoCreate] = Field(min_length=1)
    forma_pago_codigo: str = "EFECTIVO"
    notas: str | None = Field(default=None, max_length=1000)

    @field_validator("detalles")
    @classmethod
    def productos_distintos(cls, items):
        if len({item.producto_id for item in items}) != len(items):
            raise ValueError("No repetir productos en los detalles")
        return items


class PedidoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    estado: EstadoPedidoLiteral
    motivo: str | None = Field(default=None, max_length=1000)


class DetallePedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pedido_id: int
    producto_id: int
    cantidad: int
    nombre_producto_snap: str
    precio_unitario_snap: Decimal
    subtotal_snap: Decimal
    created_at: datetime


class PedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    usuario_id: int
    estado_codigo: str
    forma_pago_codigo: str
    subtotal: Decimal
    descuento: Decimal
    costo_envio: Decimal
    total: Decimal
    notas: str | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
    detalles: list[DetallePedidoRead]
