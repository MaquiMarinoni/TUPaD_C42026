from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlmodel import Session, select
from app.ingrediente.model import Ingrediente
from app.ingrediente.schema import (
    IngredienteCreate,
    IngredientePaginatedResponse,
    IngredienteRead,
    IngredienteUpdate,
)


def listar_ingredientes(
    session: Session,
    offset: int = 0,
    limit: int = 100,
    nombre: Optional[str] = None,
    incluir_inactivos: bool = False,
) -> IngredientePaginatedResponse:
    query = select(Ingrediente)
    if not incluir_inactivos:
        query = query.where(Ingrediente.deleted_at.is_(None))  # type: ignore[union-attr]
    if nombre:
        query = query.where(func.lower(Ingrediente.nombre).contains(nombre.strip().lower()))

    total_items = list(session.exec(query).all())
    total = len(total_items)
    items = total_items[offset : offset + limit]

    return IngredientePaginatedResponse(
        total=total,
        offset=offset,
        limit=limit,
        items=[IngredienteRead.model_validate(i) for i in items],
    )


def obtener_ingrediente(session: Session, ingrediente_id: int) -> Ingrediente:
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente or ingrediente.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingrediente con id {ingrediente_id} no encontrado.",
        )
    return ingrediente


def crear_ingrediente(session: Session, data: IngredienteCreate) -> Ingrediente:
    nombre_limpio = data.nombre.strip()
    existente = session.exec(
        select(Ingrediente).where(
            func.lower(Ingrediente.nombre) == nombre_limpio.lower(),
            Ingrediente.deleted_at.is_(None),  # type: ignore[union-attr]
        )
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un ingrediente con el nombre '{nombre_limpio}'.",
        )

    nuevo = Ingrediente(
        nombre=nombre_limpio,
        descripcion=(data.descripcion or "").strip(),
        unidad_medida_id=data.unidad_medida_id,
    )
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


def actualizar_ingrediente(
    session: Session, ingrediente_id: int, data: IngredienteUpdate
) -> Ingrediente:
    ingrediente = obtener_ingrediente(session, ingrediente_id)

    if data.nombre is not None:
        nombre_limpio = data.nombre.strip()
        duplicado = session.exec(
            select(Ingrediente).where(
                func.lower(Ingrediente.nombre) == nombre_limpio.lower(),
                Ingrediente.id != ingrediente_id,
                Ingrediente.deleted_at.is_(None),  # type: ignore[union-attr]
            )
        ).first()
        if duplicado:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe otro ingrediente con el nombre '{nombre_limpio}'.",
            )
        ingrediente.nombre = nombre_limpio

    if data.descripcion is not None:
        ingrediente.descripcion = data.descripcion.strip()
    if data.unidad_medida_id is not None:
        ingrediente.unidad_medida_id = data.unidad_medida_id

    ingrediente.updated_at = datetime.now(timezone.utc)
    session.add(ingrediente)
    session.commit()
    session.refresh(ingrediente)
    return ingrediente


def eliminar_ingrediente(session: Session, ingrediente_id: int) -> None:
    ingrediente = obtener_ingrediente(session, ingrediente_id)
    ingrediente.deleted_at = datetime.now(timezone.utc)
    ingrediente.updated_at = datetime.now(timezone.utc)
    session.add(ingrediente)
    session.commit()
