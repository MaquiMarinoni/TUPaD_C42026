from datetime import datetime
from typing import Literal
from pydantic import ConfigDict, field_validator
from sqlmodel import Field, SQLModel

EstadoPedidoLiteral = Literal["PENDIENTE", "CONFIRMADO", "ENTREGADO", "CANCELADO"]


class DetallePedidoCreate(SQLModel):
    producto_id: int = Field(gt=0, description="ID del producto a incluir en el pedido")
    cantidad: int = Field(ge=1, description="Cantidad solicitada (mayor o igual a 1)")


class DetallePedidoRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float


class PedidoCreate(SQLModel):
    detalles: list[DetallePedidoCreate] = Field(
        min_length=1,
        description="Lista de detalles del pedido (al menos un ítem)",
    )

    @field_validator("detalles")
    @classmethod
    def validar_productos_no_repetidos(cls, detalles: list[DetallePedidoCreate]) -> list[DetallePedidoCreate]:
        if not detalles:
            raise ValueError("El pedido debe incluir al menos un detalle.")
        vistos: set[int] = set()
        for item in detalles:
            if item.producto_id in vistos:
                raise ValueError(
                    f"El producto con id {item.producto_id} está repetido en los detalles del pedido."
                )
            vistos.add(item.producto_id)
        return detalles


class PedidoUpdate(SQLModel):
    estado: EstadoPedidoLiteral


class PedidoRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: datetime
    estado: str
    total: float
    detalles: list[DetallePedidoRead] = Field(default_factory=list)
