from typing import Optional

from pydantic import BaseModel, Field

class MecanicoCreate(BaseModel):
    documento: str = Field(..., min_length=1, max_length=15)
    nombre_completo: str = Field(..., min_length=1, max_length=100)
    especialidad: Optional[str] = Field(default=None, max_length=50)


class MecanicoResponse(MecanicoCreate):
    id: int
    activo: bool

    model_config = {"from_attributes": True}


class RepuestoCreate(BaseModel):
    codigo_sku: str = Field(..., min_length=1, max_length=20)
    nombre: str = Field(..., min_length=1, max_length=100)
    precio_compra: float = Field(..., ge=0)
    precio_venta: float = Field(..., ge=0)
    stock_actual: int = Field(default=0, ge=0)


class RepuestoResponse(RepuestoCreate):
    id: int
    model_config = {"from_attributes": True}