
from sqlmodel import SQLModel, Field


class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    producto_id: int = Field(
        foreign_key="productos.id",
        primary_key=True
    )

    categoria_id: int = Field(
        foreign_key="categorias.id",
        primary_key=True
    )

    es_principal: bool = Field(default=False, nullable=False)
