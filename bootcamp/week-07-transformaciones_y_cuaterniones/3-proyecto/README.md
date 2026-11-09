# Proyecto — Semana 07

## Qué capa se añade esta semana

Tu robot ya sabe dónde está (`odom → base_link`) y dónde lleva su sensor
(`base_link → sensor_link`). Esta semana sabe **dónde tiene su objetivo**:

- **`targeting.py`**, sin ROS: el rumbo, la elevación y la distancia de un punto
  escrito en el marco del sensor, y si cae dentro de su campo de visión y su
  alcance
- **`target_locator`**, un nodo nuevo: el objetivo de tu misión (la estantería,
  la válvula, la planta) está quieto en un punto conocido de `odom`; cada 0.2 s
  lo escribe en el marco del sensor con tf2, lo publica y dice si está a la vista
- **`bringup.launch.py`** lo arranca junto con lo de la Semana 06

```
src/proyecto_dominio_py/
├── launch/bringup.launch.py            # + target_locator
├── proyecto_dominio_py/
│   ├── targeting.py                    # nuevo — TODO (Requisito 2)
│   └── target_locator.py               # nuevo — TODO (Requisito 3)
└── test/
    ├── test_targeting.py               # nuevo
    └── test_target_locator_launch.py   # nuevo: ida y vuelta odom ↔ sensor
```

`target_locator` es Python, como manda la política de la Fase 2: no corre a
frecuencia fija ni lo pide ningún framework en C++. La capa C++ no cambia.

## Por qué va aquí

Un objetivo escrito en `odom` no le dice nada al sensor: para saber si lo tiene
delante hay que escribirlo en su marco, y eso es encadenar e invertir
transformaciones (teoría 02). En la Semana 11 la visión buscará el objetivo en la
imagen solo cuando `target_locator` diga que está a la vista; en la Semana 16
Nav2 llevará el robot hasta él. Y como el punto pasa por tf2, si montas el sensor
inclinado (pitch hacia el suelo, yaw hacia un lado), el cálculo lo tiene en
cuenta sin tocar una línea.

## Requisitos verificables

1. `colcon build --symlink-install` compila los cuatro paquetes sin errores ni warnings
2. `bearing_and_range` en `targeting.py` devuelve rumbo, elevación y distancia:
   `test_targeting.py` pasa
3. `target_locator` escribe el objetivo en el marco del sensor con
   `self._buffer.transform`, lo publica y llama a `_report_visibility`:
   `test_target_locator_launch.py` pasa
4. El objetivo, el marco del sensor, su campo de visión y su alcance son los de
   tu misión (tabla de adaptación), justificados en tu README
5. `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
6. El README de tu repositorio responde las preguntas de los tres ejercicios

## Cómo verificarlo, paso a paso

Esta semana solo cambia `proyecto_dominio_py`. Cópialo encima del tuyo y vuelve
a aplicar tus renombrados de semanas anteriores:

```bash
cp -r <ruta-al-repo>/bootcamp/week-07-transformaciones_y_cuaterniones/3-proyecto/starter/proyecto_dominio_py src/
```

Los otros tres paquetes del starter solo cambian la versión (0.7.0) y traen una
solución genérica de los Requisitos 2 y 4 de la Semana 06 (ruedas y
`odom → base_link` en C++): **conserva los tuyos**, que tienen tu robot. Si no
terminaste aquellos requisitos, compara con los del starter.

`cp -r` no borra carpetas: tu bag de referencia sigue en
`src/proyecto_dominio_py/test/data/state_bag`. Compila y prueba:

```bash
colcon build --symlink-install
# Summary: 4 packages finished [...]
source install/setup.bash
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result --test-result-base build/proyecto_dominio_py --verbose
# - proyecto_dominio_py.test.test_target_locator_launch test_target_locator_launch
# - proyecto_dominio_py.test.test_targeting test_justo_delante
#     NotImplementedError: Requisito 2: bearing_and_range
# - proyecto_dominio_py.test.test_targeting test_a_la_izquierda_el_rumbo_es_positivo
# ...
# Summary: 37 tests, 0 errors, 5 failures, 0 skipped
```

Fallan los cuatro tests de `bearing_and_range` y el de `target_locator`: es lo
esperado. Los de `in_field_of_view` ya pasan, porque viene escrita.

**Requisito 2**: en `targeting.py`, sigue el `TODO (Requisito 2)`. Rumbo y
elevación salen con `math.atan2`, como el ángulo de un punto en la teoría 01; la
elevación compara `z` con la distancia en el plano, `math.hypot(x, y)`.

**Requisito 3**: en `target_locator.py`, sigue el `TODO (Requisito 3)` de
`_on_timer`. Es el `to_frame` del Ejercicio 03 más el `try`/`except` de su nodo:
si tf2 no puede, sal sin publicar.

El test del Requisito 3 no compara con números fijos: coge el punto que publicas
en el marco del sensor, lo devuelve a `odom` con la TF del mismo instante y
comprueba que sale el objetivo. Da igual en qué punto de la ruta esté el robot.

**Comprobado a mano**:

```bash
# Terminal 1
ros2 launch proyecto_dominio_py bringup.launch.py
# ...
# [target_locator-4] [INFO] [...] [target_locator]: objetivo fuera de vista: rumbo 11°, elevación 4°, 5.4 m
# [target_locator-4] [INFO] [...] [target_locator]: objetivo a la vista: rumbo 15°, elevación 6°, 3.9 m
# [target_locator-4] [INFO] [...] [target_locator]: objetivo fuera de vista: rumbo 39°, elevación 14°, 1.7 m
# [target_locator-4] [INFO] [...] [target_locator]: objetivo a la vista: rumbo -15°, elevación 6°, 3.9 m
```

El robot sale de `x = 0` hacia el objetivo, en `(6, 1, 0.5)`: a 5.4 m queda
fuera de alcance, a 3.9 m entra, y al acercarse se sale por el lado (39° es más
que la mitad de los 60° de campo). En la vuelta lo ve otra vez, ahora a su
derecha: rumbo negativo.

```bash
# Terminal 2
ros2 topic echo /dominio/target_in_sensor geometry_msgs/msg/PointStamped --once
# header:
#   stamp:
#     sec: 1794196042
#     nanosec: 429098181
#   frame_id: sensor_link
# point:
#   x: 2.25
#   y: 1.0
#   z: 0.4
# ---
ros2 topic echo /dominio/target_visible std_msgs/msg/Bool --once
# data: true
# ---
```

Tus números serán otros. En ese instante el robot estaba en `x = 3.5` mirando
hacia `+x`: el sensor, 0.25 m por delante y 0.1 m por encima del centro, tenía
el objetivo 2.25 m delante, 1 m a la izquierda y 0.4 m más alto.

Con todo hecho:

```bash
colcon build --symlink-install
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result
# Summary: 51 tests, 0 errors, 0 failures, 0 skipped
```

Son 37 de Python (los 28 de la Semana 06, 8 de `targeting` y 1 de
`target_locator`) y los 14 de C++ de siempre.

## Criterios de calidad

- `target_locator` no calcula a mano lo que tf2 sabe: ni matrices propias ni el
  yaw de la ruta, solo `buffer.transform`
- El objetivo, el campo de visión y el alcance son parámetros, no números
  enterrados en el código
- `targeting.py` no importa nada de ROS: se prueba sin arrancar nodos
- Los ángulos se guardan en radianes y se convierten a grados solo para el log

## Adaptación al dominio

Cambia `DEFAULT_TARGET_XYZ` y `SENSOR_FRAME` en `target_locator.py`, y los
valores por defecto de `h_fov_deg`, `v_fov_deg` y `max_range_m`. Pon el objetivo
cerca de la ruta de tu robot (`ROUTE_LENGTH_M` de la Semana 06) para que entre y
salga de la vista.

| Misión | Objetivo (`DEFAULT_TARGET_XYZ`) | Sensor (campo horizontal × vertical, alcance) |
|---|---|---|
| 📦 Almacén | La etiqueta de la caja a recoger, en la estantería: `[6.0, 1.0, 0.5]` | `camera_link`: 60° × 45°, 4 m |
| 🔬 Laboratorio | El portamuestras de la mesa de destino: `[4.0, 0.8, 0.9]` | `camera_link` en el mástil: 70° × 55°, 2 m |
| 🔦 Inspección industrial | El manómetro de la válvula: `[8.0, -1.5, 1.2]` | `thermal_camera_link`: 45° × 35°, 6 m |
| 🧹 Oficina | Un objeto caído, a la altura del láser: `[5.0, 0.5, 0.15]` | `laser_link`: 270° × 2° (un láser 2D solo ve su plano), 8 m |
| 🌾 Agrícola | La planta a tratar en el surco: `[7.0, 0.3, 0.2]` | `camera_link` inclinada hacia el surco: 60° × 45°, 3 m |
| 📚 Biblioteca | El lomo del libro buscado: `[3.0, 0.9, 1.1]` | `camera_link` lateral (yaw 90°): 60° × 45°, 1.5 m |

Escribe en tu README de dónde sacaste el campo de visión y el alcance (la hoja
de datos del sensor de tu robot de referencia) y en qué tramo de la ruta tu
robot ve el objetivo.

## Checklist

- [ ] `bearing_and_range` pasa sus tests y no importa nada de ROS
- [ ] `target_locator` publica el objetivo en el marco del sensor y la ida y
      vuelta devuelve el objetivo
- [ ] Vi en el log cómo el objetivo entra y sale de la vista
- [ ] Objetivo, sensor, campo de visión y alcance son los de mi misión
- [ ] `colcon test` pasa en los dos paquetes de nodos
- [ ] Respondí las preguntas de los tres ejercicios

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03](../2-practicas/ejercicio-03-transformar_puntos_tf2_py/README.md) | **Proyecto** | [Recursos](../4-recursos/README.md) |

← [Volver a la Semana 07](../README.md)
