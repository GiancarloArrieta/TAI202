# Importaciones
from fastapi import FastAPI, Path, Query
from typing import Annotated, Optional
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

# Enpoint con parámetros obligatorios
@app.get("/productos/{producto_id}", tags=["Tienda"])
async def obtener_producto(
    producto_id: Annotated[int, Path(title="ID del producto", description="El ID debe ser mayor a 0", gt=0)]
):
    return {"item_id": producto_id, "nombre": "Laptop Pro", "precio": 1200}

# 2. Endpoint con Parámetros Opcionales
@app.get("/catalogo/", tags=["Tienda"])
async def listar_catalogo(
    categoria: Annotated[Optional[str], Query(max_length=50, description="Filtrar por categoría")] = None,
    limite: Annotated[int, Query(le=100, description="Máximo 100 resultados")] = 10
):
    return {
        "categoria_filtrada": categoria or "Todas",
        "resultados_mostrados": limite,
        "items": ["Teclado", "Mouse", "Monitor"]
    }