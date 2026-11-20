from pydantic import BaseModel
from datetime import datetime
from typing import List


class RepuestoFacturaResponse(BaseModel):
    nombre_repuesto: str
    cantidad: int
    precio_unitario_historico: float
    subtotal_linea: float

    model_config = {"from_attributes": True}

class OrdenFacturaResponse(BaseModel):
    placa: str
    modelo: str
    mecanico: str

    model_config = {"from_attributes": True}

class FacturaDetalladaResponse(BaseModel):
    id: int
    fecha_emision: datetime

    subtotal_repuestos: float
    costo_mano_obra: float
    iva: float
    total_pagar: float

    orden: OrdenFacturaResponse
    repuestos: List[RepuestoFacturaResponse]