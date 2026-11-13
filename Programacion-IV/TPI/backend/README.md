# Backend - Food Store

API REST con FastAPI, SQLModel/SQLAlchemy y PostgreSQL.

## Requisitos

Python 3.13 y PostgreSQL.

## Instalaci?n (PowerShell, desde `Backend`)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Crear la base de datos `foodstore_tpi` en PostgreSQL. Ajustar `DATABASE_URL` y `SECRET_KEY` en `.env` con valores propios. El archivo de ejemplo contiene las variables `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` y `FRONTEND_ORIGIN`. No subir `.env` a Git.

## Crear tablas y cargar datos iniciales

```powershell
.\.venv\Scripts\python.exe -m app.db.init_db
.\.venv\Scripts\python.exe -m app.db.seed
```

El seed incluye un usuario administrador, tres categor?as y ocho productos. En una base nueva, el usuario inicial es `admin` y la contrase?a de demostraci?n `Admin1234!`. Cambiarla para cualquier entorno no local. La repetici?n del seed a?n no se verific? en una base aislada.

## Iniciar API

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

- API: http://localhost:8000/api/v1
- Swagger: http://localhost:8000/docs
- Salud: http://localhost:8000/health

## M?dulos

Autenticaci?n, usuarios, categor?as, productos, pedidos, stock y estados de pedidos. Las rutas se registran bajo `/api/v1`.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
```

Resultado de la revisi?n: 33 pruebas aprobadas, con una advertencia no bloqueante de compatibilidad de Starlette/httpx.

## Organizaci?n

El c?digo se distribuye en `app/api`, `app/core`, `app/db`, `app/models`, `app/repositories`, `app/schemas`, `app/services` y `app/uow`. El esquema se inicializa mediante `app.db.init_db` y la persistencia utiliza Unit of Work.
