# app/producto/router.py
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.producto.schema import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse,
    ProductoCategoriaLink
)
from app.producto.service import ProductoService
from app.categoria.schema import CategoriaResponse

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("", response_model=List[ProductoResponse], status_code=status.HTTP_200_OK)
def listar_productos(session: Session = Depends(get_session)):
    return ProductoService.get_all(session)

@router.get("/{producto_id}", response_model=ProductoResponse, status_code=status.HTTP_200_OK)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    return ProductoService.get_by_id(session, producto_id)

@router.post("", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto_in: ProductoCreate, session: Session = Depends(get_session)):
    return ProductoService.create(session, producto_in)

@router.put("/{producto_id}", response_model=ProductoResponse, status_code=status.HTTP_200_OK)
def actualizar_producto(
    producto_id: int,
    producto_in: ProductoUpdate,
    session: Session = Depends(get_session)
):
    return ProductoService.update(session, producto_id, producto_in)

@router.delete("/{producto_id}", status_code=status.HTTP_200_OK)
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    ProductoService.delete(session, producto_id)
    return {"message": f"Producto {producto_id} eliminado con éxito"}

@router.post("/categorias/vincular", status_code=status.HTTP_200_OK)
def asociar_producto_categoria(
    link: ProductoCategoriaLink,
    session: Session = Depends(get_session)
):
    ProductoService.asociar_categoria(session, link.producto_id, link.categoria_id)
    return {"message": f"Producto {link.producto_id} vinculado con éxito a la Categoría {link.categoria_id}"}

@router.delete("/categorias/desvincular", status_code=status.HTTP_200_OK)
def desasociar_producto_categoria(
    link: ProductoCategoriaLink,
    session: Session = Depends(get_session)
):
    ProductoService.desasociar_categoria(session, link.producto_id, link.categoria_id)
    return {"message": f"Producto {link.producto_id} desvinculado de la Categoría {link.categoria_id}"}

@router.get("/{producto_id}/categorias", response_model=List[CategoriaResponse], status_code=status.HTTP_200_OK)
def listar_categorias_de_producto(producto_id: int, session: Session = Depends(get_session)):
    return ProductoService.get_categorias_de_producto(session, producto_id)