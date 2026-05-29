from sqlalchemy import String, Column, ForeignKey, UniqueConstraint
from app.core.database import Base

class Favorito(Base):
    __tablename__ = "favoritos"

    cliente_cedula = Column(String, ForeignKey("clientes.cedula"), primary_key=True)
    video_isan = Column(String, ForeignKey("videos.isan"), primary_key=True)

    __table_args__ = (
        UniqueConstraint("cliente_cedula", "video_isan", name="uq_favorito"),
    )
