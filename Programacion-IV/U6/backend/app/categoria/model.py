# app/categoria/model.py
from typing import Optional
from sqlmodel import SQLModel, Field

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    descripcion: str = Field(default="", nullable=False)