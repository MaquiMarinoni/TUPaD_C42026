# app/categoria/schema.py
from pydantic import BaseModel

# Esquema para crear una categoría (sin ID)
class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: str

# Esquema para actualizar una categoría
class CategoriaUpdate(BaseModel):
    nombre: str
    descripcion: str

# Esquema para respuesta (con ID)
class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str

    class Config:
        from_attributes = True