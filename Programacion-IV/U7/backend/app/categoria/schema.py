# app/categoria/schema.py
from pydantic import BaseModel, Field

class CategoriaCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100, description="El nombre no puede estar vacío")
    descripcion: str = Field(default="", max_length=255)

class CategoriaUpdate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100, description="El nombre no puede estar vacío")
    descripcion: str = Field(default="", max_length=255)

class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str

    class Config:
        from_attributes = True