from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import LoginRequest, TokenResponse, RegistroRequest
from app.models.user import Cliente
from datatime import date 

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_cliente(datos: RegistroRequest, db: Session = Depends(get_db)):

    cliente_existente = db.query(Cliente).filter(Cliente.cedula == datos.cedula).first()
    if cliente_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente con esta cédula."
        )       #AUTENTICACION PARA USUARIOS QUE SE REGISTREN 
    
    if datos.cedula_referido:
        referido = db.query(Cliente).filter(Cliente.cedula == datos.cedula_referido).first()
        if not referido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El cliente referido no existe."
            )
        
    nuevo_cliente = Cliente(
        nombre=datos.nombre,
        cedula=datos.cedula,
        hashed_password=hash_password(datos.password),
        fecha_registro=date.today(),
        referido_por_cedula=datos.cedula_referido
        puntos=0
    )

    if datos.cedula_referido:
        referido.puntos += 10   #10 puntos por referido 

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente) 

    return {"mensaje": "Cliente regIstraDoooOOoO CON exitOOOO!", "cedula": nuevo_cliente.cedula}

@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    Cliente = db.query(Cliente).filter(Cliente.cedula == datos.cedula).first()
#autenticar cliente, devolviendo un JWT 
cliente = db.query(Cliente).filter(Cliente.cedula == datos.cedula).first()

if not cliente or not verify_password(datos.password, cliente.hashed_password):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Cedula o contraseña Incorrectos",
        headers={"WWW-Authenticate": "Bearer"}
    )
# TOKEN con la cedula como IDENTIFICADOR 

token = create_access_token(data={"sub":cliente.cedula})

return TokenResponse(access_token=token)

