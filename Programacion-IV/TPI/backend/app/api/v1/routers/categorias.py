from fastapi import APIRouter, Depends, Response, status

from app.api.deps import require_role
from app.models.usuario import Usuario
from app.schemas.categoria import (
    CategoriaActualizar,
    CategoriaCrear,
    CategoriaLectura,
)
from app.services.categoria_service import CategoriaService


router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("", response_model=list[CategoriaLectura])
def listar():
    return CategoriaService().listar()


@router.get("/{categoria_id}", response_model=CategoriaLectura)
def obtener(categoria_id: int):
    return CategoriaService().obtener(categoria_id)


@router.post(
    "",
    response_model=CategoriaLectura,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    data: CategoriaCrear,
    admin: Usuario = Depends(require_role("admin")),
):
    return CategoriaService().crear(data)


@router.put("/{categoria_id}", response_model=CategoriaLectura)
def actualizar(
    categoria_id: int,
    data: CategoriaActualizar,
    admin: Usuario = Depends(require_role("admin")),
):
    return CategoriaService().actualizar(categoria_id, data)


@router.delete("/{categoria_id}", status_code=204)
def eliminar(
    categoria_id: int,
    admin: Usuario = Depends(require_role("admin")),
):
    CategoriaService().eliminar(categoria_id)
    return Response(status_code=204)
