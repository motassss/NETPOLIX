from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class Clasificacion(Base):
    __tablename__ = "clasificaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_cedula = Column(String, ForeignKey("clientes.cedula"), nullable=False)
    video_isan = Column(String, ForeignKey("videos.isan"), nullable=False)

    puntuacion = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint(
            puntuacion.in_(["excelente", "bueno", "regular", "mala"]),
            name="validar_puntuacion"
        ),
        )
   
   
   
    video = relationship("Video", back_populates="calificaciones")
    cliente = relationship("Cliente", back_populates="calificaciones")


