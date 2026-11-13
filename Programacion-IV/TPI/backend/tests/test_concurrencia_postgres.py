import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlmodel import SQLModel

import app.models
import app.uow.unit_of_work as uow_module
from app.core.security import hash_password
from app.db.session import engine as main_engine
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.schemas.pedido import ItemPedidoCrear, PedidoCrear
from app.services.pedido_service import PedidoService
from app.uow.unit_of_work import UnitOfWork


TEST_DB = "foodstore_tpi_concurrencia_test"


@pytest.fixture
def postgres_test(monkeypatch):
    original_url = main_engine.url

    if original_url.get_backend_name() != "postgresql":
        pytest.skip("La prueba requiere PostgreSQL")

    if original_url.database == TEST_DB:
        pytest.fail("La base principal no puede ser la base temporal")

    admin_url = original_url.set(database="postgres")
    admin_engine = create_engine(
        admin_url,
        isolation_level="AUTOCOMMIT",
    )

    test_url = original_url.set(database=TEST_DB)
    test_engine = None

    try:
        with admin_engine.connect() as conn:
            existe = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": TEST_DB},
            ).scalar()

            if existe:
                pytest.fail(
                    f"La base {TEST_DB} ya existe. "
                    "No se modificara ni eliminara automaticamente."
                )

            conn.execute(
                text(f'CREATE DATABASE "{TEST_DB}"')
            )

        test_engine = create_engine(
            test_url,
            pool_size=5,
            max_overflow=5,
        )

        SQLModel.metadata.create_all(test_engine)
        monkeypatch.setattr(uow_module, "engine", test_engine)

        with UnitOfWork() as uow:
            usuario = Usuario(
                username="cliente_concurrencia",
                full_name="Cliente Prueba",
                email="concurrencia@example.com",
                hashed_password=hash_password("Prueba123!"),
                role="user",
            )
            uow.usuarios.add(usuario)

            categoria = Categoria(nombre="Pruebas")
            uow.categorias.add(categoria)

            producto = Producto(
                categoria_id=categoria.id,
                nombre="Producto concurrencia",
                precio_base=1000,
                stock=1,
                disponible=True,
                activo=True,
            )
            uow.productos.add(producto)

            usuario_id = usuario.id
            producto_id = producto.id

        yield usuario_id, producto_id

    finally:
        monkeypatch.undo()

        if test_engine is not None:
            test_engine.dispose()

        with admin_engine.connect() as conn:
            conn.execute(
                text("""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = :name
                      AND pid <> pg_backend_pid()
                """),
                {"name": TEST_DB},
            )

            conn.execute(
                text(f'DROP DATABASE IF EXISTS "{TEST_DB}"')
            )

        admin_engine.dispose()


def test_dos_compras_simultaneas_no_generan_stock_negativo(
    postgres_test,
):
    usuario_id, producto_id = postgres_test

    barrera = Barrier(2)

    def comprar():
        datos = PedidoCrear(
            items=[
                ItemPedidoCrear(
                    producto_id=producto_id,
                    cantidad=1,
                )
            ],
            forma_pago="EFECTIVO",
            direccion_entrega="Calle de prueba 123",
        )

        barrera.wait(timeout=10)

        try:
            pedido = PedidoService().crear(datos, usuario_id)
            return ("ok", pedido.id)
        except Exception as exc:
            from fastapi import HTTPException

            if isinstance(exc, HTTPException):
                return ("error", exc.status_code)

            raise

    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(
            lambda _: comprar(),
            range(2),
        ))

    exitos = [r for r in resultados if r[0] == "ok"]
    errores = [r for r in resultados if r[0] == "error"]

    assert len(exitos) == 1, resultados
    assert len(errores) == 1, resultados
    assert errores[0][1] == 409, resultados

    with UnitOfWork() as uow:
        producto = uow.productos.get_by_id(producto_id)
        pedidos = uow.pedidos.get_all()

        assert producto.stock == 0
        assert len(pedidos) == 1
        assert pedidos[0].total == 1000

