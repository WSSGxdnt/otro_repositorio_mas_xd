# routers/mecanicos.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from core.database import obtener_bd
from models.mecanico import Mecanico as MecanicoModel
from schemas.mecanicos import MecanicoCreate, MecanicoResponse

router = APIRouter(prefix="/mecanicos", tags=["Gestión de Mecánicos"])

# ================= GET: Listar mecánicos activos =================
@router.get("/", response_model=List[MecanicoResponse])
async def obtener_mecanicos(db: AsyncSession = Depends(obtener_bd)):
    sentencia = select(MecanicoModel).where(MecanicoModel.activo == True)
    resultado = await db.execute(sentencia)
    return resultado.scalars().all()


# ================= GET: Obtener mecánico por ID =================
@router.get("/{mecanico_id}", response_model=MecanicoResponse)
async def obtener_mecanico_por_id(
    mecanico_id: int, 
    db: AsyncSession = Depends(obtener_bd)
):
    sentencia = select(MecanicoModel).where(MecanicoModel.id == mecanico_id)
    resultado = await db.execute(sentencia)
    mecanico = resultado.scalar_one_or_none()

    if not mecanico:
        raise HTTPException(status_code=404, detail="Mecánico no encontrado")

    return mecanico


# ================= POST: Registrar nuevo mecánico =================
@router.post("/", response_model=MecanicoResponse, status_code=201)
async def crear_mecanico(
    mecanico: MecanicoCreate, 
    db: AsyncSession = Depends(obtener_bd)
):
    # Validamos que el documento no esté registrado previamente
    sentencia_check = select(MecanicoModel).where(MecanicoModel.documento == mecanico.documento)
    resultado_check = await db.execute(sentencia_check)
    if resultado_check.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Ya existe un mecánico con ese número de documento")

    nuevo_mecanico = MecanicoModel(**mecanico.model_dump())
    db.add(nuevo_mecanico)

    try:
        await db.commit()
        await db.refresh(nuevo_mecanico)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error al registrar el mecánico")

    return nuevo_mecanico


# ================= DELETE: Desactivar mecánico (Soft Delete) =================
@router.delete("/{mecanico_id}", status_code=204)
async def desactivar_mecanico(
    mecanico_id: int, 
    db: AsyncSession = Depends(obtener_bd)
):
    sentencia = select(MecanicoModel).where(MecanicoModel.id == mecanico_id)
    resultado = await db.execute(sentencia)
    mecanico = resultado.scalar_one_or_none()

    if not mecanico:
        raise HTTPException(status_code=404, detail="Mecánico no encontrado")

    # En lugar de borrarlo físicamente y dañar las Foreign Keys de sus órdenes, lo desactivamos
    mecanico.activo = False
    await db.commit()

    return None