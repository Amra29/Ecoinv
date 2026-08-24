from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.utils.security import verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")

    access_token = create_access_token(data={"sub": user.email, "rol": user.rol.value, "empresa_id": user.empresa_id})
    return {"access_token": access_token, "token_type": "bearer", "rol": user.rol.value}