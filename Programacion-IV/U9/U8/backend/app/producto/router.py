from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from app.core.database import get_session
from app.producto.schema import (
    ProductoCategoriaAsignacion,
    ProductoCreate,
    ProductoPaginatedResponse,
    ProductoRead,
    ProductoUpdate,
)
from app.producto.service import (
    actualizar_producto,
    asignar_categoria_a_producto,
    crear_producto,
    eliminar_producto,
    listar_productos,
    obtener_producto,
    quitar_categoria_de_producto,
)

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("", response_model=ProductoPaginatedResponse, status_code=status.HTTP_200_OK)
@router.get("/", response_model=ProductoPaginatedResponse, status_code=status.HTTP_200_OK, include_in_schema=False)
def get_productos(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    nombre: Optional[str] = Query(default=None),
    incluir_inactivos: bool = Query(default=False),
    session: Session = Depends(get_session),
):
    return listar_productos(session, offset, limit, nombre, incluir_inactivos)


@router.get("/{producto_id}", response_model=ProductoRead, status_code=status.HTTP_200_OK)
def get_producto(producto_id: int, session: Session = Depends(get_session)):
    return obtener_producto(session, producto_id)


@router.post("", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def post_producto(data: ProductoCreate, session: Session = Depends(get_session)):
    return crear_producto(session, data)


@router.put("/{producto_id}", response_model=ProductoRead, status_code=status.HTTP_200_OK)
def put_producto(
    producto_id: int,
    data: ProductoUpdate,
    session: Session = Depends(get_session),
):
    return actualizar_producto(session, producto_id, data)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int, session: Session = Depends(get_session)):
    eliminar_producto(session, producto_id)


@router.post(
    "/{producto_id}/categorias",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED,
)
def post_producto_categoria_body(
    producto_id: int,
    data: ProductoCategoriaAsignacion,
    session: Session = Depends(get_session),
):
    return asignar_categoria_a_producto(
        session, producto_id, data.categoria_id, data.es_principal
    )


@router.post(
    "/{producto_id}/categorias/{categoria_id}",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED,
)
def post_producto_categoria_path(
    producto_id: int,
    categoria_id: int,
    session: Session = Depends(get_session),
):
    return asignar_categoria_a_producto(session, producto_id, categoria_id, False)


@router.delete(
    "/{producto_id}/categorias/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_producto_categoria(
    producto_id: int,
    categoria_id: int,
    session: Session = Depends(get_session),
):
    quitar_categoria_de_producto(session, producto_id, categoria_id)
