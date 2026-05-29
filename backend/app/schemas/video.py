from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ClasificacionResponse(BaseModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}


class CategoriaResponse(BaseModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}


class VideoBase(BaseModel):
    isan: str
    titulo_original: str = Field(..., min_length=1, max_length=200)
    anio_produccion: int = Field(..., ge=1888, le=2100)
    duracion: int = Field(..., gt=0, description="Duración en minutos")


class VideoCreate(VideoBase):
    clasificacion_id: int
    categoria_ids: list[int] = Field(..., max_length=3)
    idioma_ids: list[int]

    @field_validator("categoria_ids")
    @classmethod
    def max_tres_categorias(cls, v):
        if len(v) > 3:
            raise ValueError("No se pueden asignar más de 3 categorías")
        return v


class VideoResponse(VideoBase):
    tipo: str = "pelicula"
    imagen_url: str = ""
    descripcion: str = ""
    trailer_url: str = ""
    precio_renta: float = 3.99
    clasificacion: Optional[ClasificacionResponse] = None
    categorias: list[CategoriaResponse] = []

    model_config = {"from_attributes": True}


class CalificarRequest(BaseModel):
    puntuacion: str = Field(..., description="excelente, bueno, regular o malo")

    @field_validator("puntuacion")
    @classmethod
    def validar_puntuacion(cls, v):
        if v not in ("excelente", "bueno", "regular", "malo"):
            raise ValueError("Puntuación debe ser: excelente, bueno, regular o malo")
        return v
