from pydantic import BaseModel, Field

# Creación de modelo de usuario
class crear_usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, example="Agripino")
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 y 123")