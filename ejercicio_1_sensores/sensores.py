"""Ejercicio 1: Sanitización y análisis estadístico de sensores.

EcoTech Solutions recibe lecturas térmicas con formato heterogéneo
(espacios de más, unidades pegadas al número, ubicaciones vacías).
Este módulo normaliza cada registro y genera un reporte consolidado.
"""

UBICACION_POR_DEFECTO = "Sin ubicación"
UNIDADES_TEMPERATURA = ("°C", "ºC", "C", "°")


def limpiar_registro_sensor(registro_raw: dict) -> dict:
    """Normaliza un registro crudo de sensor (Punto A).

    - sensor_id: sin espacios sobrantes y en mayúsculas.
    - temperatura: float, sin sufijo de unidad (acepta coma decimal).
    - ubicacion: valor por defecto si falta o viene vacía.

    Eleva ValueError si el sensor no tiene ID o la temperatura no es numérica.
    """
    sensor_id = str(registro_raw.get("sensor_id", "")).strip().upper()
    if not sensor_id:
        raise ValueError("El registro no tiene sensor_id")

    temperatura_texto = str(registro_raw.get("temperatura", "")).strip().upper()
    for unidad in UNIDADES_TEMPERATURA:
        if temperatura_texto.endswith(unidad):
            temperatura_texto = temperatura_texto[: -len(unidad)].strip()
            break
    try:
        temperatura = float(temperatura_texto.replace(",", "."))
    except ValueError:
        raise ValueError(
            f"Temperatura inválida en {sensor_id}: {registro_raw.get('temperatura')!r}"
        ) from None

    ubicacion = str(registro_raw.get("ubicacion") or "").strip() or UBICACION_POR_DEFECTO

    return {"sensor_id": sensor_id, "temperatura": temperatura, "ubicacion": ubicacion}


def generar_resumen_sensores(
    lista_sensores_limpios: list[dict], umbral_temperatura: float
) -> tuple[list[str], float]:
    """Devuelve (IDs que superan el umbral, promedio térmico global) (Punto B)."""
    if not lista_sensores_limpios:
        return [], 0.0

    lista_sensores_alerta = [
        sensor["sensor_id"]
        for sensor in lista_sensores_limpios
        if sensor["temperatura"] > umbral_temperatura
    ]
    temperaturas = [sensor["temperatura"] for sensor in lista_sensores_limpios]
    promedio_temperatura = round(sum(temperaturas) / len(temperaturas), 2)

    return lista_sensores_alerta, promedio_temperatura


if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "sensor-002", "temperatura": " 31.2 °C ", "ubicacion": "Planta Sur"},
        {"sensor_id": " SENSOR-003", "temperatura": "28,7C", "ubicacion": ""},
        {"sensor_id": "SENSOR-004  ", "temperatura": "35.0"},
        {"sensor_id": "SENSOR-005", "temperatura": "error", "ubicacion": "Depósito"},
        {"sensor_id": "SENSOR-006", "temperatura": 22, "ubicacion": "Oficinas"},
    ]
    UMBRAL = 30.0

    sensores_limpios = []
    for registro in registros_crudos:
        try:
            sensores_limpios.append(limpiar_registro_sensor(registro))
        except ValueError as error:
            print(f"⚠ Registro descartado: {error}")

    alertas, promedio = generar_resumen_sensores(sensores_limpios, UMBRAL)

    print()
    print("=" * 52)
    print(" REPORTE TÉRMICO · ECOTECH SOLUTIONS".center(52))
    print("=" * 52)
    print(f"{'Sensor':<12}{'Temperatura':>13}   {'Ubicación'}")
    print("-" * 52)
    for sensor in sensores_limpios:
        marca = " ⚠" if sensor["sensor_id"] in alertas else ""
        print(f"{sensor['sensor_id']:<12}{sensor['temperatura']:>10.1f} °C   {sensor['ubicacion']}{marca}")
    print("-" * 52)
    print(f"Sensores procesados: {len(sensores_limpios)}")
    print(f"Promedio térmico de la planta: {promedio:.2f} °C")
    print(f"Sensores sobre {UMBRAL:.1f} °C: {', '.join(alertas) or 'ninguno'}")
    print("=" * 52)
