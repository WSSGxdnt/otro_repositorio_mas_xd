import json
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/ordenes", tags=["Órdenes de servicio"])

ARCHIVO = Path(__file__).resolve().parent.parent / "taller.json"


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
@router.post("/", response_model=OrdenOut, status_code=201)
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


@router.get("/", response_model=List[OrdenOut])
def consultar_ordenes(
    estado: Optional[str] = Query(None, description="Filtrar por estado exacto"),
    modelo: Optional[str] = Query(None, description="Filtrar por modelo exacto"),
    costo_minimo: Optional[float] = Query(
        None, ge=0, description="Costo de reparación mínimo (>=)"
    ),
):
    resultado = leer_ordenes()

    # Filtros acumulativos: cada filtro enviado reduce aún más la lista,
    # así que todos los que lleguen se cumplen a la vez (lógica AND).
    if estado is not None:
        resultado = [o for o in resultado if o["estado"].lower() == estado.lower()]

    if modelo is not None:
        resultado = [o for o in resultado if o["modelo"].lower() == modelo.lower()]

    if costo_minimo is not None:
        resultado = [o for o in resultado if o["costo_reparacion"] >= costo_minimo]

    return resultado


@router.put("/{placa}", response_model=OrdenOut)
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


@router.delete("/{placa}")
def eliminar_orden(placa: str):
    ordenes = leer_ordenes()

    # Se elimina la orden más recientemente registrada con esa placa.
    for i in range(len(ordenes) - 1, -1, -1):
        if ordenes[i]["placa"] == placa:
            eliminada = ordenes.pop(i)
            guardar_ordenes(ordenes)
            return {"mensaje": "Orden eliminada", "orden": eliminada}

    raise HTTPException(status_code=404, detail="Placa no encontrada")
