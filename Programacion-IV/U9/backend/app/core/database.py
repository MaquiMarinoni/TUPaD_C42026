from app.core.config import settings
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = settings.DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    import app.modules.usuarios.model  # noqa: F401
    import app.pedidos.models  # noqa: F401
    import app.categoria.model  # noqa: F401
    import app.producto.model  # noqa: F401
    import app.ingrediente.model  # noqa: F401
    import app.unidad_medida.model  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
