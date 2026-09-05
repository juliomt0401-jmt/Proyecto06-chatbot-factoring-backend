import requests
import os
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
from app.bd import BD

RUC_FACTOR = os.getenv("RUC_FACTOR")

def calcular_TEM_desde_TEA(TEA: Decimal) -> Decimal:
    TEM = (Decimal("1") + TEA) ** (Decimal("1") / Decimal("12")) - Decimal("1")
    return TEM.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def calcular_TED_desde_TEA(TEA: Decimal) -> Decimal:
    TED = (Decimal("1") + TEA) ** (Decimal("1") / Decimal("360")) - Decimal("1")
    return TED.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def calcular_TED_desde_TEM(TEM: Decimal) -> Decimal:
    TED = (Decimal("1") + TEM) ** (Decimal("1") / Decimal("30")) - Decimal("1")
    return TED.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def obtener_factor_vigente_IGV() -> Decimal:
    sql = """
        SELECT Valor1 FROM sys_parametros WHERE RUC_Factor = %s AND idParametro = '0002' AND Estado = 'V'
    """
    db = BD()
    recordset = db.ejecutar_SQL(sql, (RUC_FACTOR,))
    if not recordset:
        return Decimal("0.00")  # Valor por defecto si no se encuentra en la base de datos
    igv_vigente = Decimal(recordset[0]["Valor1"])
    return igv_vigente


def calcular_factoring(tea: Decimal, factor_adelanto: Decimal, importe: Decimal, fecha_pago: date) -> dict:

    # Plazo de financiamiento
    fecha_inicio = date.today() + timedelta(days=1)
    plazo = (fecha_pago - fecha_inicio).days + 1

    # Tasas equivalentes
    tem = calcular_TEM_desde_TEA(tea)
    ted = calcular_TED_desde_TEA(tea)

    # Adelanto
    importe_adelanto = round( round(importe * factor_adelanto, 3), 2)

    # Interés anticipado
    uno = Decimal("1")
    interes = round( round( (uno - (uno / ((uno + ted) ** plazo))) * importe_adelanto, 3), 2)

    # IGV
    igv = round( round(interes * obtener_factor_vigente_IGV(), 3), 2)

    # Importe a desembolsar
    importe_desembolsar = (importe_adelanto - interes - igv)

    # Importe remanente
    importe_remanente = (importe - importe_adelanto)

    return {
        "TEA": tea,
        "TEM": tem,
        "TED": ted,
        "Importe": importe,
        "FactorAdelanto": factor_adelanto,
        "ImporteAdelanto": importe_adelanto,
        "Plazo": plazo,
        "Interes": interes,
        "IGV": igv,
        "ImporteDesembolsar": importe_desembolsar,
        "ImporteRemanente": importe_remanente
    }


def consultar_ruc_api(RUC: str) -> str:
    try:
        url = f"https://openruc.com/api/ruc/{RUC}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        datos = response.json()
        return datos.get("razon_social", "")

    except requests.Timeout:
        print("Error: tiempo de espera agotado al consultar OpenRUC.")
        return ""
    except requests.ConnectionError:
        print("Error: no se pudo conectar con OpenRUC.")
        return ""
    except requests.HTTPError as e:
        print(f"Error HTTP al consultar OpenRUC: {e}")
        return ""
    except requests.RequestException as e:
        print(f"Error en la consulta a OpenRUC: {e}")
        return ""
    except ValueError:
        print("Error: OpenRUC devolvió una respuesta que no es JSON válido.")
        return ""


def buscar_descripcion_tabla(tabla: str, elemento: str) -> str:
    sql = """
        SELECT Descripcion
        FROM sys_tablas
        WHERE  idTabla=%s and idElemento=%s
    """
    db = BD()
    recordset = db.ejecutar_SQL(sql, (tabla, elemento))
    if not recordset:
        return ""
    descripcion = recordset[0]["Descripcion"]
    return descripcion
