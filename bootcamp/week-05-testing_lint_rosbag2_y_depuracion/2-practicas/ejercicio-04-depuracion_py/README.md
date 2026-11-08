# Ejercicio 04 — Depuración

`battery_sim` publica una batería que se descarga. `battery_watchdog` la escucha
y calcula cuánto tiempo le queda al robot. Arrancas los dos y... nada. Ningún
error, ningún mensaje. Hay tres fallos en `battery_watchdog.py`, uno detrás de
otro: cada uno esconde al siguiente. Los encuentras con el método de la teoría 05,
**antes** de mirar la corrección.

**Antes de empezar**: [teoría 05](../../1-teoria/05-depuracion-y-ros2-doctor.md)
leída.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-05-testing_lint_rosbag2_y_depuracion/2-practicas/ejercicio-04-depuracion_py/starter \
  src/ejercicio04_depuracion_py
```

Estructura:

```
src/ejercicio04_depuracion_py/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/ejercicio04_depuracion_py
├── ejercicio04_depuracion_py/
│   ├── __init__.py
│   ├── battery_sim.py                  # funciona: no lo toques
│   └── battery_watchdog.py             # PASOS 1, 2 y 3
└── test/
    └── test_watchdog_launch.py         # test de integración ya escrito
```

Verificación:

```bash
colcon build --packages-select ejercicio04_depuracion_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio04_depuracion_py
colcon test-result --verbose
# build/ejercicio04_depuracion_py/pytest.xml: 1 test, 0 errors, 1 failure, 0 skipped
```

El test arranca los dos nodos y espera hasta 15 s a que el watchdog escriba
`tiempo restante`; después comprueba que los dos terminan con código 0.

## Paso 0: El síntoma

En cada terminal, primero `source install/setup.bash`:

```bash
# Terminal 1
ros2 run ejercicio04_depuracion_py battery_sim
```

```bash
# Terminal 2
ros2 run ejercicio04_depuracion_py battery_watchdog
```

Espera diez segundos. La terminal 2 no escribe nada. Deja los dos nodos en
marcha y abre una tercera terminal para investigar.

## Paso 1: ¿Existe el topic y lo usan los dos?

```bash
# Terminal 3
ros2 topic list
# /parameter_events
# /robot/batery_percent
# /robot/battery_percent
# /rosout
ros2 node info /battery_watchdog
# /battery_watchdog
#   Subscribers:
#     /robot/batery_percent: std_msgs/msg/Float32
#   ...
```

`ros2 doctor` también lo avisa, aunque el resumen diga que todo pasó:

```bash
ros2 doctor
# .../ros2doctor/api/topic.py: 45: UserWarning: Subscriber without publisher detected on /robot/batery_percent.
# .../ros2doctor/api/topic.py: 42: UserWarning: Publisher without subscriber detected on /robot/battery_percent.
#
# All 5 checks passed
```

Puede salir antes otro aviso, `Cannot find the latest versions of packages`:
tus paquetes no están en los repositorios de ROS. Ignóralo.

**Corrige**: en `battery_watchdog.py`, descomenta el `TOPIC` del Paso 1 y borra
la línea marcada `# elimina en el Paso 1`. Cierra el watchdog (`Ctrl+C`), recompila
si no usaste `--symlink-install` y vuelve a arrancarlo.

✅ Verificación: `ros2 node info /battery_watchdog` muestra
`/robot/battery_percent` en `Subscribers`... y la terminal 2 sigue sin escribir
el tiempo restante.

## Paso 2: ¿Se conectan?

Mira **ahora sí** el arranque del watchdog en la terminal 2:

```text
[WARN] [...] [battery_watchdog]: New publisher discovered on topic 'robot/battery_percent', offering incompatible QoS. No messages will be received from it. Last incompatible policy: RELIABILITY
```

Confírmalo desde la terminal 3:

```bash
ros2 topic info -v /robot/battery_percent
# ...
# Node name: battery_sim
# Endpoint type: PUBLISHER
#   Reliability: BEST_EFFORT
# ...
# Node name: battery_watchdog
# Endpoint type: SUBSCRIPTION
#   Reliability: RELIABLE
# ...
ros2 doctor
# ...
# 1/5 check(s) failed
#
# Failed modules: middleware
```

`battery_sim` publica con el QoS de sensores (best effort, Semana 02); el
watchdog pide reliable. No hay entrega posible. Lo correcto es que el
suscriptor de un sensor use el mismo perfil.

**Corrige**: descomenta el `QOS` del Paso 2 y borra la línea marcada. Reinicia el
watchdog.

✅ Verificación: el aviso de QoS ya no sale... y el watchdog termina con un error.

## Paso 3: ¿El callback hace lo que crees?

```text
Traceback (most recent call last):
  ...
  File ".../ejercicio04_depuracion_py/battery_watchdog.py", line 46, in _on_battery
    first_s, first_percent = self._first
    ^^^^^^^^^^^^^^^^^^^^^^
TypeError: cannot unpack non-iterable NoneType object
[ros2run]: Process exited with failure 1
```

Lee el traceback de abajo arriba: `self._first` es `None` (aún no ha llegado
ninguna lectura) y el código lo desempaqueta igualmente. Los dos fallos
anteriores impedían llegar aquí: hasta ahora, el callback nunca se había
ejecutado.

**Corrige**: descomenta el bloque del Paso 3, que guarda la primera lectura y
sale. Arranca el watchdog con el log de depuración de ese nodo:

```bash
# Terminal 2
ros2 run ejercicio04_depuracion_py battery_watchdog --ros-args --log-level battery_watchdog:=debug
# [DEBUG] [...] [battery_watchdog]: lectura: 99.0 %
# [DEBUG] [...] [battery_watchdog]: lectura: 98.5 %
# [INFO] [...] [battery_watchdog]: batería 98.5 %, tiempo restante: 99 s
# [DEBUG] [...] [battery_watchdog]: lectura: 98.0 %
# [INFO] [...] [battery_watchdog]: batería 98.0 %, tiempo restante: 98 s
```

La batería baja 1 % por segundo, así que el tiempo restante coincide con el
porcentaje. Los valores exactos dependen de cuánto lleve `battery_sim` en marcha.
Sin `--log-level`, solo salen las líneas `INFO`.

✅ Verificación:

```bash
colcon test --packages-select ejercicio04_depuracion_py
colcon test-result --verbose
# build/ejercicio04_depuracion_py/pytest.xml: 1 test, 0 errors, 0 failures, 0 skipped
```

Si corriges solo los Pasos 1 y 2, el test también falla, y su test de cierre
dice por qué:

```text
AssertionError: Proc battery_watchdog-2 exited with code 1
```

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué el fallo del Paso 3 no aparecía hasta corregir los dos anteriores?
2. ¿Qué herramienta de la teoría 03 habría encontrado el fallo del Paso 3 sin
   ejecutar el nodo? Pruébala con el `mypy.ini` del Ejercicio 03.
3. Escribe, para tu misión, el orden de comandos que seguirías si tu
   `sensor_stub` dejara de llegar a otro nodo.

## Checklist

- [ ] Encontré cada fallo con una herramienta antes de mirar la corrección
- [ ] Vi el aviso de QoS incompatible en el log y en `ros2 doctor`
- [ ] Activé el nivel `DEBUG` solo para `battery_watchdog`
- [ ] El test de integración pasa

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03](../ejercicio-03-lint_y_analisis_estatico/README.md) | **Ejercicio 04** | [Proyecto](../../3-proyecto/README.md) |

← [Volver a la Semana 05](../../README.md)
