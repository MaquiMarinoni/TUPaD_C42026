from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.unidad_medida.model import UnidadMedida
from app.unidad_medida.schema import UnidadMedidaListResponse, UnidadMedidaRead

router = APIRouter(prefix="/unidades-medida", tags=["Unidades de Medida"])


@router.get("/", response_model=UnidadMedidaListResponse)
def listar_unidades_medida(session: Session = Depends(get_session)):
    unidades = session.exec(select(UnidadMedida).order_by(UnidadMedida.id)).all()
    return UnidadMedidaListResponse(total=len(unidades), items=unidades)


@router.get("/{unidad_id}", response_model=UnidadMedidaRead)
def obtener_unidad_medida(unidad_id: int, session: Session = Depends(get_session)):
    unidad = session.get(UnidadMedida, unidad_id)
    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La unidad de medida con ID {unidad_id} no existe",
        )
    return unidad