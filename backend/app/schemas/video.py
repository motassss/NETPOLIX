from pydantic import BaseModel, Field, validator
from typing import Optional



class VideoBase(BaseModel):
    isan: str 
    titulo_original: str =Field(..., min_length=1, max_length=200)
    anio_produccion: int = Field(..., ge=1888, le=2100)
    duracion: int = Field(..., gt=0, description="Duración en minutos")

class VideoCreate(VideoBase):
    clasificacion_id: int 
    categoria_ids: List[int] = Field(..., max_items=3)
    idioma_ids: List[int]

    @validator('categoria_ids')
    def max_tres_categorias(cls, v):
        if len(v) > 3:
            raise ValueError('No se pueden asignar más de 3 categorías')
        return v
    
class VideoResponse(VideoBase):
    clasificacion: Optional[dict]
    categorias: List[dict] = []   #permitir que pydantic lea objetos SQL 

    model_config = {"from_attributes": True}
    
 
