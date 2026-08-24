import uuid as uuid_lib
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel, Field
from app.database import get_db
from app.models.toner import Toner, ModeloToner, EstadoTonerEnum
from app.models.empresa import Empresa
from app.models.usuario import Usuario, RolEnum
from app.utils.dependencies import get_current_user, require_superadmin

router = APIRouter(prefix="/api/toners", tags=["Inventario Tóners"])


def _serializar_toner(t: Toner) -> dict:
    return {
        "id": t.id,
        "uuid_qr": t.uuid_qr,
        "estado": t.estado.value if hasattr(t.estado, "value") else t.estado,
        "empresa_id": t.empresa_id,
        "empresa_nombre": t.empresa.nombre if t.empresa else None,
        "modelo_id": t.modelo_id,
        "modelo_codigo": t.modelo.codigo_modelo if t.modelo else None,
        "modelo_descripcion": t.modelo.descripcion if t.modelo else None,
        "fecha_ingreso": t.fecha_ingreso.isoformat() if t.fecha_ingreso else None,
        "fecha_apertura": t.fecha_apertura.isoformat() if t.fecha_apertura else None,
    }


@router.get("/")
def listar_inventario(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    query = db.query(Toner).options(joinedload(Toner.empresa), joinedload(Toner.modelo))

    # Si es cliente, solo ve el inventario asignado a su empresa
    if current_user.rol == RolEnum.CLIENTE:
        query = query.filter(Toner.empresa_id == current_user.empresa_id)

    # Si es SuperAdmin Ecoinv, ve todo el inventario global (todas las bodegas de clientes)
    toners = query.order_by(Toner.id.desc()).all()
    return [_serializar_toner(t) for t in toners]


@router.get("/modelos")
def listar_modelos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return db.query(ModeloToner).all()


class LoteQRRequest(BaseModel):
    empresa_id: int
    modelo_id: int
    cantidad: int = Field(gt=0, le=200)


@router.post("/generar-lote")
def generar_lote_qr(
    payload: LoteQRRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superadmin),
):
    """
    Crea 'cantidad' tóners nuevos en la base de datos (con su UUID único para el QR)
    para la empresa y modelo indicados. No genera ni guarda ningún archivo en el
    servidor: devuelve los UUIDs para que el frontend genere las imágenes QR y las
    envíe directamente a una pestaña de impresión.
    """
    empresa = db.query(Empresa).filter(Empresa.id == payload.empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    modelo = db.query(ModeloToner).filter(ModeloToner.id == payload.modelo_id).first()
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo de tóner no encontrado")

    nuevos_toners = []
    for _ in range(payload.cantidad):
        toner = Toner(
            empresa_id=empresa.id,
            modelo_id=modelo.id,
            uuid_qr=str(uuid_lib.uuid4()),
            estado=EstadoTonerEnum.EN_ALMACEN,
        )
        db.add(toner)
        nuevos_toners.append(toner)

    db.commit()

    return {
        "empresa": empresa.nombre,
        "modelo": modelo.codigo_modelo,
        "cantidad": len(nuevos_toners),
        "toners": [
            {"uuid_qr": t.uuid_qr, "modelo_codigo": modelo.codigo_modelo, "empresa": empresa.nombre}
            for t in nuevos_toners
        ],
    }