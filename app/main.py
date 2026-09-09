from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from fastapi.responses import FileResponse

from app.models.adquirente import Adquirente
from app.models.proveedor import Proveedor
from app.logica import calcular_factoring
from app.cotizacion import generar_cotizacion_pdf

app = FastAPI(
    title="API Factoring",
    version="1.0.0"
)

class CalculoFactoringRequest(BaseModel):
    tea: Decimal
    factor_adelanto: Decimal
    importe: Decimal
    fecha_pago: date

class CotizacionPDFRequest(BaseModel):
    ruc_proveedor: str
    razon_social_proveedor: str
    id_proveedor: int
    facturas: list[dict]

@app.get("/")
def inicio():
    return {"mensaje": "API Factoring operativa"}

@app.get("/adquirentes/{ruc}")
def consultar_adquirente(ruc: str) -> dict:
    return Adquirente.consultar_adquirente(ruc)

@app.get("/proveedores/{ruc}")
def consultar_proveedor(ruc: str) -> dict:
    return Proveedor.consultar_proveedor(ruc)

@app.post("/calcular-factoring")
def api_calcular_factoring(datos: CalculoFactoringRequest) -> dict:
    return calcular_factoring(
        datos.tea,
        datos.factor_adelanto,
        datos.importe,
        datos.fecha_pago
    )

@app.post("/cotizaciones/pdf")
def api_generar_cotizacion_pdf(datos: CotizacionPDFRequest) -> FileResponse:

    Path("CotizacionesPDF").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ruta_pdf = Path(f"CotizacionesPDF/cotizacion_factoring_{timestamp}.pdf")

    generar_cotizacion_pdf(
        ruc_proveedor=datos.ruc_proveedor,
        razon_social_proveedor=datos.razon_social_proveedor,
        id_proveedor=datos.id_proveedor,
        facturas=datos.facturas,
        ruta_salida=ruta_pdf
    )

    return FileResponse(
        path=ruta_pdf,
        media_type="application/pdf",
        filename="cotizacion_factoring.pdf"
    )