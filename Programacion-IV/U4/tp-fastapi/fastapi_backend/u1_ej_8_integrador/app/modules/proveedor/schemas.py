from pydantic import BaseModel, Field
from typing import Optional

# Modelo base con los campos compartidos y sus validaciones
class ProveedorBase(BaseModel):
    codigo: str = Field(..., min_length=1, description="Código único del proveedor")
    razon_social: str = Field(..., min_length=3, description="Razón social del proveedor")
    cuit: str = Field(..., min_length=11, max_length=15, description="CUIT del proveedor")
    email: Optional[str] = ""
    telefono: Optional[str] = ""
    activo: Optional[bool] = True

# Modelo para crear (hereda todo del base sin agregar nada)
class ProveedorCreate(ProveedorBase):
    pass

# Modelo para devolver en las respuestas (agrega el ID generado por el backend)
class ProveedorRead(ProveedorBase):
    id: int

# Modelo para actualizar (todos los campos son opcionales para permitir reemplazo total o parcial)
class ProveedorUpdate(BaseModel):
    codigo: Optional[str] = Field(None, min_length=1)
    razon_social: Optional[str] = Field(None, min_length=3)
    cuit: Optional[str] = Field(None, min_length=11, max_length=15)
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None