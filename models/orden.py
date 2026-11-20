from sqlalchemy import Column, Integer, String, Float, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship

class Orden(Base):
    __tablename__ = "ordenes"

    # Definir las columnas
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    placa = Column(String(6), index=True, nullable=False)
    modelo = Column(String(20))
    falla_reportada = Column(String(255))
    estado = Column(String(20), default="En diagnóstico")
    costo_reparacion = Column(Float, default=0.0)

    mecanico_id = Column(Integer, ForeignKey("mecanicos.id"), nullable=True)

    # Relaciones
    mecanico = relationship("Mecanico", back_populates="ordenes")
    repuestos_usados = relationship("OrdenRepuesto", back_populates="orden", cascade="all, delete-orphan")
    factura = relationship("Factura", back_populates="orden", uselist=False)
    