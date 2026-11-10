"""Auditoría del algoritmo de emisiones (Punto A) y pruebas de integración web."""

import unittest

from django.test import SimpleTestCase
from django.urls import reverse

from .emisiones import calcular_emisiones_carbono
from .metricas import obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    """Punto A: exactitud numérica y manejo de consumos fuera de rango."""

    def test_valor_nominal_con_factor_por_defecto(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(1000), 400.0)

    def test_valor_nominal_con_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(1500, factor_emision=0.25), 375.0)

    def test_valores_decimales(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(123.45), 49.38, places=2)

    def test_consumo_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    def test_consumo_negativo_eleva_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-1)

    def test_consumo_negativo_pequeno_eleva_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-0.01)


class TestMetricasConsumo(unittest.TestCase):
    """Punto B: procesamiento del historial por planta."""

    def setUp(self):
        self.registros = [
            {"planta": "Norte", "mes": "2026-09", "consumo_kwh": 1000},
            {"planta": "Sur", "mes": "2026-09", "consumo_kwh": 3000},
            {"planta": "Norte", "mes": "2026-10", "consumo_kwh": 500},
        ]

    def test_total_global_de_emisiones(self):
        metricas = obtener_metricas_consumo(self.registros)
        self.assertAlmostEqual(metricas["total_emisiones_kg"], 1800.0)
        self.assertAlmostEqual(metricas["total_consumo_kwh"], 4500.0)

    def test_planta_de_mayor_consumo(self):
        metricas = obtener_metricas_consumo(self.registros)
        self.assertEqual(metricas["planta_mayor_consumo"]["planta"], "Sur")

    def test_agrupa_por_planta(self):
        detalle = obtener_metricas_consumo(self.registros)["detalle_plantas"]
        self.assertEqual([fila["planta"] for fila in detalle], ["Sur", "Norte"])
        self.assertEqual(detalle[1]["consumo_kwh"], 1500)

    def test_sin_registros(self):
        metricas = obtener_metricas_consumo([])
        self.assertIsNone(metricas["planta_mayor_consumo"])
        self.assertEqual(metricas["total_emisiones_kg"], 0)

    def test_consumo_negativo_se_propaga(self):
        with self.assertRaises(ValueError):
            obtener_metricas_consumo([{"planta": "X", "mes": "2026-10", "consumo_kwh": -5}])


class TestVistaPanelSustentabilidad(SimpleTestCase):
    """Integración: la vista procesa los datos y renderiza la plantilla."""

    def test_panel_responde_y_usa_la_plantilla(self):
        respuesta = self.client.get(reverse("sustentabilidad:panel"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "sustentabilidad/panel.html")

    def test_contexto_listo_para_renderizar(self):
        respuesta = self.client.get(reverse("sustentabilidad:panel"))
        for clave in ("total_emisiones_kg", "planta_mayor_consumo", "detalle_plantas"):
            self.assertIn(clave, respuesta.context)
        self.assertEqual(respuesta.context["planta_mayor_consumo"]["planta"], "Planta Sur")
        self.assertContains(respuesta, "Planta Sur")
