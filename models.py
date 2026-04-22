from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class EstacionDB(Base):
    __tablename__ = "estaciones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ubicacion = Column(String, nullable=False)
    lecturas = relationship("LecturaDB", back_populates="estacion", cascade="all, delete-orphan")

class LecturaDB(Base):
    __tablename__ = "lecturas"
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)
    estacion_id = Column(Integer, ForeignKey("estaciones.id"))
    estacion = relationship("EstacionDB", back_populates="lecturas")