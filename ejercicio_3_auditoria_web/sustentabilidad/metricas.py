"""Tubería de datos que alimenta el panel de sustentabilidad (Punto B)."""

import json
from pathlib import Path

from .emisiones import calcular_emisiones_carbono

RUTA_DATOS = Path(__file__).parent / "data" / "consumos.json"


def cargar_registros(ruta=RUTA_DATOS) -> list[dict]:
    """Lee el historial simulado de consumos (JSON con registros de prueba)."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


def obtener_metricas_consumo(registros: list[dict]) -> dict:
    """Procesa el historial de consumos por planta industrial.

    Cada registro tiene la forma {"planta": str, "mes": str, "consumo_kwh": float}.
    Devuelve el total global de emisiones, la planta de mayor consumo y el
    detalle por planta ordenado de mayor a menor consumo.
    """
    consumo_por_planta: dict[str, float] = {}
    for registro in registros:
        planta = registro["planta"]
        consumo_por_planta[planta] = consumo_por_planta.get(planta, 0) + registro["consumo_kwh"]

    detalle_plantas = sorted(
        (
            {
                "planta": planta,
                "consumo_kwh": round(consumo, 2),
                "emisiones_kg": calcular_emisiones_carbono(consumo),
            }
            for planta, consumo in consumo_por_planta.items()
        ),
        key=lambda fila: fila["consumo_kwh"],
        reverse=True,
    )

    return {
        "total_consumo_kwh": round(sum(consumo_por_planta.values()), 2),
        "total_emisiones_kg": round(sum(fila["emisiones_kg"] for fila in detalle_plantas), 2),
        "planta_mayor_consumo": detalle_plantas[0] if detalle_plantas else None,
        "detalle_plantas": detalle_plantas,
        "cantidad_registros": len(registros),
    }
