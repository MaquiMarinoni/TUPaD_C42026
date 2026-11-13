from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models.categoria import Categoria
from app.schemas.categoria import (
    CategoriaActualizar,
    CategoriaCrear,
    CategoriaLectura,
)
from app.uow.unit_of_work import UnitOfWork


class CategoriaService:
    def listar(self) -> list[CategoriaLectura]:
        with UnitOfWork() as uow:
            return [
                CategoriaLectura.model_validate(c)
                for c in uow.categorias.get_activas()
            ]

    def obtener(self, categoria_id: int) -> CategoriaLectura:
        with UnitOfWork() as uow:
            categoria = uow.categorias.get_by_id(categoria_id)

            if categoria is None or not categoria.activo:
                raise HTTPException(404, "Categoria inexistente")

            return CategoriaLectura.model_validate(categoria)

    def crear(self, data: CategoriaCrear) -> CategoriaLectura:
        nombre = data.nombre.strip()

        if len(nombre) < 2:
            raise HTTPException(422, "Nombre demasiado corto")

        try:
            with UnitOfWork() as uow:
                if uow.categorias.get_by_nombre(nombre):
                    raise HTTPException(409, "La categoria ya existe")

                categoria = Categoria(
                    nombre=nombre,
                    descripcion=data.descripcion,
                )
                uow.categorias.add(categoria)
                return CategoriaLectura.model_validate(categoria)
        except IntegrityError:
            raise HTTPException(409, "La categoria ya existe") from None

    def actualizar(
        self,
        categoria_id: int,
        data: CategoriaActualizar,
    ) -> CategoriaLectura:
        try:
            with UnitOfWork() as uow:
                categoria = uow.categorias.get_by_id(categoria_id)

                if categoria is None:
                    raise HTTPException(404, "Categoria inexistente")

                cambios = data.model_dump(exclude_unset=True)

                if "nombre" in cambios:
                    if cambios["nombre"] is None:
                        raise HTTPException(422, "Nombre obligatorio")

                    nombre = cambios["nombre"].strip()
                    if len(nombre) < 2:
                        raise HTTPException(422, "Nombre demasiado corto")

                    existente = uow.categorias.get_by_nombre(nombre)
                    if existente and existente.id != categoria_id:
                        raise HTTPException(409, "La categoria ya existe")

                    cambios["nombre"] = nombre

                if cambios.get("activo") is None and "activo" in cambios:
                    raise HTTPException(422, "Estado invalido")

                for campo, valor in cambios.items():
                    setattr(categoria, campo, valor)

                uow.session.flush()
                return CategoriaLectura.model_validate(categoria)
        except IntegrityError:
            raise HTTPException(409, "La categoria ya existe") from None

    def eliminar(self, categoria_id: int) -> None:
        with UnitOfWork() as uow:
            categoria = uow.categorias.get_by_id(categoria_id)

            if categoria is None or not categoria.activo:
                raise HTTPException(404, "Categoria inexistente")

            categoria.activo = False
            uow.session.flush()
