from datetime import datetime, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_cliente
from app.models.carrito import CarritoItem
from app.models.cliente import Cliente
from app.models.renta import Renta
from app.models.video import Video

router = APIRouter(prefix="/rentas", tags=["Rentas"])

RENTA_DIAS = 30


def _renta_activa(db: Session, cedula: str, video_isan: str) -> Renta | None:
    ahora = datetime.utcnow()
    return (
        db.query(Renta)
        .filter(
            Renta.cliente_cedula == cedula,
            Renta.video_isan == video_isan,
            Renta.expira_en > ahora,
        )
        .first()
    )


def _video_resumen(video: Video) -> dict:
    return {
        "isan": video.isan,
        "titulo_original": video.titulo_original,
        "imagen_url": video.imagen_url or "",
        "anio_produccion": video.anio_produccion,
        "precio_renta": float(video.precio_renta or 3.99),
    }


@router.get("/")
def listar_rentas(
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    ahora = datetime.utcnow()
    rentas = (
        db.query(Renta)
        .filter(Renta.cliente_cedula == cliente.cedula, Renta.expira_en > ahora)
        .order_by(Renta.rentado_en.desc())
        .all()
    )
    result = []
    for r in rentas:
        video = db.query(Video).filter(Video.isan == r.video_isan).first()
        if video:
            result.append({
                "id": r.id,
                "video_isan": r.video_isan,
                "rentado_en": r.rentado_en.isoformat() if r.rentado_en else None,
                "expira_en": r.expira_en.isoformat() if r.expira_en else None,
                "precio_pagado": float(r.precio_pagado),
                "pelicula": _video_resumen(video),
            })
    return result


@router.get("/verificar/{video_isan}")
def verificar_renta(
    video_isan: str,
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    renta = _renta_activa(db, cliente.cedula, video_isan)
    if renta:
        return {
            "rentada": True,
            "expira_en": renta.expira_en.isoformat(),
            "precio_pagado": float(renta.precio_pagado),
        }
    return {"rentada": False, "expira_en": None}


@router.post("/pagar")
def procesar_pago(
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    items = (
        db.query(CarritoItem)
        .filter(CarritoItem.cliente_cedula == cliente.cedula)
        .all()
    )
    if not items:
        raise HTTPException(status_code=400, detail="El carrito está vacío")

    ahora = datetime.utcnow()
    expira = ahora + timedelta(days=RENTA_DIAS)
    desbloqueadas = []

    for item in items:
        video = db.query(Video).filter(Video.isan == item.video_isan).first()
        if not video:
            continue

        precio = Decimal(str(video.precio_renta or 3.99))
        renta_existente = _renta_activa(db, cliente.cedula, item.video_isan)

        if renta_existente:
            renta_existente.expira_en = expira
            renta_existente.precio_pagado = precio
            renta_existente.rentado_en = ahora
        else:
            renta = Renta(
                cliente_cedula=cliente.cedula,
                video_isan=item.video_isan,
                rentado_en=ahora,
                expira_en=expira,
                precio_pagado=precio,
            )
            db.add(renta)

        desbloqueadas.append({
            "video_isan": item.video_isan,
            "titulo": video.titulo_original,
            "imagen_url": video.imagen_url or "",
            "expira_en": expira.isoformat(),
        })
        db.delete(item)

    db.commit()
    return {
        "success": True,
        "peliculas_desbloqueadas": desbloqueadas,
    }
