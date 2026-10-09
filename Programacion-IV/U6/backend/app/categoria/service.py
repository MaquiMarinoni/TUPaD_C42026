
from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaUpdate

class CategoriaService:
    @staticmethod
    def get_all(session: Session) -> List[Categoria]:
        statement = select(Categoria).order_by(Categoria.id)
        return session.exec(statement).all()

    @staticmethod
    def get_by_id(session: Session, categoria_id: int) -> Categoria:
        categoria = session.get(Categoria, categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con id {categoria_id} no encontrada"
            )
        return categoria

    @staticmethod
    def create(session: Session, categoria_in: CategoriaCreate) -> Categoria:
        # Validación de duplicados (409 Conflict)
        statement = select(Categoria).where(Categoria.nombre.ilike(categoria_in.nombre.strip()))
        existe = session.exec(statement).first()
        if existe:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una categoría con el nombre '{categoria_in.nombre}'"
            )

        db_categoria = Categoria(
            nombre=categoria_in.nombre.strip(),
            descripcion=categoria_in.descripcion.strip()
        )
        session.add(db_categoria)
        session.commit()
        session.refresh(db_categoria)
        return db_categoria

    @staticmethod
    def update(session: Session, categoria_id: int, categoria_in: CategoriaUpdate) -> Categoria:
        db_categoria = session.get(Categoria, categoria_id)
        if not db_categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con id {categoria_id} no encontrada"
            )

        # Validar si el nuevo nombre ya pertenece a OTRA categoría
        statement = select(Categoria).where(
            Categoria.nombre.ilike(categoria_in.nombre.strip()),
            Categoria.id != categoria_id
        )
        duplicada = session.exec(statement).first()
        if duplicada:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El nombre '{categoria_in.nombre}' ya está siendo utilizado por otra categoría"
            )

        db_categoria.nombre = categoria_in.nombre.strip()
        db_categoria.descripcion = categoria_in.descripcion.strip()
        session.add(db_categoria)
        session.commit()
        session.refresh(db_categoria)
        return db_categoria

    @staticmethod
    def delete(session: Session, categoria_id: int) -> None:
        db_categoria = session.get(Categoria, categoria_id)
        if not db_categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con id {categoria_id} no encontrada"
            )
        session.delete(db_categoria)
        session.commit()