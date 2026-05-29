import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Historial(Base):
    __tablename__ = "historial"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cliente_cedula: Mapped[str] = mapped_column(String, ForeignKey("clientes.cedula"), nullable=False)
    video_isan: Mapped[str] = mapped_column(String, ForeignKey("videos.isan"), nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    progreso: Mapped[int] = mapped_column(Integer, default=0)
