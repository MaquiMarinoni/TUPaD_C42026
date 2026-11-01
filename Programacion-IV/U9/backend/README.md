# FoodStore API — Unidad 9

API FastAPI y SQLModel con SQLite, JWT en cookie HttpOnly y roles vigentes en UsuarioRol. Se conserva el catálogo de U8 y se protege también el módulo de pedidos.

La instalación paso a paso para VS Code y la configuración del primer administrador están en [la guía de U9](../README.md).

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
.\.venv\Scripts\python.exe -m pytest -q
```

## Rutas

Todas las rutas de negocio usan `/api/v1`; `/health` permanece público.

| Ruta | Acceso |
|---|---|
| POST `/auth/register` | Público; siempre asigna user |
| POST `/auth/token` | Público; formulario username=email y password |
| POST `/auth/logout` | Público; elimina cookie |
| GET `/auth/me` | Usuario activo |
| GET `/auth/admin/usuarios` | Admin, incluye inactivos sin hash |
| POST `/auth/admin/usuarios/{id}/activar` o `/desactivar` | Admin |
| GET categorías, productos, ingredientes y unidades | Usuario activo |
| POST/PUT/PATCH/DELETE categorías, productos e ingredientes | Admin |
| POST/DELETE asociaciones producto–categoría | Admin |
| GET roles, formas-pago, estados-pedido | Usuario activo; escritura: 405 |
| GET pedidos | Usuario activo |
| POST pedidos | User o admin; usuario_id de sesión |
| PUT/DELETE pedidos | Admin |

Una cuenta desactivada recibe 400; la ausencia/expiración de cookie recibe 401; un rol insuficiente o vencido recibe 403. El JWT nunca se devuelve en JSON y no se acepta por Authorization.

`test_api.http` y `pedidos.http` contienen ejemplos para la extensión REST Client de VS Code. Sus credenciales son marcadores y se completan solo localmente. La extensión conserva la cookie obtenida al iniciar sesión.
