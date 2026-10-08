# Trabajo Práctico Unidad 5

**Tecnicatura Universitaria en Programación a Distancia (TUPaD) - UTN**  
**Alumna:** Macarena Aylen Marinoni  
**Fecha:** 07/10/2026

---

## 1. Introducción
El presente trabajo práctico aborda la evolución de la API REST desarrollada en la Unidad 4 (originalmente con persistencia volátil en memoria) hacia una arquitectura con persistencia relacional en PostgreSQL mediante SQLModel, acompañada de una interfaz de usuario construida con React, TypeScript, Vite y Tailwind CSS.

---

## 2. Desarrollo y Decisiones de Arquitectura

### 2.1. Parte A: Migración del Backend a PostgreSQL (FastAPI + SQLModel)
Se respetó el siguiente flujo central de datos propuesto: Request -> Validación -> Service/Commit -> Response Model, organizando el backend en cuatro capas dentro de `backend/`:

1. Configuración de Base de Datos (`database.py`):
   - Implementación de una instancia única de `engine` conectada a PostgreSQL (`postgresql+psycopg`).
   - Creación automática de tablas en el ciclo de vida (`lifespan`) mediante `SQLModel.metadata.create_all(engine)`.
   - Inyección de sesiones por petición HTTP mediante `SessionDep = Annotated[Session, Depends(get_session)]`.

2. Capa de Modelos de Tabla (`models/producto.py`):
   - Definición de la entidad `Producto(SQLModel, table=True)` mapeada a la tabla física `producto` en PostgreSQL con clave primaria autoincremental (`id`) e índices en `nombre` y `categoria`.

3. Capa de Validación y Contratos (`schemas/producto.py`):
   - Conserva las reglas de validación de la Unidad 4 sin acoplarse a la base de datos:
     * `ProductoCreate`: valida `categoria` con expresión regular `^[A-Z]{3}-\d{2}$` (ej. `MUE-01`), `precio > 0`, `stock >= 0` y `stock_minimo >= 0`.
     * `ProductoRead`: contrato de salida que incluye el `id` persistido.
     * `ProductoStockResponse`: contrato específico para el reporte de estado de stock (`stock`, `bajo_stock_minimo`, `activo`).

4. Capa de Servicios y Transacciones (`services/producto_service.py`):
   - Reemplaza la lista en memoria `db_productos` por operaciones transaccionales (`session.add`, `session.commit`, `session.refresh`, `session.rollback`).
   - Preserva la lógica de negocio de la Unidad 4: paginación con `offset` y `limit`, reemplazo total (`PUT`), borrado lógico (`desactivar` cambiando `activo = False`) y cálculo de alerta de stock (`stock < stock_minimo`).

5. Capa de Enrutamiento (`routers/producto_router.py`):
   - Expone los 6 endpoints documentados en Swagger UI (`/docs`):
     * `POST /productos/` (Alta de producto - 201 Created)
     * `GET /productos/` (Listado paginado - 200 OK)
     * `GET /productos/{id}` (Detalle por ID - 200 OK / 404 Not Found)
     * `PUT /productos/{id}` (Actualización total - 200 OK / 404 Not Found)
     * `PUT /productos/{id}/desactivar` (Borrado lógico - 200 OK / 404 Not Found)
     * `GET /productos/{id}/stock` (Consulta de alerta de stock - 200 OK / 404 Not Found)

### 2.2. Parte B: Maquetado Frontend (React + TypeScript + Vite + Tailwind CSS)
Ubicado en la carpeta `tp-productos/`, aplica las buenas prácticas de la unidad:
- Regla de oro de estructura: toda la lógica y los componentes residen dentro de `src/`.
- Tipado estricto (`src/types/producto.ts`): define el tipo `Producto` reflejando exactamente los campos del esquema `ProductoRead` del backend, sin uso de `any`.
- Componentes reutilizables (`src/components/`):
  * `Navbar.tsx`: barra de navegación superior.
  * `ProductoForm.tsx`: formulario maquetado alineado con los campos de `ProductoCreate`.
  * `ProductoList.tsx` y `ProductoCard.tsx`: renderizado dinámico con `.map()`, `key={prod.id}` y badges semánticos de Tailwind CSS para indicar alerta de "Bajo stock" y estado "Activo / Inactivo".

---

## 3. Instrucciones de Ejecución y Pruebas

### 3.1. Backend y Base de Datos
1. Crear en PostgreSQL (puerto 5432) una base de datos llamada `productos_db`.
2. Ubicarse en la carpeta `backend/`, activar el entorno virtual e instalar dependencias:
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
3. Verificar las credenciales de PostgreSQL en `database.py` y ejecutar el servidor:
   uvicorn main:app --reload
4. Verificar la documentación interactiva y schemas en Swagger UI:
   http://localhost:8000/docs

### 3.2. Archivos de Prueba Incluidos (Incisos b y c)
Dentro de `backend/` se incluyen:
- `postman_collection.json`: colección JSON lista para importar en Postman con las pruebas de los 6 endpoints.
- `pruebas_endpoints.http`: archivo ejecutable mediante la extensión REST Client de VS Code.

### 3.3. Frontend
1. Ubicarse en la carpeta `tp-productos/`, instalar dependencias y levantar el servidor:
   cd tp-productos
   pnpm install
   pnpm dev
2. Acceder en el navegador a: http://localhost:5173
3. Para verificar compilación limpia de TypeScript:
   pnpm build

