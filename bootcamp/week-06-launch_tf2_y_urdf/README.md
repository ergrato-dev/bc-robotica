# Semana 06 — Launch files, TF2 y URDF

> Tu robot ya habla, se prueba y se graba. Le falta un cuerpo y un sitio en el mundo: un modelo que diga dónde va cada pieza, un árbol de marcos que diga dónde está cada cosa en cada instante, y un launch file que lo arranque todo con una orden. Con esta semana se cierra la Fase 1.

## 🎯 Objetivos de la Semana

- Arrancar sistemas enteros con launch files en Python: argumentos, parámetros, inclusiones y condiciones
- Llevar un nodo lifecycle hasta `active` desde launch, con eventos
- Razonar sobre marcos de referencia y el árbol TF, con las convenciones de REP 103 y REP 105
- Publicar transformaciones con un *broadcaster* en Python y consultarlas con un *listener* en C++
- Describir un robot en URDF/xacro, validarlo con `check_urdf` y publicarlo con `robot_state_publisher`
- Comprobar con el checklist de paridad que dominas cada concepto de la Fase 1 en `rclpy` y `rclcpp`

## 📋 Prerrequisitos

- [Semana 05](../week-05-testing_lint_rosbag2_y_depuracion/README.md) completada:
  tests, lint y bags
- Tu proyecto del dominio de la Semana 05 pasando `colcon test`, con su bag de referencia

## 🗂️ Estructura de la Semana

```
week-06-launch_tf2_y_urdf/
├── README.md                       (este archivo)
├── rubrica-evaluacion.md
├── 0-assets/
│   ├── 01-anatomia-de-un-launch.svg
│   ├── 02-eventos-lifecycle-en-launch.svg
│   ├── 03-arbol-tf.svg
│   ├── 04-broadcaster-buffer-listener.svg
│   └── 05-urdf-links-y-joints.svg
├── 1-teoria/
│   ├── 01-launch-files-en-python.md
│   ├── 02-composicion-de-launch-y-lifecycle.md
│   ├── 03-tf2-marcos-y-transformaciones.md
│   ├── 04-broadcasters-y-listeners.md
│   └── 05-urdf-y-xacro.md
├── 2-practicas/
│   ├── ejercicio-01-tf_broadcaster_py/
│   ├── ejercicio-02-tf_listener_cpp/
│   └── ejercicio-03-urdf_y_xacro/
├── 3-proyecto/
│   └── starter/ (proyecto_dominio_interfaces/, proyecto_dominio_description/,
│                 proyecto_dominio_py/, proyecto_dominio_cpp/)
├── 4-recursos/
└── 5-glosario/
```

## 📝 Contenidos

### Teoría (3.5 h)

| Archivo | Tema |
|---|---|
| [`01-launch-files-en-python.md`](1-teoria/01-launch-files-en-python.md) | `ros2 launch`, `Node`, parámetros y YAML, argumentos, `ParameterValue`, instalación |
| [`02-composicion-de-launch-y-lifecycle.md`](1-teoria/02-composicion-de-launch-y-lifecycle.md) | `IncludeLaunchDescription`, grupos, condiciones, `choices`, lifecycle con eventos |
| [`03-tf2-marcos-y-transformaciones.md`](1-teoria/03-tf2-marcos-y-transformaciones.md) | Marcos, árbol TF, `/tf` y `/tf_static`, REP 103/105, cuaternión de un yaw, herramientas |
| [`04-broadcasters-y-listeners.md`](1-teoria/04-broadcasters-y-listeners.md) | Broadcaster y listener en `rclpy` y `rclcpp`, `lookupTransform`, excepciones, buffer sin red |
| [`05-urdf-y-xacro.md`](1-teoria/05-urdf-y-xacro.md) | Links, joints, inercia, xacro, `check_urdf`, `robot_state_publisher` |

### Prácticas (5.5 h)

| Ejercicio | Lenguaje | Qué construye |
|---|---|---|
| 01 | `rclpy` | Broadcaster TF de un robot que patrulla, launch file con argumento y TF estática, test de launch |
| 02 | `rclcpp` | Listener TF que mide la distancia al dock, launch que incluye el del 01, checklist de paridad |
| 03 | URDF/xacro | Modelo de un rover con macros, validado y publicado con `robot_state_publisher` |

### Proyecto (2.5 h)

Tu robot gana un modelo URDF propio, publica `odom → base_link` desde las dos
capas de `sensor_stub` y arranca entero, ya en `active`, con `bringup.launch.py`.
Ver [3-proyecto/README.md](3-proyecto/README.md).

## ⏱️ Distribución del Tiempo (12 horas)

| Actividad | Horas |
|---|---|
| Teoría (01-05) | 3.5 |
| Ejercicio 01 (broadcaster y launch en Python) | 2.0 |
| Ejercicio 02 (listener en C++, composición de launch y paridad) | 2.0 |
| Ejercicio 03 (URDF y xacro) | 1.5 |
| Proyecto | 2.5 |
| Autoevaluación (rúbrica) | 0.5 |
| **Total** | **12.0** |

## 🎩 Trucos y atajos

- `ros2 launch <paquete> <archivo> --show-args` — los argumentos de un launch file y sus valores por defecto
- `ros2 run tf2_ros tf2_echo <padre> <hijo>` — la transformación entre dos marcos, cada segundo
- `ros2 run tf2_tools view_frames` — el árbol TF completo en un PDF
- `xacro modelo.urdf.xacro | check_urdf /dev/stdin` — expande y valida el modelo en una línea
- `ros2 lifecycle get /<nodo>` — confirma que el bringup llevó tu nodo hasta `active`
- `ros2 topic echo /tf_static --once` — las transformaciones fijas tal cual se publicaron

## 📌 Entregables

- Los tres ejercicios de `2-practicas/` con sus tests pasando y sus checklists completos
- `3-proyecto/` con el modelo de tu robot, `odom → base_link` en las dos capas y
  `bringup.launch.py` pasando en `colcon test`
- Respuestas de los tres ejercicios y el checklist de paridad en el README de tu proyecto

## ✅ Verificación

Desde la raíz de tu workspace (la carpeta que contiene `src/`):

```bash
colcon build --symlink-install
source install/setup.bash
colcon test
colcon test-result --verbose
```

Esta semana no hay simulación: `scripts/verificar-simulaciones.sh week-06` no
encuentra mundos de Gazebo y termina sin error. Gazebo llega en la Semana 08 y
cargará el URDF de tu proyecto.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 05](../week-05-testing_lint_rosbag2_y_depuracion/README.md) | **Semana 06** | Semana 07 (pendiente de publicar) |

← [Volver al inicio del bootcamp](../../README.md)
