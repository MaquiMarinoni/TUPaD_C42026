# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app.core.database import create_db_and_tables, engine
from app.categoria.model import Categoria
from app.categoria.router import router as categoria_router
from app.producto.router import router as producto_router

# Datos semilla de Food Store según el ejemplo *pendiente completar con el proyecto original de food store
CATEGORIAS_SEMILLA = [
    {"nombre": "Pizzas", "descripcion": "Pizzas artesanales con masa fresca"},
    {"nombre": "Hamburguesas", "descripcion": "Hamburguesas gourmet con ingredientes frescos"},
    {"nombre": "Bebidas", "descripcion": "Gaseosas, jugos naturales y agua"},
    {"nombre": "Postres", "descripcion": "Helados, tortas y dulces artesanales"},
    {"nombre": "Entradas", "descripcion": "Empanadas, medialunas y snacks para compartir"},
    {"nombre": "Pastas", "descripcion": "Pastas frescas con salsas caseras"}
]

def cargar_datos_semilla():
    """Inserta categorías iniciales si la base de datos está vacía."""
    with Session(engine) as session:
        hay_categorias = session.exec(select(Categoria)).first()
        if not hay_categorias:
            for cat_data in CATEGORIAS_SEMILLA:
                session.add(Categoria(**cat_data))
            session.commit()
            print("[Food Store] Categorías iniciales cargadas exitosamente.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización al arrancar el servidor
    create_db_and_tables()
    cargar_datos_semilla()
    yield
    # Limpieza al apagar (si fuera necesario)

app = FastAPI(
    title="Food Store API",
    description="Backend FastAPI para gestión de Categorías, Productos y relaciones N:N",
    version="1.0.0",
    lifespan=lifespan
)

# Configuración de CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers modulares
app.include_router(categoria_router)
app.include_router(producto_router)

@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "Bienvenido a la API de Food Store",
        "docs": "/docs",
        "endpoints": ["/categorias", "/productos"]
    }