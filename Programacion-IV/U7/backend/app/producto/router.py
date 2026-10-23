from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.categoria.schema import CategoriaRead
from app.core.database import get_session
from app.producto.schema import (
    ProductoCreate,
    ProductoPaginatedResponse,
    ProductoRead,
    ProductoUpdate,
)
from app.producto.service import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=ProductoPaginatedResponse)
def listar_productos(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    nombre: Optional[str] = Query(default=None),
    incluir_inactivos: bool = Query(default=False),
    session: Session = Depends(get_session),
):
    return ProductoService.get_all(
        session=session,
        offset=offset,
        limit=limit,
        nombre=nombre,
        incluir_inactivos=incluir_inactivos,
    )


@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(data: ProductoCreate, session: Session = Depends(get_session)):
    return ProductoService.create(session, data)


@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    return ProductoService.get_by_id(session, producto_id)


@router.put("/{producto_id}", response_model=ProductoRead)
def actualizar_producto(
    producto_id: int, data: ProductoUpdate, session: Session = Depends(get_session)
):
    return ProductoService.update(session, producto_id, data)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)) -> None:
    ProductoService.delete(session, producto_id)
    return None


@router.get("/{producto_id}/categorias", response_model=list[CategoriaRead])
def listar_categorias_de_producto(producto_id: int, session: Session = Depends(get_session)):
    return ProductoService.get_categorias(session, producto_id)


@router.get("/{producto_id}/ingredientes")
def listar_ingredientes_de_producto(producto_id: int, session: Session = Depends(get_session)):
    return ProductoService.get_ingredientes(session, producto_id)