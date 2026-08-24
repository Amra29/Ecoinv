from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ruc_nit = Column(String(20), unique=True, nullable=False, index=True)
    creado_en = Column(DateTime, server_default=func.now())

    usuarios = relationship("Usuario", back_populates="empresa")
    toners = relationship("Toner", back_populates="empresa")