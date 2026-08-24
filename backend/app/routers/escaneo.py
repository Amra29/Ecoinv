from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models.toner import Toner, EstadoTonerEnum
from app.models.incidencia import Incidencia
from app.models.usuario import Usuario, RolEnum
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/escaneo", tags=["Escaneo QR"])

class EscaneoRequest(BaseModel):
    uuid_qr: str
    accion: str # "ABRIR" o "REPORTAR_FALLA"
    tipo_falla: str | None = None
    descripcion_falla: str | None = None

@router.post("/procesar")
def procesar_escaneo(data: EscaneoRequest, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    toner = db.query(Toner).filter(Toner.uuid_qr == data.uuid_qr).first()
    if not toner:
        raise HTTPException(status_code=404, detail="Tóner no registrado en Ecoinv.")

    # Aislamiento Multi-tenant
    if current_user.rol != RolEnum.SUPERADMIN and toner.empresa_id != current_user.empresa_id:
        raise HTTPException(status_code=403, detail="Este tóner pertenece a otra empresa.")

    if data.accion == "ABRIR":
        if toner.estado != EstadoTonerEnum.EN_ALMACEN:
            raise HTTPException(status_code=400, detail=f"El tóner ya consta como {toner.estado.value}.")
        
        toner.estado = EstadoTonerEnum.EN_USO
        toner.fecha_apertura = datetime.now()
        db.commit()
        return {"status": "ok", "mensaje": "Tóner habilitado y marcado como EN USO."}

    elif data.accion == "REPORTAR_FALLA":
        toner.estado = EstadoTonerEnum.DEFECTUOSO
        incidencia = Incidencia(
            toner_id=toner.id,
            usuario_id=current_user.id,
            tipo_falla=data.tipo_falla or "Falla No Especificada",
            descripcion=data.descripcion_falla
        )
        db.add(incidencia)
        db.commit()
        return {"status": "ok", "mensaje": "Incidencia registrada. La distribuidora fue notificada."}

    raise HTTPException(status_code=400, detail="Acción no válida.")