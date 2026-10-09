import json
from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.producto.model import Producto, ProductoCategoria
from app.producto.schema import ProductoCreate, ProductoUpdate, ProductoResponse
from app.categoria.model import Categoria

class ProductoService:
    @staticmethod
    def _to_response(db_prod: Producto) -> ProductoResponse:
        try:
            urls = json.loads(db_prod.imagen_url_raw)
        except Exception:
            urls = []
        return ProductoResponse(
            id=db_prod.id,
            nombre=db_prod.nombre,
            descripcion=db_prod.descripcion,
            precio_base=db_prod.precio_base,
            imagen_url=urls,
            disponible=db_prod.disponible
        )

    @classmethod
    def get_all(cls, session: Session) -> List[ProductoResponse]:
        productos = session.exec(select(Producto).order_by(Producto.id)).all()
        return [cls._to_response(p) for p in productos]

    @classmethod
    def get_by_id(cls, session: Session, producto_id: int) -> ProductoResponse:
        prod = session.get(Producto, producto_id)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado"
            )
        return cls._to_response(prod)

    @classmethod
    def create(cls, session: Session, producto_in: ProductoCreate) -> ProductoResponse:
        # Validación de duplicados
        statement = select(Producto).where(Producto.nombre.ilike(producto_in.nombre.strip()))
        existe = session.exec(statement).first()
        if existe:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un producto con el nombre '{producto_in.nombre}'"
            )

        raw_urls = json.dumps(producto_in.imagen_url)
        db_prod = Producto(
            nombre=producto_in.nombre.strip(),
            descripcion=producto_in.descripcion.strip(),
            precio_base=producto_in.precio_base.strip(),
            imagen_url_raw=raw_urls,
            disponible=producto_in.disponible
        )
        session.add(db_prod)
        session.commit()
        session.refresh(db_prod)
        return cls._to_response(db_prod)

    @classmethod
    def update(cls, session: Session, producto_id: int, producto_in: ProductoUpdate) -> ProductoResponse:
        db_prod = session.get(Producto, producto_id)
        if not db_prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado"
            )

        if producto_in.nombre is not None:
            # Validar duplicados al cambiar nombre
            statement = select(Producto).where(
                Producto.nombre.ilike(producto_in.nombre.strip()),
                Producto.id != producto_id
            )
            duplicado = session.exec(statement).first()
            if duplicado:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El nombre '{producto_in.nombre}' ya pertenece a otro producto"
                )
            db_prod.nombre = producto_in.nombre.strip()

        if producto_in.descripcion is not None:
            db_prod.descripcion = producto_in.descripcion.strip()
        if producto_in.precio_base is not None:
            db_prod.precio_base = producto_in.precio_base.strip()
        if producto_in.imagen_url is not None:
            db_prod.imagen_url_raw = json.dumps(producto_in.imagen_url)
        if producto_in.disponible is not None:
            db_prod.disponible = producto_in.disponible

        session.add(db_prod)
        session.commit()
        session.refresh(db_prod)
        return cls._to_response(db_prod)

    @staticmethod
    def delete(session: Session, producto_id: int) -> None:
        db_prod = session.get(Producto, producto_id)
        if not db_prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado"
            )
        # Eliminar también asociaciones en la tabla intermedia
        statement = select(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)
        relaciones = session.exec(statement).all()
        for rel in relaciones:
            session.delete(rel)

        session.delete(db_prod)
        session.commit()

    @staticmethod
    def asociar_categoria(session: Session, producto_id: int, categoria_id: int) -> None:
        prod = session.get(Producto, producto_id)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado"
            )
        cat = session.get(Categoria, categoria_id)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con id {categoria_id} no encontrada"
            )

        link = session.get(ProductoCategoria, (producto_id, categoria_id))
        if link:
            return  # Ya existe la asociación

        nuevo_link = ProductoCategoria(producto_id=producto_id, categoria_id=categoria_id)
        session.add(nuevo_link)
        session.commit()

    @staticmethod
    def desasociar_categoria(session: Session, producto_id: int, categoria_id: int) -> None:
        link = session.get(ProductoCategoria, (producto_id, categoria_id))
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe relación entre Producto {producto_id} y Categoría {categoria_id}"
            )
        session.delete(link)
        session.commit()

    @staticmethod
    def get_categorias_de_producto(session: Session, producto_id: int) -> List[Categoria]:
        prod = session.get(Producto, producto_id)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado"
            )
        statement = (
            select(Categoria)
            .join(ProductoCategoria, Categoria.id == ProductoCategoria.categoria_id)
            .where(ProductoCategoria.producto_id == producto_id)
        )
        return session.exec(statement).all()