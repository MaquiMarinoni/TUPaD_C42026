from datetime import datetime, timezone
from decimal import Decimal
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class FormaPago(SQLModel, table=True):
    __tablename__ = "formas_pago"
    codigo: str = Field(primary_key=True, max_length=30)
    descripcion: str = Field(max_length=80)
    activo: bool = True


class EstadoPedido(SQLModel, table=True):
    __tablename__ = "estados_pedido"
    codigo: str = Field(primary_key=True, max_length=20)
    descripcion: str = Field(max_length=80)
    orden: int
    es_terminal: bool = False


class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    estado_codigo: str = Field(default="PENDIENTE", foreign_key="estados_pedido.codigo")
    forma_pago_codigo: str = Field(foreign_key="formas_pago.codigo")
    subtotal: Decimal = Field(default=Decimal("0"), max_digits=10, decimal_places=2)
    descuento: Decimal = Field(default=Decimal("0"), max_digits=10, decimal_places=2)
    costo_envio: Decimal = Field(default=Decimal("0"), max_digits=10, decimal_places=2)
    total: Decimal = Field(default=Decimal("0"), ge=0, max_digits=10, decimal_places=2)
    notas: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    deleted_at: datetime | None = None


class DetallePedido(SQLModel, table=True):
    __tablename__ = "detalles_pedido"
    pedido_id: int = Field(foreign_key="pedidos.id", primary_key=True)
    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    cantidad: int = Field(ge=1)
    nombre_producto_snap: str = Field(max_length=150)
    precio_unitario_snap: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    subtotal_snap: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    created_at: datetime = Field(default_factory=utc_now)


class HistorialEstadoPedido(SQLModel, table=True):
    __tablename__ = "historial_estado_pedido"
    id: int | None = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id")
    estado_desde: str | None = Field(default=None, foreign_key="estados_pedido.codigo")
    estado_hacia: str = Field(foreign_key="estados_pedido.codigo")
    usuario_id: int = Field(foreign_key="usuarios.id")
    motivo: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
