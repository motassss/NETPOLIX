from fastapi import APIRouter, Depends, query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_cliente
from app.services.video_service import VideoService
from app.schemas.video import VideoCreate, VideoResponse
from app.models.cliente import Cliente
from typing import List

router = APIRouter(prefix="/videos", tags=["videos"])

@router.post("/", response_model=VideoResponse)
def listar_videos(
    skip: int = query(0, ge=0),
    limit: int = query(20, le=100),
    db: Session = Depends(get_db),
    _: Cliente = Depends(get_current_cliente)

):
    
    service = VideoService(db)
    return service.listar_videos(skip=skip, limit=limit)

@router.post("/", response_model=VideoResponse, status_code=201)
def crear_video(
    datos: VideoCreate,
    db: Session = Depends(get_db),
    cliente_actual: Cliente = Depends(get_current_cliente)
):
    #CREAR VIDEOM, SOLO PARA ADMINISTRADORES
    if not cliente_actual.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear videos"
        )
    
    service = VideoService(db)
    return service.create_video(datos)  

@router.get("/{isan}/clasificacion")

def ver_calificacion(isan: str, db: Session = Depends(get_db)):
    service = VideoService(db)
    return service.calcular_clasificacion_promedio(isan)

