# Unidad 9 — FoodStore: autenticación y estado global

La aplicación amplía la Unidad 8 con autenticación por cookie HttpOnly, roles y estado global. Se conserva SQLite y el CRUD de ingredientes. La copia inicial completa de U8 quedó registrada en un commit independiente; los cambios posteriores se limitan a U9.

## Alcance y decisiones

Se aplica `TP_Unidad9_v2.pdf`: login en `/api/v1/auth/token`, identificación por email, roles muchos a muchos y bajas mediante `deleted_at`. El frontend nunca lee ni almacena el JWT.

- SQLite utiliza `backend/foodstore_u9.db`, independiente de U8. Se crea una base nueva para evitar migraciones innecesarias de datos de práctica.
- Ingredientes y unidades de medida se conservan. Ingredientes requiere sesión para leer y rol admin para escribir.
- Pedidos ya existía en U8: se incorpora el usuario de la sesión, los seis estados del UML, FormaPago, auditoría, valores monetarios de la compra e historial de estados. Los detalles no se modifican ni se borran y el historial solo recibe inserciones.
- No se agrega el módulo DireccionEntrega ni personalizaciones del pedido: no estaban implementados en U8 y la consigna condiciona su protección a su existencia. No se implementa stock.
- El catálogo inicial de pagos incluye EFECTIVO; el UML no impone un listado de formas de pago. Roles, formas de pago y estados son catálogos de solo lectura.
- Las rutas antiguas del frontend `/categorias` y `/productos` redirigen a `/categories` y `/products`.
- Los roles se consultan en la base en cada petición: un rol vencido no autoriza operaciones aunque la cookie todavía sea válida.

## 1. Sincronizar en VS Code (Windows)

Abrir el repositorio en VS Code y usar Terminal → Nueva terminal. En PowerShell:

```powershell
cd C:\Users\marin\GitHub\TUPaD_C42026
git status
git pull --ff-only origin main
cd Programacion-IV\U9
```

Si `git status` muestra cambios propios, no descartarlos ni usar `reset --hard`; revisarlos antes de actualizar.

## 2. Preparar el backend

Se requiere Python 3.11, 3.12 o 3.13. Desde U9:

```powershell
cd backend
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
code .env
```

Copiar la clave generada en `SECRET_KEY` y completar `ADMIN_EMAIL` y `ADMIN_PASSWORD` para crear el primer administrador. La contraseña requiere al menos 8 caracteres y no más de 72 bytes UTF-8. Usar una contraseña propia. No cambiar `DATABASE_URL` para esta práctica.

```dotenv
DATABASE_URL=sqlite:///foodstore_u9.db
SECRET_KEY=REEMPLAZAR_POR_LA_CLAVE_GENERADA
ACCESS_TOKEN_EXPIRE_MINUTES=30
COOKIE_SECURE=false
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=REEMPLAZAR_POR_UNA_CONTRASENA_PROPIA
```

El seed es idempotente: no duplica los catálogos ni cambia contraseñas existentes. El alta pública siempre asigna `user`; el primer admin se crea desde la configuración. No se promueven usuarios existentes mediante el seed.

```powershell
.\.venv\Scripts\python.exe -m app.seed
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

El uso de la ruta al ejecutable evita depender de la política de activación de PowerShell. Mantener esta terminal abierta. Swagger: http://localhost:8000/docs

## 3. Preparar el frontend

Abrir otra terminal integrada de VS Code. Se requiere Node 22.12 o posterior compatible con Vite 8, y pnpm.

```powershell
cd C:\Users\marin\GitHub\TUPaD_C42026\Programacion-IV\U9\frontend
node --version
pnpm --version
pnpm install --frozen-lockfile
pnpm dev --port 5173 --strictPort
```

Abrir http://localhost:5173 y usar el administrador configurado en `.env`. Usar `localhost` tanto en frontend como backend; no mezclarlo con `127.0.0.1`. La URL de API predeterminada es `http://localhost:8000/api/v1`. Si se necesita cambiarla, copiar `frontend/.env.example` como `.env` y reiniciar Vite.

Registrar otra cuenta desde la pantalla de registro permite probar el rol user.

## 4. Verificación

Backend, desde su carpeta:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Las pruebas usan SQLite en memoria y no modifican la base de práctica. Cubren registro y validaciones, bcrypt, cookie HttpOnly, rechazo de Authorization, JWT inválido/vencido, roles vencidos, bloqueo de usuarios, baja lógica, permisos de escritura, catálogos de lectura, pedidos y rollback de transacciones.

Frontend, desde su carpeta:

```powershell
pnpm build
pnpm lint
```

Comprobación en navegador:

1. Abrir `/products` sin sesión: redirige a `/login`.
2. Registrar una cuenta y entrar con ella: redirige a `/categories`.
3. Recargar: se verifica `/auth/me` y se conserva la sesión.
4. Como user, comprobar categorías, productos e ingredientes sin botones de escritura; `/admin/users` muestra acceso denegado.
5. Como admin, crear/editar/eliminar y activar/desactivar cuentas.
6. En productos, comprobar las categorías y su selección en el formulario (la primera es la principal).
7. Cerrar sesión y comprobar que no se puede volver a las páginas protegidas.
8. Borrar la cookie desde las herramientas del navegador y solicitar un listado: el 401 limpia la sesión y redirige al login.

## 5. Preparar entrega

Desde U9, después de confirmar los cambios en Git:

```powershell
python preparar_entrega.py
```

Se generan `entrega/U9_backend_Marinoni.zip` y `entrega/U9_frontend_Marinoni.zip`. El script incluye solo archivos versionados y excluye entornos, dependencias, builds, cachés, bases de datos y archivos `.env`; conserva `.env.example`. No elimina archivos de trabajo.

## Estructura incorporada

| Ubicación | Responsabilidad |
|---|---|
| `backend/app/core/config.py`, `security.py`, `deps.py` | Configuración, hash/JWT y autorización |
| `backend/app/modules/usuarios/` | Modelos, esquemas, repositorio, servicio y rutas |
| `backend/app/pedidos/` | Pedidos autenticados y registros históricos |
| `backend/tests/` | Pruebas de API aisladas |
| `frontend/src/api/` | Axios y caché de consultas |
| `frontend/src/store/authStore.ts` | Login, logout y verificación de sesión; persiste solo usuario |
| `frontend/src/components/ProtectedRoute.tsx` | Protección por sesión y roles |
| `frontend/src/pages/` | Pantallas originales y acceso/registro/administración |

## Correspondencia con la consigna

| Requisito | Implementación |
|---|---|
| HU-01 Registro | UserCreate, UsuarioService, RegisterPage |
| HU-02 Login | OAuth2 (username contiene email), cookie HttpOnly, LoginPage |
| HU-03 Logout | Borrado de cookie, limpieza de store y caché |
| HU-04 Recarga/perfil | checkSession, /auth/me, Navbar |
| HU-05 Roles | require_role sobre UsuarioRol vigente y controles de escritura |
| HU-06 Rutas | ProtectedRoute, /unauthorized, /admin/users |
| HU-07 Axios | withCredentials e interceptor 401 sin leer tokens |
| Bajas lógicas | Categoría, producto, ingrediente, pedido y activación de usuario |
| Pedidos existentes | Usuario desde sesión, estados/catálogos e historial |

El logout elimina la cookie del navegador. Como en la referencia, un JWT copiado fuera del navegador no se revoca y vence según `ACCESS_TOKEN_EXPIRE_MINUTES`.
