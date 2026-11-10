# Food Store — Backend

**Programación IV — Segunda Evaluación Parcial**

**Estudiante:** Marinoni Macarena

## 1. Descripción

Este proyecto implementa una API REST para administrar el catálogo de productos de Food Store.

El backend fue desarrollado utilizando Python, FastAPI, Pydantic v2, SQLModel y PostgreSQL.

Permite administrar productos y categorías, registrar stock, establecer unidades de venta y clasificar productos en una o más categorías.

Las bajas son lógicas, por lo que los registros permanecen almacenados en la base de datos.

## 2. Requisitos previos

Para ejecutar el proyecto se necesita:

- Python 3.12 o superior.
- PostgreSQL 15 o superior.
- Visual Studio Code o una terminal compatible.
- Extensión REST Client de VS Code (opcional, para ejecutar las pruebas HTTP).

## 3. Configuración de PostgreSQL

Antes de iniciar la aplicación, crear una base de datos PostgreSQL.

Para este proyecto se utiliza el nombre:

`foodstore_p2`

La base puede crearse mediante pgAdmin o ejecutando:

```sql
CREATE DATABASE foodstore_p2;
```

No es necesario crear las tablas manualmente. La aplicación utiliza SQLModel para generarlas al iniciarse.

También se crean automáticamente los índices necesarios para garantizar la unicidad de nombres activos y la existencia de una única categoría principal por producto.

## 4. Configuración del entorno

Abrir una terminal ubicada en la carpeta `foodstore-backend`.

Crear el entorno virtual:

```powershell
python -m venv .venv
```

Activarlo en Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

## 5. Configuración de la conexión

En la raíz del backend, crear un archivo llamado `.env` tomando como referencia `.env.example`.

Configurar la variable:

```dotenv
DATABASE_URL=postgresql+psycopg://USUARIO:CONTRASENA@localhost:5432/foodstore_p2
```

Reemplazar `USUARIO` y `CONTRASENA` por las credenciales locales de PostgreSQL.

El archivo `.env` no se incluye en la entrega porque contiene información de acceso a la base de datos.

Si la contraseña contiene caracteres especiales, deben codificarse para utilizarse correctamente dentro de una URL.

## 6. Ejecución del backend

Con el entorno virtual activo, ejecutar:

```powershell
fastapi dev app/main.py
```

La API estará disponible en:

`http://127.0.0.1:8000`

La documentación interactiva Swagger se encuentra en:

`http://127.0.0.1:8000/docs`

Al iniciar la aplicación, se crean las tablas necesarias y se cargan las seis unidades de medida iniciales si todavía no existen.

## 7. Estructura del proyecto

```text
foodstore-backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── seed.py
│   └── modules/
│       ├── categorias/
│       │   ├── model.py
│       │   ├── schema.py
│       │   ├── service.py
│       │   └── router.py
│       ├── productos/
│       │   ├── model.py
│       │   ├── link_model.py
│       │   ├── schema.py
│       │   ├── service.py
│       │   └── router.py
│       └── unidades_medida/
│           ├── model.py
│           ├── schema.py
│           └── router.py
├── tests/
│   ├── productos.http
│   └── relaciones.http
├── .env.example
├── requirements.txt
└── README.md
```

## 8. Funcionalidades implementadas

**Productos**

- Alta, consulta, actualización y anulación lógica.
- Validación de nombres, precios y stock.
- Asociación con una unidad de venta.
- Cálculo automático de `hay_stock`.
- Control independiente de disponibilidad.
- Listado con paginación y filtros.

**Categorías**

- Alta, consulta, actualización y anulación lógica.
- Validación de nombres únicos entre categorías activas.
- Consulta de categorías activas y anuladas.

**Relaciones**

- Relación 1:N entre unidades de medida y productos.
- Relación N:N entre productos y categorías.
- Definición de una categoría principal por producto.
- Validaciones de duplicados y registros anulados.

## 9. Pruebas de la API

En la carpeta `tests` se incluyen:

- `productos.http`: operaciones CRUD, filtros, validaciones y stock.
- `relaciones.http`: categorías, clasificación de productos y relaciones.

Para ejecutar las pruebas:

1. Iniciar FastAPI.
2. Abrir uno de los archivos `.http` en Visual Studio Code.
3. Utilizar la extensión REST Client.
4. Ejecutar cada petición mediante **Send Request**, respetando el orden de las pruebas.

Los escenarios incluyen respuestas HTTP 200, 201, 204, 404, 409 y 422.

## 10. Consideraciones

La aplicación utiliza PostgreSQL como almacenamiento persistente.

La anulación de productos y categorías no elimina registros físicamente. Los campos `activo` y `anulado_at` permiten conservar su historial.

El campo `hay_stock` se calcula a partir de `stock_cantidad` y no se almacena en la tabla Producto.

El catálogo de unidades de medida contiene kilogramo, gramo, litro, mililitro, pieza y docena.

Las unidades de tipo contable requieren cantidades enteras de stock.