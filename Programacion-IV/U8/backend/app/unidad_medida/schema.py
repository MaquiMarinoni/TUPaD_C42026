from pydantic import BaseModel


class UnidadMedidaRead(BaseModel):
    id: int
    nombre: str
    simbolo: str
    tipo: str

    model_config = {"from_attributes": True}


class UnidadMedidaListResponse(BaseModel):
    total: int
    items: list[UnidadMedidaRead]