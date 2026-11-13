# Food Store - Trabajo Pr?ctico Integrador

**Materia:** Programaci?n IV  
**Carrera:** Tecnicatura Universitaria en Programaci?n a Distancia - UTN  
**Alumna:** Macarena Marinoni

## Descripci?n

Food Store es una aplicaci?n web para consultar un cat?logo, gestionar un carrito y realizar pedidos. Los usuarios autenticados pueden consultar su historial; el personal administrador puede gestionar productos, categor?as, usuarios y estados de pedidos.

## Tecnolog?as

- **Backend:** Python 3.13, FastAPI, SQLModel, SQLAlchemy, PostgreSQL, Pydantic y pytest.
- **Frontend:** React, TypeScript, Vite, Tailwind CSS 4, React Router, TanStack Query/Form/Table, Zustand, Axios y pnpm.

## Estructura

- `Backend/`: API REST, modelos, repositorios, servicios, pruebas y configuraci?n.
- `Frontend/`: aplicaci?n React.
- `Backend/README.md` y `Frontend/README.md`: instrucciones espec?ficas.

## Requisitos

Python 3.13, PostgreSQL, Node.js compatible con Vite 8 y pnpm.

## Puesta en marcha

1. Crear en PostgreSQL la base de datos `foodstore_tpi`.
2. Abrir una terminal en `Backend` y ejecutar:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

3. Editar `Backend/.env` con los datos locales de PostgreSQL y una clave secreta propia. Nunca publicar este archivo.
4. Inicializar tablas y datos de demostraci?n:

```powershell
.\.venv\Scripts\python.exe -m app.db.init_db
.\.venv\Scripts\python.exe -m app.db.seed
```

5. Iniciar el backend:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

6. En otra terminal, abrir `Frontend` y ejecutar:

```powershell
pnpm install --frozen-lockfile
pnpm dev
```

7. Abrir `http://localhost:5173`. API: `http://localhost:8000`; Swagger: `http://localhost:8000/docs`; salud: `http://localhost:8000/health`.

## Funcionalidades

- Cat?logo p?blico, b?squeda, filtros y paginaci?n.
- Carrito de compras con persistencia local.
- Registro, inicio y cierre de sesi?n.
- Checkout protegido y consulta de pedidos.
- Gesti?n administrativa de usuarios, categor?as, productos, stock, disponibilidad y pedidos.
- Panel de resumen, notificaciones y modo claro/oscuro.

## Datos de demostraci?n

El seed define un administrador, tres categor?as (Bebidas, Almacen y Panaderia) y ocho productos. Para una base local nueva, las credenciales iniciales son usuario `admin` y contrase?a `Admin1234!`. Cambiarlas antes de usar el sistema fuera del entorno de demostraci?n.

## Verificaciones

Backend:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
```

Frontend:

```powershell
pnpm build
```

En la revisi?n del trabajo se obtuvieron 33 pruebas de backend aprobadas y una compilaci?n frontend correcta. La idempotencia del seed en ejecuci?n todav?a requiere una prueba aislada.

## Repositorio

Repositorio de la cursada: https://github.com/MaquiMarinoni/TUPaD_C42026

Proyecto: `Programacion-IV/TPI`, rama de trabajo `tpi-food-store`. La publicaci?n y el enlace definitivo deben verificarse antes de entregar.
