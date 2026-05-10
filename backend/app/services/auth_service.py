from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.cliente import Cliente
from app.schemas.auth import RegistroRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def registrar(self, datos: RegistroRequest) -> dict:
        existe = self.db.query(Cliente).filter(Cliente.cedula == datos.cedula).first()
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un cliente con esta cédula."
            )

        if datos.cedula_referido:
            referido = self.db.query(Cliente).filter(Cliente.cedula == datos.cedula_referido).first()
            if not referido:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El cliente referido no existe."
                )

        nuevo = Cliente(
            nombre=datos.nombre,
            cedula=datos.cedula,
            hashed_password=hash_password(datos.password),
            fecha_ingreso=date.today(),
            referido_por_cedula=datos.cedula_referido,
            puntos=0,
        )

        if datos.cedula_referido:
            referido.puntos += 10

        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)

        return {"mensaje": "Cliente registrado con éxito", "cedula": nuevo.cedula}

    def login(self, datos: LoginRequest) -> dict:
        cliente = self.db.query(Cliente).filter(Cliente.cedula == datos.cedula).first()

        if not cliente or not verify_password(datos.password, cliente.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cédula o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = create_access_token(data={"sub": cliente.cedula})
        return {"access_token": token, "token_type": "bearer"}
