from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    cedula: str = Field(..., description="Cédula del cliente")
    password: str = Field(..., min_length=6, description="Contraseña del cliente")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegistroRequest(BaseModel):
    cedula: str = Field(..., description="Cédula del cliente")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre completo")
    password: str = Field(..., min_length=6, description="Contraseña")
    cedula_referido: str | None = Field(None, description="Cédula del cliente que refiere")
