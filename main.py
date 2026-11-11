from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
from models import mecanico, repuesto 
from routers import mecanicos, repuestos

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="API Taller de Motos SENA",
    description="Mecánicos y repuestos con SQLAlchemy asíncrono",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(mecanicos.router)
app.include_router(repuestos.router)