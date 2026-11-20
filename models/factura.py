from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    orden_id = Column(Integer, ForeignKey("ordenes.id"), unique=True, nullable=False)

    fecha_emision = Column(DateTime, default=datetime.utcnow)

    subtotal_repuestos = Column(Float, nullable=False)
    costo_mano_obra = Column(Float, nullable=False)
    iva = Column(Float, nullable=False)
    total_pagar = Column(Float, nullable=False)

    orden = relationship("Orden", back_populates="factura")