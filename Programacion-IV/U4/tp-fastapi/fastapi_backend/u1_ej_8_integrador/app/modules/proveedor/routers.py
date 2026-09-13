from fastapi import APIRouter, Query
from typing import List, Optional
from . import schemas, services

# Definimos el router con su prefijo y tag para que Swagger lo organice bien
router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

# HU-01: Crear proveedor
@router.post("/", response_model=schemas.ProveedorRead, status_code=201)
def create_proveedor(proveedor: schemas.ProveedorCreate):
    return services.create(proveedor)

# HU-02: Listar proveedores con paginación y filtros
@router.get("/", response_model=List[schemas.ProveedorRead])
def get_proveedores(
    skip: int = Query(0, ge=0, description="Cantidad de registros a saltar"),
    limit: int = Query(10, ge=1, le=50, description="Cantidad máxima a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado (True/False)")
):
    return services.get_all(skip=skip, limit=limit, activo=activo)

# HU-03: Consultar un proveedor por ID
@router.get("/{id}", response_model=schemas.ProveedorRead)
def get_proveedor(id: int):
    return services.get_by_id(id)

# HU-04: Actualizar un proveedor
@router.put("/{id}", response_model=schemas.ProveedorRead)
def update_proveedor(id: int, proveedor: schemas.ProveedorUpdate):
    return services.update(id, proveedor)

# HU-05: Desactivar un proveedor
@router.put("/{id}/desactivar", response_model=schemas.ProveedorRead)
def desactivar_proveedor(id: int):
    return services.deactivate(id)