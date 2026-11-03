# Sistema de Órdenes de Servicio – Taller de Motos

API con FastAPI, organizada con `APIRouter`, que guarda las órdenes en `taller.json`.

## Estructura

```
Proyecto_Inventario/
├── main.py              # Inicializa FastAPI y registra el router
├── routers/
│   └── ordenes.py       # Esquemas, persistencia JSON y endpoints
├── taller.json          # Persistencia de las órdenes
└── requirements.txt
```

## Ejecutar

```
pip install -r requirements.txt
uvicorn main:app --reload
```

Documentación interactiva: http://127.0.0.1:8000/docs

## Endpoints

| Método | Ruta               | Descripción                                             |
|--------|--------------------|---------------------------------------------------------|
| POST   | `/ordenes/`        | Crea una orden (`En diagnóstico`, costo `0`)            |
| GET    | `/ordenes/`        | Lista órdenes; filtros opcionales y acumulativos        |
| PUT    | `/ordenes/{placa}` | Actualiza estado y costo (reglas de negocio)            |
| DELETE | `/ordenes/{placa}` | Elimina la orden más reciente de esa placa              |

### Filtros de `GET /ordenes/`

| Parámetro      | Tipo   | Comportamiento                              |
|----------------|--------|---------------------------------------------|
| `estado`       | string | Estado igual (sin distinguir mayúsculas)    |
| `modelo`       | string | Modelo igual (sin distinguir mayúsculas)    |
| `costo_minimo` | float  | `costo_reparacion >= costo_minimo`          |

Los filtros enviados se aplican **a la vez**. Ejemplo:

```
GET /ordenes/?modelo=Bajaj&costo_minimo=100000
```
