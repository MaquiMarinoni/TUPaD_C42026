from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import func
from sqlmodel import select

from app.models.detalle_pedido import DetallePedido
from app.models.pedido import Pedido
from app.schemas.pedido import (
    PedidoCrear,
    PedidoLectura,
    PedidosPaginados,
    PedidoResumen,
)
from app.uow.unit_of_work import UnitOfWork


TRANSICIONES = {
    "PENDIENTE": {"EN_PREPARACION", "CANCELADO"},
    "EN_PREPARACION": {"ENTREGADO", "CANCELADO"},
    "ENTREGADO": set(),
    "CANCELADO": set(),
}


class PedidoService:
    @staticmethod
    def _lectura(uow, pedido_id: int) -> PedidoLectura:
        pedido = uow.pedidos.get_by_id_con_items(pedido_id)
        return PedidoLectura.model_validate(pedido)

    @staticmethod
    def _devolver_stock(uow, pedido_id: int) -> None:
        detalles = uow.detalles_pedido.get_by_pedido(pedido_id)

        # Orden estable para evitar bloqueos cruzados.
        for detalle in sorted(detalles, key=lambda item: item.producto_id):
            producto = uow.productos.get_for_update(detalle.producto_id)

            if producto is None:
                raise HTTPException(
                    409, "No se puede recuperar el stock del pedido"
                )

            producto.stock += detalle.cantidad

        uow.session.flush()

    def crear(self, data: PedidoCrear, usuario_id: int) -> PedidoLectura:
        ids = [item.producto_id for item in data.items]

        if len(ids) != len(set(ids)):
            raise HTTPException(
                422, "No se permiten productos repetidos en el pedido"
            )

        if not data.direccion_entrega.strip() or len(
            data.direccion_entrega.strip()
        ) < 5:
            raise HTTPException(422, "Direccion de entrega invalida")

        with UnitOfWork() as uow:
            productos = {}

            for producto_id in sorted(ids):
                producto = uow.productos.get_for_update(producto_id)

                if producto is None:
                    raise HTTPException(
                        404, f"Producto {producto_id} inexistente"
                    )

                categoria = uow.categorias.get_by_id(
                    producto.categoria_id
                )

                if (
                    not producto.activo
                    or not producto.disponible
                    or categoria is None
                    or not categoria.activo
                ):
                    raise HTTPException(
                        409, f"Producto {producto_id} no disponible"
                    )

                productos[producto_id] = producto

            total_centavos = 0
            detalles = []

            for item in data.items:
                producto = productos[item.producto_id]

                if producto.stock < item.cantidad:
                    raise HTTPException(
                        409, f"Stock insuficiente: {producto.nombre}"
                    )

                precio_centavos = round(producto.precio_base * 100)
                subtotal_centavos = precio_centavos * item.cantidad
                total_centavos += subtotal_centavos

                producto.stock -= item.cantidad

                detalles.append(
                    {
                        "producto_id": producto.id,
                        "cantidad": item.cantidad,
                        "nombre_producto": producto.nombre,
                        "precio_unitario": precio_centavos / 100,
                        "subtotal": subtotal_centavos / 100,
                    }
                )

            pedido = Pedido(
                usuario_id=usuario_id,
                estado="PENDIENTE",
                forma_pago=data.forma_pago,
                direccion_entrega=data.direccion_entrega.strip(),
                notas=data.notas,
                total=total_centavos / 100,
            )
            uow.pedidos.add(pedido)

            for detalle in detalles:
                uow.detalles_pedido.add(
                    DetallePedido(pedido_id=pedido.id, **detalle)
                )

            uow.session.flush()
            return self._lectura(uow, pedido.id)

    def listar(
        self,
        usuario_id: int | None,
        skip: int = 0,
        limit: int = 20,
        estado: str | None = None,
    ) -> PedidosPaginados:
        with UnitOfWork() as uow:
            total, pedidos = uow.pedidos.buscar(
                skip=skip,
                limit=limit,
                usuario_id=usuario_id,
                estado=estado,
            )

            return PedidosPaginados(
                total=total,
                items=[
                    PedidoLectura.model_validate(p)
                    for p in pedidos
                ],
            )

    def obtener(
        self,
        pedido_id: int,
        usuario_id: int,
        es_admin: bool,
    ) -> PedidoLectura:
        with UnitOfWork() as uow:
            pedido = uow.pedidos.get_by_id_con_items(pedido_id)

            if pedido is None:
                raise HTTPException(404, "Pedido inexistente")

            if not es_admin and pedido.usuario_id != usuario_id:
                raise HTTPException(403, "No puede consultar este pedido")

            return PedidoLectura.model_validate(pedido)

    def cambiar_estado(
        self,
        pedido_id: int,
        nuevo_estado: str,
    ) -> PedidoLectura:
        with UnitOfWork() as uow:
            pedido = uow.pedidos.get_for_update(pedido_id)

            if pedido is None:
                raise HTTPException(404, "Pedido inexistente")

            if nuevo_estado not in TRANSICIONES[pedido.estado]:
                raise HTTPException(
                    409, "Transicion de estado no permitida"
                )

            if nuevo_estado == "CANCELADO":
                self._devolver_stock(uow, pedido_id)

            pedido.estado = nuevo_estado
            pedido.updated_at = datetime.now(timezone.utc)
            uow.session.flush()

            return self._lectura(uow, pedido_id)

    def cancelar(
        self,
        pedido_id: int,
        usuario_id: int,
    ) -> PedidoLectura:
        with UnitOfWork() as uow:
            pedido = uow.pedidos.get_for_update(pedido_id)

            if pedido is None:
                raise HTTPException(404, "Pedido inexistente")

            if pedido.usuario_id != usuario_id:
                raise HTTPException(403, "No puede cancelar este pedido")

            if pedido.estado != "PENDIENTE":
                raise HTTPException(
                    409, "Solo se pueden cancelar pedidos pendientes"
                )

            self._devolver_stock(uow, pedido_id)
            pedido.estado = "CANCELADO"
            pedido.updated_at = datetime.now(timezone.utc)
            uow.session.flush()

            return self._lectura(uow, pedido_id)

    def resumen(self) -> PedidoResumen:
        with UnitOfWork() as uow:
            pedidos = uow.pedidos.get_all()
            hoy = datetime.now(timezone.utc).date()

            return PedidoResumen(
                total_pedidos=len(pedidos),
                pendientes=sum(
                    p.estado == "PENDIENTE" for p in pedidos
                ),
                en_preparacion=sum(
                    p.estado == "EN_PREPARACION" for p in pedidos
                ),
                entregados=sum(
                    p.estado == "ENTREGADO" for p in pedidos
                ),
                cancelados=sum(
                    p.estado == "CANCELADO" for p in pedidos
                ),
                pedidos_hoy=sum(
                    p.created_at.date() == hoy for p in pedidos
                ),
                ingresos_entregados=round(
                    sum(
                        p.total for p in pedidos
                        if p.estado == "ENTREGADO"
                    ),
                    2,
                ),
            )
