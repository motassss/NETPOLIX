import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_cliente
from app.models.historial import Historial
from app.models.cliente import Cliente
from app.models.renta import Renta
from app.models.video import Video

router = APIRouter(prefix="/historial", tags=["Historial"])


def _tiene_renta_activa(db: Session, cedula: str, video_isan: str) -> bool:
    ahora = datetime.utcnow()
    return (
        db.query(Renta)
        .filter(
            Renta.cliente_cedula == cedula,
            Renta.video_isan == video_isan,
            Renta.expira_en > ahora,
        )
        .first()
        is not None
    )


@router.post("/{video_isan}", status_code=201)
def registrar_vista(
    video_isan: str,
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    if not _tiene_renta_activa(db, cliente.cedula, video_isan):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Debes rentar esta película antes de registrar una vista",
        )

    limite = datetime.utcnow() - timedelta(minutes=30)
    existente = (
        db.query(Historial)
        .filter(
            Historial.cliente_cedula == cliente.cedula,
            Historial.video_isan == video_isan,
            Historial.fecha_hora >= limite,
        )
        .first()
    )
    if existente:
        return {"mensaje": "Vista ya registrada recientemente"}

    registro = Historial(
        id=str(uuid.uuid4()),
        cliente_cedula=cliente.cedula,
        video_isan=video_isan,
    )
    db.add(registro)
    db.commit()
    return {"mensaje": "Vista registrada"}


@router.get("/")
def obtener_historial(
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    registros = (
        db.query(Historial)
        .filter(Historial.cliente_cedula == cliente.cedula)
        .order_by(Historial.fecha_hora.desc())
        .all()
    )
    result = []
    for r in registros:
        video = db.query(Video).filter(Video.isan == r.video_isan).first()
        entry = {
            "video_isan": r.video_isan,
            "fecha_hora": r.fecha_hora.isoformat(),
            "progreso": r.progreso,
        }
        if video:
            entry["pelicula"] = {
                "isan": video.isan,
                "titulo_original": video.titulo_original,
                "imagen_url": video.imagen_url or "",
                "anio_produccion": video.anio_produccion,
                "duracion": video.duracion,
            }
        result.append(entry)
    return result


@router.delete("/")
def limpiar_historial(
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    db.query(Historial).filter(Historial.cliente_cedula == cliente.cedula).delete()
    db.commit()
    return {"mensaje": "Historial eliminado"}
