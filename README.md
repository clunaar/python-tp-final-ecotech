# EcoTech Solutions - TP Final

Trabajo Práctico Final del curso **C3 | Programación con Python** (IPAP Mendoza).

**Alumno:** Claudio Luna

## Estructura

```
ejercicio_1_sensores/
    sensores.py              -> limpiar_registro_sensor() y generar_resumen_sensores()
ejercicio_2_productos/
    productos.py             -> StockInvalidoError, DispositivoEcológico y PanelSolar
    gestor_inventario.py     -> GestorInventario.guardar_catalogo_json()
    main.py                  -> bloque de prueba
ejercicio_3_auditoria_web/
    manage.py
    ecotech_panel/           -> configuración del proyecto Django
    sustentabilidad/         -> app
        calculos.py          -> calcular_emisiones_carbono() y obtener_metricas_consumo()
        tests.py             -> TestCalculoEmisiones (unittest)
        views.py             -> vista_panel_sustentabilidad()
        templates/sustentabilidad/panel.html
        data/consumos.json   -> registros de prueba
```

## Cómo ejecutarlo

Crear el entorno virtual e instalar Django:

```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Ejercicio 1**

```bash
cd ejercicio_1_sensores
python sensores.py
```

**Ejercicio 2** (genera el archivo `catalogo_ecotech.json`)

```bash
cd ejercicio_2_productos
python main.py
```

**Ejercicio 3**

```bash
cd ejercicio_3_auditoria_web
python manage.py test           # corre los tests de unittest
python manage.py runserver      # abrir http://127.0.0.1:8000/
```

![Panel de sustentabilidad](docs/panel-sustentabilidad.png)
