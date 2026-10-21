from typing import Optional
from sqlmodel import SQLModel, Field

# Tabla intermedia para la relación N:N
class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categorias.id", primary_key=True)

# Entidad Producto
class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    descripcion: str = Field(default="", nullable=False)
    precio_base: str = Field(nullable=False)  # str según consigna oficial
    imagen_url_raw: str = Field(default="[]", nullable=False)  # Almacena la lista serializada en JSON
    disponible: bool = Field(default=True, nullable=False)