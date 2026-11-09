# 📖 Glosario — Semana 06

Términos A-Z. El término/API en inglés va entre paréntesis cuando existe en la
documentación oficial.

- **Acción de launch (launch action)**: cada paso de un launch file: declarar un
  argumento, arrancar un nodo, incluir otro launch file. No tiene que ver con las
  acciones de comunicación de la Semana 03.
- **Argumento de launch (launch argument)**: valor que se elige al lanzar
  (`radius_m:=2.0`). Se declara con `DeclareLaunchArgument` y se lee con
  `LaunchConfiguration`.
- **Árbol TF (TF tree)**: el conjunto de marcos unidos por transformaciones, donde
  cada marco tiene un solo padre y no hay ciclos.
- **`base_link`**: marco del cuerpo del robot (REP 105). Es el link raíz del URDF.
- **Bringup (bringup)**: el launch file que arranca el robot entero incluyendo los
  de cada subsistema.
- **Broadcaster (broadcaster)**: objeto que publica transformaciones en `/tf`
  (`TransformBroadcaster`) o en `/tf_static` (`StaticTransformBroadcaster`).
- **Buffer de TF (tf2 buffer)**: almacén con los últimos segundos (10 por defecto)
  de cada transformación, al que se le preguntan las transformaciones compuestas.
- **Condición (condition)**: campo de una acción de launch que decide si se
  ejecuta, como `IfCondition(EqualsSubstitution(...))`.
- **Cuaternión (quaternion)**: cuatro números `(x, y, z, w)` de módulo 1 que
  representan una rotación en 3D. Para un giro `yaw` en el suelo:
  `(0, 0, sin(yaw/2), cos(yaw/2))`.
- **Estática / dinámica (static / dynamic transform)**: una transformación que no
  cambia nunca (`/tf_static`) o que cambia con el tiempo (`/tf`).
- **Inercia (inertia)**: lo que cuesta hacer girar una pieza alrededor de cada eje,
  en kg·m². Va en `<inertial>` junto con la masa.
- **Joint (joint)**: en URDF, la unión entre un link padre y uno hijo, con su
  posición (`origin`) y su tipo de movimiento: `fixed`, `continuous`, `revolute`,
  `prismatic`.
- **Launch file (launch file)**: archivo Python con
  `generate_launch_description()` que describe qué procesos arrancar y con qué
  configuración. Se ejecuta con `ros2 launch`.
- **Link (link)**: en URDF, una pieza rígida del robot, con `visual`, `collision`
  e `inertial`. Cada link es un marco TF.
- **Listener (transform listener)**: objeto que se suscribe a `/tf` y `/tf_static`
  y llena un buffer de TF.
- **Marco de referencia (frame)**: un origen más tres ejes. Toda posición se da
  respecto a un marco.
- **`odom`**: marco fijo en el punto donde arrancó la odometría (REP 105). La pose
  del robot en él es continua pero deriva.
- **REP (ROS Enhancement Proposal)**: documento de convenciones de ROS. REP 103
  fija unidades y ejes; REP 105, los marcos de un robot móvil.
- **RPY (roll, pitch, yaw)**: giros alrededor de x, y y z, en radianes. Es como
  los muestra `tf2_echo` además del cuaternión.
- **Sustitución (substitution)**: valor de launch que se resuelve al ejecutar la
  acción que lo usa, como `LaunchConfiguration` o `FindPackageShare`.
- **Transformación (transform)**: traslación más rotación que dice dónde está un
  marco hijo dentro de su padre (`geometry_msgs/msg/TransformStamped`).
- **URDF (Unified Robot Description Format)**: formato XML que describe un robot
  como links unidos por joints.
- **xacro (XML macros)**: preprocesador que expande propiedades, expresiones
  `${...}` y macros de un `.urdf.xacro` y escribe un URDF.
- **Yaw (yaw)**: orientación en el suelo: giro alrededor de z. Positivo es
  antihorario visto desde arriba (girar a la izquierda).

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Webgrafía](../4-recursos/webgrafia/README.md) | **Glosario** | [Rúbrica](../rubrica-evaluacion.md) |

← [Volver a la Semana 06](../README.md)
