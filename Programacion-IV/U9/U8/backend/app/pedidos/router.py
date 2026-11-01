from fastapi import APIRouter, HTTPException, status
from app.pedidos.schemas import PedidoCreate, PedidoRead, PedidoUpdate
from app.pedidos.service import (
    EstadoPedidoTerminalError,
    PedidoNoEncontrado,
    PedidoService,
    ProductoNoEncontrado,
)

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.get("", response_model=list[PedidoRead], status_code=status.HTTP_200_OK)
@router.get("/", response_model=list[PedidoRead], status_code=status.HTTP_200_OK, include_in_schema=False)
def listar_pedidos():
    service = PedidoService()
    return service.listar()


@router.get("/{pedido_id}", response_model=PedidoRead, status_code=status.HTTP_200_OK)
def obtener_pedido(pedido_id: int):
    service = PedidoService()
    try:
        return service.obtener(pedido_id)
    except PedidoNoEncontrado as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=PedidoRead, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def crear_pedido(data: PedidoCreate):
    service = PedidoService()
    try:
        return service.crear(data)
    except ProductoNoEncontrado as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{pedido_id}", response_model=PedidoRead, status_code=status.HTTP_200_OK)
def actualizar_estado_pedido(pedido_id: int, data: PedidoUpdate):
    service = PedidoService()
    try:
        return service.actualizar_estado(pedido_id, data)
    except PedidoNoEncontrado as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EstadoPedidoTerminalError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pedido(pedido_id: int):
    service = PedidoService()
    try:
        service.eliminar(pedido_id)
    except PedidoNoEncontrado as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
