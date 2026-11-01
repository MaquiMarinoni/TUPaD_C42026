from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingredientes"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, unique=True, index=True, nullable=False)
    descripcion: str = Field(default="", max_length=255)
    unidad_medida_id: Optional[int] = Field(
        default=None,
        foreign_key="unidades_medida.id",
        nullable=True,
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)
