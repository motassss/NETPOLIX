from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
 
# config.py está en backend/app/core/config.py
# .parent -> backend/app/core/
# .parent -> backend/app/
# .parent -> backend/          ✅  aquí está el .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
 
class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    app_name: str = "SIC-NetPOLIx API"
    environment: str = "development"
 
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
 
@lru_cache()
def get_settings() -> Settings:
    return Settings()
 
settings = get_settings()