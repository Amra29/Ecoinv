from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.incidencia import Incidencia
from app.models.usuario import Usuario, RolEnum
from app.utils.dependencies import get_current_user
from app.models.toner import Toner

router = APIRouter(prefix="/api/incidencias", tags=["Reporte de Incidencias"])


def _serializar_incidencia(i: Incidencia) -> dict:
    return {
        "id": i.id,
        "toner_id": i.toner_id,
        "usuario_id": i.usuario_id,
        "tipo_falla": i.tipo_falla,
        "descripcion": i.descripcion,
        "fecha_reporte": i.fecha_reporte.isoformat() if i.fecha_reporte else None,
        "usuario_nombre": i.usuario.nombre if i.usuario else None,
    }


@router.get("/")
def listar_incidencias(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    query = db.query(Incidencia).options(joinedload(Incidencia.usuario))
    if current_user.rol == RolEnum.CLIENTE:
        query = query.join(Incidencia.toner).filter(Toner.empresa_id == current_user.empresa_id)
    incidencias = query.order_by(Incidencia.id.desc()).all()
    return [_serializar_incidencia(i) for i in incidencias]