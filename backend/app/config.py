import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Ecoinv API"
    VERSION: str = "1.0.0"
    
    # Base de datos MySQL / PostgreSQL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:amra2315SQL@localhost:3306/ecoinv_db")
    
    # Seguridad y JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "ecoinv_secret_key_super_segura_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 horas

settings = Settings()