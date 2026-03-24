# Importaciones
from fastapi import FastAPI
from app.router import usuario, misc
from app.data.db import engine
from app.data import usuarios

# Tablas de BD
usuarios.Base.metadata.create_all(bind = engine)

# Instancia del servidor
app = FastAPI(
    title="Mi primera API",
    description="Giancarlo Arrieta Zatarain",
    version="1.0"
)

app.include_router(usuario.router)
app.include_router(misc.misc)