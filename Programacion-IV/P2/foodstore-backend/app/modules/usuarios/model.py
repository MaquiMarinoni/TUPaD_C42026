from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=80)
    apellido: str = Field(max_length=80)
    email: str = Field(max_length=254, unique=True, index=True)
    celular: str | None = Field(default=None, max_length=20)
    password_hash: str = Field(max_length=60)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    deleted_at: datetime | None = None


class Rol(SQLModel, table=True):
    __tablename__ = "roles"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True)
    descripcion: str = ""


class UsuarioRol(SQLModel, table=True):
    __tablename__ = "usuario_rol"
    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    rol_id: int = Field(foreign_key="roles.id", primary_key=True)
    asignado_por_id: int | None = Field(default=None, foreign_key="usuarios.id")
    expires_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
