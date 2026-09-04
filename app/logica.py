from decimal import Decimal, ROUND_HALF_UP


def calcular_TEM_desde_TEA(TEA: Decimal) -> Decimal:
    TEM = (Decimal("1") + TEA) ** (Decimal("1") / Decimal("12")) - Decimal("1")
    return TEM.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def calcular_TED_desde_TEA(TEA: Decimal) -> Decimal:
    TED = (Decimal("1") + TEA) ** (Decimal("1") / Decimal("360")) - Decimal("1")
    return TED.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def calcular_TED_desde_TEM(TEM: Decimal) -> Decimal:
    TED = (Decimal("1") + TEM) ** (Decimal("1") / Decimal("30")) - Decimal("1")
    return TED.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)