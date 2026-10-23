import json
from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlmodel import Session, select

from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaPaginatedResponse, CategoriaUpdate
from app.producto.model import Producto, ProductoCategoria


class CategoriaService:
    @staticmethod
    def get_all(
        session: Session,
        offset: int = 0,
        limit: int = 10,
        nombre: Optional[str] = None,
        incluir_inactivos: bool = False,
    ) -> CategoriaPaginatedResponse:
        query = select(Categoria)
        if not incluir_inactivos:
            query = query.where(Categoria.deleted_at.is_(None))
        if nombre:
            query = query.where(func.lower(Categoria.nombre).contains(nombre.strip().lower()))

        todas = session.exec(query.order_by(Categoria.id)).all()
        total = len(todas)
        items = todas[offset : offset + limit]
        return CategoriaPaginatedResponse(
            total=total,
            offset=offset,
            limit=limit,
            items=items,
        )

    @staticmethod
    def get_by_id(session: Session, categoria_id: int, incluir_inactivos: bool = False) -> Categoria:
        categoria = session.get(Categoria, categoria_id)
        if not categoria or (not incluir_inactivos and categoria.deleted_at is not None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La categoría con ID {categoria_id} no existe",
            )
        return categoria

    @staticmethod
    def create(session: Session, data: CategoriaCreate) -> Categoria:
        existente = session.exec(
            select(Categoria).where(func.lower(Categoria.nombre) == data.nombre.lower())
        ).first()

        if existente:
            if existente.deleted_at is None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una categoría con el nombre '{data.nombre}'",
                )
            # Si estaba eliminada lógicamente, la reactivamos con los nuevos datos
            existente.nombre = data.nombre
            existente.descripcion = data.descripcion
            existente.deleted_at = None
            existente.updated_at = datetime.now(timezone.utc)
            session.add(existente)
            session.commit()
            session.refresh(existente)
            return existente

        nueva = Categoria(nombre=data.nombre, descripcion=data.descripcion)
        session.add(nueva)
        session.commit()
        session.refresh(nueva)
        return nueva

    @staticmethod
    def update(session: Session, categoria_id: int, data: CategoriaUpdate) -> Categoria:
        categoria = CategoriaService.get_by_id(session, categoria_id)

        duplicada = session.exec(
            select(Categoria).where(
                func.lower(Categoria.nombre) == data.nombre.lower(),
                Categoria.id != categoria_id,
            )
        ).first()

        if duplicada:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe otra categoría con el nombre '{data.nombre}'",
            )

        categoria.nombre = data.nombre
        categoria.descripcion = data.descripcion
        categoria.updated_at = datetime.now(timezone.utc)
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria

    @staticmethod
    def delete(session: Session, categoria_id: int) -> None:
        categoria = CategoriaService.get_by_id(session, categoria_id)

        # RN-05: No eliminar si tiene productos activos asociados
        enlaces = session.exec(
            select(ProductoCategoria).where(ProductoCategoria.categoria_id == categoria_id)
        ).all()

        for enlace in enlaces:
            prod = session.get(Producto, enlace.producto_id)
            if prod and getattr(prod, "deleted_at", None) is None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="No se puede eliminar la categoría porque tiene productos asociados",
                )

        categoria.deleted_at = datetime.now(timezone.utc)
        categoria.updated_at = datetime.now(timezone.utc)
        session.add(categoria)
        session.commit()

    @staticmethod
    def get_productos(session: Session, categoria_id: int) -> list[dict]:
        CategoriaService.get_by_id(session, categoria_id)
        enlaces = session.exec(
            select(ProductoCategoria).where(ProductoCategoria.categoria_id == categoria_id)
        ).all()

        resultado = []
        for enlace in enlaces:
            prod = session.get(Producto, enlace.producto_id)
            if prod and getattr(prod, "deleted_at", None) is None:
                raw_imgs = getattr(prod, "imagenes_url", None) or getattr(prod, "imagen_url", "[]")
                try:
                    imgs = json.loads(raw_imgs) if isinstance(raw_imgs, str) else list(raw_imgs)
                except Exception:
                    imgs = []
                resultado.append(
                    {
                        "id": prod.id,
                        "nombre": prod.nombre,
                        "descripcion": prod.descripcion,
                        "precio_base": float(prod.precio_base),
                        "imagenes_url": imgs,
                        "disponible": prod.disponible,
                    }
                )
        return resultado