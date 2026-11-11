from typing import Optional
from fastapi import Header, HTTPException


async def verificar_gerente(x_role: Optional[str] = Header(default=None)):
    """Solo deja pasar al rol 'Gerente'. Lee el header X-Role."""
    if x_role != "Gerente":
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado: se requiere el rol Gerente"
        )
    return x_role


async def verificar_auditor(x_role: Optional[str] = Header(default=None)):
    """Deja pasar a 'Gerente' y a 'Auditor'. Lee el header X-Role."""
    if x_role not in ("Gerente", "Auditor"):
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado: se requiere el rol Gerente o Auditor"
        )
    return x_role