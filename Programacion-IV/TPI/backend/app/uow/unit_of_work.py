from types import TracebackType

from sqlalchemy.orm import Session

from app.db.session import engine
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.detalle_pedido_repository import DetallePedidoRepository
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.usuario_repository import UsuarioRepository


class UnitOfWork:
    def __init__(self):
        self.session: Session | None = None

    def __enter__(self) -> "UnitOfWork":
        self.session = Session(engine)

        self.usuarios = UsuarioRepository(self.session)
        self.categorias = CategoriaRepository(self.session)
        self.productos = ProductoRepository(self.session)
        self.pedidos = PedidoRepository(self.session)
        self.detalles_pedido = DetallePedidoRepository(self.session)

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if self.session is None:
            return False

        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()
            self.session = None

        return False
