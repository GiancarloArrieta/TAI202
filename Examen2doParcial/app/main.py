# IMPORTACIONES
import time
from datetime import datetime
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
AllowedStatus = Literal["Por confirmar", "Confirmada", ""]

# MODELOS
class Cliente(BaseModel):
    id: int = Field(..., gt=0, description="ID del cliente")
    nombre: str = Field(..., min_length=6, description="Nombre del cliente")

class Reservacion(BaseModel):
    id: int = Field(..., gt=0, description="ID de la reservación")
    id_cliente: int = Field(..., description="ID del cliente que hizo la reservación")
    dia: str = Field(..., description="Día de la reservación")
    hora: float = Field(..., ge=8.00, le=22.00, description="Horario de la reservacion")
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
@app.get("/v1/clientes", tags=["Acciones Clientes"])
async def consultar_clientes(id_cliente: Optional[int] = None):
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

@app.post("/v1/clientes", tags=["Acciones Clientes"], status_code=HTTP_200_OK)
async def agregar_cliente(cliente_nuevo:Cliente):
    for cliente in clientes:
        if cliente.id == cliente_nuevo.id:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="El ID ya existe")
    clientes.append(cliente_nuevo)
    return{
        "mensaje": f"Cliente agregado exitosamente",
        "datos_nuevos":cliente_nuevo,
        "status":200
    }

# Endpoints reservaciones

@app.get("/v1/reservaciones", tags=["Acciones Reservaciones"], status_code=HTTP_200_OK)
async def consultar_reservaciones(id_reservacion:Optional[int] = None, autenticacion: str = Depends(verificar_peticion)):
    if not reservaciones:
        return {
            "mensaje": "No hay reservaciones registradas.",
            "status": 200
        }
    if id_reservacion is not None:
        for reservacion in reservaciones:
            if reservacion.id == id_reservacion:
                return {"peticion": f"Realizada por {autenticacion}","mensaje":"Reservacion encontrada", "reservacion":reservacion}
        return {"mensaje":"Reservación no encontrada"}
    else:
        return {
            "mensaje": f"Consulta realizada por {autenticacion}",
            "total": len(reservaciones),
            "reservaciones": reservaciones,
            "status": 200
        }

@app.post("/v1/reservaciones", tags=["Acciones Reservaciones"], status_code=HTTP_200_OK)
async def registrar_reservacion(nueva_reservacion:Reservacion):
    if any(reservacion.id == nueva_reservacion.id for reservacion in reservaciones):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="El ID de la reservación ya existe")

    cliente = next((c for c in clientes if c.id == nueva_reservacion.id_cliente), None)
    reservacion = next((r for r in reservaciones if r.id == nueva_reservacion.id), None)

    if reservacion:
        if reservacion.dia == "Domingo":
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="No se puede reservar en domingos.")

    if not cliente:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

    nueva_reservacion.estatus = "Por confirmar"
    reservaciones.append(nueva_reservacion)

    return {"mensaje": f"Reservación registrada exitosamente.", "data": nueva_reservacion}

@app.patch("/v1/reservaciones/{id_reservacion}", tags=["Acciones Reservaciones"])
async def cancelar_reservacion(id_reservacion: int):
    reservacion_index = -1
    for i, p in enumerate(reservaciones):
        if p.id == id_reservacion:
            reservacion_index = i
            break

    if reservacion_index == -1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Reservación no encontrada")

    reservacion = next((r for r in reservaciones if r.id == id_reservacion), None)
    reservacion.estatus = "Confirmada"

    return {"mensaje": f"Reservación con ID {reservacion_index + 1} confirmada exitosamente."}

@app.delete("/v1/reservaciones/{id_reservacion}", tags=["Acciones Reservaciones"])
async def cancelar_reservacion(id_reservacion: int, autenticacion: str = Depends(verificar_peticion)):
    reservacion_index = -1
    for i, p in enumerate(reservaciones):
        if p.id == id_reservacion:
            reservacion_index = i
            break

    if reservacion_index == -1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Reservación no encontrada")

    reservaciones.pop(reservacion_index)

    return {"mensaje": f"Reservación con ID {reservacion_index + 1} cancelada exitosamente por {autenticacion}."}