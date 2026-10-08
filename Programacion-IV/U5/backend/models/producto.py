from typing import Optional
from sqlmodel import SQLModel, Field


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    categoria: str = Field(index=True)
    precio: float
    stock: int
    stock_minimo: int
    activo: bool = Field(default=True)