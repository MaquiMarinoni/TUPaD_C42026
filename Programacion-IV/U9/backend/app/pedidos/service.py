from decimal import Decimal
from fastapi import HTTPException
from sqlmodel import select
from app.pedidos.models import DetallePedido, Pedido, EstadoPedido, FormaPago, HistorialEstadoPedido, utc_now
from app.pedidos.schemas import PedidoCreate, PedidoRead, PedidoUpdate, DetallePedidoRead
from app.pedidos.unit_of_work import PedidoUnitOfWork


class PedidoService:
    def __init__(self, uow: PedidoUnitOfWork | None = None):
        self.uow = uow or PedidoUnitOfWork()

    def _read(self, uow, pedido: Pedido) -> PedidoRead:
        return PedidoRead(**pedido.model_dump(), detalles=[DetallePedidoRead.model_validate(d) for d in uow.detalles.get_by_pedido_id(pedido.id)])

    def _get(self, uow, pedido_id: int) -> Pedido:
        pedido = uow.pedidos.get_by_id(pedido_id)
        if pedido is None:
            raise HTTPException(404, "Pedido no encontrado")
        return pedido

    def listar(self):
        with self.uow as uow:
            return [self._read(uow, p) for p in uow.pedidos.get_all()]

    def obtener(self, pedido_id: int):
        with self.uow as uow:
            return self._read(uow, self._get(uow, pedido_id))

    def crear(self, data: PedidoCreate, usuario_id: int):
        with self.uow as uow:
            pago = uow.session.get(FormaPago, data.forma_pago_codigo)
            if pago is None or not pago.activo:
                raise HTTPException(404, "Forma de pago no disponible")
            pedido = uow.pedidos.create(Pedido(usuario_id=usuario_id, forma_pago_codigo=pago.codigo, notas=data.notas))
            subtotal = Decimal("0.00")
            for item in data.detalles:
                producto = uow.productos.get_by_id(item.producto_id)
                if producto is None:
                    raise HTTPException(404, "Producto no encontrado")
                if not producto.disponible:
                    raise HTTPException(409, "Producto no disponible")
                precio = Decimal(str(producto.precio_base)).quantize(Decimal("0.01"))
                importe = precio * item.cantidad
                uow.detalles.create(DetallePedido(pedido_id=pedido.id, producto_id=producto.id, cantidad=item.cantidad,
                    nombre_producto_snap=producto.nombre, precio_unitario_snap=precio, subtotal_snap=importe))
                subtotal += importe
            if subtotal > Decimal("99999999.99"):
                raise HTTPException(400, "El total supera el importe permitido")
            pedido.subtotal = pedido.total = subtotal
            uow.pedidos.update(pedido)
            uow.session.add(HistorialEstadoPedido(pedido_id=pedido.id, estado_hacia="PENDIENTE", usuario_id=usuario_id))
            return self._read(uow, pedido)

    def actualizar_estado(self, pedido_id: int, data: PedidoUpdate, usuario_id: int):
        with self.uow as uow:
            pedido = self._get(uow, pedido_id)
            actual = uow.session.get(EstadoPedido, pedido.estado_codigo)
            if actual.es_terminal:
                raise HTTPException(409, "No se puede modificar un pedido en estado terminal")
            if pedido.estado_codigo == data.estado:
                raise HTTPException(409, "El pedido ya tiene ese estado")
            uow.session.add(HistorialEstadoPedido(pedido_id=pedido.id, estado_desde=pedido.estado_codigo,
                estado_hacia=data.estado, usuario_id=usuario_id, motivo=data.motivo))
            pedido.estado_codigo = data.estado
            pedido.updated_at = utc_now()
            uow.pedidos.update(pedido)
            return self._read(uow, pedido)

    def eliminar(self, pedido_id: int):
        with self.uow as uow:
            pedido = self._get(uow, pedido_id)
            pedido.updated_at = utc_now()
            uow.pedidos.delete(pedido)
