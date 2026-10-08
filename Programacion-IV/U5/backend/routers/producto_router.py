from typing import List
from fastapi import APIRouter, HTTPException, Path, Query, status
from database import SessionDep
from schemas.producto import ProductoCreate, ProductoRead, ProductoStockResponse
from services import producto_service

router = APIRouter(prefix="/productos", tags=["Productos"])


# ---------------------------------------------------------
# ALTA DE PRODUCTO
# Método: POST | Endpoint: /productos | Estado: 201 Created
# ---------------------------------------------------------
@router.post(
    "/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED
)
def alta_producto(producto: ProductoCreate, session: SessionDep):
    return producto_service.crear(session, producto)


# ---------------------------------------------------------
# LISTAR PRODUCTOS (Paginado)
# Método: GET | Endpoint: /productos | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/", response_model=List[ProductoRead], status_code=status.HTTP_200_OK
)
def listar_productos(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
):
    return producto_service.obtener_todos(session, skip, limit)


# ---------------------------------------------------------
# DETALLE DE PRODUCTO
# Método: GET | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}", response_model=ProductoRead, status_code=status.HTTP_200_OK
)
def detalle_producto(session: SessionDep, id: int = Path(..., gt=0)):
    producto = producto_service.obtener_por_id(session, id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return producto


# ---------------------------------------------------------
# ACTUALIZACIÓN (Reemplazo Total)
# Método: PUT | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}", response_model=ProductoRead, status_code=status.HTTP_200_OK
)
def actualizar_producto(
    producto: ProductoCreate, session: SessionDep, id: int = Path(..., gt=0)
):
    actualizado = producto_service.actualizar_total(session, id, producto)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return actualizado


# ---------------------------------------------------------
# BORRADO LÓGICO
# Método: PUT | Endpoint: /productos/{id}/desactivar | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}/desactivar",
    response_model=ProductoRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(session: SessionDep, id: int = Path(..., gt=0)):
    desactivado = producto_service.desactivar(session, id)
    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return desactivado


# ---------------------------------------------------------
# CONSULTAR STOCK (Lógica de Negocio)
# Método: GET | Endpoint: /productos/{id}/stock | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}/stock",
    response_model=ProductoStockResponse,
    status_code=status.HTTP_200_OK,
)
def consultar_stock(session: SessionDep, id: int = Path(..., gt=0)):
    resultado = producto_service.obtener_estado_stock(session, id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return resultado