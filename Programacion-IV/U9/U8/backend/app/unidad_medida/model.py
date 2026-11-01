from typing import Optional
from sqlmodel import Field, SQLModel


class UnidadMedida(SQLModel, table=True):
    __tablename__ = "unidades_medida"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True, index=True)
    simbolo: str = Field(max_length=10)
    tipo: str = Field(max_length=30)