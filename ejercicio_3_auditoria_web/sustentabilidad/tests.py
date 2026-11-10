# Ejercicio 3 - Punto A: Auditoría del algoritmo de emisiones con unittest
import unittest

from sustentabilidad.calculos import calcular_emisiones_carbono, obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):

    def test_valor_nominal(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(1000), 400)

    def test_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(500, 0.5), 250)

    def test_consumo_con_decimales(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(123.5), 49.4)

    def test_consumo_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    def test_consumo_negativo(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-10)


class TestMetricasConsumo(unittest.TestCase):

    def setUp(self):
        self.registros = [
            {"planta": "Norte", "consumo_kwh": 1000},
            {"planta": "Sur", "consumo_kwh": 3000},
            {"planta": "Norte", "consumo_kwh": 500},
        ]

    def test_total_emisiones(self):
        metricas = obtener_metricas_consumo(self.registros)
        self.assertAlmostEqual(metricas["total_emisiones"], 1800)

    def test_planta_mayor_consumo(self):
        metricas = obtener_metricas_consumo(self.registros)
        self.assertEqual(metricas["planta_mayor_consumo"], "Sur")


if __name__ == "__main__":
    unittest.main()
