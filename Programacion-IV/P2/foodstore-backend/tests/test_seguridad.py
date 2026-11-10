from datetime import timedelta
from sqlmodel import Session, select
from app.modules.usuarios.model import Usuario, Rol, UsuarioRol, utc_now
from app.core.security import create_access_token, verify_password
from app.categoria.model import Categoria
from app.producto.model import Producto, ProductoCategoria
from app.pedidos.models import Pedido, DetallePedido, HistorialEstadoPedido
from app.seed import run_seed
from conftest import login
import pytest

BASE = "/api/v1"


def test_registro_y_validaciones(env):
    c, engine = env
    data = dict(nombre="Ana", apellido="Pérez", email="ana@example.com", password="Prueba123!")
    r = c.post(BASE + "/auth/register", json=data)
    assert r.status_code == 201, r.text
    assert r.json()["roles"] == ["user"]
    assert "password_hash" not in r.json()
    with Session(engine) as s:
        u = s.get(Usuario, r.json()["id"])
        assert u.password_hash.startswith("$2") and verify_password(data["password"], u.password_hash)
        enlace = s.exec(select(UsuarioRol).where(UsuarioRol.usuario_id == u.id)).one()
        assert enlace.asignado_por_id is None
    assert c.post(BASE + "/auth/register", json={**data, "email": "ANA@example.com"}).status_code == 409
    for invalid in [{"email": "mal"}, {"password": "corta"}, {"nombre": "   "}, {"roles": ["admin"]}, {"password": "ñ" * 40}]:
        assert c.post(BASE + "/auth/register", json={**data, **invalid}).status_code == 422


def test_cookie_perfil_logout_y_token_expirado(env):
    c, engine = env
    assert c.get(BASE + "/auth/me").status_code == 401
    r = login(c)
    assert r.status_code == 200, r.text
    cookie = r.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=lax" in cookie and "path=/" in cookie
    assert "access_token" not in r.json()
    assert c.get(BASE + "/auth/me").json()["roles"] == ["user"]
    token = c.cookies["access_token"]
    assert c.post(BASE + "/auth/logout").status_code == 200
    assert c.get(BASE + "/auth/me").status_code == 401
    assert c.get(BASE + "/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
    c.cookies.set("access_token", create_access_token(2, timedelta(seconds=-1)))
    assert c.get(BASE + "/auth/me").status_code == 401
    c.cookies.clear(); c.cookies.set("access_token", "invalido")
    assert c.get(BASE + "/auth/me").status_code == 401
    assert c.post(BASE + "/auth/token", data={"username": "user@example.com", "password": "incorrecta"}).status_code == 401


@pytest.mark.parametrize("path", ["/categorias/", "/productos/", "/ingredientes/", "/unidades-medida/", "/pedidos", "/roles", "/formas-pago", "/estados-pedido"])
def test_lecturas_requieren_sesion(env, path):
    c, _ = env
    assert c.get(BASE + path).status_code == 401
    login(c)
    assert c.get(BASE + path).status_code == 200


@pytest.mark.parametrize("path", ["/categorias/", "/productos/", "/ingredientes/"])
def test_escrituras_solo_admin(env, path):
    c, _ = env
    login(c)
    for method, target in [("POST", path), ("PUT", path + "1"), ("PATCH", path + "1"), ("DELETE", path + "1")]:
        assert c.request(method, BASE + target, json={}).status_code == 403
    assert c.post(BASE + "/productos/1/categorias", json={"categoria_id": 1}).status_code == 403
    assert c.delete(BASE + "/productos/1/categorias/1").status_code == 403


def test_roles_vencidos_y_multiples(env):
    c, engine = env
    login(c, "admin")
    with Session(engine) as s:
        rol = s.exec(select(UsuarioRol).where(UsuarioRol.usuario_id == 1)).one()
        rol.expires_at = utc_now() - timedelta(seconds=1)
        s.add(rol); s.commit()
    assert c.get(BASE + "/auth/admin/usuarios").status_code == 403
    assert c.get(BASE + "/auth/me").json()["roles"] == []
    with Session(engine) as s:
        rol = s.exec(select(UsuarioRol).where(UsuarioRol.usuario_id == 1)).one()
        rol.expires_at = utc_now() + timedelta(days=1)
        s.add(rol)
        user_role = s.exec(select(Rol).where(Rol.nombre == "user")).one()
        s.add(UsuarioRol(usuario_id=1, rol_id=user_role.id)); s.commit()
    assert c.get(BASE + "/auth/me").json()["roles"] == ["admin", "user"]
    assert c.get(BASE + "/auth/admin/usuarios").status_code == 200


def test_desactivar_bloquea_sesion_existente_y_login(env):
    c, _ = env
    login(c); user_cookie = c.cookies["access_token"]
    assert c.get(BASE + "/auth/admin/usuarios").status_code == 403
    login(c, "admin")
    r = c.post(BASE + "/auth/admin/usuarios/2/desactivar")
    assert r.status_code == 200 and r.json()["deleted_at"]
    users = c.get(BASE + "/auth/admin/usuarios").json()
    assert len(users) == 2 and "password_hash" not in users[0]
    c.cookies.clear(); c.cookies.set("access_token", user_cookie)
    assert c.get(BASE + "/categorias/").status_code == 400
    assert login(c).status_code == 400
    c.cookies.clear(); login(c, "admin")
    assert c.post(BASE + "/auth/admin/usuarios/2/activar").json()["deleted_at"] is None
    assert login(c).status_code == 200


def test_borrado_logico_y_relaciones(env):
    c, engine = env
    login(c, "admin")
    cat = c.post(BASE + "/categorias/", json={"nombre": "Prueba"}).json()
    r = c.post(BASE + "/productos/", json={"nombre": "Nuevo", "precio_base": 10, "categoria_ids": [cat["id"]]})
    assert r.status_code == 201, r.text
    prod = r.json()
    assert prod["categoria_ids"] == [cat["id"]]
    assert c.delete(BASE + f"/categorias/{cat['id']}").status_code == 409
    assert c.delete(BASE + f"/productos/{prod['id']}/categorias/{cat['id']}").status_code == 204
    with Session(engine) as s:
        assert s.get(Producto, prod["id"]) is not None
        assert s.get(ProductoCategoria, (prod["id"], cat["id"])) is None
    assert c.delete(BASE + f"/productos/{prod['id']}").status_code == 204
    assert c.delete(BASE + f"/categorias/{cat['id']}").status_code == 204
    for path, id_ in [("productos", prod["id"]), ("categorias", cat["id"])]:
        assert c.get(BASE + f"/{path}/{id_}").status_code == 404
        assert id_ not in [i["id"] for i in c.get(BASE + f"/{path}/?incluir_inactivos=true").json()["items"]]
    with Session(engine) as s:
        assert s.get(Producto, prod["id"]).deleted_at
        assert s.get(Categoria, cat["id"]).deleted_at


def test_pedidos_usuario_rollback_historial_y_baja(env):
    c, engine = env
    login(c)
    data = {"detalles": [{"producto_id": 1, "cantidad": 2}]}
    assert c.post(BASE + "/pedidos", json={**data, "usuario_id": 1}).status_code == 422
    r = c.post(BASE + "/pedidos", json=data)
    assert r.status_code == 201, r.text
    p = r.json()
    assert p["usuario_id"] == 2 and float(p["total"]) == 19000
    assert p["detalles"][0]["nombre_producto_snap"] == "Hamburguesa Doble Cheddar"
    bad = {"detalles": [{"producto_id": 1, "cantidad": 1}, {"producto_id": 9999, "cantidad": 1}]}
    assert c.post(BASE + "/pedidos", json=bad).status_code == 404
    assert len(c.get(BASE + "/pedidos").json()) == 1
    assert c.put(BASE + f"/pedidos/{p['id']}", json={"estado": "CONFIRMADO"}).status_code == 403
    assert c.delete(BASE + f"/pedidos/{p['id']}").status_code == 403
    login(c, "admin")
    for estado in ["CONFIRMADO", "EN_PREP", "EN_CAMINO", "ENTREGADO"]:
        assert c.put(BASE + f"/pedidos/{p['id']}", json={"estado": estado}).status_code == 200
    assert c.put(BASE + f"/pedidos/{p['id']}", json={"estado": "CANCELADO"}).status_code == 409
    assert c.delete(BASE + f"/pedidos/{p['id']}").status_code == 204
    assert c.get(BASE + "/pedidos").json() == []
    with Session(engine) as s:
        assert s.get(Pedido, p["id"]).deleted_at
        assert len(s.exec(select(DetallePedido)).all()) == 1
        assert len(s.exec(select(HistorialEstadoPedido)).all()) == 5


def test_catalogos_solo_lectura_seed_idempotente_y_cors(env):
    c, _ = env
    login(c, "admin")
    run_seed()
    assert len(c.get(BASE + "/roles").json()) == 2
    assert [x["codigo"] for x in c.get(BASE + "/estados-pedido").json()] == ["PENDIENTE", "CONFIRMADO", "EN_PREP", "EN_CAMINO", "ENTREGADO", "CANCELADO"]
    for path in ["roles", "formas-pago", "estados-pedido"]:
        for method in ["POST", "PUT", "PATCH", "DELETE"]:
            assert c.request(method, BASE + "/" + path, json={}).status_code == 405
    r = c.options(BASE + "/auth/token", headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"})
    assert r.headers["access-control-allow-credentials"] == "true"
    assert r.headers["access-control-allow-origin"] == "http://localhost:5173"
