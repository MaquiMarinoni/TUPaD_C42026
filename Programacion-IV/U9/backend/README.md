# FoodStore API - Backend (Trabajo Práctico Unidad 8)

API REST desarrollada como Trabajo Práctico Integrador de la **Unidad 8** de Programación IV (TUPaD - UTN).
Implementa los CRUD de **Categorías**, **Productos**, **Ingredientes** y el módulo transaccional de **Pedidos y Detalles de Pedido** utilizando la arquitectura **Models - Schemas - Repository - Unit of Work - Service - Router**.

## Requisitos e Instalación

```bash
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Ejecución del Servidor

```bash
python -m fastapi dev app/main.py
```

* Documentación interactiva (Swagger UI): `http://localhost:8000/docs`
* Pruebas REST Client: `pedidos.http` y `test_api.http`
