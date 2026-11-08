# Ejercicio 04 — Parámetros en Python y C++

Un nodo `heartbeat` que publica `"<robot_name>: alive"` en `robot/heartbeat` cada
`period_s` segundos, escrito en los dos lenguajes con los mismos parámetros. Un
solo archivo YAML configura cualquiera de las dos versiones.

**Antes de empezar**: teoría [05](../../1-teoria/05-parametros.md) leída.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-03-servicios_acciones_y_parametros/2-practicas/ejercicio-04-parametros/starter/* \
  src/
```

```
src/
├── ejercicio04_parametros_py/
│   ├── config/heartbeat.yaml                        # se instala en share/
│   ├── ejercicio04_parametros_py/heartbeat.py       # PASOS 1, 2 y 3
│   └── test/test_heartbeat.py
└── ejercicio04_parametros_cpp/
    ├── config/heartbeat.yaml                        # idéntico al de Python
    ├── include/ejercicio04_parametros_cpp/heartbeat.hpp   # PASOS 1, 2 y 3
    └── test/test_heartbeat.cpp
```

Haz cada paso primero en Python y después en C++. Verificación:

```bash
colcon build --packages-select ejercicio04_parametros_py ejercicio04_parametros_cpp --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio04_parametros_py ejercicio04_parametros_cpp
colcon test-result --verbose
```

## Paso 1: Declarar con descriptor

**Abre `heartbeat.py`** y descomenta el bloque del Paso 1. Luego lo mismo en
**`heartbeat.hpp`**.

**Por qué**: el descriptor convierte reglas que tendrías que programar ("el
periodo va de 0.1 a 5 s", "el nombre no cambia en marcha") en algo que ROS2
comprueba solo.

**Verifica**: pasan `test_declara_parametros_con_descriptor` y
`test_rechaza_valores_invalidos` (y sus equivalentes `HeartbeatTest.*` en C++).

## Paso 2: Leer y usar

**Descomenta el bloque del Paso 2** en los dos archivos.

**Verifica**: pasa `test_publica_latido_con_nombre` / `PublicaLatidoConNombre`.

## Paso 3: Cambios en marcha

**Descomenta el bloque del Paso 3** en los dos archivos. En Python, la callback
`_on_parameters_set` ya está escrita debajo; en C++ va dentro del bloque.

**Verifica**: pasa `test_cambio_de_periodo_en_marcha` / `CambioDePeriodoEnMarcha`.
Los ocho tests pasan.

## Paso 4: `ros2 param` en marcha

En cada terminal nueva, primero `source install/setup.bash`.

```bash
# Terminal 1
ros2 run ejercicio04_parametros_py heartbeat
```

```bash
# Terminal 2
ros2 param list /heartbeat
#   period_s
#   robot_name
#   start_type_description_service
#   use_sim_time

ros2 param describe /heartbeat period_s
# Parameter name: period_s
#   Type: double
#   Description: Segundos entre latidos
#   Constraints:
#     Min value: 0.1
#     Max value: 5.0
```

Ahora los tres rechazos y un cambio válido:

```bash
ros2 param set /heartbeat period_s 10.0
# Setting parameter failed: Parameter period_s out of range Min: 0.1, Max: 5.0, value: 10.0
ros2 param set /heartbeat robot_name otro
# Setting parameter failed: Trying to set a read-only parameter: robot_name.
ros2 param set /heartbeat period_s 1
# Setting parameter failed: Wrong parameter type, expected 'Type.DOUBLE' got 'Type.INTEGER'
ros2 param set /heartbeat period_s 0.2
# Set parameter successful
```

✅ Verificación: en la terminal 1 aparece `Nuevo periodo: 0.2 s`, y
`ros2 topic hz /robot/heartbeat` da unos 5 Hz.

```bash
ros2 param dump /heartbeat
# /heartbeat:
#   ros__parameters:
#     period_s: 0.2
#     robot_name: robot
#     start_type_description_service: true
#     use_sim_time: false
```

## Paso 5: Un YAML para los dos lenguajes

Cierra el nodo Python. Arranca el de C++ con el YAML **del paquete Python**:

```bash
# Terminal 1
ros2 run ejercicio04_parametros_cpp heartbeat --ros-args \
  --params-file install/ejercicio04_parametros_py/share/ejercicio04_parametros_py/config/heartbeat.yaml
```

```bash
# Terminal 2
ros2 param get /heartbeat robot_name
# String value is: explorer
ros2 topic echo /robot/heartbeat --once
# data: 'explorer: alive'
# ---
```

✅ Verificación: el nodo C++ tomó `explorer` y `0.5` del YAML. Funciona porque la
clave de primer nivel del YAML es el **nombre del nodo** (`heartbeat`), igual en
los dos lenguajes.

Por último, `-p` y `--params-file` juntos: gana el que va **después**.

```bash
ros2 run ejercicio04_parametros_py heartbeat --ros-args \
  --params-file install/ejercicio04_parametros_py/share/ejercicio04_parametros_py/config/heartbeat.yaml \
  -p period_s:=0.3
# En otra terminal: ros2 param get /heartbeat period_s  ->  Double value is: 0.3
```

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué `robot_name` es de solo lectura y `period_s` no?
2. ¿Qué pasaría si declararas `period_s` con valor por defecto `1` en vez de `1.0`?
3. Python cambia el periodo del timer sin recrearlo y C++ crea otro. ¿Qué
   alternativa usarías si una librería no permitiera ninguna de las dos?

## Checklist

- [ ] Los ocho tests (cuatro por lenguaje) pasan
- [ ] Provoqué los tres rechazos de `ros2 param set` y leí sus mensajes
- [ ] El nodo C++ arrancó con el YAML del paquete Python
- [ ] Comprobé qué gana entre `-p` y `--params-file`

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03](../ejercicio-03-accion_compartida/README.md) | **Ejercicio 04** | [Proyecto](../../3-proyecto/README.md) |

← [Volver a la Semana 03](../../README.md)
