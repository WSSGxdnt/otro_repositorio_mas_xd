from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from core.database import obtener_bd
from models.factura import Factura
from models.orden import Orden
from models.orden_repuesto import OrdenRepuesto
from schemas.facturas import FacturaDetalladaResponse

router = APIRouter(prefix="/facturas", tags=["Gestionar facturas"])

@router.get("/{orden_id}", response_model=FacturaDetalladaResponse)
async def obtener_factura(
    orden_id: int,
    db: AsyncSession = Depends(obtener_bd)):
    sentencia = (select(Factura).options(joinedload(Factura.orden).joinedload(Orden.mecanico), selectinload(Factura.orden).selectinload(Orden.repuestos_usados).joinedload(OrdenRepuesto.repuesto)).where(Factura.orden_id == orden_id))

    resultado = await db.execute(sentencia)
    factura = resultado.unique().scalar_one_or_none()

    if not factura:
        raise HTTPException(status_code=404, detail="No existe una factura para esta orden")

    orden = factura.orden

    return {
        "id": factura.id,
        "fecha_emision": factura.fecha_emision,
        "subtotal_repuestos": factura.subtotal_repuestos,
        "costo_mano_obra": factura.costo_mano_obra,
        "iva": factura.iva,
        "total_pagar": factura.total_pagar,

        "orden": {
            "placa": orden.placa,
            "modelo": orden.modelo,
            "mecanico": orden.mecanico.nombre_completo if orden.mecanico else "Sin mecánico"
        },

        "repuestos": [
            {
                "nombre_repuesto": detalle.repuesto.nombre,
                "cantidad": detalle.cantidad,
                "precio_unitario_historico": detalle.precio_unitario_historico,
                "subtotal_linea": detalle.cantidad * detalle.precio_unitario_historico
            }
            for detalle in orden.repuestos_usados
        ]
    }