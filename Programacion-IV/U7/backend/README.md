# Food Store — Backend API (FastAPI + SQLModel)

API REST desarrollada como Trabajo Práctico de la Unidad 6 

El servicio gestiona el catálogo de **Categorías**, **Productos** y la relación muchos a muchos (**Producto_Categoria**), con persistencia en base de datos relacional SQLite mediante SQLModel, validaciones estrictas con Pydantic y documentación OpenAPI/Swagger automática.

---

## Tecnologías utilizadas

- **Python 3.10+**
- **FastAPI**
- **Uvicorn**
- **SQLModel**
- **SQLite**
- **CORSMiddleware**

---

## Estructura del proyecto (Arquitectura en Capas)

El backend respeta estrictamente la separación de responsabilidades y la modularización por dominio requerida:

```text

backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Instancia de FastAPI, configuración de CORS, lifespan y seed data
│   ├── core/
│   │   ├── __init__.py
│   │   └── database.py      # Conexión al motor SQLite y generador de sesiones
│   ├── categoria/
│   │   ├── __init__.py
│   │   ├── model.py         # Entidad Categoria (SQLModel, table=True)
│   │   ├── schema.py        # Schemas Pydantic con validación min_length=1
│   │   ├── service.py       # Lógica de negocio y control de excepciones (404, 409)
│   │   └── router.py        # Endpoints HTTP delegados a la capa de servicio
│   └── producto/
│       ├── __init__.py
│       ├── model.py         # Entidad Producto y tabla intermedia ProductoCategoria (N:N)
│       ├── schema.py        # Schemas Pydantic de Producto y Link N:N
│       ├── service.py       # Lógica CRUD, serialización de imágenes y vínculos N:N
│       └── router.py        # Endpoints HTTP de Productos y vinculación
├── .env.example             # Ejemplo de configuración de variables de entorno
├── requirements.txt         # Dependencias del proyecto
└── test_api.http            # Suite de pruebas ejecutables con REST Client

```

## Estructura del proyecto (Arquitectura en Capas) 

* Validación de campos no vacíos: Atributo nombre protegido con Field(min_length=1).
* Control de unicidad (409 Conflict): No se permite la creación ni actualización de categorías o productos con nombres repetidos (control case-insensitive).
* Control de existencia (404 Not Found): Lanzado directamente en la capa de servicios (service.py) al buscar, actualizar o eliminar registros inexistentes.
* Relación N:N: Asociación y desasociación segura entre productos y categorías con endpoints dedicados.
* Carga inicial automática (Seed Data): Al iniciar por primera vez, el evento lifespan precarga las 6 categorías solicitadas en la consigna (Pizzas, Hamburguesas, Bebidas, Postres, Entradas, Pastas).

## Instrucciones de instalación y ejecución

Prerrequisitos
Python 3.10 o superior instalado en el sistema.

Pasos para iniciar:
1. Posicionarse en el directorio del backend
2. Crear y activar el entorno virtual:
   1. En Windows (PowerShell):
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
   2. En macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Instalar dependencias:
```bash
pip install -r requirements.txt
```
4. Ejecutar el servidor con Uvicorn:
```bash
python -m uvicorn app.main:app --reload --port 8000
```
5. Abrir en el navegador:
* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc