# app/producto/schema.py
from typing import List, Optional
from pydantic import BaseModel, Field

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio_base: str
    imagen_url: List[str] = Field(default_factory=list)
    disponible: bool = True

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[str] = None
    imagen_url: Optional[List[str]] = None
    disponible: Optional[bool] = None

class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True

# Esquema para asociar o desasociar producto y categoría
class ProductoCategoriaLink(BaseModel):
    producto_id: int
    categoria_id: int