from fastapi import HTTPException, Depends, APIRouter, status
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

# DECLARACIÓN DE ROUTER
router = APIRouter(
    prefix = "/v1/usuarios",
    tags = ["CRUD Usuarios"]
)

# MÉTODO GET
@router.get("/", status_code = status.HTTP_200_OK)
async def leer_usuarios():
    return{
        "total":len(usuarios),
        "usuarios":usuarios
    }

# MÉTODO POST
@router.post("/", status_code = status.HTTP_201_CREATED)
async def agregar_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El ID ya existe")
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado exitosamente",
        "datos_nuevos":usuario
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