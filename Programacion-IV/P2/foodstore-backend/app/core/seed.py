
from sqlmodel import Session, select

from app.core.database import engine
from app.modules.unidades_medida.model import UnidadMedida, TipoUnidad


def run_seed():
    with Session(engine) as session:
        unidades_existentes = session.exec(
            select(UnidadMedida)
        ).first()

        if unidades_existentes is not None:
            return

        unidades = [
            UnidadMedida(nombre="kilogramo", simbolo="kg", tipo=TipoUnidad.peso),
            UnidadMedida(nombre="gramo", simbolo="g", tipo=TipoUnidad.peso),
            UnidadMedida(nombre="litro", simbolo="L", tipo=TipoUnidad.volumen),
            UnidadMedida(nombre="mililitro", simbolo="mL", tipo=TipoUnidad.volumen),
            UnidadMedida(nombre="pieza", simbolo="u", tipo=TipoUnidad.contable),
            UnidadMedida(nombre="docena", simbolo="doc", tipo=TipoUnidad.contable),
        ]

        session.add_all(unidades)
        session.commit()
        print("Unidades de medida cargadas correctamente")
