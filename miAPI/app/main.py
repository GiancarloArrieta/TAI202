# Importaciones
from fastapi import FastAPI
from app.router import usuario, misc

# Instancia del servidor
app = FastAPI(
    title="Mi primera API",
    description="Giancarlo Arrieta Zatarain",
    version="1.0"
)

app.include_router(usuario.router)
app.include_router(misc.misc)