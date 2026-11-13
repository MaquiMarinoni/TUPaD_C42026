import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine

import app.models
import app.uow.unit_of_work as uow_module
from app.core.security import hash_password
from app.main import app
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

    with TestClient(app) as test_client:
        yield test_client

    engine.dispose()


def iniciar_admin(client):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "Admin1234!"},
    )
    assert response.status_code == 200


def test_listado_publico_vacio(client):
    response = client.get("/api/v1/categorias")
    assert response.status_code == 200
    assert response.json() == []


def test_usuario_anonimo_no_puede_crear(client):
    response = client.post(
        "/api/v1/categorias",
        json={"nombre": "Bebidas"},
    )
    assert response.status_code == 401


def test_admin_crea_y_consulta_categoria(client):
    iniciar_admin(client)

    response = client.post(
        "/api/v1/categorias",
        json={"nombre": "Bebidas", "descripcion": "Sin alcohol"},
    )
    assert response.status_code == 201

    categoria_id = response.json()["id"]
    consulta = client.get(f"/api/v1/categorias/{categoria_id}")
    assert consulta.status_code == 200
    assert consulta.json()["nombre"] == "Bebidas"


def test_categoria_duplicada(client):
    iniciar_admin(client)

    datos = {"nombre": "Lacteos"}
    assert client.post("/api/v1/categorias", json=datos).status_code == 201
    assert client.post("/api/v1/categorias", json=datos).status_code == 409


def test_actualizacion_y_borrado_logico(client):
    iniciar_admin(client)

    creada = client.post(
        "/api/v1/categorias",
        json={"nombre": "Panificados"},
    )
    categoria_id = creada.json()["id"]

    actualizada = client.put(
        f"/api/v1/categorias/{categoria_id}",
        json={"nombre": "Panaderia"},
    )
    assert actualizada.status_code == 200
    assert actualizada.json()["nombre"] == "Panaderia"

    eliminada = client.delete(f"/api/v1/categorias/{categoria_id}")
    assert eliminada.status_code == 204

    assert client.get(f"/api/v1/categorias/{categoria_id}").status_code == 404
    assert client.get("/api/v1/categorias").json() == []

    with UnitOfWork() as uow:
        categoria = uow.categorias.get_by_id(categoria_id)
        assert categoria is not None
        assert categoria.activo is False
