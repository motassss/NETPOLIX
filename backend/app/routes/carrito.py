from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_cliente
from app.models.carrito import CarritoItem
from app.models.cliente import Cliente
from app.models.video import Video
from app.models.renta import Renta
from datetime import datetime

router = APIRouter(prefix="/carrito", tags=["Carrito"])


class CarritoAddRequest(BaseModel):
    video_isan: str


def _video_to_dict(video: Video) -> dict:
    cats = [c.nombre for c in video.categorias] if video.categorias else []
    return {
        "isan": video.isan,
        "titulo_original": video.titulo_original,
        "anio_produccion": video.anio_produccion,
        "duracion": video.duracion,
        "tipo": video.tipo,
        "imagen_url": video.imagen_url or "",
        "descripcion": video.descripcion or "",
        "trailer_url": video.trailer_url or "",
        "precio_renta": float(video.precio_renta or 3.99),
        "categorias": cats,
        "genero": cats[0] if cats else "",
    }


@router.get("/")
def listar_carrito(
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    items = (
        db.query(CarritoItem)
        .filter(CarritoItem.cliente_cedula == cliente.cedula)
        .order_by(CarritoItem.agregado_en.desc())
        .all()
    )
    result = []
    for item in items:
        video = db.query(Video).filter(Video.isan == item.video_isan).first()
        if video:
            result.append({
                "id": item.id,
                "video_isan": item.video_isan,
                "agregado_en": item.agregado_en.isoformat() if item.agregado_en else None,
                "pelicula": _video_to_dict(video),
            })
    return {"items": result, "count": len(result)}


@router.post("/", status_code=status.HTTP_201_CREATED)
def agregar_al_carrito(
    datos: CarritoAddRequest,
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    video = db.query(Video).filter(Video.isan == datos.video_isan).first()
    if not video:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    ahora = datetime.utcnow()
    renta_activa = (
        db.query(Renta)
        .filter(
            Renta.cliente_cedula == cliente.cedula,
            Renta.video_isan == datos.video_isan,
            Renta.expira_en > ahora,
        )
        .first()
    )
    if renta_activa:
        raise HTTPException(status_code=400, detail="Ya tienes esta película rentada")

    existente = (
        db.query(CarritoItem)
        .filter(
            CarritoItem.cliente_cedula == cliente.cedula,
            CarritoItem.video_isan == datos.video_isan,
        )
        .first()
    )
    if existente:
        return {"mensaje": "Ya está en el carrito", "items": 1}

    item = CarritoItem(cliente_cedula=cliente.cedula, video_isan=datos.video_isan)
    db.add(item)
    db.commit()
    return {"mensaje": "Agregada al carrito"}


@router.delete("/{video_isan}")
def quitar_del_carrito(
    video_isan: str,
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    item = (
        db.query(CarritoItem)
        .filter(
            CarritoItem.cliente_cedula == cliente.cedula,
            CarritoItem.video_isan == video_isan,
        )
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="No está en el carrito")
    db.delete(item)
    db.commit()
    return {"mensaje": "Eliminada del carrito"}
