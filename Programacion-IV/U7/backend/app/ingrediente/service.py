from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlmodel import Session, select

from app.ingrediente.model import Ingrediente
from app.ingrediente.schema import (
    IngredienteCreate,
    IngredientePaginatedResponse,
    IngredienteUpdate,
)
from app.unidad_medida.model import UnidadMedida


class IngredienteService:
    @staticmethod
    def get_all(
        session: Session,
        offset: int = 0,
        limit: int = 10,
        nombre: Optional[str] = None,
        incluir_inactivos: bool = False,
    ) -> IngredientePaginatedResponse:
        query = select(Ingrediente)
        if not incluir_inactivos:
            query = query.where(Ingrediente.deleted_at.is_(None))
        if nombre:
            query = query.where(func.lower(Ingrediente.nombre).contains(nombre.strip().lower()))

        todos = session.exec(query.order_by(Ingrediente.id)).all()
        total = len(todos)
        items = todos[offset : offset + limit]
        return IngredientePaginatedResponse(
            total=total,
            offset=offset,
            limit=limit,
            items=items,
        )

    @staticmethod
    def get_by_id(session: Session, ingrediente_id: int) -> Ingrediente:
        ingrediente = session.get(Ingrediente, ingrediente_id)
        if not ingrediente or ingrediente.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El ingrediente con ID {ingrediente_id} no existe",
            )
        return ingrediente

    @staticmethod
    def create(session: Session, data: IngredienteCreate) -> Ingrediente:
        if not session.get(UnidadMedida, data.unidad_medida_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La unidad de medida con ID {data.unidad_medida_id} no existe",
            )

        existente = session.exec(
            select(Ingrediente).where(func.lower(Ingrediente.nombre) == data.nombre.lower())
        ).first()

        if existente:
            if existente.deleted_at is None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un ingrediente con el nombre '{data.nombre}'",
                )
            existente.nombre = data.nombre
            existente.descripcion = data.descripcion
            existente.unidad_medida_id = data.unidad_medida_id
            existente.deleted_at = None
            existente.updated_at = datetime.now(timezone.utc)
            session.add(existente)
            session.commit()
            session.refresh(existente)
            return existente

        nuevo = Ingrediente(
            nombre=data.nombre,
            descripcion=data.descripcion,
            unidad_medida_id=data.unidad_medida_id,
        )
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        return nuevo

    @staticmethod
    def update(session: Session, ingrediente_id: int, data: IngredienteUpdate) -> Ingrediente:
        ingrediente = IngredienteService.get_by_id(session, ingrediente_id)

        if not session.get(UnidadMedida, data.unidad_medida_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La unidad de medida con ID {data.unidad_medida_id} no existe",
            )

        duplicado = session.exec(
            select(Ingrediente).where(
                func.lower(Ingrediente.nombre) == data.nombre.lower(),
                Ingrediente.id != ingrediente_id,
            )
        ).first()

        if duplicado:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe otro ingrediente con el nombre '{data.nombre}'",
            )

        ingrediente.nombre = data.nombre
        ingrediente.descripcion = data.descripcion
        ingrediente.unidad_medida_id = data.unidad_medida_id
        ingrediente.updated_at = datetime.now(timezone.utc)
        session.add(ingrediente)
        session.commit()
        session.refresh(ingrediente)
        return ingrediente

    @staticmethod
    def delete(session: Session, ingrediente_id: int) -> None:
        ingrediente = IngredienteService.get_by_id(session, ingrediente_id)
        ingrediente.deleted_at = datetime.now(timezone.utc)
        ingrediente.updated_at = datetime.now(timezone.utc)
        session.add(ingrediente)
        session.commit()