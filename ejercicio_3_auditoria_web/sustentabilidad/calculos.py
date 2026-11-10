# Ejercicio 3 - Algoritmo de emisiones y procesamiento de métricas


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo")
    return consumo_kwh * factor_emision


# Punto B: procesamiento de métricas
def obtener_metricas_consumo(registros):
    total_emisiones = 0
    consumo_por_planta = {}

    for registro in registros:
        planta = registro["planta"]
        consumo = registro["consumo_kwh"]

        total_emisiones += calcular_emisiones_carbono(consumo)

        # Acumulamos el consumo de cada planta en un diccionario
        if planta in consumo_por_planta:
            consumo_por_planta[planta] += consumo
        else:
            consumo_por_planta[planta] = consumo

    # Buscamos la planta que más consumió
    planta_mayor_consumo = None
    mayor_consumo = 0
    for planta, consumo in consumo_por_planta.items():
        if consumo > mayor_consumo:
            mayor_consumo = consumo
            planta_mayor_consumo = planta

    return {
        "total_emisiones": round(total_emisiones, 2),
        "planta_mayor_consumo": planta_mayor_consumo,
        "mayor_consumo": round(mayor_consumo, 2),
        "consumo_por_planta": consumo_por_planta,
    }
