from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel, EmailStr, Field
from app.database import get_db
from app.models.usuario import Usuario, RolEnum
from app.models.empresa import Empresa
from app.utils.security import hash_password
from app.utils.dependencies import require_superadmin

router = APIRouter(prefix="/api/usuarios", tags=["Gestión de Usuarios (Admin)"])


def _serializar_usuario(u: Usuario) -> dict:
    return {
        "id": u.id,
        "nombre": u.nombre,
        "email": u.email,
        "rol": u.rol.value if hasattr(u.rol, "value") else u.rol,
        "empresa_id": u.empresa_id,
        "empresa_nombre": u.empresa.nombre if u.empresa else None,
    }


@router.get("/")
def listar_usuarios(db: Session = Depends(get_db), current_user: Usuario = Depends(require_superadmin)):
    """Lista todos los usuarios (clientes y super admins) para gestión."""
    usuarios = db.query(Usuario).options(joinedload(Usuario.empresa)).order_by(Usuario.rol, Usuario.nombre).all()
    return [_serializar_usuario(u) for u in usuarios]


# ---------- Usuarios CLIENTE (credenciales para que un cliente vea su inventario) ----------

class CrearClienteRequest(BaseModel):
    empresa_id: int
    nombre: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


@router.post("/clientes")
def crear_usuario_cliente(
    payload: CrearClienteRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superadmin),
):
    if db.query(Usuario).filter(Usuario.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo")

    empresa = db.query(Empresa).filter(Empresa.id == payload.empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    nuevo = Usuario(
        empresa_id=empresa.id,
        nombre=payload.nombre.strip(),
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        rol=RolEnum.CLIENTE,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return _serializar_usuario(nuevo)


# ---------- Usuarios SUPERADMIN (para que varias personas administren Ecoinv) ----------

class CrearSuperAdminRequest(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


@router.post("/superadmins")
def crear_superadmin(
    payload: CrearSuperAdminRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superadmin),
):
    if db.query(Usuario).filter(Usuario.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo")

    nuevo = Usuario(
        empresa_id=None,
        nombre=payload.nombre.strip(),
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        rol=RolEnum.SUPERADMIN,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return _serializar_usuario(nuevo)


# ---------- Eliminar cualquier usuario (cliente o super admin) ----------

@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superadmin),
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propia cuenta mientras tienes la sesión activa")

    if usuario.rol == RolEnum.SUPERADMIN:
        total_admins = db.query(Usuario).filter(Usuario.rol == RolEnum.SUPERADMIN).count()
        if total_admins <= 1:
            raise HTTPException(status_code=400, detail="Debe existir al menos un SuperAdmin activo en el sistema")

    db.delete(usuario)
    db.commit()
    return {"detail": f"Usuario '{usuario.nombre}' eliminado correctamente"}