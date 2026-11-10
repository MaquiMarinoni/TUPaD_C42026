import json
from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlmodel import Session, select
from app.categoria.model import Categoria
from app.ingrediente.model import Ingrediente
from app.producto.model import Producto, ProductoCategoria, ProductoIngrediente
from app.producto.schema import (
    ProductoCreate,
    ProductoIngredienteInput,
    ProductoPaginatedResponse,
    ProductoRead,
    ProductoUpdate,
)


def _to_producto_read(session: Session, producto: Producto) -> ProductoRead:
    try:
        imagenes = json.loads(producto.imagenes_url) if isinstance(producto.imagenes_url, str) else (producto.imagenes_url or [])
    except Exception:
        imagenes = []

    relaciones_cat = session.exec(
        select(ProductoCategoria).where(ProductoCategoria.producto_id == producto.id)
    ).all()
    categoria_ids = [rel.categoria_id for rel in relaciones_cat]

    return ProductoRead(
        id=producto.id,  # type: ignore[arg-type]
        nombre=producto.nombre,
        descripcion=producto.descripcion or "",
        precio_base=producto.precio_base,
        imagenes_url=imagenes,
        disponible=producto.disponible,
        categoria_ids=categoria_ids,
        created_at=getattr(producto, "created_at", None),
        updated_at=getattr(producto, "updated_at", None),
        deleted_at=getattr(producto, "deleted_at", None),
    )


def listar_productos(
    session: Session,
    offset: int = 0,
    limit: int = 100,
    nombre: Optional[str] = None,
    incluir_inactivos: bool = False,
) -> ProductoPaginatedResponse:
    query = select(Producto)
    query = query.where(Producto.deleted_at.is_(None))  # type: ignore[union-attr]
    if nombre:
        query = query.where(func.lower(Producto.nombre).contains(nombre.strip().lower()))

    todos = list(session.exec(query).all())
    total = len(todos)
    recorte = todos[offset : offset + limit]

    return ProductoPaginatedResponse(
        total=total,
        offset=offset,
        limit=limit,
        items=[_to_producto_read(session, p) for p in recorte],
    )


def obtener_producto_entidad(session: Session, producto_id: int) -> Producto:
    producto = session.get(Producto, producto_id)
    if not producto or producto.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {producto_id} no encontrado.",
        )
    return producto


def obtener_producto(session: Session, producto_id: int) -> ProductoRead:
    producto = obtener_producto_entidad(session, producto_id)
    return _to_producto_read(session, producto)


def _sincronizar_categorias(session: Session, producto_id: int, categoria_ids: list[int]) -> None:
    existentes = session.exec(
        select(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)
    ).all()
    for rel in existentes:
        session.delete(rel)
    session.flush()

    vistos: set[int] = set()
    for idx, cat_id in enumerate(categoria_ids):
        if cat_id in vistos:
            continue
        vistos.add(cat_id)
        cat = session.get(Categoria, cat_id)
        if not cat or cat.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con id {cat_id} no encontrada.",
            )
        session.add(
            ProductoCategoria(
                producto_id=producto_id,
                categoria_id=cat_id,
                es_principal=(idx == 0),
            )
        )


def _sincronizar_ingredientes(session: Session, producto_id: int, ingredientes_input: list) -> None:
    existentes = session.exec(
        select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)
    ).all()
    for rel in existentes:
        session.delete(rel)
    session.flush()

    vistos: set[int] = set()
    for item in ingredientes_input:
        if isinstance(item, int):
            ing_id = item
            cantidad = 1.0
        elif isinstance(item, ProductoIngredienteInput):
            ing_id = item.ingrediente_id
            cantidad = item.cantidad
        elif isinstance(item, dict):
            ing_id = int(item.get("ingrediente_id", 0))
            cantidad = float(item.get("cantidad", 1.0))
        else:
            continue

        if ing_id in vistos:
            continue
        vistos.add(ing_id)

        ing = session.get(Ingrediente, ing_id)
        if not ing or ing.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ingrediente con id {ing_id} no encontrado.",
            )
        session.add(
            ProductoIngrediente(
                producto_id=producto_id,
                ingrediente_id=ing_id,
                cantidad=cantidad,
            )
        )


def crear_producto(session: Session, data: ProductoCreate) -> ProductoRead:
    nuevo = Producto(
        nombre=data.nombre.strip(),
        descripcion=(data.descripcion or "").strip(),
        precio_base=data.precio_base,
        imagenes_url=json.dumps(data.imagenes_url or []),
        disponible=data.disponible,
    )
    session.add(nuevo)
    session.flush()

    if data.categoria_ids:
        _sincronizar_categorias(session, nuevo.id, data.categoria_ids)  # type: ignore[arg-type]
    if data.ingredientes:
        _sincronizar_ingredientes(session, nuevo.id, data.ingredientes)  # type: ignore[arg-type]

    session.commit()
    session.refresh(nuevo)
    return _to_producto_read(session, nuevo)


def actualizar_producto(
    session: Session, producto_id: int, data: ProductoUpdate
) -> ProductoRead:
    producto = obtener_producto_entidad(session, producto_id)

    if data.nombre is not None:
        producto.nombre = data.nombre.strip()
    if data.descripcion is not None:
        producto.descripcion = data.descripcion.strip()
    if data.precio_base is not None:
        producto.precio_base = data.precio_base
    if data.imagenes_url is not None:
        producto.imagenes_url = json.dumps(data.imagenes_url)
    if data.disponible is not None:
        producto.disponible = data.disponible

    if data.categoria_ids is not None:
        _sincronizar_categorias(session, producto_id, data.categoria_ids)
    if data.ingredientes is not None:
        _sincronizar_ingredientes(session, producto_id, data.ingredientes)

    producto.updated_at = datetime.now(timezone.utc)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return _to_producto_read(session, producto)


def eliminar_producto(session: Session, producto_id: int) -> None:
    producto = obtener_producto_entidad(session, producto_id)
    producto.deleted_at = datetime.now(timezone.utc)
    producto.updated_at = datetime.now(timezone.utc)
    session.add(producto)
    session.commit()


def asignar_categoria_a_producto(
    session: Session,
    producto_id: int,
    categoria_id: int,
    es_principal: bool = False,
) -> ProductoRead:
    producto = obtener_producto_entidad(session, producto_id)
    categoria = session.get(Categoria, categoria_id)
    if not categoria or categoria.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con id {categoria_id} no encontrada.",
        )

    existente = session.exec(
        select(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id,
            ProductoCategoria.categoria_id == categoria_id,
        )
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La categoría {categoria_id} ya está asignada al producto {producto_id}.",
        )

    relacion = ProductoCategoria(
        producto_id=producto_id,
        categoria_id=categoria_id,
        es_principal=es_principal,
    )
    session.add(relacion)
    session.commit()
    session.refresh(producto)
    return _to_producto_read(session, producto)


def quitar_categoria_de_producto(
    session: Session, producto_id: int, categoria_id: int
) -> None:
    obtener_producto_entidad(session, producto_id)
    relacion = session.exec(
        select(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id,
            ProductoCategoria.categoria_id == categoria_id,
        )
    ).first()
    if not relacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La categoría {categoria_id} no está asociada al producto {producto_id}.",
        )
    session.delete(relacion)
    session.commit()
