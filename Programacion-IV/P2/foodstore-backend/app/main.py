
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
from app.core.seed import run_seed
from app.modules.categorias.router import router as categorias_router
from app.modules.productos.router import router as productos_router
from app.modules.unidades_medida.router import router as unidades_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    run_seed()
    yield


app = FastAPI(
    title="Food Store - Parcial 2",
    description="API REST para administrar el catalogo de productos",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(
    categorias_router,
    prefix="/api/v1"
)

app.include_router(
    productos_router,
    prefix="/api/v1"
)

app.include_router(
    unidades_router,
    prefix="/api/v1"
)
