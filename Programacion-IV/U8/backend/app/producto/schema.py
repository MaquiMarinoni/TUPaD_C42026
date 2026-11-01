from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator


class ProductoIngredienteInput(BaseModel):
    ingrediente_id: int = Field(ge=1)
    cantidad: float = Field(default=1.0, ge=0)


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str = Field(default="")
    precio_base: float = Field(ge=0)
    imagenes_url: list[str] = Field(default_factory=list)
    disponible: bool = Field(default=True)

    @field_validator("nombre")
    @classmethod
    def validar_nombre_no_vacio(cls, v: str) -> str:
        limpio = v.strip()
        if not limpio:
            raise ValueError("El nombre del producto no puede estar vacío ni contener solo espacios")
        return limpio

    @field_validator("descripcion")
    @classmethod
    def limpiar_descripcion(cls, v: Optional[str]) -> str:
        if v is None:
            return ""
        return v.strip()


class ProductoCreate(ProductoBase):
    # RN-19: obligatorio y al menos 1 ID de categoría
    categoria_ids: list[int] = Field(min_length=1)
    # RN-20: opcional; acepta lista de IDs [1, 2] o lista de objetos [{"ingrediente_id": 1, "cantidad": 100}]
    ingredientes: Optional[list[Union[int, ProductoIngredienteInput]]] = None


class ProductoUpdate(ProductoBase):
    # RN-12: si se envía, reemplaza todas las categorías asociadas
    categoria_ids: Optional[list[int]] = None
    # RN-21: si se envía, reemplaza todos los ingredientes asociados
    ingredientes: Optional[list[Union[int, ProductoIngredienteInput]]] = None

    @field_validator("categoria_ids")
    @classmethod
    def validar_categorias_en_update(cls, v: Optional[list[int]]) -> Optional[list[int]]:
        if v is not None and len(v) == 0:
            raise ValueError("El producto debe tener al menos una categoría asociada")
        return v


class ProductoRead(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio_base: float
    imagenes_url: list[str]
    disponible: bool
    categoria_ids: list[int] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


ProductoResponse = ProductoRead


class ProductoPaginatedResponse(BaseModel):
    total: int
    offset: int
    limit: int
    items: list[ProductoRead]