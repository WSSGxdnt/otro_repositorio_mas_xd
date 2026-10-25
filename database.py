import json
import asyncio
from pathlib import Path
 
import aiofiles
 
ARCHIVO_BD = Path(__file__).parent / "taller.json"
db_lock = asyncio.Lock()
 
 
async def leer_base_datos():
    try:
        async with aiofiles.open(ARCHIVO_BD, mode="r", encoding="utf-8") as f:
            contenido = await f.read()
            return json.loads(contenido) if contenido.strip() else []
    except FileNotFoundError:
        return []
 
 
async def guardar_base_datos(datos):
    async with aiofiles.open(ARCHIVO_BD, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(datos, indent=4, ensure_ascii=False))