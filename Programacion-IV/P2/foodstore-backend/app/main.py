from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.core.health import router as health_router
from app.unidad_medida.router import router as unidad_medida_router
from app.categoria.router import router as categoria_router
from app.ingrediente.router import router as ingrediente_router
from app.producto.router import router as producto_router
from app.pedidos.router import router as pedidos_router
import app.pedidos.models  # noqa: F401 - Registra Pedido y DetallePedido en SQLModel.metadata
from app.seed import run_seed
from app.core.deps import catalog_access, get_current_active_user
from app.modules.usuarios.router import router as auth_router, roles_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    run_seed()
    yield


app = FastAPI(
    title="FoodStore API - Catálogo y Pedidos (Unidad 9)",
    description="API REST Full Stack con FastAPI, SQLModel, Repository y Unit of Work para Categorías, Productos, Ingredientes y Pedidos.",
    version="4.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(unidad_medida_router, prefix="/api/v1", dependencies=[Depends(get_current_active_user)])
app.include_router(categoria_router, prefix="/api/v1", dependencies=[Depends(catalog_access)])
app.include_router(ingrediente_router, prefix="/api/v1", dependencies=[Depends(catalog_access)])
app.include_router(producto_router, prefix="/api/v1", dependencies=[Depends(catalog_access)])
app.include_router(pedidos_router, prefix="/api/v1")
app.include_router(auth_router)
app.include_router(roles_router, prefix="/api/v1")
