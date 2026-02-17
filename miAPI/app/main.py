# Importaciones
from fastapi import FastAPI, status, HTTPException
from typing import Optional
import asyncio

# Instancia del servidor
app = FastAPI(
    title="Mi primera API",
    description="Giancarlo Arrieta Zatarain",
    version="1.0"
)

# TB Ficticia
usuarios = [
    {"id":1,"nombre":"Fernanda","edad":20},
    {"id":2,"nombre":"Sergio","edad":22},
    {"id":3,"nombre":"Jesús Manuel","edad":20},
]

# Endpoints
@app.get("/")
async def holaMundo():
    return {"mensaje":"Hola Mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"Bienvenido a FastAPI",
        "estatus":200
    }

# Enpoint con parámetros obligatorios
@app.get("/v1/parametroObligatorio/{id}", tags=["Parametro Obligatorio"])
async def consulta_uno(id: int):
    return {"mensaje":"Usuario encontrado",
            "usuario":id,
            "status":200}

# Endpoint con parámetros opcionales
@app.get("/v1/parametroOpcional/", tags=["Parámetro Opcional"])
async def consulta_todos(id:Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje":"Usuario encontrado", "usuario":usuarioK}
        return {"mensaje":"Usuario no encontrado", "status":200}
    else:
        return {"mensaje":"No se proporcionó ID.", "status":200}

# MÉTODO GET
@app.get("/v1/usuarios/", tags=["HTTP CRUD"])
async def leer_usuarios():
    return{
        "total":len(usuarios),
        "usuarios":usuarios,
        "status":200
    }

# MÉTODO POST
@app.post("/v1/crearUsuario/", tags=["HTTP CRUD"])
async def agregar_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(status_code=400, detail="El ID ya existe")

    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado exitosamente",
        "datos_nuevos":usuario,
        "status":200
    }

# MÉTODO PUT
@app.put("/v1/actualizarUsuario/{user_id}", tags=["HTTP CRUD"])
async def actualizar_usuario(user_id:int, usuario_actualizado:dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == user_id:
            usuario_actualizado["id"] = user_id
            usuarios[index] = usuario_actualizado
            return {
                "mensaje":"Usuario actualizado exitosamente",
                "datos_nuevos":usuario_actualizado,
                "status":200
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# MÉTODO PATCH
@app.patch("/v1/modificarUsuario/{user_id}", tags=["HTTP CRUD"])
async def modificar_usuario(user_id:int, datos_parciales:dict):
    for usr in usuarios:
        if usr["id"] == user_id:
            usr.update(datos_parciales)
            return {
                "mensaje":"Usuario modificado exitosamente",
                "datos_actualizados":usr,
                "status":200
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# MÉTODO DELETE
@app.delete("/v1/eliminarUsuario/{user_id}", tags=["HTTP CRUD"])
async def eliminar_usuario(user_id:int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == user_id:
            usuarios.pop(index)
            return {
                "mensaje":"Usuario eliminado exitosamente",
                "status":200
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")