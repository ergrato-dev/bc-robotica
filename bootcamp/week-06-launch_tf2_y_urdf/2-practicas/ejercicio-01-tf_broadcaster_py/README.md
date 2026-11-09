# Ejercicio 01 — Broadcaster TF y launch file en Python (`rclpy`)

Un robot patrulla en círculo alrededor del origen de `odom`. Tú escribes la
geometría de su movimiento, el nodo que la publica en TF, el launch file que lo
arranca junto con su láser y el test que comprueba que todo el árbol está bien.

**Antes de empezar**: teorías [01](../../1-teoria/01-launch-files-en-python.md),
[03](../../1-teoria/03-tf2-marcos-y-transformaciones.md) y
[04](../../1-teoria/04-broadcasters-y-listeners.md) leídas.

## Preparar el workspace

Copia el starter dentro de `src/` de tu workspace (la carpeta que contiene `src/`):

```bash
cp -r <ruta-al-repo>/bootcamp/week-06-launch_tf2_y_urdf/2-practicas/ejercicio-01-tf_broadcaster_py/starter \
  src/ejercicio01_tf_broadcaster_py
```

Estructura:

```
src/ejercicio01_tf_broadcaster_py/
├── package.xml                         # rclpy, geometry_msgs, tf2_ros, launch_ros
├── setup.py                            # instala launch/ en share/
├── setup.cfg
├── resource/ejercicio01_tf_broadcaster_py
├── ejercicio01_tf_broadcaster_py/
│   ├── __init__.py
│   ├── geometry.py                     # PASO 1
│   └── patrol_broadcaster.py           # PASO 2
├── launch/
│   └── patrol.launch.py                # PASO 3
└── test/
    ├── test_geometry.py                # tests ya escritos del Paso 1
    └── test_patrol_launch.py           # PASO 4
```

Verificación, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio01_tf_broadcaster_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio01_tf_broadcaster_py
colcon test-result --verbose
# build/ejercicio01_tf_broadcaster_py/pytest.xml: 10 tests, 0 errors, 8 failures, 0 skipped
```

Fallan los ocho tests de `circle_pose`: esperan el Paso 1. Los dos del
cuaternión ya pasan: `yaw_to_quaternion` viene escrita (teoría 03, sección 3).

## Paso 1: La geometría, sin ROS

**Abre `ejercicio01_tf_broadcaster_py/geometry.py`**, descomenta el bloque del
Paso 1 en `circle_pose` y **borra la línea `raise NotImplementedError(...)`**
marcada con `# elimina en el Paso 1`.

**Por qué**: la pose del robot es pura matemática. Separada del nodo, se prueba en
milisegundos y sin arrancar nada, como el filtro de la Semana 05.

✅ Verificación:

```bash
colcon test --packages-select ejercicio01_tf_broadcaster_py
colcon test-result --verbose
# build/ejercicio01_tf_broadcaster_py/pytest.xml: 10 tests, 0 errors, 0 failures, 0 skipped
```

**¿El test detecta fallos?** Cambia `angle + math.pi / 2.0` por
`angle - math.pi / 2.0`: el robot seguiría el círculo, pero mirando hacia atrás.
Vuelve a probar: falla `test_empieza_en_el_eje_x_mirando_hacia_y`. Deshaz el cambio.

## Paso 2: El broadcaster

**Abre `ejercicio01_tf_broadcaster_py/patrol_broadcaster.py`** y descomenta los
tres bloques del Paso 2 (imports, `__init__` y `_on_timer`). **Borra la línea
`pass`** marcada con `# elimina en el Paso 2`.

**Por qué**: el nodo es la única pieza que sabe dónde está el robot. Lo publica
en `/tf` 20 veces por segundo y cualquier otro nodo puede preguntarlo.

✅ Verificación (en cada terminal, primero `source install/setup.bash`):

```bash
colcon build --packages-select ejercicio01_tf_broadcaster_py --symlink-install
# Terminal 1
ros2 run ejercicio01_tf_broadcaster_py patrol_broadcaster
```

```bash
# Terminal 2
ros2 run tf2_ros tf2_echo odom base_link
# [INFO] [...] [tf2_echo]: Waiting for transform odom ->  base_link: Invalid frame ID "odom" passed to canTransform argument target_frame - frame does not exist
# At time 1794192510.575654583
# - Translation: [-0.582, 1.383, 0.000]
# - Rotation: in Quaternion (xyzw) [0.000, 0.000, 0.980, -0.198]
# - Rotation: in RPY (radian) [0.000, -0.000, -2.743]
# - Rotation: in RPY (degree) [0.000, -0.000, -157.180]
# ...
```

Tus números serán otros (depende de cuándo arrancaste), pero cada segundo cambian
y `√(x² + y²)` es siempre 1.5, el radio por defecto. El yaw en grados avanza 18°
por segundo: una vuelta en 20 s. Cierra las dos terminales.

## Paso 3: El launch file

**Abre `launch/patrol.launch.py`**, descomenta los dos bloques del Paso 3 y
**borra la línea `return LaunchDescription([])`** marcada con
`# elimina en el Paso 3`.

El launch file arranca el broadcaster con el argumento `radius_m` y un
`static_transform_publisher` para el láser, montado 0.20 m por delante y 0.15 m
por encima del centro del robot.

**Por qué**: dos nodos, un argumento y una orden. Y la posición del láser, que no
cambia nunca, va a `/tf_static` una sola vez.

✅ Verificación:

```bash
colcon build --packages-select ejercicio01_tf_broadcaster_py --symlink-install
ros2 launch ejercicio01_tf_broadcaster_py patrol.launch.py --show-args
# Arguments (pass arguments as '<name>:=<value>'):
#
#     'radius_m':
#         Radio del círculo de la patrulla, en metros
#         (default: '1.5')
```

```bash
# Terminal 1
ros2 launch ejercicio01_tf_broadcaster_py patrol.launch.py radius_m:=2
# [INFO] [patrol_broadcaster-1]: process started with pid [57]
# [INFO] [static_transform_publisher-2]: process started with pid [58]
# [static_transform_publisher-2] [INFO] [...]: Spinning until stopped - publishing transform
# [static_transform_publisher-2] translation: ('0.200000', '0.000000', '0.150000')
# ...
```

```bash
# Terminal 2
ros2 run tf2_ros tf2_echo base_link laser_link
# At time 0.0
# - Translation: [0.200, 0.000, 0.150]
# - Rotation: in Quaternion (xyzw) [0.000, 0.000, 0.000, 1.000]
# ...
ros2 run tf2_tools view_frames
# [INFO] [...] [view_frames]: Exporting graph in frames_<fecha>.pdf file...
```

Abre el PDF: `odom → base_link → laser_link`. `At time 0.0` indica una estática.
Fíjate en que `radius_m:=2` (un entero) funciona: es el `ParameterValue` del
launch file. Cierra la terminal 1.

## Paso 4: Probar el launch file

**Abre `test/test_patrol_launch.py`** y descomenta el bloque del Paso 4. El test
incluye `patrol.launch.py` con `radius_m:=2.0`, escucha TF con un `Buffer` y
comprueba tres cosas: que el robot está a 2.0 m del origen, que el láser cuelga de
`base_link` donde debe y que la cadena `odom → laser_link` se mueve.

**Por qué**: el Paso 1 prueba la geometría; este, que el launch file arranca lo
que debe, que el argumento llega al nodo y que el árbol queda completo.

✅ Verificación:

```bash
colcon build --packages-select ejercicio01_tf_broadcaster_py --symlink-install
colcon test --packages-select ejercicio01_tf_broadcaster_py
colcon test-result --verbose
# build/ejercicio01_tf_broadcaster_py/pytest.xml: 11 tests, 0 errors, 0 failures, 0 skipped
```

**¿El test detecta fallos?** En `patrol.launch.py`, cambia
`parameters=[{"radius_m": radius_m}]` por `parameters=[]`: el argumento se declara
pero no llega al nodo, que se queda con 1.5. Vuelve a compilar y a probar:

```text
- ejercicio01_tf_broadcaster_py.test.test_patrol_launch test_patrol_launch
Summary: 11 tests, 0 errors, 1 failure, 0 skipped
```

`test_geometry.py` sigue en verde: la geometría está bien, el fallo está en el
cableado del launch file. Deshaz el cambio.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué el láser se publica en `/tf_static` y el robot en `/tf`? ¿Qué pasaría
   si publicaras el láser en `/tf` una sola vez al arrancar?
2. Sin `ParameterValue`, ¿con qué valor de `radius_m` falla el nodo y por qué?
3. En tu misión, ¿qué sensor va fijo al chasis y a qué distancia del centro?

## Checklist

- [ ] Los 11 tests del paquete pasan
- [ ] Vi la pose del robot con `tf2_echo` y el árbol en el PDF de `view_frames`
- [ ] Lancé con `radius_m:=2` y entiendo por qué no falla
- [ ] Rompí la geometría y el Paso 1 lo detectó; rompí el launch file y lo detectó el Paso 4

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Prácticas](../README.md) | **Ejercicio 01** | [Ejercicio 02](../ejercicio-02-tf_listener_cpp/README.md) |

← [Volver a la Semana 06](../../README.md)
