from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Integer, ForeignKey, Table, Column, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.clasificacion import Clasificacion
from app.models.categoria import Categoria
from app.models.idioma import Idioma

if TYPE_CHECKING:
    from app.models.calificacion import Calificacion


video_idioma = Table(
    "video_idioma",
    Base.metadata,
    Column("video_isan", ForeignKey("videos.isan")),
    Column("idioma_id", ForeignKey("idiomas.id")),
)

video_categoria = Table(
    "video_categoria",
    Base.metadata,
    Column("video_isan", ForeignKey("videos.isan")),
    Column("categoria_id", ForeignKey("categorias.id")),
)


class Video(Base):
    __tablename__ = "videos"

    isan: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    titulo_original: Mapped[str] = mapped_column(String, nullable=False)
    anio_produccion: Mapped[int] = mapped_column(Integer, nullable=False)
    duracion: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String, nullable=False, default="pelicula")
    clasificacion_id: Mapped[int] = mapped_column(Integer, ForeignKey("clasificaciones.id"), nullable=False)
    imagen_url: Mapped[str] = mapped_column(String, default="")
    descripcion: Mapped[str] = mapped_column(String, default="")
    trailer_url: Mapped[str] = mapped_column(String, default="")
    precio_renta: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("3.99"))

    clasificacion: Mapped[Clasificacion] = relationship("Clasificacion", back_populates="videos")
    categorias: Mapped[list[Categoria]] = relationship("Categoria", secondary=video_categoria, back_populates="videos")
    idiomas: Mapped[list[Idioma]] = relationship("Idioma", secondary=video_idioma, back_populates="videos")
    calificaciones: Mapped[list["Calificacion"]] = relationship("Calificacion", back_populates="video")
