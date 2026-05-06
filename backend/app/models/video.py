# backend/app/models/video.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

# Tabla de asociación muchos-a-muchos: un video puede tener varios idiomas
# y un idioma puede estar en varios videos. SQLAlchemy necesita esta tabla
# intermedia pero no la manejamos como un modelo propio (no tiene lógica extra).
video_idioma = Table(
    "video_idioma",
    Base.metadata,
    Column("video_isan", String, ForeignKey("videos.isan")),
    Column("idioma_id", Integer, ForeignKey("idiomas.id"))
)

# Lo mismo para categorías (máximo 3 por video, validaremos esto en el service)
video_categoria = Table(
    "video_categoria",
    Base.metadata,
    Column("video_isan", String, ForeignKey("videos.isan")),
    Column("categoria_id", Integer, ForeignKey("categorias.id"))
)

class Video(Base):
    __tablename__ = "videos"
    
    isan = Column(String, primary_key=True, index=True)  # Identificador único internacional
    titulo_original = Column(String, nullable=False)
    anio_produccion = Column(Integer, nullable=False)
    duracion = Column(Integer, nullable=False)  # En minutos
    
    # Llave foránea — apunta a la tabla clasificaciones
    clasificacion_id = Column(Integer, ForeignKey("clasificaciones.id"), nullable=False)
    
    # Relaciones — SQLAlchemy cargará estos objetos automáticamente
    clasificacion = relationship("Clasificacion", back_populates="videos")
    categorias = relationship("Categoria", secondary=video_categoria, back_populates="videos")
    idiomas = relationship("Idioma", secondary=video_idioma, back_populates="videos")
    calificaciones = relationship("Calificacion", back_populates="video")
    
    # Discriminador de tipo: ¿es una película, un capítulo de serie, etc.?
    tipo = Column(String, nullable=False, default="pelicula")    