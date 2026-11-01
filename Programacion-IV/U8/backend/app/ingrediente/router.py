from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.ingrediente.schema import (
    IngredienteCreate,
    IngredientePaginatedResponse,
    IngredienteRead,
    IngredienteUpdate,
)
from app.ingrediente.service import IngredienteService

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


@router.get("/", response_model=IngredientePaginatedResponse)
def listar_ingredientes(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    nombre: Optional[str] = Query(default=None),
    incluir_inactivos: bool = Query(default=False),
    session: Session = Depends(get_session),
):
    return IngredienteService.get_all(
        session=session,
        offset=offset,
        limit=limit,
        nombre=nombre,
        incluir_inactivos=incluir_inactivos,
    )


@router.post("/", response_model=IngredienteRead, status_code=status.HTTP_201_CREATED)
def crear_ingrediente(data: IngredienteCreate, session: Session = Depends(get_session)):
    return IngredienteService.create(session, data)


@router.get("/{ingrediente_id}", response_model=IngredienteRead)
def obtener_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    return IngredienteService.get_by_id(session, ingrediente_id)


@router.put("/{ingrediente_id}", response_model=IngredienteRead)
def actualizar_ingrediente(
    ingrediente_id: int, data: IngredienteUpdate, session: Session = Depends(get_session)
):
    return IngredienteService.update(session, ingrediente_id, data)


@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)) -> None:
    IngredienteService.delete(session, ingrediente_id)
    return None