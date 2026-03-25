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
async def actualizar_usuario(user_id:int, usuarioPy:crear_usuario, db:Session = Depends(get_db)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == user_id).first()
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    usuario_db.nombre = usuarioPy.nombre
    usuario_db.edad = usuarioPy.edad

    db.commit(); db.refresh(usuario_db)
    
    return {
        "mensaje":"Usuario actualizado exitosamente",
        "datos_nuevos":usuario_db
    }

# MÉTODO PATCH
@router.patch("/{user_id}", status_code = status.HTTP_200_OK)
async def modificar_usuario(user_id:int, datos_parciales:dict, db:Session = Depends(get_db)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == user_id).first()
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    for key, value in datos_parciales.items():
        if hasattr(usuario_db, key):
            setattr(usuario_db, key, value)

    db.commit()
    db.refresh(usuario_db)
    
    return {
        "mensaje":"Usuario modificado exitosamente",
        "datos_actualizados":usuario_db
    }

# MÉTODO DELETE
@router.delete("/{user_id}", status_code = status.HTTP_200_OK)
async def eliminar_usuario(user_id:int, usuarioAuth: str = Depends(verificar_peticion), db:Session = Depends(get_db)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == user_id).first()
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    db.delete(usuario_db)
    db.commit()
    
    return {
        "mensaje": f"Usuario eliminado por: {usuarioAuth}"
    }
