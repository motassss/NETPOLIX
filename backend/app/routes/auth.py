from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_cliente
from app.core.security import hash_password, verify_password
from app.schemas.auth import LoginRequest, TokenResponse, RegistroRequest
from app.services.auth_service import AuthService
from app.models.cliente import Cliente
from app.models.favorito import Favorito
from app.models.historial import Historial
from app.models.renta import Renta
from sqlalchemy import func
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Autenticación"])


class CambioNombreRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)


class CambioPasswordRequest(BaseModel):
    password_actual: str
    password_nuevo: str = Field(..., min_length=6)


@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_cliente(datos: RegistroRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.registrar(datos)


@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(datos)


@router.get("/me")
def perfil_actual(
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    total_favoritos = db.query(Favorito).filter(Favorito.cliente_cedula == cliente.cedula).count()
    total_vistas = db.query(Historial).filter(Historial.cliente_cedula == cliente.cedula).count()
    ultima_vista = (
        db.query(Historial)
        .filter(Historial.cliente_cedula == cliente.cedula)
        .order_by(Historial.fecha_hora.desc())
        .first()
    )
    ahora = datetime.utcnow()
    total_rentas = (
        db.query(Renta)
        .filter(Renta.cliente_cedula == cliente.cedula, Renta.expira_en > ahora)
        .count()
    )
    gasto_total = (
        db.query(func.coalesce(func.sum(Renta.precio_pagado), 0))
        .filter(Renta.cliente_cedula == cliente.cedula)
        .scalar()
    )

    return {
        "cedula": cliente.cedula,
        "nombre": cliente.nombre,
        "is_admin": cliente.is_admin,
        "fecha_ingreso": cliente.fecha_ingreso.isoformat(),
        "total_favoritos": total_favoritos,
        "total_vistas": total_vistas,
        "total_rentas": total_rentas,
        "gasto_total": float(gasto_total or 0),
        "ultima_vista": {
            "video_isan": ultima_vista.video_isan,
            "fecha_hora": ultima_vista.fecha_hora.isoformat(),
        } if ultima_vista else None,
    }


@router.patch("/me/nombre")
def cambiar_nombre(
    datos: CambioNombreRequest,
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    cliente.nombre = datos.nombre
    db.commit()
    return {"mensaje": "Nombre actualizado correctamente"}


@router.patch("/me/password")
def cambiar_password(
    datos: CambioPasswordRequest,
    db: Session = Depends(get_db),
    cliente: Cliente = Depends(get_current_cliente),
):
    if not verify_password(datos.password_actual, cliente.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual no es correcta",
        )
    cliente.hashed_password = hash_password(datos.password_nuevo)
    db.commit()
    return {"mensaje": "Contraseña actualizada correctamente"}
