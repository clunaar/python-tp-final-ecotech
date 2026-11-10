"""Persistencia del catálogo en disco (Punto B)."""

import json
from pathlib import Path


class GestorInventario:
    """Guarda el catálogo de dispositivos en un archivo JSON."""

    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo="catalogo_ecotech.json") -> Path:
        ruta = Path(ruta_archivo)
        datos = [dispositivo.to_dict() for dispositivo in lista_dispositivos]
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        return ruta
