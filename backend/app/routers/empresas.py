from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database import get_db
from app.models.empresa import Empresa
from app.models.usuario import Usuario, RolEnum
from app.utils.dependencies import require_superadmin

router = APIRouter(prefix="/api/empresas", tags=["Gestión Empresas (Admin)"])


def _serializar_empresa(e: Empresa) -> dict:
    return {
        "id": e.id,
        "nombre": e.nombre,
        "ruc_nit": e.ruc_nit,
        "creado_en": e.creado_en.isoformat() if e.creado_en else None,
    }


@router.get("/")
def listar_empresas(db: Session = Depends(get_db), current_user: Usuario = Depends(require_superadmin)):
    empresas = db.query(Empresa).order_by(Empresa.nombre).all()
    return [_serializar_empresa(e) for e in empresas]


class CrearEmpresaRequest(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    ruc_nit: str = Field(min_length=3, max_length=20)


@router.post("/")
def crear_empresa(
    payload: CrearEmpresaRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superadmin),
):
    if db.query(Empresa).filter(Empresa.ruc_nit == payload.ruc_nit).first():
        raise HTTPException(status_code=400, detail="Ya existe una empresa registrada con ese RUC/NIT")

    nueva = Empresa(nombre=payload.nombre.strip(), ruc_nit=payload.ruc_nit.strip())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return _serializar_empresa(nueva)


@router.delete("/{empresa_id}")
def eliminar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superadmin),
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    # Elimina también las credenciales de los usuarios CLIENTE de esa empresa,
    # ya que sin empresa asociada su acceso no tendría sentido.
    db.query(Usuario).filter(Usuario.empresa_id == empresa_id, Usuario.rol == RolEnum.CLIENTE).delete()

    # Los tóners de la empresa se eliminan en cascada por la relación en la BD (ON DELETE CASCADE)
    db.delete(empresa)
    db.commit()
    return {"detail": f"Empresa '{empresa.nombre}' y sus datos asociados fueron eliminados correctamente"}