# Ejercicio 2 - Bloque de prueba
from productos import DispositivoEcológico, PanelSolar, StockInvalidoError
from gestor_inventario import GestorInventario

# --- PRUEBA ---
compostera = DispositivoEcológico("Compostera doméstica", 85000, 25)
panel_1 = PanelSolar("Panel solar 450W", 320000, 40, 450, 21.5)
panel_2 = PanelSolar("Panel solar 300W", 210000, 12, 300, 18)

productos_validos = [compostera, panel_1, panel_2]

print("=== Fichas técnicas ===")
for producto in productos_validos:
    print(producto.ficha_tecnica())

print("\n=== Prueba de stock inválido ===")
try:
    panel_1.set_stock(-10)
except StockInvalidoError as error:
    print(f"Error capturado: {error}")
print(f"El stock de {panel_1.nombre} sigue en {panel_1.get_stock()}")

try:
    panel_roto = PanelSolar("Panel defectuoso", 100000, -5, 200, 15)
except StockInvalidoError as error:
    print(f"Error capturado: {error}")

print("\n=== Exportación ===")
gestor = GestorInventario()
gestor.guardar_catalogo_json(productos_validos, "catalogo_ecotech.json")
