from pydantic import BaseModel, Field, model_validator
from typing import Optional

# Lo que entra cuando llega la moto
class OrdenCreate(BaseModel):
    placa: str = Field(..., min_length=5, max_length=6, description="Placa de la moto (sin espacios)")
    modelo: str = Field(..., description="Marca y modelo. Ej: Bajaj Dominar 400")
    falla_reportada: str = Field(..., description="Descripción del problema por el cliente")
    mecanico_id: int

# Lo que entra cuando el mecánico actualiza la orden
class OrdenUpdate(BaseModel):
    nuevo_estado: str = Field(..., description="Ej: En diagnóstico, Reparada, Entregada")
    costo_reparacion: float = Field(..., ge=0, description="Debe ser 0 o mayor")

    @model_validator(mode='after')
    def validar_costo_reparacion(self):
        if self.nuevo_estado == "Reparada" and self.costo_reparacion == 0:
            raise ValueError("No se puede marcar como reparada sin asignar un costo de reparación mayor a cero.")

        self.nuevo_estado = self.nuevo_estado.capitalize()
        return self
    
class OrdenPatch(BaseModel):
    nuevo_estado: Optional[str] = Field(None, description="Ej: En diagnóstico, Reparada, Entregada")
    costo_reparacion: Optional[float] = Field(None, ge=0)
    mano_obra: Optional[float] = Field(None, ge=0, description="Costo de mano de obra")
    falla_reportada: Optional[str] = None

class MecanicoResumen(BaseModel):
    id: int
    nombre_completo: str
    especialidad: Optional[str] = None

    model_config = {"from_attributes": True}

class OrdenResponse(BaseModel):
    id: int
    placa: str
    modelo: str
    falla_reportada: Optional[str] = None
    estado: str
    costo_reparacion: float

    mecanico: Optional[MecanicoResumen] = None

    # Para que entienda ORM
    model_config = {"from_attributes": True}

class AgregarRepuestoOrden(BaseModel):
    repuesto_id: int
    cantidad: int = Field(..., gt=0, description="Debe agregar al menos 1 unidad")

class RepuestoEnOrdenResponse(BaseModel):
    id: int
    repuesto_id: int
    cantidad: int
    precio_unitario_historico: float

    model_config = {"from_attributes": True}