# Ejercicio 01 — Callback groups en Python (`rclpy`)

El nodo `monitor` tiene un timer que cuenta ticks a 10 Hz y un servicio,
`robot/slow_check` (`std_srvs/srv/Trigger`), que tarda 0.5 s y responde cuántos
ticks dio el timer mientras él trabajaba. Empiezas con 0 ticks y terminas con
unos 5.

**Antes de empezar**: teorías [01](../../1-teoria/01-executors-y-spin.md) y
[02](../../1-teoria/02-callback-groups.md) leídas.

## Preparar el workspace

Copia el starter dentro de `src/` de tu workspace (la carpeta que contiene `src/`):

```bash
cp -r <ruta-al-repo>/bootcamp/week-04-executors_composicion_y_lifecycle/2-practicas/ejercicio-01-callback_groups_py/starter \
  src/ejercicio01_callback_groups_py
```

Estructura:

```
src/ejercicio01_callback_groups_py/
├── package.xml                         # depende de rclpy y std_srvs
├── setup.py
├── setup.cfg
├── resource/ejercicio01_callback_groups_py
├── ejercicio01_callback_groups_py/
│   ├── __init__.py
│   └── monitor.py                      # PASOS 1 y 2
└── test/
    └── test_monitor.py                 # tests ya escritos
```

Verificación, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio01_callback_groups_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio01_callback_groups_py
colcon test-result --verbose
```

Antes del primer paso, los dos tests fallan. Es lo esperado.

## Paso 0: Ver el problema

Sin tocar nada, arranca el nodo y llama al servicio (en cada terminal, primero
`source install/setup.bash`):

```bash
# Terminal 1
ros2 run ejercicio01_callback_groups_py monitor
```

```bash
# Terminal 2
ros2 service call /robot/slow_check std_srvs/srv/Trigger
# ...
# response:
# std_srvs.srv.Trigger_Response(success=True, message='ticks durante la comprobación: 0')
```

Medio segundo sin un solo tick. Cierra el nodo con `Ctrl+C`.

## Paso 1: Un grupo para cada callback

**Abre `ejercicio01_callback_groups_py/monitor.py`** y descomenta el bloque del
Paso 1: crea dos `MutuallyExclusiveCallbackGroup`. Las líneas que crean el timer
y el servicio ya pasan `callback_group=self.timer_group` y
`callback_group=self.service_group`; hasta ahora valían `None`, es decir, el
grupo por defecto.

**Por qué**: con el grupo por defecto, timer y servicio comparten fila. Con un
grupo cada uno, un executor multihilo puede correrlos a la vez.

**Verifica**: pasan `test_usa_grupos_propios` y
`test_timer_sigue_durante_la_comprobacion`. El segundo test crea su propio
`MultiThreadedExecutor`; por eso pasa aunque tu `main` todavía no lo use.

Repite el Paso 0: **sigue saliendo 0**. El `main` usa un executor de un solo
hilo, y con un hilo los grupos no cambian nada (teoría 02, sección 3.3).

## Paso 2: Executor multihilo

**Descomenta el bloque del Paso 2** en `main()` y **borra la línea
`executor = rclpy.executors.SingleThreadedExecutor()`** marcada con
`# elimina en el Paso 2`.

✅ Verificación: repite el Paso 0.

```text
std_srvs.srv.Trigger_Response(success=True, message='ticks durante la comprobación: 5')
```

En la terminal 1 aparece el mismo mensaje en el log del nodo. 4 o 6 también es
correcto: depende de en qué momento del ciclo del timer llega la request.

## Paso 3: Experimento con `Reentrant`

Cambia los dos grupos por **uno solo** compartido:

```python
shared = ReentrantCallbackGroup()  # from rclpy.callback_groups import ReentrantCallbackGroup
self.timer_group = shared
self.service_group = shared
```

Recompila, arranca el nodo y lanza **dos** llamadas casi a la vez:

```bash
ros2 service call /robot/slow_check std_srvs/srv/Trigger & \
ros2 service call /robot/slow_check std_srvs/srv/Trigger
```

Observa en la terminal 1 que los dos logs salen casi juntos: las dos llamadas se
atendieron en paralelo. Con dos `MutuallyExclusive` separados, la segunda
habría esperado a la primera. Deja después los dos grupos como en el Paso 1
(`test_usa_grupos_propios` exige grupos distintos).

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué el Paso 1 hace pasar el test pero no cambia la salida de la CLI?
2. En el Paso 3, ¿qué podría salir mal si `_on_slow_check` guardara el resultado
   en una variable compartida, como `self.last_result`?
3. Un nodo de tu misión tiene un callback que tarda 2 s en procesar una imagen y
   un timer de seguridad a 20 Hz. ¿Qué executor y qué grupos le pondrías?

## Checklist

- [ ] Los dos tests de `test/test_monitor.py` pasan
- [ ] Vi 0 ticks antes de los pasos y unos 5 después del Paso 2
- [ ] Hice el experimento del Paso 3 y dejé los grupos como en el Paso 1

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Prácticas](../README.md) | **Ejercicio 01** | [Ejercicio 02](../ejercicio-02-componente_cpp/README.md) |

← [Volver a la Semana 04](../../README.md)
