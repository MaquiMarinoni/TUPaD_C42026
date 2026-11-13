from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import auth, usuarios, categorias, productos, pedidos
from app.core.config import settings


app = FastAPI(
    title="Food Store API",
    description="API del Trabajo Practico Integrador de Programacion IV",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(dict.fromkeys([settings.FRONTEND_ORIGIN, "http://localhost:5173", "http://127.0.0.1:5173"])),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
app.include_router(categorias.router, prefix="/api/v1")
app.include_router(productos.router, prefix="/api/v1")
app.include_router(pedidos.router, prefix="/api/v1")


@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok", "app": "Food Store API"}


@app.get("/api/v1", tags=["Sistema"])
def api_root():
    return {"message": "Food Store API v1"}




