from typing import Optional
from app.pedidos.models import DetallePedido, Pedido
from app.pedidos.schemas import (
    DetallePedidoRead,
    PedidoCreate,
    PedidoRead,
    PedidoUpdate,
)
from app.pedidos.unit_of_work import PedidoUnitOfWork


class ProductoNoEncontrado(Exception):
    def __init__(self, producto_id: int):
        self.producto_id = producto_id
        super().__init__(f"El producto con id {producto_id} no existe o fue eliminado.")


class PedidoNoEncontrado(Exception):
    def __init__(self, pedido_id: int):
        self.pedido_id = pedido_id
        super().__init__(f"El pedido con id {pedido_id} no existe o fue eliminado.")


class EstadoPedidoTerminalError(Exception):
    def __init__(self, estado_actual: str):
        self.estado_actual = estado_actual
        super().__init__(
            f"No se puede modificar el estado de un pedido que ya se encuentra {estado_actual}."
        )


class PedidoService:
    def __init__(self, uow: Optional[PedidoUnitOfWork] = None):
        self.uow = uow or PedidoUnitOfWork()

    def _build_pedido_read(self, pedido: Pedido, detalles: list[DetallePedido]) -> PedidoRead:
        return PedidoRead(
            id=pedido.id,  # type: ignore[arg-type]
            fecha=pedido.fecha,
            estado=pedido.estado,
            total=pedido.total,
            detalles=[DetallePedidoRead.model_validate(d) for d in detalles],
        )

    def listar(self) -> list[PedidoRead]:
        with self.uow as uow:
            pedidos = uow.pedidos.get_all()
            resultado: list[PedidoRead] = []
            for p in pedidos:
                detalles = uow.detalles.get_by_pedido_id(p.id)  # type: ignore[arg-type]
                resultado.append(self._build_pedido_read(p, detalles))
            return resultado

    def obtener(self, pedido_id: int) -> PedidoRead:
        with self.uow as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if pedido is None:
                raise PedidoNoEncontrado(pedido_id)
            detalles = uow.detalles.get_by_pedido_id(pedido_id)
            return self._build_pedido_read(pedido, detalles)

    def crear(self, data: PedidoCreate) -> PedidoRead:
        with self.uow as uow:
            pedido = uow.pedidos.create(Pedido(estado="PENDIENTE", total=0.0))
            total = 0.0
            detalles_creados: list[DetallePedido] = []

            for item in data.detalles:
                producto = uow.productos.get_by_id(item.producto_id)
                if producto is None:
                    raise ProductoNoEncontrado(item.producto_id)

                detalle = uow.detalles.create(
                    DetallePedido(
                        pedido_id=pedido.id,  # type: ignore[arg-type]
                        producto_id=producto.id,  # type: ignore[arg-type]
                        cantidad=item.cantidad,
                        precio_unitario=producto.precio_base,
                    )
                )
                detalles_creados.append(detalle)
                total += item.cantidad * producto.precio_base

            pedido.total = round(total, 2)
            uow.pedidos.update(pedido)
            return self._build_pedido_read(pedido, detalles_creados)

    def actualizar_estado(self, pedido_id: int, data: PedidoUpdate) -> PedidoRead:
        with self.uow as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if pedido is None:
                raise PedidoNoEncontrado(pedido_id)

            if pedido.estado in ("ENTREGADO", "CANCELADO"):
                raise EstadoPedidoTerminalError(pedido.estado)

            pedido.estado = data.estado
            uow.pedidos.update(pedido)
            detalles = uow.detalles.get_by_pedido_id(pedido_id)
            return self._build_pedido_read(pedido, detalles)

    def eliminar(self, pedido_id: int) -> None:
        with self.uow as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if pedido is None:
                raise PedidoNoEncontrado(pedido_id)
            uow.pedidos.delete(pedido)
