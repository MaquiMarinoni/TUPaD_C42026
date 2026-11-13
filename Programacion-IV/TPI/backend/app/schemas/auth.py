from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UsuarioRegistro(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("username")
    @classmethod
    def validar_username(cls, value: str) -> str:
        value = value.strip()
        if not value or not all(
            char.isalnum() or char in "_-" for char in value
        ):
            raise ValueError(
                "El usuario solo puede contener letras, numeros, _ y -"
            )
        return value


class UsuarioLectura(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    email: EmailStr
    role: Literal["user", "admin"]
    disabled: bool
    created_at: datetime


class UsuarioEstado(BaseModel):
    disabled: bool


class Mensaje(BaseModel):
    message: str
