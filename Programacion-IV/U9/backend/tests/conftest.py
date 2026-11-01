import os
os.environ["SECRET_KEY"] = "clave-de-pruebas-de-mas-de-32-caracteres"
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["ADMIN_EMAIL"] = ""
os.environ["ADMIN_PASSWORD"] = ""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine, select
from app.main import app
from app.core.database import get_session
from app.core.security import hash_password
from app.modules.usuarios.model import Usuario, UsuarioRol, Rol
from app.seed import run_seed


@pytest.fixture()
def env(monkeypatch):
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    monkeypatch.setattr("app.seed.engine", engine)
    monkeypatch.setattr("app.core.unit_of_work.engine", engine)
    run_seed()
    with Session(engine) as s:
        roles = {r.nombre: r.id for r in s.exec(select(Rol)).all()}
        for name in ["admin", "user"]:
            u = Usuario(nombre=name, apellido="Prueba", email=f"{name}@example.com", password_hash=hash_password("Prueba123!"))
            s.add(u); s.flush()
            s.add(UsuarioRol(usuario_id=u.id, rol_id=roles[name]))
        s.commit()
    def session_override():
        with Session(engine) as session:
            yield session
    app.dependency_overrides[get_session] = session_override
    client = TestClient(app)
    yield client, engine
    client.close()
    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


def login(client, name="user"):
    return client.post("/api/v1/auth/token", data={"username": f"{name}@example.com", "password": "Prueba123!"})
