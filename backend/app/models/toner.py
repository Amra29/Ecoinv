from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class EstadoTonerEnum(str, enum.Enum):
    EN_ALMACEN = "EN_ALMACEN"
    EN_USO = "EN_USO"
    DEFECTUOSO = "DEFECTUOSO"
    AGOTADO = "AGOTADO"

class ModeloToner(Base):
    __tablename__ = "modelos_toner"

    id = Column(Integer, primary_key=True, index=True)
    codigo_modelo = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)

    toners = relationship("Toner", back_populates="modelo")

class Toner(Base):
    __tablename__ = "toners"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    modelo_id = Column(Integer, ForeignKey("modelos_toner.id"), nullable=False)
    uuid_qr = Column(String(36), unique=True, nullable=False, index=True)
    estado = Column(Enum(EstadoTonerEnum), default=EstadoTonerEnum.EN_ALMACEN, nullable=False)
    fecha_ingreso = Column(DateTime, nullable=True)
    fecha_apertura = Column(DateTime, nullable=True)

    empresa = relationship("Empresa", back_populates="toners")
    modelo = relationship("ModeloToner", back_populates="toners")
    incidencias = relationship("Incidencia", back_populates="toner")