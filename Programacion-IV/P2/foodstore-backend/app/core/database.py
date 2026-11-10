
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False
)


def create_db_and_tables():
    import app.modules.unidades_medida.model
    import app.modules.categorias.model
    import app.modules.productos.model

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
