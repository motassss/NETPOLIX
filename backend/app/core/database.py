# backend/app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# El engine es la conexión real a la base de datos.
# check_same_thread=False es necesario SOLO para SQLite con FastAPI
# porque FastAPI puede usar múltiples hilos.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# SessionLocal es una fábrica de sesiones.
# Cada petición HTTP obtendrá su propia sesión, la usará, y la cerrará.
# autocommit=False significa que debemos confirmar los cambios manualmente.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase padre de todos nuestros modelos ORM.
# Cuando hagamos class Video(Base), SQLAlchemy sabrá que es una tabla.
Base = declarative_base()

def get_db():
  
  
    db = SessionLocal()
    try:
        yield db  # "yield" pausa aquí y entrega db al endpoint
    finally:
        db.close()  # Esto corre SIEMPRE al terminar el endpoint