import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DateTime, ForeignKey, Numeric, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Renta(Base):
    __tablename__ = "rentas"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cliente_cedula: Mapped[str] = mapped_column(String, ForeignKey("clientes.cedula"), nullable=False)
    video_isan: Mapped[str] = mapped_column(String, ForeignKey("videos.isan"), nullable=False)
    rentado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    expira_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    precio_pagado: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        UniqueConstraint("cliente_cedula", "video_isan", name="uq_renta_cliente_video"),
    )
