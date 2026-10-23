from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class IngredienteBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str = Field(default="", max_length=255)
    unidad_medida_id: int = Field(ge=1)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        limpio = v.strip()
        if not limpio:
            raise ValueError("El nombre del ingrediente no puede estar vacío")
        return limpio


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(IngredienteBase):
    pass


class IngredienteRead(BaseModel):
    id: int
    nombre: str
    descripcion: str
    unidad_medida_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class IngredientePaginatedResponse(BaseModel):
    total: int
    offset: int
    limit: int
    items: list[IngredienteRead]