
import asyncio
from fastapi import FastAPI

from database import cargar_inventario,crear_producto, vender_producto

resultados_prueba = []


async def preparar_inventario():
    """Prepara los productos para la prueba de estres. rkejgiuehwgi"""

    productos_prueba = [
        ("P001", "Teclado mecanico", 120000, 10),
        ("P002", "Mouse gamer", 65000, 5),
        ("P003", "Monitor sospechoso", 450000, 4),
        ("P004", "Audifonos de combate", 90000, 8)
    ]

    inventario = await cargar_inventario()

    if inventario["productos"]:
        return

    for codigo, nombre, precio, stock in productos_prueba:
        await crear_producto(codigo, nombre, precio, stock)


async def venta_segura(codigo, cantidad, descripcion):
    """Ejecuta una venta y captura sus errores. ajhfiughaiuosegh"""

    try:
        producto = await vender_producto(codigo, cantidad)

        mensaje = (
            f"{descripcion}: venta exitosa de {cantidad} unidades xd"
            f"de {producto['nombre']}. "
            f"Stock restante: {producto['stock']}."
        )

        print(mensaje)

        # Aviso de stock bajo.
        if producto["stock"] <= 2:
            aviso = (
                f"ALERTA: quedan solamente {producto['stock']} "
                f"unidades de {producto['nombre']}."
            )

            print(aviso)

            resultados_prueba.append({
                "tipo": "alerta_stock",
                "mensaje": aviso
            })

        resultado = {
            "tipo": "venta_exitosa",
            "mensaje": mensaje,
            "producto": producto
        }

        resultados_prueba.append(resultado)
        return resultado

    except ValueError as error:
        mensaje = f"{descripcion}: venta rechazada. {error}"
        print(mensaje)

        resultado = {
            "tipo": "error",
            "mensaje": mensaje
        }

        resultados_prueba.append(resultado)
        return resultado

    except Exception as error:
        mensaje = f"{descripcion}: error inesperado. {error}"
        print(mensaje)

        resultado = {
            "tipo": "error_inesperado",
            "mensaje": mensaje
        }

        resultados_prueba.append(resultado)
        return resultado


async def ejecutar_prueba():
    """Simula cuatro ventas concurrentes."""

    await preparar_inventario()

    resultados_prueba.clear()

    print("\n===== INICIO DE LA PRUEBA o no se xd =====")

    await asyncio.gather(
        # Caso 1: venta normal.
        venta_segura("P001", 3, "Venta 1"),

        # Caso 2: deja el stock en 2 y activa la alerta.
        venta_segura("P002", 3, "Venta 2"),

        # Caso 3: intenta vender mas unidades de las disponibles.
        venta_segura("P003", 10, "Venta 3"),

        # Caso 4: otra venta normal.
        venta_segura("P004", 2, "Venta 4")
    )

    print("===== FIN DE LA PRUEBA xd =====\n")



app = FastAPI(
    title="Proyecto Inventario",
    description="API de inventario y prueba.... :D",
    version="1.0.0"
)


@app.on_event("startup")
async def iniciar_aplicacion():
    await ejecutar_prueba()


@app.get("/")
async def inicio():
    return {
        "mensaje": "Inventario iniciado correctamente.",
        "documentacion": "/docs",
        "rutas_disponibles": [
            "/",
            "/inventario",
            "/resultados"
        ]
    }


@app.get("/inventario")
async def consultar_inventario():
    return await cargar_inventario()


@app.get("/resultados")
async def consultar_resultados():
    return {
        "total_resultados": len(resultados_prueba),
        "resultados": resultados_prueba
    }