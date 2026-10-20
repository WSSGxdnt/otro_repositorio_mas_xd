
import asyncio
import json
import aiofiles

from pathlib import Path

RUTA_ARCHIVO = Path(__file__).parent / "inventario.json"

# Evita que varias operaciones modifiquen el archivo al mismo tiempo.
candado = asyncio.Lock()


async def _cargar_sin_bloqueo():
    """Funcion interna para leer el archivo."""

    if not RUTA_ARCHIVO.exists():
        return {"productos": []}

    async with aiofiles.open(
        RUTA_ARCHIVO,
        mode="r",
        encoding="utf-8"
    ) as archivo:
        contenido = await archivo.read()

    return json.loads(contenido)


async def _guardar_sin_bloqueo(inventario):
    """Funcion interna para guardar el archivo."""

    contenido = json.dumps(
        inventario,
        indent=4,
        ensure_ascii=False
    )

    async with aiofiles.open(
        RUTA_ARCHIVO,
        mode="w",
        encoding="utf-8"
    ) as archivo:
        await archivo.write(contenido)


async def cargar_inventario():
    """Consulta el inventario completo."""

    async with candado:
        return await _cargar_sin_bloqueo()


async def obtener_producto(codigo):
    """Busca un producto por su codigo."""

    async with candado:
        inventario = await _cargar_sin_bloqueo()

        for producto in inventario["productos"]:
            if producto["codigo"] == codigo:
                return producto.copy()

        return None


async def crear_producto(codigo, nombre, precio, stock):
    """Registra un producto nuevo."""

    if not codigo.strip() or not nombre.strip():
        raise ValueError("El codigo y el nombre son obligatorios.")

    if precio < 0 or stock < 0:
        raise ValueError("El precio y el stock no pueden ser negativos.")

    async with candado:
        inventario = await _cargar_sin_bloqueo()

        if any(
            producto["codigo"] == codigo
            for producto in inventario["productos"]
        ):
            raise ValueError("Ese codigo ya existe.")

        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "stock": stock
        }

        inventario["productos"].append(producto)

        await _guardar_sin_bloqueo(inventario)

        return producto.copy()


async def vender_producto(codigo, cantidad):
    """Realiza una venta y comprueba que haya stock suficiente."""

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")

    async with candado:
        inventario = await _cargar_sin_bloqueo()

        for producto in inventario["productos"]:
            if producto["codigo"] == codigo:

                if producto["stock"] < cantidad:
                    raise ValueError(
                        f"Stock insuficiente para {producto['nombre']}. "
                        f"Disponible: {producto['stock']}, "
                        f"solicitado: {cantidad}."
                    )

                producto["stock"] -= cantidad

                await _guardar_sin_bloqueo(inventario)

                return producto.copy()

        raise ValueError(f"No existe el producto {codigo}.")


async def eliminar_producto(codigo):
    """Elimina un producto por su codigo."""

    async with candado:
        inventario = await _cargar_sin_bloqueo()

        for producto in inventario["productos"]:
            if producto["codigo"] == codigo:
                inventario["productos"].remove(producto)

                await _guardar_sin_bloqueo(inventario)

                return True

        return False