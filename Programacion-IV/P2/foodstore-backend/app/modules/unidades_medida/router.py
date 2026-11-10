
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.modules.unidades_medida.model import UnidadMedida
from app.modules.unidades_medida.schema import UnidadMedidaPublic


router = APIRouter(
    prefix="/unidades-medida",
    tags=["Unidades de Medida"]
)


@router.get(
    "",
    response_model=list[UnidadMedidaPublic]
)
def listar_unidades(
    session: Session = Depends(get_session)
):
    unidades = session.exec(
        select(UnidadMedida).order_by(UnidadMedida.id)
    ).all()

    return unidades
