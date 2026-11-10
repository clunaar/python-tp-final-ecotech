import json
import tempfile
import unittest
from pathlib import Path

from dispositivos import DispositivoEcológico, PanelSolar
from excepciones import StockInvalidoError
from gestor import GestorInventario


class TestDispositivos(unittest.TestCase):
    def setUp(self):
        self.panel = PanelSolar("SOL-1", "Panel 450 W", 320000, 10, 450, 0.215)

    def test_stock_negativo_al_crear(self):
        with self.assertRaises(StockInvalidoError):
            DispositivoEcológico("ECO-1", "Compostera", 1000, -1)

    def test_stock_negativo_al_asignar_no_modifica(self):
        with self.assertRaises(StockInvalidoError):
            self.panel.stock = -3
        self.assertEqual(self.panel.stock, 10)

    def test_stock_no_entero(self):
        for valor in ("5", 2.5, True, None):
            with self.subTest(valor=valor), self.assertRaises(StockInvalidoError):
                self.panel.stock = valor

    def test_stock_cero_es_valido(self):
        self.panel.stock = 0
        self.assertEqual(self.panel.stock, 0)

    def test_stock_privado(self):
        self.assertFalse(hasattr(self.panel, "__stock"))

    def test_herencia_y_polimorfismo(self):
        self.assertIsInstance(self.panel, DispositivoEcológico)
        base = DispositivoEcológico("ECO-1", "Compostera", 1000, 1).ficha_tecnica()
        self.assertNotIn("Potencia", base)
        self.assertIn("Potencia: 450 W", self.panel.ficha_tecnica())


class TestGestorInventario(unittest.TestCase):
    def test_guardar_catalogo_json(self):
        catalogo = [
            DispositivoEcológico("ECO-1", "Compostera", 1000, 5),
            PanelSolar("SOL-1", "Panel", 2000, 3, 450, 0.2),
        ]
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = GestorInventario.guardar_catalogo_json(catalogo, Path(carpeta) / "catalogo_ecotech.json")
            datos = json.loads(ruta.read_text(encoding="utf-8"))
        self.assertEqual(len(datos), 2)
        self.assertEqual(datos[0]["tipo"], "DispositivoEcológico")
        self.assertEqual(datos[1]["potencia_w"], 450)
        self.assertEqual(datos[1]["stock"], 3)


if __name__ == "__main__":
    unittest.main()
