from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth_router, escaneo_router, empresas_router, toners_router, incidencias_router, usuarios_router

# Crear las tablas automáticamente en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API Backend para la plataforma de gestión de tóners multi-tenant Ecoinv"
)

# Configuración de CORS para permitir conexiones desde el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Reemplazar con dominio específico en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar Routers
app.include_router(auth_router)
app.include_router(escaneo_router)
app.include_router(empresas_router)
app.include_router(toners_router)
app.include_router(incidencias_router)
app.include_router(usuarios_router)

@app.get("/")
def root():
    return {"status": "online", "sistema": settings.PROJECT_NAME, "version": settings.VERSION}