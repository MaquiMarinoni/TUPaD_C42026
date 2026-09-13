from fastapi import HTTPException
from typing import List, Optional
from .schemas import ProveedorCreate, ProveedorUpdate, ProveedorRead

# Base de datos en memoria simulada (lista de diccionarios)
proveedores_db = []
current_id = 1

def get_all(skip: int = 0, limit: int = 10, activo: Optional[bool] = None) -> List[dict]:
    resultados = proveedores_db
    if activo is not None:
        resultados = [p for p in resultados if p["activo"] == activo]
    return resultados[skip : skip + limit]

def get_by_id(proveedor_id: int) -> dict:
    for p in proveedores_db:
        if p["id"] == proveedor_id:
            return p
    # RN-04: No se puede consultar un id inexistente
    raise HTTPException(status_code=404, detail="Proveedor no encontrado") 

def create(proveedor_in: ProveedorCreate) -> dict:
    global current_id
    # RN-02: El código es único
    if any(p["codigo"] == proveedor_in.codigo for p in proveedores_db):
        raise HTTPException(status_code=409, detail="El código del proveedor ya existe")
    
    nuevo_proveedor = proveedor_in.model_dump()
    nuevo_proveedor["id"] = current_id
    
    proveedores_db.append(nuevo_proveedor)
    current_id += 1
    return nuevo_proveedor

def update(proveedor_id: int, proveedor_in: ProveedorUpdate) -> dict:
    proveedor_idx = next((index for (index, d) in enumerate(proveedores_db) if d["id"] == proveedor_id), None)
    
    if proveedor_idx is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado") # RN-04
        
    proveedor_actual = proveedores_db[proveedor_idx]
    datos_actualizar = proveedor_in.model_dump(exclude_unset=True)
    
    # RN-02: Validar que el nuevo código no colisione con otro proveedor existente
    if "codigo" in datos_actualizar and datos_actualizar["codigo"] != proveedor_actual["codigo"]:
        if any(p["codigo"] == datos_actualizar["codigo"] for p in proveedores_db):
            raise HTTPException(status_code=409, detail="El nuevo código ya está en uso")
            
    proveedor_actual.update(datos_actualizar)
    proveedores_db[proveedor_idx] = proveedor_actual
    return proveedor_actual

def deactivate(proveedor_id: int) -> dict:
    proveedor_idx = next((index for (index, d) in enumerate(proveedores_db) if d["id"] == proveedor_id), None)
    
    if proveedor_idx is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado") # RN-04
        
    if not proveedores_db[proveedor_idx]["activo"]:
        raise HTTPException(status_code=409, detail="El proveedor ya se encuentra desactivado") # RN-05
        
    proveedores_db[proveedor_idx]["activo"] = False
    return proveedores_db[proveedor_idx]