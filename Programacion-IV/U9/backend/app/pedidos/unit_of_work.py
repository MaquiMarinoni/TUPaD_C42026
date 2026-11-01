from app.core.unit_of_work import UnitOfWork
from app.pedidos.repository import (
    DetallePedidoRepository,
    PedidoRepository,
    ProductoLookupRepository,
)


class PedidoUnitOfWork(UnitOfWork):
    """Unit of Work del módulo pedidos: expone los repositorios pedidos, detalles y productos."""

    pedidos: PedidoRepository
    detalles: DetallePedidoRepository
    productos: ProductoLookupRepository

    def __enter__(self):
        super().__enter__()
        assert self.session is not None
        self.pedidos = PedidoRepository(self.session)
        self.detalles = DetallePedidoRepository(self.session)
        self.productos = ProductoLookupRepository(self.session)
        return self
