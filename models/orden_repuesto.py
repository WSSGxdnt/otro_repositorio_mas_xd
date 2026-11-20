from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class OrdenRepuesto(Base):
    __tablename__ = "orden_repuestos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    orden_id = Column(Integer, ForeignKey("ordenes.id"), nullable=False)
    repuesto_id = Column(Integer, ForeignKey("repuestos.id"), nullable=False)

    # Atributos propios de la tabla intermedia
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario_historico = Column(Float, nullable=False)

    # Relaciones
    orden = relationship("Orden", back_populates="repuestos_usados")
    repuesto = relationship("Repuesto", back_populates="ordenes_asociadas")
