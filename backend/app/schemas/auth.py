from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    cedula: str = Field(..., description="1234567890")
    contraseña: str = Field(..., description="password123")
#datos pa iniciar sesion :v 

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

#lo que devuelve el servidor 

class registroRequest(BaseModel):
    cedula: str = Field(..., description="1234567890")
    nombre: str = Field(..., description="John Doe")
    contraseña: str = Field(..., description="password123")
    cedula_referido: str | None = None 
#datos para registrarse



