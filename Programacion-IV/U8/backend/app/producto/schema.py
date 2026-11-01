from datetime import datetime
from typing import Annotated, Optional, Union
from pydantic import ConfigDict, StringConstraints, field_validator
from sqlmodel import Field, SQLModel

NombreProductoNoVacio = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]


class ProductoIngredienteInput(SQLModel):
    ingrediente_id: int = Field(gt=0)
    cantidad: float = Field(default=1.0, gt=0)


class ProductoCategoriaAsignacion(SQLModel):
    categoria_id: int = Field(gt=0)
    es_principal: bool = Field(default=False)


class ProductoCreate(SQLModel):
    nombre: NombreProductoNoVacio
    descripcion: Optional[str] = Field(default="", max_length=500)
    precio_base: float = Field(ge=0, description="Precio base mayor o igual a 0")
    imagenes_url: Optional[list[str]] = Field(default_factory=list)
    disponible: bool = Field(default=True)
    categoria_ids: Optional[list[int]] = Field(default_factory=list)
    ingredientes: Optional[list[Union[int, ProductoIngredienteInput]]] = Field(default=None)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        limpio = v.strip()
        if not limpio:
            raise ValueError("El nombre del producto es obligatorio.")
        return limpio


class ProductoUpdate(SQLModel):
    nombre: Optional[NombreProductoNoVacio] = None
    descripcion: Optional[str] = Field(default=None, max_length=500)
    precio_base: Optional[float] = Field(default=None, ge=0)
    imagenes_url: Optional[list[str]] = None
    disponible: Optional[bool] = None
    categoria_ids: Optional[list[int]] = None
    ingredientes: Optional[list[Union[int, ProductoIngredienteInput]]] = None

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            limpio = v.strip()
            if not limpio:
                raise ValueError("El nombre del producto no puede estar vacío.")
            return limpio
        return v


class ProductoRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str = ""
    precio_base: float
    imagenes_url: list[str] = Field(default_factory=list)
    disponible: bool = True
    categoria_ids: list[int] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class ProductoPaginatedResponse(SQLModel):
    total: int
    offset: int
    limit: int
    items: list[ProductoRead]
