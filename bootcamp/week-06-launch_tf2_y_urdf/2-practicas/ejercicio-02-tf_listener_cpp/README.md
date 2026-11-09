# Ejercicio 02 — Listener TF y composición de launch en C++ (`rclcpp`)

El robot del Ejercicio 01 sigue patrullando. Ahora hay un **dock** (la estación
de carga) fijo en el suelo, a 3 m del origen de `odom`. Un nodo C++ pregunta a TF
dónde está el dock visto desde el robot y publica la distancia. El launch file de
este paquete incluye el del Ejercicio 01: un sistema con nodos Python y C++
arrancado con una sola orden. Al final, el checklist de paridad cierra la Fase 1.

**Antes de empezar**: Ejercicio 01 terminado (este paquete lo necesita en el mismo
workspace) y teorías [02](../../1-teoria/02-composicion-de-launch-y-lifecycle.md)
y [04](../../1-teoria/04-broadcasters-y-listeners.md) leídas.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-06-launch_tf2_y_urdf/2-practicas/ejercicio-02-tf_listener_cpp/starter \
  src/ejercicio02_tf_listener_cpp
```

Estructura:

```
src/ejercicio02_tf_listener_cpp/
├── package.xml                         # tf2_ros + exec_depend del Ejercicio 01
├── CMakeLists.txt                      # biblioteca, ejecutable, launch/ y dos gtest
├── include/ejercicio02_tf_listener_cpp/
│   └── dock_geometry.hpp               # DockReading y dock_reading()
├── src/
│   ├── dock_geometry.cpp               # PASO 1
│   └── dock_monitor.cpp                # PASO 2
├── launch/
│   └── dock.launch.py                  # PASO 3
└── test/
    ├── test_dock_geometry.cpp          # tests ya escritos del Paso 1
    └── test_tf_buffer.cpp              # tf2::BufferCore sin red (teoría 04, sección 5)
```

Verificación, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio02_tf_listener_cpp --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio02_tf_listener_cpp
colcon test-result --test-result-base build/ejercicio02_tf_listener_cpp --verbose | grep tests,
# build/ejercicio02_tf_listener_cpp/test_results/ejercicio02_tf_listener_cpp/test_dock_geometry.gtest.xml: 4 tests, 0 errors, 4 failures, 0 skipped
# build/ejercicio02_tf_listener_cpp/test_results/ejercicio02_tf_listener_cpp/test_tf_buffer.gtest.xml: 3 tests, 0 errors, 2 failures, 0 skipped
```

`--test-result-base` limita el resumen a este paquete (si no, suma también los del
Ejercicio 01). De `test_tf_buffer` ya pasa `SinCadenaLanzaExcepcion`: no depende
de tu código.

## Paso 1: Distancia y rumbo

**Abre `src/dock_geometry.cpp`**, descomenta el bloque del Paso 1 y **borra las
dos líneas** marcadas con `// elimina en el Paso 1`.

**Por qué**: `dock_reading` recibe la transformación ya expresada en el marco del
robot, así que la cuenta es sencilla: la distancia es `hypot(x, y)` y el rumbo,
`atan2(y, x)`: 0 delante, positivo a la izquierda (REP 103).

✅ Verificación:

```bash
colcon build --packages-select ejercicio02_tf_listener_cpp --symlink-install
colcon test --packages-select ejercicio02_tf_listener_cpp
colcon test-result --test-result-base build/ejercicio02_tf_listener_cpp
# Summary: 9 tests, 0 errors, 0 failures, 0 skipped
```

Son 7 tests de gtest más los 2 resultados que CTest anota por ejecutable.

Lee ahora `test/test_tf_buffer.cpp`. `RobotGiradoNoventaGradosTieneElDockALaDerecha`
mete en un `tf2::BufferCore` el dock a 3 m en el eje x de `odom` y el robot en
`(1, 0)` mirando hacia +y. En `odom`, el dock está "delante" en x; desde el robot,
a 2 m **a su derecha**. El buffer compone `base_link → odom → dock` y
`dock_reading` da −90°.

**¿El test detecta fallos?** Cambia `std::atan2(y, x)` por `std::atan2(x, y)`.
Compila y prueba: fallan cinco tests, en los dos archivos (solo
`LaAlturaNoCuenta` sigue en verde: no mira el rumbo). Deshaz el cambio.

## Paso 2: El listener

**Abre `src/dock_monitor.cpp`** y descomenta los dos bloques del Paso 2 (el del
constructor y el de `on_timer`).

**Por qué**: el `Buffer` y el `TransformListener` se crean una vez, en el
constructor; el timer solo consulta. En el arranque, antes de que llegue el primer
mensaje de `/tf`, la consulta falla: el nodo avisa con `THROTTLE` y sigue.

✅ Verificación (en cada terminal, primero `source install/setup.bash`):

```bash
colcon build --packages-select ejercicio02_tf_listener_cpp --symlink-install
# Terminal 1: el monitor, solo
ros2 run ejercicio02_tf_listener_cpp dock_monitor
# [WARN] [...] [dock_monitor]: Sin TF base_link -> dock: "base_link" passed to lookupTransform argument target_frame does not exist.
```

Nadie publica TF todavía: el aviso se repite cada 2 s. Arranca la patrulla y el dock:

```bash
# Terminal 2
ros2 launch ejercicio01_tf_broadcaster_py patrol.launch.py
```

```bash
# Terminal 3
ros2 run tf2_ros static_transform_publisher --x 3.0 --frame-id odom --child-frame-id dock
```

En la terminal 1 los avisos paran y aparece:

```text
[INFO] [...] [dock_monitor]: Dock a 1.50 m, rumbo -94 grados
[INFO] [...] [dock_monitor]: Dock a 2.04 m, rumbo -155 grados
[INFO] [...] [dock_monitor]: Dock a 3.01 m, rumbo +165 grados
```

La distancia oscila entre 1.5 m (el robot pasa junto al dock) y 4.5 m (en el lado
opuesto del círculo). Cierra las tres terminales.

**Experimento**: invierte la consulta, `lookupTransform(dock_frame_, "base_link", ...)`.
La distancia sale igual, pero el rumbo ya no: ahora es dónde está el robot visto
desde el dock. Ningún test de este paquete lo detecta porque `dock_reading` es
correcta: el error está en la pregunta. Deshaz el cambio.

## Paso 3: Un launch file que incluye otro

**Abre `launch/dock.launch.py`**, descomenta los dos bloques del Paso 3 y **borra
la línea `return LaunchDescription([])`** marcada con `# elimina en el Paso 3`.

**Por qué**: el launch de este paquete no copia los nodos de la patrulla: incluye
`patrol.launch.py` con `FindPackageShare` y le reenvía `radius_m`. Si mañana la
patrulla gana un nodo, este launch lo arranca sin tocarlo.

✅ Verificación:

```bash
colcon build --packages-select ejercicio02_tf_listener_cpp --symlink-install
ros2 launch ejercicio02_tf_listener_cpp dock.launch.py
# [INFO] [patrol_broadcaster-1]: process started with pid [38]
# [INFO] [static_transform_publisher-2]: process started with pid [39]
# [INFO] [static_transform_publisher-3]: process started with pid [40]
# [INFO] [dock_monitor-4]: process started with pid [41]
# ...
# [dock_monitor-4] [WARN] [...] [dock_monitor]: Sin TF base_link -> dock: "base_link" passed to lookupTransform argument target_frame does not exist.
# [dock_monitor-4] [INFO] [...] [dock_monitor]: Dock a 1.50 m, rumbo -94 grados
```

Cuatro procesos, dos lenguajes, una orden. El aviso inicial es normal: el monitor
arrancó una décima antes que el primer mensaje de `/tf`. En otra terminal:

```bash
ros2 run tf2_tools view_frames
```

El PDF muestra `odom` con dos hijos (`base_link` y `dock`) y `laser_link` bajo
`base_link`. Prueba también `radius_m:=0.5`: el robot pasa a 2.5 m del dock como
mínimo.

## Paso 4: Checklist de paridad (cierre de la Fase 1)

La Fase 1 enseña cada concepto de comunicación en los dos lenguajes. Antes de la
Semana 07, donde Python pasa a ser el lenguaje por defecto, comprueba que sabes
escribir cada fila en los dos. Copia esta tabla en el README de tu proyecto y
marca cada celda con el archivo donde lo hiciste:

| Concepto | Semana | `rclpy` | `rclcpp` |
|---|---|---|---|
| Nodo y `spin` | 01 | `rclpy.node.Node`, `rclpy.spin` | `rclcpp::Node`, `rclcpp::spin` |
| Publisher y subscriber | 01 | `create_publisher`, `create_subscription` | `create_publisher<T>`, `create_subscription<T>` |
| Perfil QoS | 02 | `rclpy.qos.QoSProfile` | `rclcpp::QoS` |
| Interfaz propia (`.msg`/`.srv`) | 02 | `from <pkg>.msg import T` | `#include "<pkg>/msg/t.hpp"` |
| Servicio: servidor y cliente | 03 | `create_service`, `create_client` + `call_async` | `create_service<T>`, `create_client<T>` + `async_send_request` |
| Acción: servidor y cliente | 03 | `rclpy.action.ActionServer`, `ActionClient` | `rclcpp_action::create_server`, `create_client` |
| Parámetros con descriptor y callback | 03 | `declare_parameter`, `add_post_set_parameters_callback` | `declare_parameter<T>`, `add_post_set_parameters_callback` |
| Executor y callback groups | 04 | `MultiThreadedExecutor`, `MutuallyExclusiveCallbackGroup` | `rclcpp::executors::MultiThreadedExecutor`, `create_callback_group` |
| Componente en un container | 04 | (no existe en `rclpy`) | `RCLCPP_COMPONENTS_REGISTER_NODE` |
| Nodo lifecycle | 04 | `rclpy.lifecycle.Node` | `rclcpp_lifecycle::LifecycleNode` |
| Test unitario | 05 | `pytest` | `gtest` (`ament_add_gtest`) |
| Lint y análisis estático | 05 | `ruff`, `mypy` | `clang-format`, `clang-tidy` |
| Leer una bag | 05 | `rosbag2_py.SequentialReader` | `rosbag2_cpp::Reader` |
| Broadcaster TF | 06 | `tf2_ros.TransformBroadcaster` | `tf2_ros::TransformBroadcaster` |
| Listener TF | 06 | `tf2_ros.Buffer` + `TransformListener` | `tf2_ros::Buffer` + `TransformListener` |

Launch files y tests de integración (`launch_testing`) se escriben siempre en
Python, sea cual sea el lenguaje de los nodos que arrancan. Si una celda te cuesta,
vuelve al ejercicio de esa semana antes de seguir: a partir de la Semana 10 el C++
vuelve para escribir plugins, y da por sabida esta tabla.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. En el experimento del Paso 2, ¿por qué la distancia no cambió al invertir la
   consulta y el rumbo sí?
2. ¿Qué ventaja tiene incluir `patrol.launch.py` frente a copiar sus dos nodos en
   `dock.launch.py`? ¿Qué dependencia añadiste en `package.xml` por ello?
3. ¿Qué fila del checklist de paridad te costó más en C++ y qué harías para
   repasarla?

## Checklist

- [ ] Los 9 resultados de `colcon test-result` del paquete pasan
- [ ] Vi el aviso de arranque del monitor y cómo desaparece al llegar TF
- [ ] `dock.launch.py` arranca los cuatro procesos y `view_frames` muestra el árbol
- [ ] Rellené el checklist de paridad en el README de mi proyecto

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01](../ejercicio-01-tf_broadcaster_py/README.md) | **Ejercicio 02** | [Ejercicio 03](../ejercicio-03-urdf_y_xacro/README.md) |

← [Volver a la Semana 06](../../README.md)
