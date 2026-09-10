from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Si se definió DB_SSL_CA (caso de Aiven en producción), se conecta con SSL.
# Si no está definida (tu MySQL local), se conecta normal sin SSL.
connect_args = {}
if settings.DB_SSL_CA:
    connect_args = {"ssl": {"ca": settings.DB_SSL_CA}}

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para inyectar la sesión en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()