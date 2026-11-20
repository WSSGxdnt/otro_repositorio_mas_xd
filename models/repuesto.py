from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from core.database import Base

class Repuesto(Base):
    __tablename__ = "repuestos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo_sku = Column(String(20), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    precio_compra = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    stock_actual = Column(Integer, default=0, nullable=False)

    # Relación con la tabla intermedia orden_repuestos
    ordenes_asociadas = relationship("OrdenRepuesto", back_populates="repuesto")
