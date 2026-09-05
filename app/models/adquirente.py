from typing import Dict, Any
from decimal import Decimal
from app.bd import BD
from app.logica import calcular_TEM_desde_TEA, consultar_ruc_api


def _calcular_TEA_adquirente_por_ranking_top(RUC: str) -> Decimal:

    sql = """
        SELECT Ranking FROM Top10K WHERE RUC = %s
    """
    db = BD()
    recordset = db.ejecutar_SQL(sql, (RUC,))
    if not recordset:
        return Decimal("0.3000")
    ranking = recordset[0]["Ranking"]
    bloque = ((ranking - 1001) // 200) + 1

    # Top 1 al 1000
    if ranking <= 1000: return Decimal("0.1200")

    # Top 1001 al 3000
    if ranking <= 3000: return (Decimal("0.1200") + Decimal(bloque) * Decimal("0.0020"))

    # Top 3001 al 5000
    if ranking <= 5000: return (Decimal("0.1400") + Decimal(bloque) * Decimal("0.0020"))

    # Fuera de política
    return Decimal("0.3000")


def _calcular_FactorAdelanto_adquirente_por_ranking_top(RUC: str) -> Decimal:

    sql = """
        SELECT Ranking FROM Top10K WHERE RUC = %s
    """
    db = BD()
    recordset = db.ejecutar_SQL(sql, (RUC,))
    if not recordset:
        return Decimal("0.9000")
    ranking = recordset[0]["Ranking"]

    # Top 1 al 1000
    if ranking <= 1000: return Decimal("0.9900")

    # Top 1001 al 3000
    if ranking <= 3000: return Decimal("0.9800")

    # Top 3001 al 5000
    if ranking <= 5000: return Decimal("0.9700")

    # Fuera de política
    return Decimal("0.9000")


class Adquirente:

    def __init__(
        self,
        idAdquirente: int | None = None,
        RUC: str | None = None,
        RazonSocial: str | None = None,
        NombreComercial: str | None = None,
        DireccionFiscal: str | None = None,
        Telefono: str | None = None,
        TipoContribuyente: str | None = None,
        UBIGEO: str | None = None,
        LineaAsignada: Decimal = Decimal("0.00"),
        TEA: Decimal = Decimal("0.0000"),
        TEM: Decimal = Decimal("0.0000"),
        FactorAdelanto: Decimal = Decimal("0.0000"),
        Estado: str | None = None
    ):
        self.idAdquirente = idAdquirente
        self.RUC = RUC
        self.RazonSocial = RazonSocial
        self.NombreComercial = NombreComercial
        self.DireccionFiscal = DireccionFiscal
        self.Telefono = Telefono
        self.TipoContribuyente = TipoContribuyente
        self.UBIGEO = UBIGEO
        self.LineaAsignada = LineaAsignada
        self.TEA = TEA
        self.TEM = TEM
        self.FactorAdelanto = FactorAdelanto
        self.Estado = Estado


    @staticmethod
    def consultar_adquirente(RUC: str) -> Dict[str, Any]:
        #Verifica si un adquirente existe por su RUC.
        #Retorna un diccionario con idAdquirente, RazonSocial, NombreComercial, LineaAsignada, TEA, TEM, Estado.
        #Si no existe, idAdquirente retorna 0 y buscará RazonSocial en el API con el RUC.
        db = BD()
        sql = """
            SELECT idAdquirente, RazonSocial, NombreComercial, LineaAsignada, TEA, TEM, FactorAdelanto, Estado
            FROM empresas e inner join adquirentes a on e.RUC = a.RUC 
            WHERE e.RUC = %s
        """
        recordset = db.ejecutar_SQL(sql, (RUC,))
        
        if recordset:
            return recordset[0]

        razon_social = consultar_ruc_api(RUC)
        FactorAdelanto = _calcular_FactorAdelanto_adquirente_por_ranking_top(RUC)
        TEA = _calcular_TEA_adquirente_por_ranking_top(RUC)
        TEM = calcular_TEM_desde_TEA(TEA)
 
        return {
            "idAdquirente": 0,
            "RazonSocial": razon_social,
            "NombreComercial": "",
            "LineaAsignada": Decimal("0.00"),
            "TEA": TEA,
            "TEM": TEM,
            "FactorAdelanto": FactorAdelanto,
            "Estado": ""
        }
