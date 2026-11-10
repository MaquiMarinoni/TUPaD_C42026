
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


NombreCategoria = Annotated[str, Field(min_length=3)]


class CategoriaBase(BaseModel):
    nombre: NombreCategoria
    descripcion: str | None = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaPublic(CategoriaBase):
    id: int
    activo: bool
    anulado_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
