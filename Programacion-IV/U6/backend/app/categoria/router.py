# app/categoria/router.py
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.categoria.schema import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.categoria.service import CategoriaService

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("", response_model=List[CategoriaResponse], status_code=status.HTTP_200_OK)
def listar_categorias(session: Session = Depends(get_session)):
    return CategoriaService.get_all(session)

@router.get("/{categoria_id}", response_model=CategoriaResponse, status_code=status.HTTP_200_OK)
def obtener_categoria(categoria_id: int, session: Session = Depends(get_session)):
    return CategoriaService.get_by_id(session, categoria_id)

@router.post("", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria_in: CategoriaCreate, session: Session = Depends(get_session)):
    return CategoriaService.create(session, categoria_in)

@router.put("/{categoria_id}", response_model=CategoriaResponse, status_code=status.HTTP_200_OK)
def actualizar_categoria(
    categoria_id: int,
    categoria_in: CategoriaUpdate,
    session: Session = Depends(get_session)
):
    return CategoriaService.update(session, categoria_id, categoria_in)

@router.delete("/{categoria_id}", status_code=status.HTTP_200_OK)
def eliminar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    CategoriaService.delete(session, categoria_id)
    return {"message": f"Categoría {categoria_id} eliminada con éxito"}