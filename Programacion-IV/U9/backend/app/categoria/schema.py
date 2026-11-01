from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class CategoriaBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str = Field(default="", max_length=255)

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        limpio = v.strip()
        if not limpio:
            raise ValueError("El nombre de la categoría no puede estar vacío ni contener solo espacios")
        return limpio

    @field_validator("descripcion")
    @classmethod
    def limpiar_descripcion(cls, v: Optional[str]) -> str:
        if v is None:
            return ""
        return v.strip()


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaRead(BaseModel):
    id: int
    nombre: str
    descripcion: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# Alias para mantener compatibilidad con imports existentes
CategoriaResponse = CategoriaRead


class CategoriaPaginatedResponse(BaseModel):
    total: int
    offset: int
    limit: int
    items: list[CategoriaRead]