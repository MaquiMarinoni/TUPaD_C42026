
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy import func

from app.modules.productos.model import Producto
from app.modules.productos.link_model import ProductoCategoria
from app.modules.productos.schema import (
    ProductoCreate,
    ProductoUpdate,
    ProductoPublic,
    CategoriaProductoPublic,
)
from app.modules.categorias.model import Categoria
from app.modules.unidades_medida.model import UnidadMedida, TipoUnidad
from app.modules.unidades_medida.schema import UnidadMedidaPublic


def obtener_modelo(session: Session, producto_id: int):
    producto = session.get(Producto, producto_id)

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto


def validar_nombre(
    session: Session,
    nombre: str,
    excluir_id: int | None = None
):
    consulta = select(Producto).where(
        func.lower(Producto.nombre) == nombre.lower(),
        Producto.activo == True
    )

    if excluir_id is not None:
        consulta = consulta.where(Producto.id != excluir_id)

    existente = session.exec(consulta).first()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un producto activo con ese nombre"
        )


def validar_unidad_y_stock(
    session: Session,
    unidad_id: int,
    stock: Decimal
):
    unidad = session.get(UnidadMedida, unidad_id)

    if unidad is None:
        raise HTTPException(
            status_code=404,
            detail="Unidad de medida no encontrada"
        )

    if unidad.tipo == TipoUnidad.contable:
        if stock != stock.to_integral_value():
            raise HTTPException(
                status_code=422,
                detail="El stock de una unidad contable debe ser entero"
            )

    return unidad


def preparar_respuesta(session: Session, producto: Producto):
    unidad = session.get(
        UnidadMedida,
        producto.unidad_venta_id
    )

    relaciones = session.exec(
        select(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto.id
        )
    ).all()

    categorias = []

    for relacion in relaciones:
        categoria = session.get(
            Categoria,
            relacion.categoria_id
        )

        if categoria is not None:
            categorias.append(
                CategoriaProductoPublic(
                    id=categoria.id,
                    nombre=categoria.nombre,
                    descripcion=categoria.descripcion,
                    activo=categoria.activo,
                    anulado_at=categoria.anulado_at,
                    es_principal=relacion.es_principal
                )
            )

    return ProductoPublic(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio_base=producto.precio_base,
        unidad_venta_id=producto.unidad_venta_id,
        stock_cantidad=producto.stock_cantidad,
        disponible=producto.disponible,
        activo=producto.activo,
        anulado_at=producto.anulado_at,
        unidad_venta=UnidadMedidaPublic.model_validate(
            unidad,
            from_attributes=True
        ),
        categorias=categorias,
        hay_stock=producto.stock_cantidad > 0
    )


def crear_producto(session: Session, datos: ProductoCreate):
    validar_nombre(session, datos.nombre)

    validar_unidad_y_stock(
        session,
        datos.unidad_venta_id,
        datos.stock_cantidad
    )

    producto = Producto(**datos.model_dump())

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return preparar_respuesta(session, producto)


def listar_productos(
    session: Session,
    skip: int = 0,
    limit: int = 10,
    activo: bool | None = None,
    disponible: bool | None = None,
    categoria_id: int | None = None,
    search: str | None = None
):
    consulta = select(Producto)

    if activo is None:
        consulta = consulta.where(Producto.activo == True)
    else:
        consulta = consulta.where(Producto.activo == activo)

    if disponible is not None:
        consulta = consulta.where(
            Producto.disponible == disponible
        )

    if categoria_id is not None:
        consulta = consulta.where(
            Producto.id.in_(
                select(ProductoCategoria.producto_id).where(
                    ProductoCategoria.categoria_id == categoria_id
                )
            )
        )

    if search:
        consulta = consulta.where(
            Producto.nombre.ilike(f"%{search}%")
        )

    consulta = consulta.order_by(Producto.id)
    consulta = consulta.offset(skip).limit(limit)

    productos = session.exec(consulta).all()

    return [
        preparar_respuesta(session, producto)
        for producto in productos
    ]


def obtener_producto(session: Session, producto_id: int):
    producto = obtener_modelo(session, producto_id)
    return preparar_respuesta(session, producto)


def actualizar_producto(
    session: Session,
    producto_id: int,
    datos: ProductoUpdate
):
    producto = obtener_modelo(session, producto_id)

    if not producto.activo:
        raise HTTPException(
            status_code=409,
            detail="No se puede modificar un producto anulado"
        )

    validar_nombre(
        session,
        datos.nombre,
        excluir_id=producto_id
    )

    validar_unidad_y_stock(
        session,
        datos.unidad_venta_id,
        datos.stock_cantidad
    )

    for campo, valor in datos.model_dump().items():
        setattr(producto, campo, valor)

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return preparar_respuesta(session, producto)


def anular_producto(session: Session, producto_id: int):
    producto = obtener_modelo(session, producto_id)

    if not producto.activo:
        raise HTTPException(
            status_code=409,
            detail="El producto ya esta anulado"
        )

    producto.activo = False
    producto.anulado_at = datetime.now(timezone.utc)

    session.add(producto)
    session.commit()


def clasificar_producto(
    session: Session,
    producto_id: int,
    categoria_id: int,
    es_principal: bool = False
):
    producto = obtener_modelo(session, producto_id)

    if not producto.activo:
        raise HTTPException(
            status_code=409,
            detail="No se puede clasificar un producto anulado"
        )

    categoria = session.get(Categoria, categoria_id)

    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    if not categoria.activo:
        raise HTTPException(
            status_code=409,
            detail="No se puede utilizar una categoria anulada"
        )

    relacion_existente = session.get(
        ProductoCategoria,
        (producto_id, categoria_id)
    )

    if relacion_existente is not None:
        raise HTTPException(
            status_code=409,
            detail="El producto ya pertenece a esta categoria"
        )

    if es_principal:
        relaciones = session.exec(
            select(ProductoCategoria).where(
                ProductoCategoria.producto_id == producto_id,
                ProductoCategoria.es_principal == True
            )
        ).all()

        for relacion in relaciones:
            relacion.es_principal = False
            session.add(relacion)

    nueva_relacion = ProductoCategoria(
        producto_id=producto_id,
        categoria_id=categoria_id,
        es_principal=es_principal
    )

    session.add(nueva_relacion)
    session.commit()
    session.refresh(nueva_relacion)

    return obtener_categorias_producto(session, producto_id)


def obtener_categorias_producto(
    session: Session,
    producto_id: int
):
    obtener_modelo(session, producto_id)

    relaciones = session.exec(
        select(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id
        )
    ).all()

    resultado = []

    for relacion in relaciones:
        categoria = session.get(
            Categoria,
            relacion.categoria_id
        )

        if categoria is not None:
            resultado.append(
                CategoriaProductoPublic(
                    id=categoria.id,
                    nombre=categoria.nombre,
                    descripcion=categoria.descripcion,
                    activo=categoria.activo,
                    anulado_at=categoria.anulado_at,
                    es_principal=relacion.es_principal
                )
            )

    return resultado
