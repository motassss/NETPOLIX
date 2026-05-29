from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_cliente
from app.models.favorito import Favorito
from app.models.cliente import Cliente

router = APIRouter(prefix="/favoritos", tags=["Favoritos"])

@router.get("/")
def mis_favoritos(db: Session = Depends(get_db), cliente: Cliente = Depends(get_current_cliente)):
    return db.query(Favorito).filter(Favorito.cliente_cedula == cliente.cedula).all()

@router.post("/{video_isan}", status_code=201)
def agregar_favorito(video_isan: str, db: Session = Depends(get_db), cliente: Cliente = Depends(get_current_cliente)):
    existente = db.query(Favorito).filter_by(cliente_cedula=cliente.cedula, video_isan=video_isan).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya está en tu lista")
    fav = Favorito(cliente_cedula=cliente.cedula, video_isan=video_isan)
    db.add(fav)
    db.commit()
    return {"mensaje": "Agregado a Mi Lista"}

@router.delete("/{video_isan}")
def quitar_favorito(video_isan: str, db: Session = Depends(get_db), cliente: Cliente = Depends(get_current_cliente)):
    fav = db.query(Favorito).filter_by(cliente_cedula=cliente.cedula, video_isan=video_isan).first()
    if not fav:
        raise HTTPException(status_code=404, detail="No está en tu lista")
    db.delete(fav)
    db.commit()
    return {"mensaje": "Quitado de Mi Lista"}
