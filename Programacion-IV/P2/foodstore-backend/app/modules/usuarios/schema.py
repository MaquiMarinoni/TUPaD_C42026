from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre: str = Field(min_length=1, max_length=80)
    apellido: str = Field(min_length=1, max_length=80)
    email: EmailStr = Field(max_length=254)
    celular: str | None = Field(default=None, max_length=20)
    password: str = Field(min_length=8, max_length=72)

    @field_validator("nombre", "apellido")
    @classmethod
    def texto_no_vacio(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El campo no puede estar vacío")
        return value

    @field_validator("password")
    @classmethod
    def limite_bcrypt(cls, value: str) -> str:
        if len(value.encode()) > 72:
            raise ValueError("La contraseña no puede superar 72 bytes UTF-8")
        return value


class UserPublic(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    celular: str | None = None
    roles: list[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
