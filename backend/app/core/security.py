from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#deprecated actualiza automaticamente hashes antiguos a bcrypt, pero no elimina los antiguos.

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Convierte una contraseña de texto plano en un hash seguro usando bcrypt.

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
# Verifica que la contraseña de texto plano coincida con el hash almacenado.

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

# Crea un token JWT con los datos proporcionados y una fecha de expiración.
 
def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None

# Decodifica un token JWT y devuelve su contenido. Si el token es inválido o ha expirado, devuelve None.

