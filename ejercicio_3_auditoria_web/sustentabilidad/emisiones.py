"""Algoritmo de cálculo de huella de carbono industrial."""

FACTOR_EMISION_POR_DEFECTO = 0.4  # kg de CO2 por kWh


def calcular_emisiones_carbono(consumo_kwh: float, factor_emision: float = FACTOR_EMISION_POR_DEFECTO) -> float:
    """Devuelve los kg de CO2 emitidos para un consumo eléctrico dado.

    Eleva ValueError si el consumo es negativo.
    """
    if consumo_kwh < 0:
        raise ValueError(f"El consumo no puede ser negativo: {consumo_kwh}")
    return round(consumo_kwh * factor_emision, 2)
