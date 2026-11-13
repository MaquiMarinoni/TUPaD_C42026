import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine

import app.models
import app.uow.unit_of_work as uow_module
from app.models.categoria import Categoria
from app.uow.unit_of_work import UnitOfWork


@pytest.fixture
def test_engine(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    monkeypatch.setattr(uow_module, "engine", engine)
    yield engine
    engine.dispose()


def test_commit_guarda_los_cambios(test_engine):
    with UnitOfWork() as uow:
        uow.categorias.add(
            Categoria(nombre="Categoria prueba", descripcion="Test")
        )

    with UnitOfWork() as uow:
        categorias = uow.categorias.get_all()
        assert len(categorias) == 1
        assert categorias[0].nombre == "Categoria prueba"


def test_rollback_revierte_los_cambios(test_engine):
    with pytest.raises(ValueError):
        with UnitOfWork() as uow:
            uow.categorias.add(
                Categoria(nombre="Categoria rollback")
            )
            raise ValueError("Error simulado")

    with UnitOfWork() as uow:
        assert uow.categorias.get_all() == []


def test_repositorios_comparten_sesion(test_engine):
    with UnitOfWork() as uow:
        assert uow.usuarios.session is uow.session
        assert uow.categorias.session is uow.session
        assert uow.productos.session is uow.session
        assert uow.pedidos.session is uow.session
        assert uow.detalles_pedido.session is uow.session


def test_no_permite_categoria_duplicada(test_engine):
    with UnitOfWork() as uow:
        uow.categorias.add(Categoria(nombre="Bebidas"))

    with pytest.raises(Exception):
        with UnitOfWork() as uow:
            uow.categorias.add(Categoria(nombre="Bebidas"))

    with UnitOfWork() as uow:
        assert len(uow.categorias.get_all()) == 1
