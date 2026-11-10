
from sqlmodel import SQLModel, Session, create_engine, text

from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    echo=False
)


def create_db_and_tables():
    # Registrar los modelos
    import app.modules.unidades_medida.model
    import app.modules.categorias.model
    import app.modules.productos.model

    # Crear las tablas si no existen
    SQLModel.metadata.create_all(engine)

    # Crear los indices de integridad
    with engine.begin() as connection:
        connection.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            uq_categoria_nombre_activo
            ON categorias (LOWER(nombre))
            WHERE activo = TRUE
        """))

        connection.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            uq_producto_nombre_activo
            ON productos (LOWER(nombre))
            WHERE activo = TRUE
        """))

        connection.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            uq_producto_categoria_principal
            ON producto_categoria (producto_id)
            WHERE es_principal = TRUE
        """))


def get_session():
    with Session(engine) as session:
        yield session
