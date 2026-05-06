# backend/app/core/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Pydantic leerá automáticamente estas variables desde el archivo .env.
    Si una variable no existe, lanzará un error claro en el arranque,
    lo que es mejor que fallar silenciosamente más tarde.
    """
    # Base de datos
    database_url: str
    
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App
    app_name: str = "SIC-NetPOLIx API"
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False  # DATABASE_URL y database_url son equivalentes

@lru_cache()  # Esto evita releer el archivo .env en cada petición
def get_settings() -> Settings:
    return Settings()

# Instancia global que importaremos desde otros módulos
settings = get_settings()