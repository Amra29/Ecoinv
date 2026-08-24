from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Incidencia(Base):
    __tablename__ = "incidencias"

    id = Column(Integer, primary_key=True, index=True)
    toner_id = Column(Integer, ForeignKey("toners.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo_falla = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_reporte = Column(DateTime, server_default=func.now())

    toner = relationship("Toner", back_populates="incidencias")
    usuario = relationship("Usuario", back_populates="incidencias")