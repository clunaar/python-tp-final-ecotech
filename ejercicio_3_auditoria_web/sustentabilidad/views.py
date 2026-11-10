from django.shortcuts import render

from .metricas import cargar_registros, obtener_metricas_consumo


def vista_panel_sustentabilidad(request):
    """Vista basada en función (FBV): procesa las métricas y renderiza el panel."""
    metricas = obtener_metricas_consumo(cargar_registros())
    contexto = {"titulo": "Panel de Sustentabilidad", **metricas}
    return render(request, "sustentabilidad/panel.html", contexto)
