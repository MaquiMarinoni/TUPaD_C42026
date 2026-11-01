from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    estado: str = Field(default="PENDIENTE", max_length=20, nullable=False)
    total: float = Field(default=0.0, ge=0, nullable=False)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)


class DetallePedido(SQLModel, table=True):
    __tablename__ = "detalles_pedido"

    pedido_id: int = Field(foreign_key="pedidos.id", primary_key=True)
    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    cantidad: int = Field(ge=1, nullable=False)
    precio_unitario: float = Field(ge=0, nullable=False)
