# Ejercicio 2 - Punto B: Persistencia y gestión del catálogo
import json


class GestorInventario:
    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        # Pasamos cada objeto a diccionario para poder guardarlo en JSON
        catalogo = []
        for dispositivo in lista_dispositivos:
            catalogo.append(dispositivo.a_diccionario())

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(catalogo, archivo, indent=4, ensure_ascii=False)

        print(f"Catálogo guardado en {ruta_archivo} ({len(catalogo)} productos)")
