from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.video import Video


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cliente_cedula: Mapped[str] = mapped_column(String, ForeignKey("clientes.cedula"), nullable=False)
    video_isan: Mapped[str] = mapped_column(String, ForeignKey("videos.isan"), nullable=False)
    puntuacion: Mapped[str] = mapped_column(String, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "puntuacion IN ('excelente', 'bueno', 'regular', 'malo')",
            name="validar_puntuacion"
        ),
    )

    video: Mapped["Video"] = relationship("Video", back_populates="calificaciones")
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="calificaciones")
