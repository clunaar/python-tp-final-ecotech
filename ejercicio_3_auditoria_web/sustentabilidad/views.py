import json
import os

from django.shortcuts import render

from sustentabilidad.calculos import obtener_metricas_consumo

# Ruta al JSON con los registros de prueba
RUTA_DATOS = os.path.join(os.path.dirname(__file__), "data", "consumos.json")


def vista_panel_sustentabilidad(request):
    with open(RUTA_DATOS, "r", encoding="utf-8") as archivo:
        registros = json.load(archivo)

    metricas = obtener_metricas_consumo(registros)

    contexto = {
        "total_emisiones": metricas["total_emisiones"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "mayor_consumo": metricas["mayor_consumo"],
        "consumo_por_planta": metricas["consumo_por_planta"],
        "cantidad_registros": len(registros),
    }
    return render(request, "sustentabilidad/panel.html", contexto)
