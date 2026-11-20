from pydantic import BaseModel, Field
from typing import Optional

class MecanicoCreate(BaseModel):
    documento: str = Field(..., min_length=5, max_length=15, description="Cédula o documento de identidad")
    nombre_completo: str = Field(..., min_length=3, max_length=100, description="Nombre y apellidos del mecánico")
    especialidad: Optional[str] = Field(None, max_length=50, description="Ej: Electricidad, Motor, Frenos")

class MecanicoResponse(MecanicoCreate):
    id: int
    activo: bool

    model_config = {"from_attributes": True}

