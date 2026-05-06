from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "clientes" 


    nombre = Column(String, nullable=False)
    cedula = Column(String, primary_key=True, index=True)
    fecha_ingreso = Column(Date, nullable=False)
    puntos = Column(Integer,default=0)


    referido_por_cedula = Column(String, ForeignKey("clientes.cedula"), nullable=True)
    referido_por = relationship("Cliente", remote_side=[cedula])

    hashed_password = Column(String, nullable=False)

    calificaciones = relationship("Calificacion", back_populates="cliente")

    