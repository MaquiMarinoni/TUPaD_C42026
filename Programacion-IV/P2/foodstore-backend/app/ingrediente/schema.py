from datetime import datetime
from typing import Annotated, Optional
from pydantic import ConfigDict, StringConstraints, field_validator
from sqlmodel import Field, SQLModel

NombreNoVacio = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class IngredienteBase(SQLModel):
    nombre: NombreNoVacio
    descripcion: Optional[str] = Field(default="", max_length=255)
    unidad_medida_id: Optional[int] = Field(default=None)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        limpio = v.strip()
        if not limpio:
            raise ValueError("El nombre del ingrediente no puede estar vacío ni contener solo espacios.")
        return limpio


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(SQLModel):
    nombre: Optional[NombreNoVacio] = None
    descripcion: Optional[str] = Field(default=None, max_length=255)
    unidad_medida_id: Optional[int] = Field(default=None)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            limpio = v.strip()
            if not limpio:
                raise ValueError("El nombre del ingrediente no puede estar vacío ni contener solo espacios.")
            return limpio
        return v


class IngredienteRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: Optional[str] = ""
    unidad_medida_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class IngredientePaginatedResponse(SQLModel):
    total: int
    offset: int
    limit: int
    items: list[IngredienteRead]
