"""Bloque de prueba del Ejercicio 2.

1. Crea productos válidos (incluido un PanelSolar).
2. Intenta asignar un stock erróneo y captura StockInvalidoError.
3. Exporta los productos válidos a catalogo_ecotech.json.
"""

from pathlib import Path

from dispositivos import DispositivoEcológico, PanelSolar
from excepciones import StockInvalidoError
from gestor import GestorInventario

RUTA_CATALOGO = Path(__file__).parent / "catalogo_ecotech.json"


def main():
    catalogo = [
        DispositivoEcológico("ECO-100", "Compostera doméstica 120 L", 85000, 25),
        PanelSolar("SOL-450", "Panel solar monocristalino 450 W", 320000, 40, 450, 0.215),
        PanelSolar("SOL-300", "Panel solar policristalino 300 W", 210000, 12, 300, 0.18),
    ]

    print("=== Fichas técnicas (polimorfismo) ===")
    for producto in catalogo:
        print(producto.ficha_tecnica())
        print()

    print("=== Validación de stock ===")
    # Caso 1: un producto que nace con stock negativo no entra al catálogo.
    try:
        catalogo.append(PanelSolar("SOL-999", "Panel defectuoso", 100000, -5, 200, 0.15))
    except StockInvalidoError as error:
        print(f"✔ Producto rechazado: {error}")

    # Caso 2: asignación errónea sobre un producto existente; el stock no cambia.
    panel = catalogo[1]
    try:
        panel.stock = -10
    except StockInvalidoError as error:
        print(f"✔ Asignación rechazada en {panel}: {error}")
    print(f"  Stock de {panel} sin cambios: {panel.stock} u.")

    ruta = GestorInventario.guardar_catalogo_json(catalogo, RUTA_CATALOGO)
    print(f"\n✔ {len(catalogo)} productos válidos exportados a {ruta.name}")


if __name__ == "__main__":
    main()
