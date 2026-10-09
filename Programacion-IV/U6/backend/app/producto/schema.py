# app/producto/schema.py
from typing import List, Optional
from pydantic import BaseModel, Field

class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=120, description="El nombre no puede estar vacío")
    descripcion: str = Field(default="", max_length=255)
    precio_base: str = Field(min_length=1, description="El precio base no puede estar vacío")
    imagen_url: List[str] = Field(default_factory=list)
    disponible: bool = True

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1)
    descripcion: Optional[str] = None
    precio_base: Optional[str] = Field(default=None, min_length=1)
    imagen_url: Optional[List[str]] = None
    disponible: Optional[bool] = None

class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True

class ProductoCategoriaLink(BaseModel):
    producto_id: int
    categoria_id: int