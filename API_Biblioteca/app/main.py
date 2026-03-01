# IMPORTACIONES
from datetime import datetime
from fastapi import FastAPI, HTTPException
from typing import Optional, Literal, List
from pydantic import BaseModel, Field, EmailStr

# INSTANCIA DEL SERVIDOR
app = FastAPI(
    title="API Biblioteca",
    description="Autor: Giancarlo Arrieta Zatarain",
    version="1.0"
)

# DECLARACIÓN DE ESTATUS PERMITIDOS
AllowedStatus = Literal["disponible", "prestado"]

# CREACIÓN DE MODELOS
class CrearUsuario(BaseModel):
    id: int = Field(...,gt=0, description="Identificador único del usuario.")
    nombre: str = Field(..., min_length=3, max_length=50)
    correo: EmailStr = Field(..., min_length=6, max_length=50)
    libros_prestados_ids: List[int] = []

class CrearLibro(BaseModel):
    id: int = Field(...,gt=0, description="Identificador único del libro.")
    nombre: str = Field(..., min_length=2, max_length=100, example="Don Quijote")
    anyio: int = Field(..., gt=1450, le=2026, description="Año de publicación del libro.")
    paginas: int = Field(..., gt=0, description="Cantidad de páginas del libro.")
    estatus: AllowedStatus = Field(..., description="Estatus del libro (disponible o prestado).")

class Prestamo(BaseModel):
    id: int = Field(..., gt=0, description="Identificador único del préstamo")
    id_usuario: int = Field(..., gt=0, description="Identificador del usuario que tiene el libro")
    id_libro: int = Field(..., gt=0, description="Identificador del libro que tiene el usuario")
    fecha_prestamo: datetime = Field(default_factory=datetime.now, description="Fecha y hora de registro del préstamo")

# DECLARACIÓN DE TABLAS
usuarios: List[CrearUsuario] = [
    CrearUsuario(id=1, nombre="Giancarlo", correo="giancarlo@libros.com")
]
libros: List[CrearLibro] = [
    CrearLibro(id=1, nombre="Como Agua Para Chocolate", anyio=1989, paginas=272, estatus="disponible"),
    CrearLibro(id=2, nombre="Bajo la Misma Estrella", anyio=2012, paginas=304, estatus="disponible")
]
prestamos: List[Prestamo] = []

# --- ENDPOINTS USUARIOS ---

# Método GET
@app.get("/v1/usuarios", tags=["CRUD Usuarios"])
async def consultar_usuarios(id_usuario:Optional[int] = None):
    if not usuarios:
        return {
            "mensaje": "No hay usuarios registrados.",
            "status": 200
        }
    if id_usuario is not None:
        for usuario in usuarios:
            if usuario.id == id_usuario:
                return {"mensaje":"Usuario encontrado", "usuario":usuario}
        return {"mensaje":"Usuario no encontrado", "status":200}
    else:
        return {
            "total": len(usuarios),
            "usuarios": usuarios,
            "status": 200
        }

# Método POST
@app.post("/v1/usuarios", tags=["CRUD Usuarios"])
async def agregar_usuario(usuario_nuevo:CrearUsuario):
    for usuario in usuarios:
        if usuario.id == usuario_nuevo.id:
            raise HTTPException(status_code=400, detail="El ID ya existe")
    usuarios.append(usuario_nuevo)
    return{
        "mensaje":"Usuario agregado exitosamente",
        "datos_nuevos":usuario_nuevo,
        "status":200
    }

# Método PUT
@app.put("/v1/usuarios/{id_usuario}", tags=["CRUD Usuarios"])
async def actualizar_usuario(id_usuario:int, usuario_actualizado:CrearUsuario):
    for index, usr in enumerate(usuarios):
        if usr.id == id_usuario:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje":"Usuario actualizado exitosamente",
                "datos_nuevos":usuario_actualizado,
                "status":200
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Método PATCH
@app.patch("/v1/usuarios/{id_usuario}")
async def modificar_usuario(id_usuario: int, datos_parciales: dict):
    usuario = next((u for u in usuarios if u.id == id_usuario), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in datos_parciales.items():
        if hasattr(usuario, key):
            setattr(usuario, key, value)
    return {"mensaje": "Usuario modificado exitosamente", "usuario": usuario, "status": 200}

# Método DELETE
@app.delete("/v1/usuarios/{id_usuario}", tags=["CRUD Usuarios"])
async def eliminar_usuario(id_usuario:int):
    for index, usr in enumerate(usuarios):
        if usr.id == id_usuario:
            usuarios.pop(index)
            return {
                "mensaje":"Usuario eliminado exitosamente",
                "status":200
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# --- ENDPOINTS LIBROS ---

# Método GET
@app.get("/v1/libros", tags=["CRUD Libros"])
async def consultar_libros(nombre_libro: Optional[str] = None):
    if not libros:
        return {
            "mensaje": "No hay libros registrados.",
            "status": 200
        }
    if nombre_libro is not None:
        for libro in libros:
            if libro.nombre == nombre_libro:
                return {"mensaje":"Libro encontrado", "libro":libro}
        return {"mensaje":"Libro no encontrado", "status":400}
    else:
        return {
            "total": len(libros),
            "libros": libros,
            "status": 200
        }

# Método POST
@app.post("/v1/libros", tags=["CRUD Libros"])
async def agregar_libro(libro_nuevo:CrearLibro):
    for lib in libros:
        if lib.id == libro_nuevo.id:
            raise HTTPException(status_code=400, detail="El ID ya existe")
    libros.append(libro_nuevo)
    return{
        "mensaje":"Usuario agregado exitosamente",
        "datos_nuevos":libro_nuevo,
        "status":201
    }

# Método PUT
@app.put("/v1/libros/{id_libro}", tags=["CRUD Libros"])
async def actualizar_libro(id_libro:int, libro_actualizado:CrearLibro):
    for index, libro in enumerate(libros):
        if libro.id == id_libro:
            libros[index] = libro_actualizado
            return {
                "mensaje":"Libro actualizado exitosamente",
                "datos_nuevos":libro_actualizado,
                "status":200
            }

    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Método PATCH
@app.patch("/v1/libros/{id_libro}", tags=["CRUD Libros"])
async def modificar_libro(id_libro: int, datos_parciales: dict):
    libro = next((l for l in libros if l.id == id_libro), None)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    for key, value in datos_parciales.items():
        if hasattr(libro, key):
            setattr(libro, key, value)
    return {"mensaje": "Libro modificado", "libro": libro, "status": 200}

# Método DELETE
@app.delete("/v1/libros/{id_libro}", tags=["CRUD Libros"])
async def eliminar_libro(id_libro:int):
    for index, libro in enumerate(libros):
        if libro.id == id_libro:
            libros.pop(index)
            return {
                "mensaje":"Libro eliminado exitosamente",
                "status":200
            }

    raise HTTPException(status_code=404, detail="Libro no encontrado")

# --- ENDPOINTS PRÉSTAMOS ---

# Consulta de préstamos activos (GET)
@app.get("/v1/prestamos", tags=["Acciones Préstamos"])
async def consultar_prestamos():
    if not prestamos:
        return {"mensaje": "No hay préstamos activos.", "status": 200}
    return {"total": len(prestamos), "prestamos": prestamos, "status": 200}

# Registro de préstamo (POST)
@app.post("/v1/prestamos", tags=["Acciones Préstamos"])
async def registrar_prestamo(prestamo_nuevo:Prestamo):
    if any(prestamo.id == prestamo_nuevo.id for prestamo in prestamos):
        raise HTTPException(status_code=400, detail="El ID de préstamo ya existe")

    usuario = next((u for u in usuarios if u.id == prestamo_nuevo.id_usuario), None)
    libro = next((l for l in libros if l.id == prestamo_nuevo.id_libro), None)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    if libro.estatus == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya se encuentra prestado")

    libro.estatus = "prestado"
    usuario.libros_prestados_ids.append(prestamo_nuevo.id_libro)
    prestamos.append(prestamo_nuevo)

    return {"mensaje": "Préstamo registrado exitosamente", "data": prestamo_nuevo, "status": 201}

# Devolución de un libro (DELETE)
@app.delete("/v1/prestamos/{id_prestamo}", tags=["Acciones Préstamos"])
async def devolver_libro(id_prestamo: int):
    prestamo_index = -1
    for i, p in enumerate(prestamos):
        if p.id == id_prestamo:
            prestamo_index = i
            break

    if prestamo_index == -1:
        raise HTTPException(status_code=409, detail="Préstamo no encontrado")

    p_temp = prestamos[prestamo_index]

    libro = next((l for l in libros if l.id == p_temp.id_libro), None)
    if libro:
        libro.estatus = "disponible"

    usuario = next((u for u in usuarios if u.id == p_temp.id_usuario), None)
    if usuario and p_temp.id_libro in usuario.libros_prestados_ids:
        usuario.libros_prestados_ids.remove(p_temp.id_libro)

    prestamos.pop(prestamo_index)

    return {"mensaje": f"Libro ID {p_temp.id_libro} devuelto y préstamo finalizado", "status": 200}