import json
from datetime import datetime, timezone
from typing import Optional, Union
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlmodel import Session, select

from app.categoria.model import Categoria
from app.categoria.schema import CategoriaRead
from app.ingrediente.model import Ingrediente
from app.producto.model import Producto, ProductoCategoria, ProductoIngrediente
from app.producto.schema import (
    ProductoCreate,
    ProductoIngredienteInput,
    ProductoPaginatedResponse,
    ProductoRead,
    ProductoUpdate,
)


class ProductoService:
    @staticmethod
    def _to_read(session: Session, producto: Producto) -> ProductoRead:
        try:
            imagenes = json.loads(producto.imagenes_url) if producto.imagenes_url else []
        except Exception:
            imagenes = []

        enlaces = session.exec(
            select(ProductoCategoria).where(ProductoCategoria.producto_id == producto.id)
        ).all()
        cat_ids = [e.categoria_id for e in enlaces]

        return ProductoRead(
            id=producto.id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio_base=producto.precio_base,
            imagenes_url=imagenes,
            disponible=producto.disponible,
            categoria_ids=cat_ids,
            created_at=producto.created_at,
            updated_at=producto.updated_at,
            deleted_at=producto.deleted_at,
        )

    @staticmethod
    def _validar_categorias(session: Session, categoria_ids: list[int]) -> list[int]:
        ids_unicos = list(dict.fromkeys(categoria_ids))
        for cat_id in ids_unicos:
            cat = session.get(Categoria, cat_id)
            if not cat or cat.deleted_at is not None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"La categoría con ID {cat_id} no existe",
                )
        return ids_unicos

    @staticmethod
    def _normalizar_y_validar_ingredientes(
        session: Session,
        ingredientes: list[Union[int, ProductoIngredienteInput]],
    ) -> list[tuple[int, float]]:
        resultado: dict[int, float] = {}
        for item in ingredientes:
            if isinstance(item, int):
                ing_id, cant = item, 1.0
            else:
                ing_id, cant = item.ingrediente_id, item.cantidad

            ing = session.get(Ingrediente, ing_id)
            if not ing or ing.deleted_at is not None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"El ingrediente con ID {ing_id} no existe",
                )
            resultado[ing_id] = cant
        return list(resultado.items())

    @staticmethod
    def get_all(
        session: Session,
        offset: int = 0,
        limit: int = 10,
        nombre: Optional[str] = None,
        incluir_inactivos: bool = False,
    ) -> ProductoPaginatedResponse:
        query = select(Producto)
        if not incluir_inactivos:
            query = query.where(Producto.deleted_at.is_(None))
        if nombre:
            query = query.where(func.lower(Producto.nombre).contains(nombre.strip().lower()))

        todos = session.exec(query.order_by(Producto.id)).all()
        total = len(todos)
        paginados = todos[offset : offset + limit]
        items = [ProductoService._to_read(session, p) for p in paginados]
        return ProductoPaginatedResponse(
            total=total,
            offset=offset,
            limit=limit,
            items=items,
        )

    @staticmethod
    def get_by_id(session: Session, producto_id: int) -> ProductoRead:
        producto = session.get(Producto, producto_id)
        if not producto or producto.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con ID {producto_id} no existe",
            )
        return ProductoService._to_read(session, producto)

    @staticmethod
    def create(session: Session, data: ProductoCreate) -> ProductoRead:
        cat_ids = ProductoService._validar_categorias(session, data.categoria_ids)
        ing_validados = (
            ProductoService._normalizar_y_validar_ingredientes(session, data.ingredientes)
            if data.ingredientes
            else []
        )

        nuevo = Producto(
            nombre=data.nombre,
            descripcion=data.descripcion,
            precio_base=data.precio_base,
            imagenes_url=json.dumps(data.imagenes_url),
            disponible=data.disponible,
        )
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)

        for idx, cat_id in enumerate(cat_ids):
            session.add(
                ProductoCategoria(
                    producto_id=nuevo.id,
                    categoria_id=cat_id,
                    es_principal=(idx == 0),
                )
            )

        for ing_id, cant in ing_validados:
            session.add(
                ProductoIngrediente(
                    producto_id=nuevo.id,
                    ingrediente_id=ing_id,
                    cantidad=cant,
                )
            )

        session.commit()
        return ProductoService._to_read(session, nuevo)

    @staticmethod
    def update(session: Session, producto_id: int, data: ProductoUpdate) -> ProductoRead:
        producto = session.get(Producto, producto_id)
        if not producto or producto.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con ID {producto_id} no existe",
            )

        cat_ids = (
            ProductoService._validar_categorias(session, data.categoria_ids)
            if data.categoria_ids is not None
            else None
        )
        ing_validados = (
            ProductoService._normalizar_y_validar_ingredientes(session, data.ingredientes)
            if data.ingredientes is not None
            else None
        )

        producto.nombre = data.nombre
        producto.descripcion = data.descripcion
        producto.precio_base = data.precio_base
        producto.imagenes_url = json.dumps(data.imagenes_url)
        producto.disponible = data.disponible
        producto.updated_at = datetime.now(timezone.utc)
        session.add(producto)

        # RN-12: Reemplazar todas las categorías si se enviaron en el PUT
        if cat_ids is not None:
            actuales = session.exec(
                select(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)
            ).all()
            for rel in actuales:
                session.delete(rel)
            session.flush()
            for idx, cat_id in enumerate(cat_ids):
                session.add(
                    ProductoCategoria(
                        producto_id=producto_id,
                        categoria_id=cat_id,
                        es_principal=(idx == 0),
                    )
                )

        # RN-21: Reemplazar todos los ingredientes si se enviaron en el PUT
        if ing_validados is not None:
            ing_actuales = session.exec(
                select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)
            ).all()
            for rel in ing_actuales:
                session.delete(rel)
            session.flush()
            for ing_id, cant in ing_validados:
                session.add(
                    ProductoIngrediente(
                        producto_id=producto_id,
                        ingrediente_id=ing_id,
                        cantidad=cant,
                    )
                )

        session.commit()
        session.refresh(producto)
        return ProductoService._to_read(session, producto)

    @staticmethod
    def delete(session: Session, producto_id: int) -> None:
        producto = session.get(Producto, producto_id)
        if not producto or producto.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con ID {producto_id} no existe",
            )

        # RN-14: Borrado en cascada de las relaciones del producto
        rel_cats = session.exec(
            select(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)
        ).all()
        for rel in rel_cats:
            session.delete(rel)

        rel_ings = session.exec(
            select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)
        ).all()
        for rel in rel_ings:
            session.delete(rel)

        # Borrado lógico del producto
        producto.deleted_at = datetime.now(timezone.utc)
        producto.updated_at = datetime.now(timezone.utc)
        session.add(producto)
        session.commit()

    @staticmethod
    def get_categorias(session: Session, producto_id: int) -> list[CategoriaRead]:
        producto = session.get(Producto, producto_id)
        if not producto or producto.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con ID {producto_id} no existe",
            )

        enlaces = session.exec(
            select(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)
        ).all()

        categorias: list[CategoriaRead] = []
        for enlace in enlaces:
            cat = session.get(Categoria, enlace.categoria_id)
            if cat and cat.deleted_at is None:
                categorias.append(CategoriaRead.model_validate(cat))
        return categorias

    @staticmethod
    def get_ingredientes(session: Session, producto_id: int) -> list[dict]:
        producto = session.get(Producto, producto_id)
        if not producto or producto.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con ID {producto_id} no existe",
            )

        enlaces = session.exec(
            select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)
        ).all()

        resultado = []
        for enlace in enlaces:
            ing = session.get(Ingrediente, enlace.ingrediente_id)
            if ing and ing.deleted_at is None:
                resultado.append(
                    {
                        "id": ing.id,
                        "nombre": ing.nombre,
                        "descripcion": ing.descripcion,
                        "unidad_medida_id": ing.unidad_medida_id,
                        "cantidad": enlace.cantidad,
                    }
                )
        return resultado