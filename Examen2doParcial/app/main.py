# IMPORTACIONES
from datetime import datetime, date, time
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, Literal, List
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND

# INSTANCIA DEL SERVIDOR
app = FastAPI(
    title="Examen Segundo Parcial: API Restaurante",
    description="Hecho por: Giancarlo Arrieta Zatarain",
    version="1.0"
)

# ESTATUS PERMITIDOS
AllowedStatus = Literal["Por confirmar", "Confirmada"]

# MODELOS
class Cliente(BaseModel):
    id: int = Field(..., gt=0, description="ID del cliente")
    nombre: str = Field(..., min_length=6, description="Nombre del cliente")

class Reservacion(BaseModel):
    id: int = Field(..., gt=0, description="ID de la reservación")
    id_cliente: int = Field(..., description="ID del cliente que hizo la reservación")
    fecha: datetime = Field(..., ge=time, description="Fecha de la reservacion")
    num_personas: int = Field(..., ge=1, le=10, description="Numero de personas")
    estatus: AllowedStatus = Field(..., description="Estatus de la reservación")

clientes: List[Cliente] = [
    Cliente(id=1, nombre="Giancarlo Arrieta")
]
reservaciones: List[Reservacion] = []

# IMPLEMENTACIÓN DE SEGURIDAD

security = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    usuario_correcto = secrets.compare_digest(credenciales.username,"admin")
    contrasena_correcta = secrets.compare_digest(credenciales.password,"rest123")

    if not(usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no válidas."
        )
    return credenciales.username

# Endpoints Clientes
@app.get("/v1/clientes", tags=["CRUD Clientes"])
async def consultar_clientes(id_cliente: Optional[id] = None):
    if not clientes:
        return {
            "mensaje": "No hay clientes registrados.",
            "status": 200
        }
    if id_cliente is not None:
        for cliente in clientes:
            if cliente.id == id_cliente:
                return {"mensaje":"Cliente encontrado", "cliente":cliente}
        return {"mensaje":"Cliente no encontrado", "status":400}
    else:
        return {
            "total": len(clientes),
            "libros": clientes,
            "status": 200
        }

# Endpoints reservaciones
@app.post("/v1/reservaciones", tags=["Acciones Préstamos"], status_code=HTTP_200_OK)
async def registrar_reservacion(nueva_reservacion:Reservacion, autenticacion: str = Depends(verificar_peticion)):
    if any(reservacion.id == nueva_reservacion.id for reservacion in reservaciones):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="El ID de la reservación ya existe")

    cliente = next((c for c in clientes if c.id == nueva_reservacion.id_usuario), None)

    if not cliente:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

    
    reservaciones.append(nueva_reservacion)

    return {"mensaje": f"Reservación registrada exitosamente por {autenticacion}", "data": nueva_reservacion}

@app.delete("/v1/reservaciones/{id_reservacion}", tags=["Acciones Préstamos"])
async def devolver_libro(id_reservacion: int, autenticacion: str = Depends(verificar_peticion)):
    reservacion_index = -1
    for i, p in enumerate(reservaciones):
        if p.id == id_reservacion:
            reservacion_index = i
            break

    if reservacion_index == -1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Reservación no encontrada")

    reservaciones.pop(reservacion_index)

    return {"mensaje": f"Reservación con ID {reservacion_index} cancelada exitosamente por f{autenticacion}."}