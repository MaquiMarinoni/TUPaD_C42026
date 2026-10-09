# app/core/database.py
import os
from sqlmodel import SQLModel, create_engine, Session

# Archivo de base de datos SQLite local
DATABASE_FILE = "foodstore.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# check_same_thread=False es necesario para SQLite con FastAPI
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Crea las tablas en la base de datos si no existen."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Generador de sesión para inyección de dependencias en los endpoints."""
    with Session(engine) as session:
        yield session