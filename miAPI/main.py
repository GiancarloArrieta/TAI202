# Importaciones
from fastapi import FastAPI
import asyncio

# Instancia del servidor
app = FastAPI()

# Endpoints
@app.get("/")
async def holaMundo():
    return {"mensaje":"Hola Mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"Hola Mundo FastAPI",
        "estatus": "200"
    }