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

    with TestClient(app) as test_client:
        yield test_client

    engine.dispose()


def registrar(client):
    return client.post(
        "/api/v1/auth/register",
        json={
            "username": "cliente1",
            "full_name": "Cliente de prueba",
            "email": "cliente1@example.com",
            "password": "ClaveSegura123!",
        },
    )


def login(client, username="cliente1", password="ClaveSegura123!"):
    return client.post(
        "/api/v1/auth/token",
        data={"username": username, "password": password},
    )


def test_registro_y_usuario_duplicado(client):
    response = registrar(client)
    assert response.status_code == 201
    assert response.json()["role"] == "user"
    assert "hashed_password" not in response.json()

    duplicado = registrar(client)
    assert duplicado.status_code == 409


def test_login_cookie_y_sesion(client):
    registrar(client)
    response = login(client)

    assert response.status_code == 200
    assert "access_token" in client.cookies
    assert "httponly" in response.headers["set-cookie"].lower()
    assert "access_token" not in response.json()

    me = client.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.json()["username"] == "cliente1"


def test_credenciales_incorrectas(client):
    registrar(client)
    assert login(client, password="incorrecta").status_code == 401


def test_sesion_sin_autenticacion(client):
    assert client.get("/api/v1/auth/me").status_code == 401


def test_logout(client):
    registrar(client)
    login(client)

    assert client.post("/api/v1/auth/logout").status_code == 200
    assert client.get("/api/v1/auth/me").status_code == 401


def test_usuario_no_puede_listar_usuarios(client):
    registrar(client)
    login(client)

    response = client.get("/api/v1/usuarios")
    assert response.status_code == 403


def test_admin_puede_gestionar_usuarios(client):
    registrar(client)

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

    assert login(client, "admin", "Admin1234!").status_code == 200

    listado = client.get("/api/v1/usuarios")
    assert listado.status_code == 200
    assert len(listado.json()) == 2

    desactivar = client.patch(
        "/api/v1/usuarios/1/estado",
        json={"disabled": True},
    )
    assert desactivar.status_code == 200
    assert desactivar.json()["disabled"] is True

    autodesactivar = client.patch(
        "/api/v1/usuarios/2/estado",
        json={"disabled": True},
    )
    assert autodesactivar.status_code == 400

    client.post("/api/v1/auth/logout")
    assert login(client).status_code == 400
