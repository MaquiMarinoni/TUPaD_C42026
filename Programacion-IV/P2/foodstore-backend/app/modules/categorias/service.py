
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session, select

from app.modules.categorias.model import Categoria
from app.modules.categorias.schema import (
    CategoriaCreate,
    CategoriaUpdate
)


def listar_categorias(
    session: Session,
    activo: bool | None = None,
    search: str | None = None
):
    consulta = select(Categoria)

    if activo is None:
        consulta = consulta.where(Categoria.activo == True)
    else:
        consulta = consulta.where(Categoria.activo == activo)

    if search:
        consulta = consulta.where(
            Categoria.nombre.ilike(f"%{search}%")
        )

    return session.exec(consulta).all()


def obtener_categoria(session: Session, categoria_id: int):
    categoria = session.get(Categoria, categoria_id)

    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    return categoria


def validar_nombre(
    session: Session,
    nombre: str,
    excluir_id: int | None = None
):
    consulta = select(Categoria).where(
        Categoria.nombre == nombre,
        Categoria.activo == True
    )

    if excluir_id is not None:
        consulta = consulta.where(Categoria.id != excluir_id)

    existente = session.exec(consulta).first()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una categoria activa con ese nombre"
        )


def crear_categoria(session: Session, datos: CategoriaCreate):
    validar_nombre(session, datos.nombre)

    categoria = Categoria(**datos.model_dump())

    session.add(categoria)
    session.commit()
    session.refresh(categoria)

    return categoria


def actualizar_categoria(
    session: Session,
    categoria_id: int,
    datos: CategoriaUpdate
):
    categoria = obtener_categoria(session, categoria_id)

    if not categoria.activo:
        raise HTTPException(
            status_code=409,
            detail="No se puede modificar una categoria anulada"
        )

    validar_nombre(session, datos.nombre, categoria_id)

    categoria.nombre = datos.nombre
    categoria.descripcion = datos.descripcion

    session.add(categoria)
    session.commit()
    session.refresh(categoria)

    return categoria


def anular_categoria(session: Session, categoria_id: int):
    categoria = obtener_categoria(session, categoria_id)

    if not categoria.activo:
        raise HTTPException(
            status_code=409,
            detail="La categoria ya esta anulada"
        )

    categoria.activo = False
    categoria.anulado_at = datetime.now(timezone.utc)

    session.add(categoria)
    session.commit()
