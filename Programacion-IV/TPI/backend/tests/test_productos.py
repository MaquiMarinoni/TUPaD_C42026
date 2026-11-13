import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine

import app.models
import app.uow.unit_of_work as uow_module
from app.core.security import hash_password
from app.main import app
from app.models.categoria import Categoria
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
        uow.usuarios.add(
            Usuario(
                username="admin",
                full_name="Administrador",
                email="admin@example.com",
                hashed_password=hash_password("Admin1234!"),
                role="admin",
            )
        )
        uow.categorias.add(Categoria(nombre="Bebidas"))
        uow.categorias.add(Categoria(nombre="Alimentos"))

    with TestClient(app) as test_client:
        yield test_client

    engine.dispose()


def login_admin(client):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "Admin1234!"},
    )
    assert response.status_code == 200


def crear_producto(client, nombre="Agua", categoria_id=1, stock=10):
    return client.post(
        "/api/v1/productos",
        json={
            "categoria_id": categoria_id,
            "nombre": nombre,
            "descripcion": "Producto de prueba",
            "precio_base": 1500,
            "stock": stock,
            "disponible": True,
        },
    )


def test_catalogo_publico_vacio(client):
    response = client.get("/api/v1/productos")
    assert response.status_code == 200
    assert response.json() == {"total": 0, "items": []}


def test_anonimo_no_puede_crear(client):
    assert crear_producto(client).status_code == 401


def test_admin_crea_y_publico_consulta(client):
    login_admin(client)
    response = crear_producto(client)
    assert response.status_code == 201

    producto = response.json()
    assert producto["nombre"] == "Agua"
    assert producto["categoria"]["nombre"] == "Bebidas"

    consulta = client.get(f"/api/v1/productos/{producto['id']}")
    assert consulta.status_code == 200
    assert consulta.json()["stock"] == 10


def test_filtros_y_paginacion(client):
    login_admin(client)
    assert crear_producto(client, "Agua", 1).status_code == 201
    assert crear_producto(client, "Jugo", 1).status_code == 201
    assert crear_producto(client, "Pan", 2).status_code == 201

    response = client.get("/api/v1/productos?limit=2&skip=0")
    assert response.status_code == 200
    assert response.json()["total"] == 3
    assert len(response.json()["items"]) == 2

    filtrado = client.get("/api/v1/productos?categoria_id=1")
    assert filtrado.json()["total"] == 2

    busqueda = client.get("/api/v1/productos?buscar=pan")
    assert busqueda.json()["total"] == 1


def test_stock_y_disponibilidad(client):
    login_admin(client)
    producto_id = crear_producto(client).json()["id"]

    stock = client.patch(
        f"/api/v1/productos/{producto_id}/stock",
        json={"stock": 25},
    )
    assert stock.status_code == 200
    assert stock.json()["stock"] == 25

    disponibilidad = client.patch(
        f"/api/v1/productos/{producto_id}/disponible",
        json={"disponible": False},
    )
    assert disponibilidad.status_code == 200
    assert disponibilidad.json()["disponible"] is False

    filtrado = client.get("/api/v1/productos?disponible=true")
    assert filtrado.json()["total"] == 0


def test_borrado_logico(client):
    login_admin(client)
    producto_id = crear_producto(client).json()["id"]

    response = client.delete(f"/api/v1/productos/{producto_id}")
    assert response.status_code == 204

    assert client.get(f"/api/v1/productos/{producto_id}").status_code == 404
    assert client.get("/api/v1/productos").json()["total"] == 0

    with UnitOfWork() as uow:
        producto = uow.productos.get_by_id(producto_id)
        assert producto is not None
        assert producto.activo is False


def test_validaciones(client):
    login_admin(client)

    categoria_inexistente = crear_producto(
        client, "Producto", categoria_id=999
    )
    assert categoria_inexistente.status_code == 404

    stock_negativo = client.post(
        "/api/v1/productos",
        json={
            "categoria_id": 1,
            "nombre": "Producto",
            "precio_base": 100,
            "stock": -5,
        },
    )
    assert stock_negativo.status_code == 422
