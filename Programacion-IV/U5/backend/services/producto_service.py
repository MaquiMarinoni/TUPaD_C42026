from typing import List, Optional
from sqlmodel import Session, select
from models.producto import Producto
from schemas.producto import ProductoCreate


def crear(session: Session, data: ProductoCreate) -> Producto:
    # 1. Transformamos el DTO validado (ProductoCreate) en el Modelo de Tabla (Producto)
    nuevo_producto = Producto(**data.model_dump())
    try:
        # 2. Registramos el objeto en la sesión activa
        session.add(nuevo_producto)
        # 3. Confirmamos la transacción en PostgreSQL
        session.commit()
        # 4. Refrescamos la instancia para obtener el ID autogenerado por la BD
        session.refresh(nuevo_producto)
        return nuevo_producto
    except Exception:
        session.rollback()
        raise


def obtener_todos(session: Session, skip: int, limit: int) -> List[Producto]:
    # Consulta paginada delegada a PostgreSQL mediante OFFSET y LIMIT
    statement = select(Producto).offset(skip).limit(limit)
    resultados = session.exec(statement).all()
    return list(resultados)


def obtener_por_id(session: Session, id: int) -> Optional[Producto]:
    # Búsqueda directa por Primary Key en PostgreSQL
    return session.get(Producto, id)


def actualizar_total(
    session: Session, id: int, data: ProductoCreate
) -> Optional[Producto]:
    # Reemplazo total (PUT): buscamos la entidad persistida
    producto_db = session.get(Producto, id)
    if not producto_db:
        return None

    # Actualizamos todos los atributos con los datos validados del DTO
    datos_actualizados = data.model_dump()
    for campo, valor in datos_actualizados.items():
        setattr(producto_db, campo, valor)

    try:
        session.add(producto_db)
        session.commit()
        session.refresh(producto_db)
        return producto_db
    except Exception:
        session.rollback()
        raise


def desactivar(session: Session, id: int) -> Optional[Producto]:
    # Borrado lógico (Soft Delete): solo altera el estado 'activo' a False
    producto_db = session.get(Producto, id)
    if not producto_db:
        return None

    producto_db.activo = False
    try:
        session.add(producto_db)
        session.commit()
        session.refresh(producto_db)
        return producto_db
    except Exception:
        session.rollback()
        raise


def obtener_estado_stock(session: Session, id: int) -> Optional[dict]:
    producto_db = session.get(Producto, id)
    if not producto_db:
        return None

    # La lógica de negocio vive en la capa de servicio
    alerta_stock = producto_db.stock < producto_db.stock_minimo

    return {
        "stock": producto_db.stock,
        "bajo_stock_minimo": alerta_stock,
        "activo": producto_db.activo,
    }