# Trabajo Práctico — Unidad 9
## Programación IV · FoodStore

**Alumna:** Macarena Marinoni

Este trabajo continúa el proyecto de la Unidad 8 e incorpora registro de usuarios, inicio y cierre de sesión, permisos por rol y protección de rutas.

Se mantiene SQLite como base de datos y se conservan las funcionalidades de categorías, productos, ingredientes y pedidos. Las siguientes instrucciones permiten preparar el proyecto y comprobar su funcionamiento.

## 1. Requisitos

Para ejecutar el proyecto se necesita:

- Python 3.11, 3.12 o 3.13.
- Node.js 22.12 o una versión posterior compatible con Vite 8.
- pnpm.
- Visual Studio Code, o un editor con acceso a una terminal.

Los comandos de esta guía están preparados para Windows con PowerShell.

No es necesario instalar un servidor de base de datos. El archivo de SQLite se crea al iniciar el backend.

## 2. Abrir el proyecto

Si se recibe la entrega en archivos ZIP, descomprimir ambos proyectos. Las carpetas `backend` y `frontend` deben quedar accesibles desde el editor.

Abrir la carpeta que contiene ambos proyectos en Visual Studio Code y seleccionar **Terminal → Nueva terminal**.

El backend y el frontend se ejecutan en terminales separadas. Ambas deben permanecer abiertas mientras se utiliza la aplicación.

## 3. Configurar y ejecutar el backend

Desde la carpeta principal del proyecto, ingresar al backend:

```powershell
cd backend
```

Crear el entorno virtual e instalar las dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Estos comandos utilizan directamente el Python del entorno virtual, por lo que no hace falta activarlo.

### Configurar las variables de entorno

Crear el archivo `.env` a partir de la plantilla incluida:

```powershell
Copy-Item .env.example .env
```

Generar una clave para firmar los tokens:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
```

Abrir `.env` en el editor y completar los valores:

| Variable | Configuración |
|---|---|
| `DATABASE_URL` | Mantener `sqlite:///foodstore_u9.db`. |
| `SECRET_KEY` | Reemplazar el marcador por la clave generada. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Mantener `30`. |
| `COOKIE_SECURE` | Mantener `false` para la ejecución local por HTTP. |
| `ADMIN_EMAIL` | Ingresar el email que se utilizará para la cuenta administradora. |
| `ADMIN_PASSWORD` | Ingresar una contraseña propia de al menos 8 caracteres y hasta 72 bytes UTF-8. |

Guardar el archivo antes de continuar.

La cuenta administradora se crea con estos datos. Para iniciar sesión en el frontend se deben utilizar el mismo email y la misma contraseña.

El archivo `.env` no se incluye en la entrega porque contiene información privada.

### Cargar los datos iniciales

Ejecutar:

```powershell
.\.venv\Scripts\python.exe -m app.seed
```

Este paso crea las tablas y carga los datos iniciales del catálogo, los roles, los estados de pedido, la forma de pago y la cuenta administradora configurada.

El comando puede ejecutarse nuevamente sin duplicar los datos iniciales. Si una cuenta ya existe, no se modifica su contraseña ni su rol desde este proceso.

### Iniciar el servidor

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Dejar esta terminal ejecutándose.

Para comprobar el backend:

- Documentación de la API: http://localhost:8000/docs
- Estado del servicio: http://localhost:8000/health

La dirección `http://localhost:8000/` no tiene una página configurada. Para verificar el funcionamiento se deben utilizar las direcciones anteriores.

## 4. Configurar y ejecutar el frontend

Abrir una segunda terminal en Visual Studio Code, sin detener el backend.

Desde la carpeta principal del proyecto, ingresar al frontend:

```powershell
cd frontend
```

Instalar las dependencias:

```powershell
pnpm install --frozen-lockfile
```

Iniciar la aplicación:

```powershell
pnpm dev --port 5173 --strictPort
```

Abrir en el navegador:

http://localhost:5173

La aplicación utiliza por defecto la API disponible en `http://localhost:8000/api/v1`. Para esta configuración no es necesario crear un archivo `.env` en el frontend.

Utilizar `localhost` en ambos proyectos para evitar problemas con el envío de la cookie de sesión.

## 5. Ingresar y comprobar los permisos

La aplicación cuenta con dos roles:

| Rol | Funciones |
|---|---|
| `admin` | Consultar y modificar el catálogo, y activar o desactivar usuarios. |
| `user` | Consultar categorías, productos e ingredientes, sin permisos para modificar el catálogo. |

### Cuenta administradora

Ingresar desde el login con el email y la contraseña definidos en `backend/.env`.

Para comprobar sus funciones:

1. Crear una categoría de prueba.
2. Editar su descripción.
3. Eliminarla, siempre que no tenga productos activos asociados.
4. Consultar, crear y editar productos.
5. Verificar la selección de categorías de un producto.
6. Consultar el listado de ingredientes.
7. Ingresar a la sección **Usuarios**.
8. Recargar la página y comprobar que la sesión se mantiene.

En los formularios de productos, la primera categoría seleccionada se toma como principal.

### Cuenta de usuario común

Cerrar la sesión del administrador y seleccionar **Registrate**.

Completar el formulario con un email diferente e iniciar sesión con la nueva cuenta. El registro público asigna automáticamente el rol `user`.

Comprobar que:

- Se pueden consultar categorías, productos e ingredientes.
- No aparecen botones para crear, editar o eliminar.
- Al ingresar a `http://localhost:5173/admin/users`, se muestra la página de acceso denegado.
- La sesión se mantiene al recargar.
- Al cerrar sesión, la aplicación vuelve al login.

### Activación y desactivación de usuarios

Para verificar esta función:

1. Ingresar como administrador.
2. Abrir **Usuarios** y desactivar la cuenta de prueba.
3. Cerrar sesión.
4. Intentar ingresar con la cuenta desactivada.

La aplicación debe mostrar el mensaje **“Cuenta de usuario desactivada”**.

Luego se puede volver a ingresar como administrador y activar la cuenta.

## 6. Comprobar el módulo de pedidos

El módulo de pedidos se conserva en el backend. Sus operaciones pueden consultarse desde Swagger o mediante el archivo `backend/pedidos.http`.

Para utilizar el archivo `.http` se necesita la extensión **REST Client** de Visual Studio Code. Primero se debe iniciar sesión con la solicitud incluida en `backend/test_api.http`, completando las credenciales de prueba.

Las reglas principales son:

- Los usuarios con rol `user` o `admin` pueden crear pedidos.
- El usuario del pedido se obtiene de la sesión, no del cuerpo de la solicitud.
- Solo el administrador puede cambiar estados o realizar una baja.
- Los estados y las formas de pago son catálogos de solo lectura.
- El borrado de pedidos es lógico: se conservan sus detalles y su historial.

## 7. Ejecutar las pruebas

Para ejecutar las pruebas del backend, abrir una terminal adicional dentro de `backend`:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Las pruebas utilizan SQLite en memoria y no modifican los datos guardados en la base de la aplicación.

Para comprobar la compilación y revisar el código del frontend, ejecutar desde `frontend`:

```powershell
pnpm build
pnpm lint
```

## 8. Consideraciones sobre la entrega

- La base de U9 se guarda en `backend/foodstore_u9.db`.
- Se mantienen ingredientes y unidades de medida por tratarse de una continuación del proyecto anterior.
- No se incorporan stock ni un módulo nuevo de direcciones de entrega.
- Las contraseñas se almacenan con hash bcrypt.
- El JWT se envía mediante una cookie HttpOnly. El frontend no lo lee ni lo guarda.
- Las bajas de las entidades principales son lógicas, mediante `deleted_at`.
- Los archivos `.env`, las bases locales, `node_modules` y `.venv` no forman parte de la entrega.