import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Sistema de Órdenes de Servicio - Taller de Motos")

ARCHIVO = Path(__file__).parent / "taller.json"


# ---------- Esquemas Pydantic ----------
class OrdenCreate(BaseModel):
    placa: str = Field(..., min_length=1, max_length=6)
    modelo: str = Field(..., min_length=1)
    falla_reportada: str = Field(..., min_length=1)


class OrdenUpdate(BaseModel):
    nuevo_estado: str = Field(..., min_length=1)
    costo_reparacion: float


class OrdenOut(BaseModel):
    placa: str
    modelo: str
    falla_reportada: str
    estado: str
    costo_reparacion: float


# ---------- Persistencia en JSON ----------
def leer_ordenes() -> list:
    if not ARCHIVO.exists():
        return []
    try:
        contenido = ARCHIVO.read_text(encoding="utf-8").strip()
        return json.loads(contenido) if contenido else []
    except json.JSONDecodeError:
        return []


def guardar_ordenes(ordenes: list) -> None:
    ARCHIVO.write_text(
        json.dumps(ordenes, indent=4, ensure_ascii=False), encoding="utf-8"
    )


# ---------- Endpoints ----------
@app.post("/ordenes", response_model=OrdenOut, status_code=201)
def crear_orden(orden: OrdenCreate):
    ordenes = leer_ordenes()

    for o in ordenes:
        if o["placa"] == orden.placa and o["estado"] != "Entregada":
            raise HTTPException(
                status_code=400, detail="La moto ya se encuentra en el taller"
            )

    nueva = orden.model_dump()
    nueva["estado"] = "En diagnóstico"
    nueva["costo_reparacion"] = 0

    ordenes.append(nueva)
    guardar_ordenes(ordenes)
    return nueva


@app.get("/ordenes", response_model=List[OrdenOut])
def consultar_ordenes():
    return leer_ordenes()


@app.put("/ordenes/{placa}", response_model=OrdenOut)
def actualizar_orden(placa: str, datos: OrdenUpdate):
    ordenes = leer_ordenes()

    # Regla 1: la placa debe existir. Si hay varias órdenes con la misma
    # placa (reingresos), se toma la más reciente (la última registrada).
    orden = next((o for o in reversed(ordenes) if o["placa"] == placa), None)
    if orden is None:
        raise HTTPException(status_code=404, detail="Placa no encontrada")

    # Regla 2: no se puede marcar como reparada sin costo mayor a 0
    if datos.nuevo_estado == "Reparada" and datos.costo_reparacion <= 0:
        raise HTTPException(
            status_code=400,
            detail="No se puede marcar como reparada sin asignar un costo de reparación",
        )

    # Regla 3: actualizar estado y costo
    orden["estado"] = datos.nuevo_estado
    orden["costo_reparacion"] = datos.costo_reparacion
    guardar_ordenes(ordenes)
    return orden
