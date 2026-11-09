# Ejercicio 03 — Llevar detecciones del láser a `odom` con tf2

Un detector publica lo que ve escrito en el marco de su sensor. Para usar esa
posición (ir hacia ella, recordarla, compararla con otra detección) hace falta
escrita en un marco que no se mueva con el robot. Aquí escribes el nodo que hace
esa conversión con tf2, su launch file y el escenario de los ejercicios
anteriores: el resultado tiene que ser otra vez `(2, 1.2)`.

**Antes de empezar**: teoría [05](../../1-teoria/05-tf-transformations-y-tf2.md)
leída. Repasa el listener de la Semana 06 (teoría 04 de aquella semana).

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-07-transformaciones_y_cuaterniones/2-practicas/ejercicio-03-transformar_puntos_tf2_py/starter \
  src/ejercicio03_point_transform_py
```

Estructura:

```
src/ejercicio03_point_transform_py/
├── package.xml                         # rclpy, tf2_ros, tf2_geometry_msgs, launch_ros
├── setup.py                            # instala launch/ y el ejecutable detection_relay
├── setup.cfg
├── resource/ejercicio03_point_transform_py
├── ejercicio03_point_transform_py/
│   ├── __init__.py
│   └── detection_relay.py              # PASOS 1 y 2
├── launch/
│   └── relay.launch.py                 # PASO 3
└── test/
    ├── test_to_frame.py                # tests ya escritos del Paso 1
    └── test_relay_launch.py            # test ya escrito de los Pasos 2 y 3
```

Verificación, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio03_point_transform_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio03_point_transform_py
colcon test-result --test-result-base build/ejercicio03_point_transform_py
# Summary: 4 tests, 0 errors, 4 failures, 0 skipped
```

Son tres tests de `to_frame` y uno de launch (`colcon` cuenta el archivo de
launch_testing entero como un test).

## Paso 1: Transformar un punto

**Abre `ejercicio03_point_transform_py/detection_relay.py`**. Descomenta el
bloque del Paso 1 en `to_frame` y borra su línea `# elimina en el Paso 1`.

**Por qué**: `buffer.transform` hace en una llamada lo que en el Ejercicio 01
eran dos: buscar `T_target_source` en el árbol y aplicarla al punto. Lee el
marco de origen del `header.frame_id` del punto y el instante de su
`header.stamp`. Fíjate en el `import tf2_geometry_msgs` del principio: no se usa
por nombre, pero sin él `buffer.transform` no sabe qué es un `PointStamped`
(teoría 05, sección 5).

✅ Verificación:

```bash
colcon test --packages-select ejercicio03_point_transform_py
colcon test-result --test-result-base build/ejercicio03_point_transform_py
# Summary: 4 tests, 0 errors, 1 failure, 0 skipped
```

Los tres tests de `test_to_frame.py` usan un `tf2_ros.Buffer` sin red, como el
Paso 4 del Ejercicio 01. `test_un_marco_desconocido_lanza_lookup_exception`
comprueba que un `frame_id` que no existe lanza `LookupException`: el nodo del
Paso 2 tiene que estar preparado.

## Paso 2: El nodo

En el mismo archivo, descomenta los dos bloques del Paso 2 (en `__init__` y en
`_on_detection`) y borra la línea `pass  # elimina en el Paso 2`.

**Por qué**: el `TransformListener` llena el buffer con `/tf` y `/tf_static`
(Semana 06). Cada `PointStamped` que llega a `laser/detection` sale por
`detection` escrito en `target_frame`. Si tf2 no puede (al arrancar aún no han
llegado las transformaciones, o el `frame_id` está mal escrito), el nodo avisa y
descarta esa detección en vez de caerse: la siguiente puede salir bien.

✅ Verificación: el test de launch sigue fallando hasta el Paso 3, porque el
launch file aún no arranca nada. Comprueba que el paquete sigue limpio:

```bash
colcon build --packages-select ejercicio03_point_transform_py --symlink-install
# Summary: 1 package finished [...]
```

## Paso 3: El escenario en un launch file

**Abre `launch/relay.launch.py`**, descomenta los dos bloques del Paso 3 y
**borra la línea `return LaunchDescription([])`** marcada con
`# elimina en el Paso 3`.

**Por qué**: dos `static_transform_publisher` montan el árbol de los ejercicios
anteriores (`odom → base_link` con el robot en `(2, 0)` y yaw de 90°, y
`base_link → laser_link` a 0.20 m) y el argumento `target_frame` pasa al
parámetro del relé. El robot está quieto, así que aquí basta una transformación
estática; en tu proyecto `odom → base_link` la publica `sensor_stub` en `/tf`.

✅ Verificación:

```bash
colcon test --packages-select ejercicio03_point_transform_py
colcon test-result --test-result-base build/ejercicio03_point_transform_py
# Summary: 4 tests, 0 errors, 0 failures, 0 skipped
```

Pruébalo a mano:

```bash
# Terminal 1
ros2 launch ejercicio03_point_transform_py relay.launch.py
# [INFO] [static_transform_publisher-1]: process started with pid [53]
# [INFO] [static_transform_publisher-2]: process started with pid [54]
# [INFO] [detection_relay-3]: process started with pid [55]
# ...
```

```bash
# Terminal 2
ros2 topic echo /detection geometry_msgs/msg/PointStamped --once
```

```bash
# Terminal 3
ros2 topic pub --times 3 laser/detection geometry_msgs/msg/PointStamped \
  '{header: {frame_id: laser_link}, point: {x: 1.0}}'
```

En la terminal 2:

```text
header:
  stamp:
    sec: 0
    nanosec: 0
  frame_id: odom
point:
  x: 2.0
  y: 1.2
  z: 0.0
---
```

El mismo `(2, 1.2)` del Ejercicio 01, ahora calculado por un nodo con los datos
de `/tf_static`. Publica una detección con un marco que no existe:

```bash
ros2 topic pub --once laser/detection geometry_msgs/msg/PointStamped \
  '{header: {frame_id: camera_link}, point: {x: 1.0}}'
```

La terminal 1 muestra el aviso y el nodo sigue vivo:

```text
[detection_relay-3] [WARN] [...] [detection_relay]: no puedo llevar camera_link a odom: "camera_link" passed to lookupTransform argument source_frame does not exist.
```

Relanza con `target_frame:=base_link` y la misma detección sale en
`(1.2, 0, 0)`: 1 m delante del láser es 1.20 m delante del centro del robot.
`ros2 launch ejercicio03_point_transform_py relay.launch.py --show-args` enseña
el argumento:

```text
Arguments (pass arguments as '<name>:=<value>'):

    'target_frame':
        Marco en el que se publican las detecciones
        (default: 'odom')
```

**¿El test detecta fallos?** Quita `laser_tf` de la lista que devuelve el launch
file. Sin `base_link → laser_link`, el árbol no llega al láser:

```bash
colcon test --packages-select ejercicio03_point_transform_py
colcon test-result --test-result-base build/ejercicio03_point_transform_py --verbose
# - ejercicio03_point_transform_py.test.test_relay_launch test_relay_launch
# Summary: 4 tests, 0 errors, 1 failure, 0 skipped
```

En `log/latest_test/ejercicio03_point_transform_py/stdout_stderr.log` verás el
aviso del relé con `"laser_link" passed to lookupTransform argument source_frame
does not exist`. Deshaz el cambio.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Qué pasaría si el nodo no capturase `LookupException`? ¿Y si la capturase
   con `except Exception`?
2. El punto que publicas lleva `stamp` 0. ¿Qué instante de TF usa
   `buffer.transform`, y qué cambiaría si el robot se moviera y el detector
   pusiera el instante real de la medida?
3. ¿Qué detecciones de tu misión necesitarías en `odom` y cuáles te basta tener
   en el marco del sensor?

## Checklist

- [ ] Los 4 tests del paquete pasan
- [ ] Vi la misma detección en `odom` y en `base_link` cambiando un argumento
- [ ] Vi el aviso de un marco inexistente sin que el nodo se cayera
- [ ] Rompí el launch file y el test lo detectó

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02](../ejercicio-02-euler_y_cuaterniones_py/README.md) | **Ejercicio 03** | [Proyecto](../../3-proyecto/README.md) |

← [Volver a la Semana 07](../../README.md)
