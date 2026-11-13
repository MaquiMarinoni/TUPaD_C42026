from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.categoria import CategoriaLectura


class ProductoCrear(BaseModel):
    categoria_id: int = Field(gt=0)
    nombre: str = Field(min_length=2, max_length=150)
    descripcion: str | None = None
    precio_base: float = Field(ge=0)
    imagen_url: str | None = None
    stock: int = Field(default=0, ge=0)
    disponible: bool = True

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("El nombre debe tener al menos dos caracteres")
        return value


class ProductoActualizar(BaseModel):
    categoria_id: int | None = Field(default=None, gt=0)
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    descripcion: str | None = None
    precio_base: float | None = Field(default=None, ge=0)
    imagen_url: str | None = None
    stock: int | None = Field(default=None, ge=0)
    disponible: bool | None = None

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if len(value) < 2:
            raise ValueError("El nombre debe tener al menos dos caracteres")
        return value


class ProductoStock(BaseModel):
    stock: int = Field(ge=0)


class ProductoDisponibilidad(BaseModel):
    disponible: bool


class ProductoLectura(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    categoria_id: int
    nombre: str
    descripcion: str | None
    precio_base: float
    imagen_url: str | None
    stock: int
    disponible: bool
    activo: bool
    categoria: CategoriaLectura


class ProductosPaginados(BaseModel):
    total: int
    items: list[ProductoLectura]
