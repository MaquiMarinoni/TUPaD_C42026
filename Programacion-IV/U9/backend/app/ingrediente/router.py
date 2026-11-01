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
from app.ingrediente.service import (
    actualizar_ingrediente,
    crear_ingrediente,
    eliminar_ingrediente,
    listar_ingredientes,
    obtener_ingrediente,
)

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


@router.get("", response_model=IngredientePaginatedResponse, status_code=status.HTTP_200_OK)
@router.get("/", response_model=IngredientePaginatedResponse, status_code=status.HTTP_200_OK, include_in_schema=False)
def get_ingredientes(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    nombre: Optional[str] = Query(default=None),
    incluir_inactivos: bool = Query(default=False),
    session: Session = Depends(get_session),
):
    return listar_ingredientes(session, offset, limit, nombre, incluir_inactivos)


@router.get("/{ingrediente_id}", response_model=IngredienteRead, status_code=status.HTTP_200_OK)
def get_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    return obtener_ingrediente(session, ingrediente_id)


@router.post("", response_model=IngredienteRead, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=IngredienteRead, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def post_ingrediente(data: IngredienteCreate, session: Session = Depends(get_session)):
    return crear_ingrediente(session, data)


@router.patch("/{ingrediente_id}", response_model=IngredienteRead, status_code=status.HTTP_200_OK)
@router.put("/{ingrediente_id}", response_model=IngredienteRead, status_code=status.HTTP_200_OK)
def put_ingrediente(
    ingrediente_id: int,
    data: IngredienteUpdate,
    session: Session = Depends(get_session),
):
    return actualizar_ingrediente(session, ingrediente_id, data)


@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    eliminar_ingrediente(session, ingrediente_id)
