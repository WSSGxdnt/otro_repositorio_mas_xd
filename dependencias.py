from fastapi import Header, HTTPException, Query

async def verificar_api_key(x_api_key: str = Header(..., description="API Key secreta del taller")):
    if x_api_key != "Sena2026":
        raise HTTPException(status_code=401, detail="Acceso denegado. API Key inválido")
    return x_api_key

def parametros_paginacion(
    skip: int = Query(0, description="Cuantos registros saltar"),
    limit: int = Query(10, description="Limite de registros a devolver")
):
    return {"skip": skip, "limit": limit}

async def simular_base_datos():
    print("1. [DEPENDENCIA] Abriendo la conexión con el Json...")
    yield "Conexión está lista"
    print("3. [DEPENDENCIA] Cerrando archivo Json y liberando memoria...")
