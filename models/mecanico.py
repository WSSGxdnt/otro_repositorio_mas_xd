# models/mecanico.py
from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base
from sqlalchemy.orm import relationship

class Mecanico(Base):
    __tablename__ = "mecanicos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    documento = Column(String(15), unique=True, index=True, nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    especialidad = Column(String(50))
    activo = Column(Boolean, default=True)

    ordenes = relationship("Orden", back_populates="mecanico") # back_populates crea el puente bidireccional
