import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Ecoinv API"
    VERSION: str = "1.0.0"

    # Base de datos MySQL (local por defecto; en producción se sobreescribe con
    # la variable de entorno DATABASE_URL apuntando a Aiven u otro proveedor)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:amra2315SQL@localhost:3306/ecoinv_db"
    )

    # Ruta al certificado CA para conexiones SSL (requerido por Aiven).
    # Déjalo vacío/sin definir para tu MySQL local (no usa SSL).
    DB_SSL_CA: str = os.getenv("DB_SSL_CA", "")

    # Seguridad y JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "ecoinv_secret_key_super_segura_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas

settings = Settings()