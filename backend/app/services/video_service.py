from sqlalchemy.orm import Session
from app.repositories.video_repository import VideoRepository
from app.models.video import Video
from app.schemas.video import VideoCreate
from fastapi import HTTPException,status


class VideoService:

    def __init__(self, db: Session):
        self.repo = VideoRepository(db)
        self.db = db

    def create_video(self, video_create: VideoCreate) -> Video:
        if self.repo.get_by_isan(datos.isan):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                 detail=f"ya existe un video con ISAN{datos.isan}"

            )
        nuevo_video = Video(
            isan=datos.isan,
            titulo_original=datos.titulo_original,
            año_produccion=datos.año_produccion,
            duracion=datos.duracion,
            clasificacion_id=datos.clasificacion_id
        )

        return self.repo.create(nuevo_video)
    
    def calcular_clasificacion_promedio(self, isan:str) -> dict:

        video = self.repo.get_by_isan(isan)
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Video con ISAN {isan} no encontrado"
            )

        pesos = {"excelente": 4, "bueno": 3, "regular": 2, "malo": 1}
        conteo = {"excelente": 0, "bueno": 0, "regular": 0, "malo": 0}

        for cal in video.calificaciones:
            conteo[cal.calificacion] += 1

        total_votos = sum(conteo.values())
        if total_votos == 0:
            return {"promedio": None, "conteo": conteo, "total_votos": 0}
        
        suma_ponderada = sum(pesos[k] * v for k, v in conteo.items())
        promedio = suma_ponderada / total_votos

        return {"promedio": round(promedio, 2),
                "conteo": conteo, 
                "total_votos": total_votos}
    
    