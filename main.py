from fastapi import FastAPI, HTTPException
from database import leer_base_datos, guardar_base_datos, db_lock
from schemas import OrdenCreate, OrdenUpdate

apiRest = FastAPI(
    title="API Taller de Motos SENA",
    description="Módulo de recepción y seguimiento de motocicletas",
    version="1.0.0"
)

@apiRest.post("/ordenes", status_code=201)
async def crear_orden(orden: OrdenCreate):
    async with db_lock:
        datos = await leer_base_datos()

        for dato in datos:
            if dato["placa"] == orden.placa and dato["estado"] != "Entregada":
                raise HTTPException(status_code=400, detail="La moto ya se encuentra en el taller")

        nueva_orden = orden.model_dump()
        nueva_orden["estado"] = "En diagnóstico"
        nueva_orden["costo_reparacion"] = 0

        datos.append(nueva_orden)
        await guardar_base_datos(datos)

    return nueva_orden

@apiRest.get("/ordenes")
async def listar_ordenes():
    return await leer_base_datos()

@apiRest.put("/ordenes/{placa}")
async def actualizar_orden(placa: str, cambios: OrdenUpdate):
    async with db_lock:
        datos = await leer_base_datos()
        posicion = None
        for i in range(len(datos) - 1, -1, -1):
            if datos[i]["placa"] == placa:
                posicion = i
                break
        if posicion is None:
            raise HTTPException(status_code=404, detail="No existe una orden con esa placa")
        if cambios.nuevo_estado == "Reparada" and cambios.costo_reparacion <= 0:
            raise HTTPException(
                status_code=400,
                detail="No se puede marcar como reparada sin asignar un costo de reparación"
            )

        datos[posicion]["estado"] = cambios.nuevo_estado
        datos[posicion]["costo_reparacion"] = cambios.costo_reparacion
        await guardar_base_datos(datos)

        return datos[posicion]