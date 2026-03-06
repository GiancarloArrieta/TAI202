# IMPORTACIONES
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import asyncio
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

##############
# SEGURIDAD
##############

# Configuración de seguridad
SECRET_KEY = "Cl4v3_5eGuRa_123098"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para encriptar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__truncate_error=False)

# Creación de tokens de acceso
def crear_token_acceso(data: dict):
    datos_a_cifrar = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_a_cifrar.update({"exp": expiracion})
    token_jwt = jwt.encode(datos_a_cifrar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

# Definir de dónde obtendrá el token FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Consulta y verificación de tokens
async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return username

#Definir usuarios
usuarios_db = {
    "giancarlo": {
        "username": "giancarlo",
        "nombre": "Giancarlo",
        "password_hashed": pwd_context.hash("secreto123")
    }
}

##########################
# INSTANCIA DEL SERVIDOR
##########################
app = FastAPI(
    title="Mi API JWT",
    description="Giancarlo Arrieta Zatarain",
    version="1.0"
)

# TB Ficticia
usuarios = [
    {"id":1,"nombre":"Fernanda","edad":20},
    {"id":2,"nombre":"Sergio","edad":22},
    {"id":3,"nombre":"Jesús Manuel","edad":20},
]

# Creación de modelo
class crear_usuario(BaseModel):
    id: int = Field(...,gt=0, description="Identificador único del usuario")
    nombre: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "Agripino"})
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 y 123")

#############
# ENDPOINTS
#############

# Endpoint de autenticación
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = usuarios_db.get(form_data.username)
    if not usuario or not pwd_context.verify(form_data.password, usuario["password_hashed"]):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    access_token = crear_token_acceso(data={"sub": usuario["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

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
@app.get("/v1/parametroObligatorio/{id}", tags=["Parametro Obligatorio"], status_code=HTTP_200_OK)
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
@app.get("/v1/usuarios/", tags=["HTTP CRUD"], status_code=HTTP_200_OK)
async def leer_usuarios():
    return{
        "total":len(usuarios),
        "usuarios":usuarios
    }

# MÉTODO POST
@app.post("/v1/usuarios/", tags=["HTTP CRUD"], status_code=HTTP_200_OK)
async def agregar_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El ID ya existe")
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado exitosamente",
        "datos_nuevos":usuario
    }

# MÉTODO PUT
@app.put("/v1/usuarios/{user_id}", tags=["HTTP CRUD"], status_code=HTTP_200_OK)
async def actualizar_usuario(user_id:int, usuario_actualizado:dict, token: str = Depends(obtener_usuario_actual)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == user_id:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": f"Usuario con ID {user_id} actualizado exitosamente por {token}",
                "datos_nuevos":usuario_actualizado
            }

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

# MÉTODO PATCH
@app.patch("/v1/usuarios/{user_id}", tags=["HTTP CRUD"], status_code=HTTP_200_OK)
async def modificar_usuario(user_id:int, datos_parciales:dict):
    for usr in usuarios:
        if usr["id"] == user_id:
            usr.update(datos_parciales)
            return {
                "mensaje":"Usuario modificado exitosamente",
                "datos_actualizados":usr
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# MÉTODO DELETE
@app.delete("/v1/usuarios/{user_id}", tags=["HTTP CRUD"], status_code=HTTP_200_OK)
async def eliminar_usuario(user_id:int, token: str = Depends(obtener_usuario_actual)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == user_id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario con ID {user_id} eliminado exitosamente por {token}."
            }

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Usuario no encontrado")