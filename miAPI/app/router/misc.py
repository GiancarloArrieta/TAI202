from fastapi import HTTPException, Depends, APIRouter, status
from typing import Optional
from app.data.database import usuarios
import asyncio

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuarios import usuario as dbUsuario

# DECLARACIÓN DE ROUTER
misc = APIRouter(
    tags = ["Otros"]
)

# Endpoints
@misc.get("/")
async def holaMundo():
    return {"mensaje":"Hola Mundo FastAPI"}

@misc.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"Bienvenido a FastAPI",
        "estatus":200
    }

# Enpoint con parámetros obligatorios
@misc.get("/v1/parametroObligatorio/{id}", status_code = status.HTTP_200_OK)
async def consulta_uno(id: int, db:Session = Depends(get_db)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    return{
        "mensaje":"Usuaro encontrado",
        "usuario":usuario_db
    }

# Endpoint con parámetros opcionales
@misc.get("/v1/parametroOpcional", status_code = status.HTTP_200_OK)
async def consulta_todos(id:Optional[int] = None, db:Session = Depends(get_db)):
    if id is not None:
        usuario_db = db.query(dbUsuario).filter(dbUsuario.id == id).first()
        if not usuario_db:
            return {"mensaje":"Usuario no encontrado"}
    else:
        return {"mensaje":"No se proporcionó ID."}