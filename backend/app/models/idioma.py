from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.video import Video


class Idioma(Base):
    __tablename__ = "idiomas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    videos: Mapped[list["Video"]] = relationship("Video", secondary="video_idioma", back_populates="idiomas")
