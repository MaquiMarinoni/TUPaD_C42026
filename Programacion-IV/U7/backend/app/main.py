from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.categoria.router import router as categoria_router
from app.core.database import create_db_and_tables
from app.core.health import router as health_router
from app.ingrediente.router import router as ingrediente_router
from app.producto.router import router as producto_router
from app.seed import run_seed
from app.unidad_medida.router import router as unidad_medida_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    run_seed()
    yield


app = FastAPI(
    title="FoodStore API - Catálogo de Productos",
    description="API REST para gestión de Categorías, Productos, Ingredientes y Unidades de Medida",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(unidad_medida_router)
app.include_router(categoria_router)
app.include_router(ingrediente_router)
app.include_router(producto_router)