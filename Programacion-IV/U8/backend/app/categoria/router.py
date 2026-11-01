from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.categoria.schema import (
    CategoriaCreate,
    CategoriaPaginatedResponse,
    CategoriaRead,
    CategoriaUpdate,
)
from app.categoria.service import CategoriaService
from app.core.database import get_session

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("/", response_model=CategoriaPaginatedResponse)
def listar_categorias(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    nombre: Optional[str] = Query(default=None),
    incluir_inactivos: bool = Query(default=False),
    session: Session = Depends(get_session),
):
    return CategoriaService.get_all(
        session=session,
        offset=offset,
        limit=limit,
        nombre=nombre,
        incluir_inactivos=incluir_inactivos,
    )


@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def crear_categoria(data: CategoriaCreate, session: Session = Depends(get_session)):
    return CategoriaService.create(session, data)


@router.get("/{categoria_id}", response_model=CategoriaRead)
def obtener_categoria(categoria_id: int, session: Session = Depends(get_session)):
    return CategoriaService.get_by_id(session, categoria_id)


@router.put("/{categoria_id}", response_model=CategoriaRead)
def actualizar_categoria(
    categoria_id: int, data: CategoriaUpdate, session: Session = Depends(get_session)
):
    return CategoriaService.update(session, categoria_id, data)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(categoria_id: int, session: Session = Depends(get_session)) -> None:
    CategoriaService.delete(session, categoria_id)
    return None


@router.get("/{categoria_id}/productos")
def listar_productos_de_categoria(
    categoria_id: int, session: Session = Depends(get_session)
):
    return CategoriaService.get_productos(session, categoria_id)