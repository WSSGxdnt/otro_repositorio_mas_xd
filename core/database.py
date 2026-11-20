from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from core.config import settings

# 1. El engine. Va a hablar con la BD
engine = create_async_engine(
    settings.DATABASE_URL,
    echo = True # Imprimir en la consola lo que se haga en SQL
)

# 2. La sesión: Transacción con la BD
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 3. Base: Es la clase padre
Base = declarative_base()

# 4. Dependencia para FastAPI
async def obtener_bd():
    db = SessionLocal()
    try:
        # Pasamos la conexión a la ruta que la haya pedido
        yield db
    finally:
        # Cerramos la conexión cada vez que terminemos
        await db.close()
