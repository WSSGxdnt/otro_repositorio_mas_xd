# routers/repuestos.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from core.database import obtener_bd
from models.repuesto import Repuesto as RepuestoModel
from schemas.repuestos import RepuestoCreate, RepuestoPatch, RepuestoResponse
from dependencias import parametros_paginacion

router = APIRouter(prefix="/repuestos", tags=["Gestión de Repuestos"])

@router.get("/", response_model=List[RepuestoResponse])
async def listar_repuestos(
    solo_con_stock: bool = Query(False, description="Filtrar únicamente repuestos disponibles"),
    paginacion: dict = Depends(parametros_paginacion),
    db: AsyncSession = Depends(obtener_bd)
):
    sentencia = select(RepuestoModel)

    if solo_con_stock:
        sentencia = sentencia.where(RepuestoModel.stock_actual > 0)

    sentencia = sentencia.offset(paginacion["skip"]).limit(paginacion["limit"])
    resultado = await db.execute(sentencia)
    return resultado.scalars().all()

@router.get("/{repuesto_id}", response_model=RepuestoResponse)
async def obtener_repuesto_por_id(
    repuesto_id: int,
    db: AsyncSession = Depends(obtener_bd)
):
    sentencia = select(RepuestoModel).where(RepuestoModel.id == repuesto_id)
    resultado = await db.execute(sentencia)
    repuesto = resultado.scalar_one_or_none()

    if not repuesto:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")

    return repuesto

@router.post("/", status_code=201, response_model=RepuestoResponse)
async def crear_repuesto(
    repuesto: RepuestoCreate,
    db: AsyncSession = Depends(obtener_bd)
):
    # Verificar que el SKU no exista previamente
    consulta_sku = select(RepuestoModel).where(RepuestoModel.codigo_sku == repuesto.codigo_sku)
    res_sku = await db.execute(consulta_sku)
    if res_sku.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un repuesto registrado con el SKU '{repuesto.codigo_sku}'."
        )

    nuevo_repuesto = RepuestoModel(**repuesto.model_dump())
    db.add(nuevo_repuesto)

    try:
        await db.commit()
        await db.refresh(nuevo_repuesto)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error al registrar el repuesto en la base de datos.")

    return nuevo_repuesto

@router.patch("/{repuesto_id}", response_model=RepuestoResponse)
async def actualizar_repuesto(
    repuesto_id: int,
    repuesto_patch: RepuestoPatch,
    db: AsyncSession = Depends(obtener_bd)
):
    sentencia = select(RepuestoModel).where(RepuestoModel.id == repuesto_id)
    resultado = await db.execute(sentencia)
    repuesto_db = resultado.scalar_one_or_none()

    if not repuesto_db:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")

    datos_nuevos = repuesto_patch.model_dump(exclude_unset=True)
    for campo, valor in datos_nuevos.items():
        setattr(repuesto_db, campo, valor)

    try:
        await db.commit()
        await db.refresh(repuesto_db)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar el repuesto.")

    return repuesto_db

@router.delete("/{repuesto_id}", status_code=204)
async def eliminar_repuesto(
    repuesto_id: int,
    db: AsyncSession = Depends(obtener_bd)
):
    sentencia = select(RepuestoModel).where(RepuestoModel.id == repuesto_id)
    resultado = await db.execute(sentencia)
    repuesto_db = resultado.scalar_one_or_none()

    if not repuesto_db:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")

    try:
        await db.delete(repuesto_db)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el repuesto porque está asociado a órdenes de servicio."
        )

    return None