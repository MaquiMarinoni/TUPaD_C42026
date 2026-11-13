from fastapi import HTTPException

from app.models.producto import Producto
from app.schemas.producto import (
    ProductoActualizar,
    ProductoCrear,
    ProductoLectura,
    ProductosPaginados,
)
from app.uow.unit_of_work import UnitOfWork


class ProductoService:
    @staticmethod
    def _validar_categoria(uow, categoria_id: int) -> None:
        categoria = uow.categorias.get_by_id(categoria_id)
        if categoria is None or not categoria.activo:
            raise HTTPException(404, "Categoria inexistente o inactiva")

    def listar(
        self,
        skip: int = 0,
        limit: int = 20,
        buscar: str | None = None,
        categoria_id: int | None = None,
        disponible: bool | None = None,
        solo_activos: bool = True,
    ) -> ProductosPaginados:
        with UnitOfWork() as uow:
            total, productos = uow.productos.buscar(
                skip=skip,
                limit=limit,
                buscar=buscar,
                categoria_id=categoria_id,
                disponible=disponible,
                solo_activos=solo_activos,
            )
            return ProductosPaginados(
                total=total,
                items=[
                    ProductoLectura.model_validate(p)
                    for p in productos
                ],
            )

    def obtener(
        self, producto_id: int, solo_activos: bool = True
    ) -> ProductoLectura:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id_con_categoria(producto_id)
            if producto is None:
                raise HTTPException(404, "Producto inexistente")
            if solo_activos and (
                not producto.activo or not producto.categoria.activo
            ):
                raise HTTPException(404, "Producto inexistente")
            return ProductoLectura.model_validate(producto)

    def crear(self, data: ProductoCrear) -> ProductoLectura:
        with UnitOfWork() as uow:
            self._validar_categoria(uow, data.categoria_id)

            producto = Producto(**data.model_dump())
            uow.productos.add(producto)

            producto = uow.productos.get_by_id_con_categoria(producto.id)
            return ProductoLectura.model_validate(producto)

    def actualizar(
        self, producto_id: int, data: ProductoActualizar
    ) -> ProductoLectura:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id(producto_id)
            if producto is None or not producto.activo:
                raise HTTPException(404, "Producto inexistente")

            cambios = data.model_dump(exclude_unset=True)

            no_nulos = {
                "categoria_id", "nombre", "precio_base",
                "stock", "disponible",
            }
            for campo in no_nulos:
                if campo in cambios and cambios[campo] is None:
                    raise HTTPException(422, f"{campo} no puede ser nulo")

            if "categoria_id" in cambios:
                self._validar_categoria(uow, cambios["categoria_id"])

            for campo, valor in cambios.items():
                setattr(producto, campo, valor)

            uow.session.flush()
            producto = uow.productos.get_by_id_con_categoria(producto_id)
            return ProductoLectura.model_validate(producto)

    def cambiar_stock(
        self, producto_id: int, stock: int
    ) -> ProductoLectura:
        with UnitOfWork() as uow:
            producto = uow.productos.get_for_update(producto_id)
            if producto is None or not producto.activo:
                raise HTTPException(404, "Producto inexistente")

            producto.stock = stock
            uow.session.flush()
            producto = uow.productos.get_by_id_con_categoria(producto_id)
            return ProductoLectura.model_validate(producto)

    def cambiar_disponibilidad(
        self, producto_id: int, disponible: bool
    ) -> ProductoLectura:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id(producto_id)
            if producto is None or not producto.activo:
                raise HTTPException(404, "Producto inexistente")

            producto.disponible = disponible
            uow.session.flush()
            producto = uow.productos.get_by_id_con_categoria(producto_id)
            return ProductoLectura.model_validate(producto)

    def eliminar(self, producto_id: int) -> None:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id(producto_id)
            if producto is None or not producto.activo:
                raise HTTPException(404, "Producto inexistente")

            producto.activo = False
            uow.session.flush()
