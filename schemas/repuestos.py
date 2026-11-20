# schemas/repuestos.py
from pydantic import BaseModel, Field, model_validator
from typing import Optional

class RepuestoCreate(BaseModel):
    codigo_sku: str = Field(..., min_length=3, max_length=20, description="Código único del repuesto. Ej: FIL-001")
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del repuesto")
    precio_compra: float = Field(..., gt=0, description="Costo de adquisición al proveedor")
    precio_venta: float = Field(..., gt=0, description="Precio de venta al público")
    stock_actual: int = Field(0, ge=0, description="Cantidad inicial en bodega")

    @model_validator(mode="after")
    def validar_margen_ganancia(self):
        if self.precio_venta < self.precio_compra:
            raise ValueError("El precio de venta no puede ser menor al precio de compra.")
        self.codigo_sku = self.codigo_sku.upper().strip()
        return self

class RepuestoPatch(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    precio_compra: Optional[float] = Field(None, gt=0)
    precio_venta: Optional[float] = Field(None, gt=0)
    stock_actual: Optional[int] = Field(None, ge=0)

class RepuestoResponse(BaseModel):
    id: int
    codigo_sku: str
    nombre: str
    precio_compra: float
    precio_venta: float
    stock_actual: int

    model_config = {"from_attributes": True}
    