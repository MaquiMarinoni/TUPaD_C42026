import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

# Cadena de conexión hacia PostgreSQL (ajustá usuario, contraseña, host y base de datos según tu entorno)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:admin@localhost:5432/productos_db"
)

# echo=True permite ver en consola las sentencias SQL que genera SQLModel
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]