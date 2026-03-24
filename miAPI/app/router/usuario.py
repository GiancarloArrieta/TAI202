from fastapi import HTTPException, Depends, APIRouter, status
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuarios import usuario as dbUsuario

# DECLARACIÓN DE ROUTER
router = APIRouter(
    prefix = "/v1/usuarios",
    tags = ["CRUD Usuarios"]
)

# MÉTODO GET
@router.get("/", status_code = status.HTTP_200_OK)
async def leer_usuarios(db:Session = Depends(get_db)):
    queryUsuarios = db.query(dbUsuario).all()
    return{
        "total":len(queryUsuarios),
        "usuarios":queryUsuarios
    }

# MÉTODO POST
@router.post("/", status_code = status.HTTP_201_CREATED)
async def agregar_usuario(usuarioPy:crear_usuario, db:Session = Depends(get_db)):
    nuevoUsuario = dbUsuario(
        nombre = usuarioPy.nombre,
        edad = usuarioPy.edad
    )
    db.add(nuevoUsuario); db.commit(); db.refresh(nuevoUsuario)
    return{
        "mensaje":"Usuario agregado exitosamente",
        "usuario":nuevoUsuario
    }

# MÉTODO PUT
@router.put("/{user_id}", status_code = status.HTTP_200_OK)
async def actualizar_usuario(user_id:int, usuario_actualizado:dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == user_id:
            usuario_actualizado["id"] = user_id
            usuarios[index] = usuario_actualizado
            return {
                "mensaje":"Usuario actualizado exitosamente",
                "datos_nuevos":usuario_actualizado
            }

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

# MÉTODO PATCH
@router.patch("/{user_id}", status_code = status.HTTP_200_OK)
async def modificar_usuario(user_id:int, datos_parciales:dict):
    for usr in usuarios:
        if usr["id"] == user_id:
            usr.update(datos_parciales)
            return {
                "mensaje":"Usuario modificado exitosamente",
                "datos_actualizados":usr
            }

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

# MÉTODO DELETE
@router.delete("/{user_id}", status_code = status.HTTP_200_OK)
async def eliminar_usuario(user_id:int, usuarioAuth: str = Depends(verificar_peticion)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == user_id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por: {usuarioAuth}"
            }

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")