from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class RolEnum(str, enum.Enum):
    SUPERADMIN = "SUPERADMIN"
    CLIENTE = "CLIENTE"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="SET NULL"), nullable=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), default=RolEnum.CLIENTE, nullable=False)

    empresa = relationship("Empresa", back_populates="usuarios")
    incidencias = relationship("Incidencia", back_populates="usuario")