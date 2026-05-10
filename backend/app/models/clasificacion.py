from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.video import Video


class Clasificacion(Base):
    __tablename__ = "clasificaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    videos: Mapped[list["Video"]] = relationship("Video", back_populates="clasificacion")
