import unittest

from sensores import (
    UBICACION_POR_DEFECTO,
    generar_resumen_sensores,
    limpiar_registro_sensor,
)


class TestLimpiarRegistroSensor(unittest.TestCase):
    def test_limpia_id_temperatura_y_ubicacion(self):
        resultado = limpiar_registro_sensor(
            {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"}
        )
        self.assertEqual(
            resultado,
            {"sensor_id": "SENSOR-001", "temperatura": 24.5, "ubicacion": "Planta Norte"},
        )

    def test_acepta_grados_y_coma_decimal(self):
        self.assertEqual(limpiar_registro_sensor({"sensor_id": "S1", "temperatura": " 31.2 °C "})["temperatura"], 31.2)
        self.assertEqual(limpiar_registro_sensor({"sensor_id": "S1", "temperatura": "28,7C"})["temperatura"], 28.7)

    def test_ubicacion_por_defecto(self):
        self.assertEqual(limpiar_registro_sensor({"sensor_id": "S1", "temperatura": "20"})["ubicacion"], UBICACION_POR_DEFECTO)
        self.assertEqual(limpiar_registro_sensor({"sensor_id": "S1", "temperatura": "20", "ubicacion": "  "})["ubicacion"], UBICACION_POR_DEFECTO)

    def test_temperatura_invalida_eleva_error(self):
        with self.assertRaises(ValueError):
            limpiar_registro_sensor({"sensor_id": "S1", "temperatura": "error"})

    def test_sin_id_eleva_error(self):
        with self.assertRaises(ValueError):
            limpiar_registro_sensor({"sensor_id": "   ", "temperatura": "20"})


class TestGenerarResumenSensores(unittest.TestCase):
    def test_alertas_y_promedio(self):
        sensores = [
            {"sensor_id": "A", "temperatura": 20.0, "ubicacion": "X"},
            {"sensor_id": "B", "temperatura": 32.0, "ubicacion": "X"},
            {"sensor_id": "C", "temperatura": 31.0, "ubicacion": "X"},
        ]
        self.assertEqual(generar_resumen_sensores(sensores, 30), (["B", "C"], 27.67))

    def test_igual_al_umbral_no_alerta(self):
        self.assertEqual(generar_resumen_sensores([{"sensor_id": "A", "temperatura": 30.0}], 30)[0], [])

    def test_lista_vacia(self):
        self.assertEqual(generar_resumen_sensores([], 30), ([], 0.0))


if __name__ == "__main__":
    unittest.main()
