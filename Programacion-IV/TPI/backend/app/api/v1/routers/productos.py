from pydantic import AliasChoices
from fastapi import APIRouter, Depends, Query, Response, status

from app.api.deps import require_role
from app.models.usuario import Usuario
from app.schemas.producto import (
    ProductoActualizar,
    ProductoCrear,
    ProductoDisponibilidad,
    ProductoLectura,
    ProductoStock,
    ProductosPaginados,
)
from app.services.producto_service import ProductoService


router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("", response_model=ProductosPaginados)
def listar(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    buscar: str | None = Query(default=None, validation_alias=AliasChoices("search", "buscar")),
    categoria_id: int | None = Query(default=None, gt=0),
    disponible: bool | None = None,
):
    return ProductoService().listar(
        skip, limit, buscar, categoria_id, disponible
    )


@router.get("/admin/todos", response_model=ProductosPaginados)
def listar_administracion(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    admin: Usuario = Depends(require_role("admin")),
):
    return ProductoService().listar(
        skip=skip, limit=limit, solo_activos=False
    )


@router.get("/{producto_id}", response_model=ProductoLectura)
def obtener(producto_id: int):
    return ProductoService().obtener(producto_id)


@router.post(
    "",
    response_model=ProductoLectura,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    data: ProductoCrear,
    admin: Usuario = Depends(require_role("admin")),
):
    return ProductoService().crear(data)


@router.put("/{producto_id}", response_model=ProductoLectura)
def actualizar(
    producto_id: int,
    data: ProductoActualizar,
    admin: Usuario = Depends(require_role("admin")),
):
    return ProductoService().actualizar(producto_id, data)


@router.patch("/{producto_id}/stock", response_model=ProductoLectura)
def cambiar_stock(
    producto_id: int,
    data: ProductoStock,
    admin: Usuario = Depends(require_role("admin")),
):
    return ProductoService().cambiar_stock(producto_id, data.stock)


@router.patch("/{producto_id}/disponible", response_model=ProductoLectura)
def cambiar_disponibilidad(
    producto_id: int,
    data: ProductoDisponibilidad,
    admin: Usuario = Depends(require_role("admin")),
):
    return ProductoService().cambiar_disponibilidad(
        producto_id, data.disponible
    )


@router.delete("/{producto_id}", status_code=204)
def eliminar(
    producto_id: int,
    admin: Usuario = Depends(require_role("admin")),
):
    ProductoService().eliminar(producto_id)
    return Response(status_code=204)
