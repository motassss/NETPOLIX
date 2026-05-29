from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_cliente
from app.services.video_service import VideoService
from app.schemas.video import VideoCreate, VideoResponse, CalificarRequest
from app.models.cliente import Cliente
from typing import List

router = APIRouter(prefix="/videos", tags=["Videos"])


@router.get("/", response_model=List[VideoResponse])
def listar_videos(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
    _: Cliente = Depends(get_current_cliente),
):
    service = VideoService(db)
    return service.listar_videos(skip=skip, limit=limit)


@router.post("/", response_model=VideoResponse, status_code=201)
def crear_video(
    datos: VideoCreate,
    db: Session = Depends(get_db),
    cliente_actual: Cliente = Depends(get_current_cliente),
):
    if not cliente_actual.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear videos",
        )

    service = VideoService(db)
    return service.create_video(datos)


@router.get("/categorias")
def listar_categorias(db: Session = Depends(get_db)):
    from app.models.categoria import Categoria
    return db.query(Categoria).all()

@router.get("/categoria/{categoria_nombre}")
def videos_por_categoria(
    categoria_nombre: str,
    db: Session = Depends(get_db),
    _: Cliente = Depends(get_current_cliente),
):
    service = VideoService(db)
    return service.listar_por_categoria(categoria_nombre)

@router.get("/buscar")
def buscar_videos(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    _: Cliente = Depends(get_current_cliente),
):
    service = VideoService(db)
    return service.buscar(q)

@router.get("/tendencias")
def tendencias(
    db: Session = Depends(get_db),
    _: Cliente = Depends(get_current_cliente),
):
    service = VideoService(db)
    return service.tendencias()

@router.get("/{isan}")
def obtener_video(
    isan: str,
    db: Session = Depends(get_db),
    _: Cliente = Depends(get_current_cliente),
):
    service = VideoService(db)
    return service.obtener_por_isan(isan)

@router.get("/{isan}/clasificacion")
def ver_calificacion(isan: str, db: Session = Depends(get_db)):
    service = VideoService(db)
    return service.calcular_calificacion_promedio(isan)


@router.post("/{isan}/calificar")
def calificar_video(
    isan: str,
    datos: CalificarRequest,
    db: Session = Depends(get_db),
    cliente_actual: Cliente = Depends(get_current_cliente),
):
    service = VideoService(db)
    return service.calificar_video(isan, cliente_actual.cedula, datos.puntuacion)
