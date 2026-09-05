import requests
from decimal import Decimal, ROUND_HALF_UP
from app.bd import BD


def calcular_TEM_desde_TEA(TEA: Decimal) -> Decimal:
    TEM = (Decimal("1") + TEA) ** (Decimal("1") / Decimal("12")) - Decimal("1")
    return TEM.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def calcular_TED_desde_TEA(TEA: Decimal) -> Decimal:
    TED = (Decimal("1") + TEA) ** (Decimal("1") / Decimal("360")) - Decimal("1")
    return TED.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def calcular_TED_desde_TEM(TEM: Decimal) -> Decimal:
    TED = (Decimal("1") + TEM) ** (Decimal("1") / Decimal("30")) - Decimal("1")
    return TED.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)

def _consultar_ruc_api(RUC: str) -> str:
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


def buscar_descripcion_tabla(tabla: str, elemento: str) -> str | None:
    sql = """
        SELECT Descripcion
        FROM sys_tablas
        WHERE  idTabla=%s and iElemento=%s
    """
    db = BD()
    recordset = db.ejecutar_SQL(sql, (tabla, elemento))
    if not recordset:
        return ""
    descripcion = recordset[0]["Descripcion"]
    return descripcion
