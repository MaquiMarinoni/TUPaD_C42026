from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


EstadoPedido = Literal[
    "PENDIENTE", "EN_PREPARACION", "ENTREGADO", "CANCELADO"
]
FormaPago = Literal["EFECTIVO", "TRANSFERENCIA"]


class ItemPedidoCrear(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(ge=1)


class PedidoCrear(BaseModel):
    items: list[ItemPedidoCrear] = Field(min_length=1)
    forma_pago: FormaPago
    direccion_entrega: str = Field(min_length=5, max_length=200)
    notas: str | None = None


class DetallePedidoLectura(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    producto_id: int
    cantidad: int
    nombre_producto: str
    precio_unitario: float
    subtotal: float


class PedidoLectura(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    estado: EstadoPedido
    forma_pago: FormaPago
    direccion_entrega: str
    notas: str | None
    total: float
    created_at: datetime
    updated_at: datetime
    items: list[DetallePedidoLectura]


class PedidosPaginados(BaseModel):
    total: int
    items: list[PedidoLectura]


class PedidoEstadoActualizar(BaseModel):
    estado: EstadoPedido


class PedidoResumen(BaseModel):
    total_pedidos: int
    pendientes: int
    en_preparacion: int
    entregados: int
    cancelados: int
    pedidos_hoy: int
    ingresos_entregados: float
