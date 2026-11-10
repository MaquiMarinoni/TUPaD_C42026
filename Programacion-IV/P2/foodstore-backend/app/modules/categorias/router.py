
from fastapi import APIRouter, Depends, Path, Query, Response
from sqlmodel import Session

from app.core.database import get_session
from app.modules.categorias.schema import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaPublic,
)
from app.modules.categorias import service


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


@router.post(
    "",
    response_model=CategoriaPublic,
    status_code=201
)
def crear_categoria(
    datos: CategoriaCreate,
    session: Session = Depends(get_session)
):
    return service.crear_categoria(session, datos)


@router.get(
    "",
    response_model=list[CategoriaPublic]
)
def listar_categorias(
    activo: bool | None = Query(default=None),
    search: str | None = Query(default=None),
    session: Session = Depends(get_session)
):
    return service.listar_categorias(session, activo, search)


@router.get(
    "/{categoria_id}",
    response_model=CategoriaPublic
)
def obtener_categoria(
    categoria_id: int = Path(ge=1),
    session: Session = Depends(get_session)
):
    return service.obtener_categoria(session, categoria_id)


@router.put(
    "/{categoria_id}",
    response_model=CategoriaPublic
)
def actualizar_categoria(
    datos: CategoriaUpdate,
    categoria_id: int = Path(ge=1),
    session: Session = Depends(get_session)
):
    return service.actualizar_categoria(
        session, categoria_id, datos
    )


@router.delete(
    "/{categoria_id}",
    status_code=204,
    response_class=Response
)
def anular_categoria(
    categoria_id: int = Path(ge=1),
    session: Session = Depends(get_session)
):
    service.anular_categoria(session, categoria_id)
    return Response(status_code=204)
