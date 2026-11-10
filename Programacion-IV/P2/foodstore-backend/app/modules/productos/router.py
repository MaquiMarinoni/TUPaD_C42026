
from fastapi import APIRouter, Depends, Path, Query, Response
from sqlmodel import Session

from app.core.database import get_session
from app.modules.productos.schema import (
    ProductoCreate,
    ProductoUpdate,
    ProductoPublic,
    ProductoCategoriaCreate,
    CategoriaProductoPublic,
)
from app.modules.productos import service


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.post(
    "",
    response_model=ProductoPublic,
    status_code=201
)
def crear_producto(
    datos: ProductoCreate,
    session: Session = Depends(get_session)
):
    return service.crear_producto(session, datos)


@router.get(
    "",
    response_model=list[ProductoPublic]
)
def listar_productos(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=50),
    activo: bool | None = Query(default=None),
    disponible: bool | None = Query(default=None),
    categoria_id: int | None = Query(default=None),
    search: str | None = Query(default=None),
    session: Session = Depends(get_session)
):
    return service.listar_productos(
        session=session,
        skip=skip,
        limit=limit,
        activo=activo,
        disponible=disponible,
        categoria_id=categoria_id,
        search=search
    )


@router.get(
    "/{producto_id}",
    response_model=ProductoPublic
)
def obtener_producto(
    producto_id: int = Path(ge=1),
    session: Session = Depends(get_session)
):
    return service.obtener_producto(session, producto_id)


@router.put(
    "/{producto_id}",
    response_model=ProductoPublic
)
def actualizar_producto(
    datos: ProductoUpdate,
    producto_id: int = Path(ge=1),
    session: Session = Depends(get_session)
):
    return service.actualizar_producto(
        session,
        producto_id,
        datos
    )


@router.delete(
    "/{producto_id}",
    status_code=204,
    response_class=Response
)
def anular_producto(
    producto_id: int = Path(ge=1),
    session: Session = Depends(get_session)
):
    service.anular_producto(session, producto_id)
    return Response(status_code=204)


@router.post(
    "/{producto_id}/categorias",
    response_model=list[CategoriaProductoPublic],
    status_code=201
)
def clasificar_producto(
    datos: ProductoCategoriaCreate,
    producto_id: int = Path(ge=1),
    session: Session = Depends(get_session)
):
    return service.clasificar_producto(
        session,
        producto_id,
        datos.categoria_id,
        datos.es_principal
    )


@router.get(
    "/{producto_id}/categorias",
    response_model=list[CategoriaProductoPublic]
)
def obtener_categorias_producto(
    producto_id: int = Path(ge=1),
    session: Session = Depends(get_session)
):
    return service.obtener_categorias_producto(
        session,
        producto_id
    )
