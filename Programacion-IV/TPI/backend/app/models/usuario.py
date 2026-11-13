from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.pedido import Pedido


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(
        sa_column=Column(String(100), unique=True, nullable=False, index=True)
    )
    full_name: str = Field(max_length=150)
    email: str = Field(
        sa_column=Column(String(255), unique=True, nullable=False, index=True)
    )
    hashed_password: str
    role: str = Field(default="user", max_length=10)
    disabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)

    pedidos: list["Pedido"] = Relationship(back_populates="usuario")

