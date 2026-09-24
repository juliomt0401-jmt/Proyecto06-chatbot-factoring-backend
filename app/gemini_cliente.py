import os
import time
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Literal
from pydantic import BaseModel, Field
from pathlib import Path
from dotenv import load_dotenv
from contextvars import ContextVar
from google import genai
from google.genai import types
from google.genai import errors

from app.prompt import SYSTEM_INSTRUCTION
from app.models.adquirente import Adquirente
from app.models.proveedor import Proveedor
from app.logica import calcular_factoring as calcular_factoring_backend
from app.cotizacion import generar_cotizacion_pdf as generar_cotizacion_pdf_backend


class RespuestaAgente(BaseModel):
    respuesta: str = Field(
        description="Respuesta al usuario en español, con formato Markdown."
    )
    etapa: Literal[
        "identificacion",
        "facturas",
        "evaluacion",
        "cotizacion",
    ] = Field(
        description=("Etapa actual de la conversación, determinada según las reglas del SYSTEM_INSTRUCTION.")
    )


# Inicializar cliente
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")   # Local (.env)
file_search_store = os.environ["GEMINI_FILE_SEARCH_STORE"]
client = genai.Client(api_key=api_key)

chats: dict[str, Any] = {}
pdf_generado: dict[str, dict[str, str]] = {}
sesion_actual: ContextVar[str] = ContextVar("sesion_actual", default="")

#Función para convertir valores a JSON serializable
def convertir_json(valor: Any) -> Any:
    if isinstance(valor, Decimal):
        return str(valor)

    if isinstance(valor, (date, datetime)):
        return valor.isoformat()

    if isinstance(valor, dict):
        return {
            clave: convertir_json(dato)
            for clave, dato in valor.items()
        }

    if isinstance(valor, list):
        return [convertir_json(dato) for dato in valor]

    return valor


# Definimos las cuatro herramientas del backend

def consultar_adquirente(RUC: str) -> dict[str, Any]:
    #Consulta un adquirente utilizando su RUC.
    #Input: RUC del adquirente.
    #Output: Diccionario con los datos del adquirente.
    print(f">>> TOOL consultar_adquirente: {RUC}")
    resultado = Adquirente.consultar_adquirente(RUC)
    return convertir_json(resultado)

def consultar_proveedor(RUC: str) -> dict[str, Any]:
    #Consulta un proveedor utilizando su RUC.
    #Input: RUC del proveedor.
    #Output: Diccionario con los datos del proveedor
    print(f">>> TOOL consultar_proveedor: {RUC}")
    resultado = Proveedor.consultar_proveedor(RUC)
    return convertir_json(resultado)

def calcular_factoring(tea: str, factor_adelanto: str, importe: str, fecha_pago: str) -> dict[str, Any]:
    #Calcula una operación de factoring.
    #Input:     tea: TEA obtenida del adquirente.
    #           factor_adelanto: Factor de Adelanto obtenido del adquirente.
    #           importe: VNPP de la factura.
    #           fecha_pago: Fecha de pago en formato YYYY-MM-DD.
    #Output: Diccionario con el cálculo del factoring
    print(
        f">>> TOOL calcular_factoring: "
        f"TEA={tea}, Factor={factor_adelanto}, "
        f"Importe={importe}, Fecha={fecha_pago}"
    )
    resultado = calcular_factoring_backend(
        tea=Decimal(str(tea)),
        factor_adelanto=Decimal(str(factor_adelanto)),
        importe=Decimal(str(importe)),
        fecha_pago=date.fromisoformat(fecha_pago)
    )
    return convertir_json(resultado)

def generar_cotizacion_pdf(ruc_proveedor: str, id_proveedor: int, facturas: list[dict]) -> dict[str, str]:
    #Genera el documento PDF formal de una cotización de factoring.
    #Input: ruc_proveedor: RUC del proveedor.
    #       id_proveedor: Identificador del proveedor.
    #       facturas: Lista de facturas ya calculadas.
    #Output: Ruta del archivo PDF generado.
    print(f">>> TOOL generar_cotizacion_pdf: {ruc_proveedor}")
    print(f"ruc_proveedor={ruc_proveedor}")
    print(f"id_proveedor={id_proveedor}")
    print(f"facturas={facturas}")

    proveedor = Proveedor.consultar_proveedor(ruc_proveedor)
    razon_social_proveedor = proveedor["RazonSocial"]

    BASE_DIR = Path(__file__).resolve().parent.parent
    CARPETA_COTIZACIONES = BASE_DIR / "CotizacionesPDF"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = (f"cotizacion_{ruc_proveedor}_{timestamp}.pdf")
    ruta_salida = (CARPETA_COTIZACIONES / nombre_archivo)

    # Convertir los valores recibidos desde Gemini
    # nuevamente a los tipos usados por el Backend.
    campos_decimal = [
        "TEM",
        "FactorAdelanto",
        "importe",
        "ImporteAdelanto",
        "Interes",
        "ComisionFactoring",
        "IGV",
        "ImporteDesembolsar",
        "ImporteRemanente"
    ]

    facturas_backend = []

    for factura in facturas:
        f = factura.copy()
        for campo in campos_decimal:
            if campo in f:
                f[campo] = Decimal(str(f[campo]))
        if isinstance(f.get("fecha_pago"), str):
            f["fecha_pago"] = date.fromisoformat(f["fecha_pago"])
        facturas_backend.append(f)
    generar_cotizacion_pdf_backend(
        ruc_proveedor=ruc_proveedor,
        razon_social_proveedor=razon_social_proveedor,
        id_proveedor=id_proveedor,
        facturas=facturas_backend,
        ruta_salida=ruta_salida
    )
    session_id = sesion_actual.get()
    pdf_generado[session_id] = {
        "nombre": nombre_archivo,
        "url": f"/cotizaciones/{nombre_archivo}"
    }

    return {"nombre_archivo": nombre_archivo}


# Funciones para sala de chat multiusuarios

def crear_chat():
    return client.chats.create(
        model="gemini-3.6-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=RespuestaAgente,
            tools=[
                types.Tool(
                    file_search=types.FileSearch(
                        file_search_store_names=[file_search_store]
                    )
                ),
                consultar_adquirente,
                consultar_proveedor,
                calcular_factoring,
                generar_cotizacion_pdf
            ],
            tool_config=types.ToolConfig(
                include_server_side_tool_invocations=True,
                function_calling_config=types.FunctionCallingConfig(
                    mode=types.FunctionCallingConfigMode.VALIDATED
                )
            )
        )
    )

def obtener_chat(session_id: str):
    if session_id not in chats:
        chats[session_id] = crear_chat()

    return chats[session_id]

def consumir_pdf_generado(session_id: str) -> dict[str, str] | None:
    return pdf_generado.pop(session_id, None)


def enviar_mensaje(session_id: str, mensaje: str) -> dict:

    inicio = time.perf_counter()
    token = sesion_actual.set(session_id)
    try:
        chat = obtener_chat(session_id)
        response = chat.send_message(mensaje)
        fin = time.perf_counter()
        print(f">>> Sesión: {session_id}")
        print(f">>> Tiempo Gemini: {fin - inicio:.2f} segundos")

        #Limpiando la respuesta para evitar que salga warnings en la terminal
        textos: list[str] = []
        if response.candidates:
            content = response.candidates[0].content

            if content and content.parts:
                for part in content.parts:
                    if part.text:
                        textos.append(part.text)

        resultado = RespuestaAgente.model_validate_json("".join(textos))
        return {
            "response": resultado.respuesta,
            "etapa": resultado.etapa,
        }
    except errors.ServerError as e:
        print(f">>> Error Gemini ServerError: {e}")
        return {
            "response": "El servicio de atención está temporalmente ocupado. Por favor, intenta nuevamente en unos segundos.",
            "etapa": None,
        }
    except Exception as e:
        print(f">>> Error inesperado: {e}")
        return {
            "response": "Ocurrió un problema al procesar tu mensaje. Por favor, intenta nuevamente.",
            "etapa": None,
        }
    finally:
        sesion_actual.reset(token)