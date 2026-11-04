from pydantic import BaseModel, Field


class OrdenCreate(BaseModel):
    """Datos que envía el cliente al registrar una moto en el taller."""
    placa: str = Field(..., min_length=1, max_length=6, description="Placa de la moto (máximo 6 caracteres)")
    modelo: str = Field(..., min_length=1, description="Modelo de la moto")
    falla_reportada: str = Field(..., min_length=1, description="Falla reportada por el cliente")


class OrdenUpdate(BaseModel):
    """Datos que envía el cliente al actualizar diagnóstico y facturación."""
    nuevo_estado: str = Field(..., min_length=1, description="Nuevo estado de la orden")
    costo_reparacion: float = Field(..., description="Costo correspondiente a la reparación")