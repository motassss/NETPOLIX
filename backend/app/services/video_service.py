from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.video_repository import VideoRepository
from app.models.video import Video
from app.models.calificacion import Calificacion
from app.models.categoria import Categoria
from app.models.idioma import Idioma
from app.schemas.video import VideoCreate


class VideoService:
    def __init__(self, db: Session):
        self.repo = VideoRepository(db)
        self.db = db

    def listar_videos(self, skip: int = 0, limit: int = 20) -> list[Video]:
        return self.repo.get_all(skip=skip, limit=limit)

    def listar_por_categoria(self, categoria_nombre: str) -> list[Video]:
        from app.models.categoria import Categoria
        cat = self.db.query(Categoria).filter(Categoria.nombre == categoria_nombre).first()
        if not cat:
            return []
        return [v for v in cat.videos]

    def buscar(self, query: str) -> list[Video]:
        return self.db.query(Video).filter(
            Video.titulo_original.ilike(f"%{query}%")
        ).all()

    def tendencias(self) -> list[Video]:
        from app.models.calificacion import Calificacion
        from sqlalchemy import func
        subq = (
            self.db.query(
                Calificacion.video_isan,
                func.count(Calificacion.id).label("votos")
            )
            .group_by(Calificacion.video_isan)
            .subquery()
        )
        results = (
            self.db.query(Video)
            .outerjoin(subq, Video.isan == subq.c.video_isan)
            .order_by(subq.c.votos.desc().nullslast())
            .limit(20)
            .all()
        )
        return results

    def obtener_por_isan(self, isan: str) -> Video:
        video = self.repo.get_by_isan(isan)
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Video con ISAN {isan} no encontrado",
            )
        return video

    def create_video(self, datos: VideoCreate) -> Video:
        if self.repo.get_by_isan(datos.isan):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un video con ISAN {datos.isan}",
            )

        categorias = self.db.query(Categoria).filter(Categoria.id.in_(datos.categoria_ids)).all()
        idiomas = self.db.query(Idioma).filter(Idioma.id.in_(datos.idioma_ids)).all()

        nuevo = Video(
            isan=datos.isan,
            titulo_original=datos.titulo_original,
            anio_produccion=datos.anio_produccion,
            duracion=datos.duracion,
            clasificacion_id=datos.clasificacion_id,
            categorias=categorias,
            idiomas=idiomas,
        )

        return self.repo.create(nuevo)

    def calcular_calificacion_promedio(self, isan: str) -> dict:
        video = self.repo.get_by_isan(isan)
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Video con ISAN {isan} no encontrado",
            )

        pesos = {"excelente": 4, "bueno": 3, "regular": 2, "malo": 1}
        conteo = {"excelente": 0, "bueno": 0, "regular": 0, "malo": 0}

        for cal in video.calificaciones:
            conteo[cal.puntuacion] += 1

        total_votos = sum(conteo.values())
        if total_votos == 0:
            return {"promedio": None, "conteo": conteo, "total_votos": 0}

        suma_ponderada = sum(pesos[k] * v for k, v in conteo.items())
        promedio = suma_ponderada / total_votos

        return {
            "promedio": round(promedio, 2),
            "conteo": conteo,
            "total_votos": total_votos,
        }

    def calificar_video(self, isan: str, cedula_cliente: str, puntuacion: str) -> dict:
        video = self.repo.get_by_isan(isan)
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Video con ISAN {isan} no encontrado",
            )

        calificacion = Calificacion(
            cliente_cedula=cedula_cliente,
            video_isan=isan,
            puntuacion=puntuacion,
        )
        self.db.add(calificacion)
        self.db.commit()

        return {"mensaje": "Calificación registrada con éxito"}
