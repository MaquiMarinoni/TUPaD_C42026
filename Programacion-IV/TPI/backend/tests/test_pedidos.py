import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine

import app.models
import app.uow.unit_of_work as uow_module
from app.core.security import hash_password
from app.main import app
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.uow.unit_of_work import UnitOfWork


@pytest.fixture
def client(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    monkeypatch.setattr(uow_module, "engine", engine)

    with UnitOfWork() as uow:
        uow.usuarios.add(Usuario(
            username="cliente",
            full_name="Cliente",
            email="cliente@example.com",
            hashed_password=hash_password("Cliente123!"),
            role="user",
        ))
        uow.usuarios.add(Usuario(
            username="admin",
            full_name="Administrador",
            email="admin@example.com",
            hashed_password=hash_password("Admin1234!"),
            role="admin",
        ))
        categoria = uow.categorias.add(Categoria(nombre="Bebidas"))
        uow.productos.add(Producto(
            categoria_id=categoria.id,
            nombre="Agua mineral",
            precio_base=1500,
            stock=10,
            disponible=True,
            activo=True,
        ))
        uow.productos.add(Producto(
            categoria_id=categoria.id,
            nombre="Jugo",
            precio_base=2000,
            stock=5,
            disponible=True,
            activo=True,
        ))

    with TestClient(app) as test_client:
        yield test_client

    engine.dispose()


def login(client, username="cliente", password="Cliente123!"):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200


def crear(client, items=None):
    return client.post("/api/v1/pedidos", json={
        "items": items or [{"producto_id": 1, "cantidad": 2}],
        "forma_pago": "EFECTIVO",
        "direccion_entrega": "Calle Falsa 123",
    })


def stock(client, producto_id=1):
    return client.get(
        f"/api/v1/productos/{producto_id}"
    ).json()["stock"]


def test_compra_descuenta_stock_y_conserva_precio(client):
    login(client)
    response = crear(client)

    assert response.status_code == 201
    pedido = response.json()
    assert pedido["estado"] == "PENDIENTE"
    assert pedido["total"] == 3000
    assert pedido["items"][0]["nombre_producto"] == "Agua mineral"
    assert pedido["items"][0]["precio_unitario"] == 1500
    assert stock(client) == 8


def test_stock_insuficiente_no_modifica_inventario(client):
    login(client)
    response = crear(client, [
        {"producto_id": 1, "cantidad": 11}
    ])
    assert response.status_code == 409
    assert stock(client) == 10
    assert client.get("/api/v1/pedidos").json()["total"] == 0


def test_productos_duplicados_rechazados(client):
    login(client)
    response = crear(client, [
        {"producto_id": 1, "cantidad": 1},
        {"producto_id": 1, "cantidad": 2},
    ])
    assert response.status_code == 422
    assert stock(client) == 10


def test_error_en_segundo_producto_revierte_compra(client):
    login(client)
    response = crear(client, [
        {"producto_id": 1, "cantidad": 2},
        {"producto_id": 2, "cantidad": 99},
    ])
    assert response.status_code == 409
    assert stock(client, 1) == 10
    assert stock(client, 2) == 5


def test_cancelacion_devuelve_stock(client):
    login(client)
    pedido_id = crear(client).json()["id"]
    assert stock(client) == 8

    response = client.patch(
        f"/api/v1/pedidos/{pedido_id}/cancelar"
    )
    assert response.status_code == 200
    assert response.json()["estado"] == "CANCELADO"
    assert stock(client) == 10

    segunda = client.patch(
        f"/api/v1/pedidos/{pedido_id}/cancelar"
    )
    assert segunda.status_code == 409
    assert stock(client) == 10


def test_admin_avanza_estado_y_no_revierte_entregado(client):
    login(client)
    pedido_id = crear(client).json()["id"]

    login(client, "admin", "Admin1234!")

    preparacion = client.patch(
        f"/api/v1/pedidos/{pedido_id}/estado",
        json={"estado": "EN_PREPARACION"},
    )
    assert preparacion.status_code == 200

    entregado = client.patch(
        f"/api/v1/pedidos/{pedido_id}/estado",
        json={"estado": "ENTREGADO"},
    )
    assert entregado.status_code == 200

    cancelacion = client.patch(
        f"/api/v1/pedidos/{pedido_id}/estado",
        json={"estado": "CANCELADO"},
    )
    assert cancelacion.status_code == 409
    assert stock(client) == 8


def test_cliente_no_puede_administrar(client):
    login(client)
    pedido_id = crear(client).json()["id"]

    response = client.patch(
        f"/api/v1/pedidos/{pedido_id}/estado",
        json={"estado": "ENTREGADO"},
    )
    assert response.status_code == 403
    assert client.get("/api/v1/pedidos/resumen").status_code == 403


def test_resumen_administrativo(client):
    login(client)
    crear(client)

    login(client, "admin", "Admin1234!")
    response = client.get("/api/v1/pedidos/resumen")

    assert response.status_code == 200
    resumen = response.json()
    assert resumen["total_pedidos"] == 1
    assert resumen["pendientes"] == 1
    assert resumen["pedidos_hoy"] == 1
    assert resumen["ingresos_entregados"] == 0


def test_listado_y_detalle_protegidos(client):
    login(client)
    pedido_id = crear(client).json()["id"]

    listado = client.get("/api/v1/pedidos?limit=1")
    assert listado.status_code == 200
    assert listado.json()["total"] == 1

    detalle = client.get(f"/api/v1/pedidos/{pedido_id}")
    assert detalle.status_code == 200

    client.post("/api/v1/auth/logout")
    assert client.get("/api/v1/pedidos").status_code == 401
