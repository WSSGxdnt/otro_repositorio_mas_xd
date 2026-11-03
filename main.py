from fastapi import FastAPI

from routers import ordenes

app = FastAPI(title="Sistema de Órdenes de Servicio - Taller de Motos")

app.include_router(ordenes.router)
