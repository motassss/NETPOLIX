from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.calificacion import Calificacion


class Cliente(Base):
    __tablename__ = "clientes"

    cedula: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    fecha_ingreso: Mapped[date] = mapped_column(Date, nullable=False)
    puntos: Mapped[int] = mapped_column(Integer, default=0)
    referido_por_cedula: Mapped[Optional[str]] = mapped_column(String, ForeignKey("clientes.cedula"), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    referido_por: Mapped[Optional["Cliente"]] = relationship("Cliente", remote_side=[cedula])
    calificaciones: Mapped[list["Calificacion"]] = relationship("Calificacion", back_populates="cliente")
