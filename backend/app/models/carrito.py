import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class CarritoItem(Base):
    __tablename__ = "carrito"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cliente_cedula: Mapped[str] = mapped_column(String, ForeignKey("clientes.cedula"), nullable=False)
    video_isan: Mapped[str] = mapped_column(String, ForeignKey("videos.isan"), nullable=False)
    agregado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("cliente_cedula", "video_isan", name="uq_carrito_cliente_video"),
    )
