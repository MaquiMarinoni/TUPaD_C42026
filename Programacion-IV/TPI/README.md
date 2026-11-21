# Food Store - Trabajo Practico Integrador

**Materia:** Programación IV
**Carrera:** Tecnicatura Universitaria en Programación a Distancia - UTN
**Alumna:** Macarena Marinoni

## Descripci?n

Food Store es una aplicación web para consultar un catálogo, gestionar un carrito y realizar pedidos. Los usuarios autenticados pueden consultar su historial; el personal administrador puede gestionar productos, categorías, usuarios y estados de pedidos.

## Tecnolog?as

- **Backend:** Python 3.13, FastAPI, SQLModel, SQLAlchemy, PostgreSQL, Pydantic y pytest.
- **Frontend:** React, TypeScript, Vite, Tailwind CSS 4, React Router, TanStack Query/Form/Table, Zustand, Axios y pnpm.

## Estructura

- `Backend/`: API REST, modelos, repositorios, servicios, pruebas y configuración.
- `Frontend/`: aplicación React.
- `Backend/README.md` y `Frontend/README.md`: instrucciones específicas.

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
4. Inicializar tablas y datos de demostración:

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

- Catálogo p?blico, busqueda, filtros y paginación.
- Carrito de compras con persistencia local.
- Registro, inicio y cierre de sesión.
- Checkout protegido y consulta de pedidos.
- Gestión administrativa de usuarios, categorías, productos, stock, disponibilidad y pedidos.
- Panel de resumen, notificaciones y modo claro/oscuro.

## Datos de demostración

El seed define un administrador, tres categorías (Bebidas, Almacen y Panaderia) y ocho productos. Para una base local nueva, las credenciales iniciales son usuario `admin` y contraseña `Admin1234!`. Cambiarlas antes de usar el sistema fuera del entorno de demostración.

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

En la revisi?n se obtuvieron 33 pruebas de backend aprobadas y una compilaci?n frontend correcta. Adem?s, el seed se ejecut? dos veces en una base SQLite aislada sin duplicar registros (1 administrador, 3 categor?as y 8 productos).

## Repositorio

Repositorio: https://github.com/MaquiMarinoni/TUPaD_C42026/tree/tpi-food-store/Programacion-IV/TPI

Proyecto publicado en la rama `tpi-food-store`: https://github.com/MaquiMarinoni/TUPaD_C42026/tree/tpi-food-store/Programacion-IV/TPI

## Video de demostración

El video presenta el funcionamiento del TPI Food Store, incluyendo el registro de usuarios, la compra como cliente, la administración de pedidos y la cancelación con restitución del stock.

Ver video de demostración: https://www.youtube.com/watch?v=8QbaWf5HZ78
