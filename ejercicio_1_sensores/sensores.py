# Ejercicio 1 - Sanitización y Análisis Estadístico de Sensores
# EcoTech Solutions


# Punto A: Normalización de lecturas
def limpiar_registro_sensor(registro_raw):
    # Sacamos los espacios que sobran del identificador
    sensor_id = registro_raw.get("sensor_id", "").strip()

    # La temperatura viene como texto con la unidad pegada, por ejemplo "24.5C"
    temperatura = str(registro_raw.get("temperatura", "0"))
    temperatura = temperatura.replace("°", "").replace("C", "").strip()
    temperatura = float(temperatura)

    # Si no viene la ubicación (o viene vacía) usamos un valor por defecto
    ubicacion = registro_raw.get("ubicacion")
    if not ubicacion:
        ubicacion = "Sin ubicación"

    registro_limpio = {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }
    return registro_limpio


# Punto B: Monitoreo y mapeo estadístico
def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    lista_sensores_alerta = []
    suma_temperaturas = 0

    for sensor in lista_sensores_limpios:
        suma_temperaturas += sensor["temperatura"]
        if sensor["temperatura"] > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])

    if len(lista_sensores_limpios) > 0:
        promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    else:
        promedio_temperatura = 0

    return (lista_sensores_alerta, promedio_temperatura)


# --- PRUEBA ---
if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 31.2°C ", "ubicacion": "Planta Sur"},
        {"sensor_id": " SENSOR-003", "temperatura": "28.7C", "ubicacion": ""},
        {"sensor_id": "SENSOR-004  ", "temperatura": "35.0C"},
        {"sensor_id": "SENSOR-005", "temperatura": "22C", "ubicacion": "Oficinas"},
    ]
    umbral = 30

    # 1. Limpiamos cada registro crudo
    sensores_limpios = []
    for registro in registros_crudos:
        sensores_limpios.append(limpiar_registro_sensor(registro))

    # 2. Generamos el resumen
    alertas, promedio = generar_resumen_sensores(sensores_limpios, umbral)

    # 3. Imprimimos el reporte final
    print("-" * 45)
    print("REPORTE DE SENSORES - ECOTECH SOLUTIONS")
    print("-" * 45)
    for sensor in sensores_limpios:
        print(f"{sensor['sensor_id']} | {sensor['temperatura']:.1f} °C | {sensor['ubicacion']}")
    print("-" * 45)
    print(f"Promedio de temperatura de la planta: {promedio:.2f} °C")
    print(f"Sensores que superan los {umbral} °C: {alertas}")
    print("-" * 45)
