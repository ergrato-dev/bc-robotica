# 🤖 Instrucciones para GitHub Copilot

## 📋 Contexto del Bootcamp

Este es un **Bootcamp Robótica Zero to Advanced**: 33 semanas sobre **ROS2 (Jazzy
Jalisco)** desde cero absoluto en robótica hasta el nivel avanzado, en una **ruta única**
que todos cursan completa: robot móvil autónomo (SLAM+Nav2), brazo manipulador con visión
(MoveIt2), manipulación móvil y un bloque avanzado (multi-robot, tiempo real, seguridad,
despliegue, micro-ROS). No es un curso de "instalar ROS y correr un ejemplo": forma a
alguien capaz de diseñar, simular, depurar, extender y desplegar un sistema robótico
completo, con Python y C++ como herramientas igual de reales.

### 📊 Datos del Bootcamp

- **Duración**: 33 semanas (~8 meses)
- **Dedicación semanal**: 12 horas
- **Total de horas**: 396 horas
- **Por qué 33 semanas**: el número lo fija la completitud y pertinencia del temario, no
  la extensión de otros bootcamps. Ver [`docs/decision-semanas.md`](../docs/decision-semanas.md)
- **Modalidad**: autoestudio asincrónico con verificación automática (`colcon test` +
  simulación headless en Gazebo)
- **Nivel de entrada**: cero absoluto en robótica, **con programación previa en Python
  y/o C++** (no se enseña sintaxis básica de ningún lenguaje; para eso están `bc-python`
  y `bc-cpp`)
- **Nivel de salida**: avanzado — capaz de diseñar, simular, depurar, extender (plugins)
  y desplegar un sistema ROS2 completo de navegación, manipulación y manipulación móvil
- **Lenguajes objetivo**: **Python (`rclpy`) y C++ (`rclcpp`), ambos de primera clase**.
  Ver [Política Python/C++](#-política-pythonc)
- **Toolchain**: ROS2 Jazzy, Ubuntu 24.04, Gazebo Harmonic, `ros2_control`, Nav2,
  MoveIt2, `colcon`, `uv`, Docker
- **Sistema operativo**: Docker (`osrf/ros:jazzy-desktop-full`, base Ubuntu 24.04) como
  entorno obligatorio. Ver `docs/setup/`
- **Idioma**: nomenclatura técnica en inglés (identificadores, paquetes, topics, API);
  documentación y comentarios educativos en español

### 📏 Reglas de redacción y herramientas (no negociables)

- **Siempre tuteo, nunca voseo**: "tienes", "puedes", "haz", "mira"; nunca "tenés",
  "podés", "hacé", "mirá"
- **Nunca `pip`, siempre `uv`**. Política exacta en [Python y `uv`](#python-y-uv)
- **Nunca `npm`, siempre `pnpm`** (si alguna herramienta web lo requiere, p. ej. un
  dashboard de telemetría)
- **Nunca MySQL, siempre PostgreSQL** (si se persiste telemetría o resultados de misión)
- **Docker siempre que se requiera**, sobre Ubuntu 24.04
- **Ejemplos claros, detallados y paso a paso; nunca asumir**. Los ejercicios no dan
  nada por sabido: cada comando se muestra completo con su salida esperada, cada archivo
  con su ruta, cada término se define la primera vez
- **Comentarios que documentan qué, para qué e impacto** donde hacen falta (decisiones no
  obvias, parámetros con efecto físico, QoS, límites). Nunca un comentario que repite el
  código ni uno repetido en varios archivos
- **Navegación al pie de todo documento** en tabla `Anterior | Actual | Siguiente`
  (formato en [README.md de Semana](#readmemd-de-semana))
- **Commit + push al terminar cada semana**, una vez pasada la verificación

---

## 🎯 Objetivos de Aprendizaje

Al finalizar el bootcamp, los estudiantes serán capaces de:

- ✅ Explicar el grafo computacional de ROS2 (nodos, topics, servicios, acciones) y su
  transporte DDS
- ✅ Escribir nodos equivalentes en `rclpy` y `rclcpp`, y saber cuándo usar cada uno
- ✅ Diseñar interfaces propias (`.msg`/`.srv`/`.action`) y componer nodos con `colcon`
- ✅ Modelar un robot en URDF/Xacro y razonar sobre su árbol TF2
- ✅ Simular un robot completo (sensores, física, control) en Gazebo Harmonic, y
  verificarlo en modo headless
- ✅ Construir un pipeline de percepción con OpenCV (y opcionalmente detección por deep
  learning)
- ✅ Fusionar sensores con un EKF (`robot_localization`) y justificar cuándo un nodo
  necesita C++ por latencia
- ✅ Controlar actuadores simulados con `ros2_control` (hardware interface y controllers)
- ✅ Cartografiar con `slam_toolbox`, localizar con AMCL y navegar de forma autónoma con
  Nav2, incluida la escritura de plugins de costmap layer y controller en C++
- ✅ Calcular cinemática directa e inversa de un brazo serie, planificar con MoveIt2 y
  ejecutar un pipeline de pick&place con percepción 3D, incluido un planning adapter en C++
- ✅ Integrar navegación y manipulación en un manipulador móvil
- ✅ Operar varios robots en el mismo grafo, medir y mejorar latencia con `ros2_tracing`,
  asegurar el grafo con SROS2, desplegar con Docker multi-stage y CI, y conectar un
  microcontrolador con micro-ROS
- ✅ Escribir el nodo correcto en el lenguaje correcto: Python para prototipar y
  orquestar, C++ donde el framework lo exige o hay presupuesto de latencia real
- ✅ Documentar y demostrar un sistema robótico con evidencia reproducible (`ros2 bag`,
  tests, video)

---

## 📚 Estructura del Bootcamp

### Distribución por Fases

#### **Fase 1 · Fundamentos ROS2 bilingüe (Semanas 1-6)** — 72 horas

- Grafo ROS2/DDS, workspace `colcon`, primer nodo
- Topics, QoS, interfaces custom
- Servicios, acciones, parámetros
- Executors, composición, lifecycle
- Testing y lint dual, `rosbag2`, depuración
- Launch files, TF2, URDF/xacro

#### **Fase 2 · Matemáticas, simulación y control (Semanas 7-12)** — 72 horas

- Transformaciones y cuaterniones
- Gazebo Harmonic, `ros_gz`, spawn y teleop
- Sensores simulados (LiDAR, cámara, IMU), RViz2
- `ros2_control`
- Visión clásica con OpenCV
- Odometría y fusión sensorial (EKF)

#### **Fase 3 · Robot móvil autónomo (Semanas 13-18)** — 72 horas

- Cinemática diferencial y control (PID, pure pursuit)
- SLAM, AMCL, costmaps, planners/controllers, behavior trees
- Misión autónoma y checkpoint

#### **Fase 4 · Manipulación (Semanas 19-24)** — 72 horas

- Cinemática de brazo serie
- MoveIt2, OMPL, colisiones
- Percepción 3D, grasping, pick&place y checkpoint

#### **Fase 5 · Avanzado (Semanas 25-30)** — 72 horas

- Detección con deep learning
- Manipulación móvil
- Multi-robot
- Rendimiento y tiempo real
- Seguridad (SROS2), despliegue y CI
- micro-ROS

#### **Fase 6 · Capstone (Semanas 31-33)** — 36 horas

- Arquitectura, implementación y entrega del sistema del dominio

### Contenido Semana a Semana

| Semana | Carpeta | Tema | Ej.1 (rclpy) | Ej.2 (rclcpp) |
| --- | --- | --- | --- | --- |
| 01 | `bootcamp/week-01-fundamentos_ros2_y_workspace` | Grafo ROS2/DDS, `colcon`, `ament_python` vs `ament_cmake` | publisher/subscriber | mismo nodo; comparar latencia (`ros2 topic hz`) |
| 02 | `bootcamp/week-02-topicos_qos_e_interfaces` | QoS profiles, `.msg` custom (`rosidl`) | pub/sub con QoS | mismo nodo; interfaz compartida agnóstica de lenguaje |
| 03 | `bootcamp/week-03-servicios_acciones_y_parametros` | Servicios, acciones, parámetros | server + cliente | mismo servicio; cliente en el lenguaje contrario al server |
| 04 | `bootcamp/week-04-executors_composicion_y_lifecycle` | Executors, callback groups, component containers, lifecycle nodes | nodo lifecycle | componente cargado en container; justificación de executor |
| 05 | `bootcamp/week-05-testing_lint_rosbag2_y_depuracion` | `pytest`/`gtest`, `launch_testing`, `ruff`/`mypy`/`clang-tidy`, `rosbag2`, `ros2 doctor` | tests + grabación con `rosbag2` | tests gtest + reproducción de bag |
| 06 | `bootcamp/week-06-launch_tf2_y_urdf` | Launch files, TF2, URDF/xacro | TF broadcaster | TF listener; checklist de paridad que cierra la fase |
| 07 | `bootcamp/week-07-transformaciones_y_cuaterniones` | Matrices homogéneas, ángulos de Euler, cuaterniones, `tf_transformations` | calculadora de transformaciones NumPy | — (se reutiliza en C++ vía `tf2` en la 06) |
| 08 | `bootcamp/week-08-gazebo_harmonic_y_teleop` | `gz-sim`, SDF, `ros_gz_bridge`, spawn, teleop | scripts de teleop | nodo puente de comandos con clamp |
| 09 | `bootcamp/week-09-sensores_simulados_y_rviz2` | `sensor_msgs` (LiDAR, cámara, IMU), plugins de sensor, RViz2 | procesado de `LaserScan` | — |
| 10 | `bootcamp/week-10-ros2_control` | `ros2_control`, hardware interface, `diff_drive_controller`, `joint_trajectory_controller` | cliente de controller_manager | hardware interface propio (`pluginlib`) — CORE |
| 11 | `bootcamp/week-11-vision_clasica_opencv` | `cv_bridge`, filtros, color/forma, calibración de cámara, ArUco | detección clásica | — |
| 12 | `bootcamp/week-12-odometria_y_fusion_ekf` | Odometría, ruido, `robot_localization` EKF | configuración EKF | nodo de odometría a frecuencia fija — CORE |
| 13 | `bootcamp/week-13-cinematica_diferencial_y_control` | Cinemática diferencial, PID, pure pursuit | prototipo NumPy | controlador a frecuencia fija — CORE |
| 14 | `bootcamp/week-14-slam_toolbox_y_cartografiado` | SLAM online/offline, guardar/cargar mapa | orquestar `slam_toolbox` | — |
| 15 | `bootcamp/week-15-amcl_y_costmaps` | AMCL, costmaps 2D, capas | localizar desde pose desconocida | plugin de costmap layer (`nav2_costmap_2d::Layer`) |
| 16 | `bootcamp/week-16-planners_y_controllers_nav2` | NavFn/Smac, DWB/RPP/MPPI, `nav2_simple_commander` | enviar goals, reintentos | plugin de controller (`nav2_core::Controller`) |
| 17 | `bootcamp/week-17-behavior_trees_y_recovery` | BT XML, BT.CPP, recovery, waypoints | BT con `nav2_simple_commander` | nodo BT nativo (BT.CPP) |
| 18 | `bootcamp/week-18-mision_autonoma_y_checkpoint_movil` | Misión multi-objetivo, manejo de fallos, checkpoint móvil | orquestación de misión | benchmarking `rclpy` vs `rclcpp` + informe |
| 19 | `bootcamp/week-19-cinematica_de_brazos` | Brazo serie, DH, FK, IK numérica, Jacobiano | FK/IK en NumPy | IK como servicio de baja latencia |
| 20 | `bootcamp/week-20-moveit2_fundamentos` | Arquitectura MoveIt2, Setup Assistant, planning scene | `moveit_py` | `MoveGroupInterface` en C++ |
| 21 | `bootcamp/week-21-ompl_colisiones_y_adapters` | Planners OMPL, collision objects, restricciones | definir escena | plugin `planning_request_adapter` |
| 22 | `bootcamp/week-22-percepcion_3d_y_hand_eye` | Point clouds, PCL, segmentación, calibración hand-eye | segmentación de objetos | nodo C++ detección→pose (latencia real) |
| 23 | `bootcamp/week-23-grasping_y_gripper` | `GripperCommand`, grasp planning, MoveIt Task Constructor | secuencia orquestada | controller de gripper con feedback |
| 24 | `bootcamp/week-24-pick_and_place_y_checkpoint` | Pipeline pick&place completo, fallos, checkpoint manipulación | orquestación `moveit_py` | benchmarking + informe |
| 25 | `bootcamp/week-25-deteccion_deep_learning` | YOLO (`ultralytics`) vs clásico, benchmarking | inferencia + comparación | — |
| 26 | `bootcamp/week-26-manipulacion_movil` | Nav2 + MoveIt2 en un mismo robot, coordinación base-brazo | orquestador de misión | — |
| 27 | `bootcamp/week-27-multi_robot` | Namespaces, `ROS_DOMAIN_ID`, TF multi-robot, flotas | lanzar N robots | — |
| 28 | `bootcamp/week-28-rendimiento_y_tiempo_real` | `ros2_tracing`, intra-process, zero-copy (loaned messages), kernel RT | perfilado | nodo optimizado y medido — CORE |
| 29 | `bootcamp/week-29-sros2_despliegue_y_ci` | SROS2, Docker multi-stage, CI con GitHub Actions | pipeline CI | imagen de despliegue |
| 30 | `bootcamp/week-30-micro_ros` | micro-ROS, agente, plataforma host (hardware opcional) | agente + monitor | cliente micro-ROS (C) |
| 31 | `bootcamp/week-31-capstone_arquitectura` | Diseño del sistema del dominio, ADR, interfaces | — | — |
| 32 | `bootcamp/week-32-capstone_implementacion` | Sistema completo del dominio | — | al menos un nodo C++ justificado |
| 33 | `bootcamp/week-33-capstone_entrega_y_demo` | Pulido, documentación, demo, hardware opcional | — | — |

---

## 🔀 Política Python/C++

No es una alternancia arbitraria. Tres reglas fijas:

1. **Semanas 01-06**: todo concepto de comunicación se enseña **dos veces**, en `rclpy`
   y en `rclcpp`, replicando el propio patrón de los tutoriales oficiales de ROS2.
   Ningún lenguaje es "el principal" en esta fase.
2. **Semanas 07-13**: Python por defecto (prototipado, scripting, ecosistema Python-first
   como OpenCV/NumPy), salvo donde el framework solo expone el punto de extensión en C++
   (hardware interface de `ros2_control`, semana 10) o el nodo está en un bucle a
   frecuencia fija (odometría semana 12, controlador semana 13): ahí C++ se justifica por
   escrito, nunca por dogma.
3. **Semanas 14-30**: Python para orquestación de alto nivel (`nav2_simple_commander`,
   `moveit_py` — las APIs oficiales para eso). **C++ obligatorio** donde el framework lo
   exige (plugins vía `pluginlib`, que no tiene binding Python) o donde hay presupuesto de
   latencia real (percepción→acción, semana 22; tiempo real, semana 28). El capstone
   exige al menos un nodo C++ con justificación escrita.

**Regla dura**: ningún plugin `pluginlib` se escribe en Python — no está soportado por
el framework, no es una elección pedagógica.

---

## 🗂️ Estructura de Carpetas

Todas las semanas, planas en `bootcamp/` (ruta única, sin tracks):

```
bootcamp/
├── README.md                               # índice de semanas con su estado
├── week-01-fundamentos_ros2_y_workspace/
├── …
└── week-33-capstone_entrega_y_demo/
```

Cada semana sigue esta estructura estándar:

```
week-XX-tema_principal/
├── README.md                 # Descripción y objetivos de la semana
├── rubrica-evaluacion.md     # Criterios de evaluación detallados
├── 0-assets/                 # Diagramas SVG
├── 1-teoria/                 # Material teórico (archivos .md)
├── 2-practicas/              # Ejercicios guiados con starter/ (patrón descomentar)
│   └── ejercicio-NN-tema/
│       ├── README.md
│       └── starter/          # paquete(s) ROS2: rclpy y/o rclcpp según la semana
├── 3-proyecto/                # Capa semanal del proyecto del dominio
│   ├── README.md              # Requisitos del entregable
│   └── starter/                # Paquete con TODOs adaptable al dominio
├── 4-recursos/                # Recursos adicionales
│   ├── ebooks-free/
│   ├── videografia/
│   └── webgrafia/
└── 5-glosario/                 # Términos clave de la semana (A-Z)
    └── README.md
```

### 📁 Carpetas Raíz

- **`assets/`**: recursos visuales globales (header del README)
- **`docs/`**: documentación transversal (setup, `stack-versions.md`, `dominios.md`,
  `decision-semanas.md`, `hardware-opcional.md`, `dependency-security-policy.md`)
- **`scripts/`**: `verificar-enlaces.sh`, `verificar-simulaciones.sh`
- **`bootcamp/`**: contenido semanal

---

## 🎓 Componentes de Cada Semana

### 1. **Teoría** (`1-teoria/`)

- Archivos markdown con explicaciones conceptuales **en español**
- **El número de archivos es libre**: los que pida el temario. Cuatro a seis es lo
  normal. Nunca se sacrifica profundidad para que quepa
- **Extensión por archivo: ~250 líneas** (rango sano 200-300). Si un archivo se va de
  ahí, mezcla dos temas: divídelo, no lo recortes
- Cada tema en este orden: **qué problema resuelve → cómo funciona en ROS2 → cómo se
  escribe en Python (`rclpy`) y/o C++ (`rclcpp`) → antipatrones → trucos**
- **Cero absoluto de robótica**: la primera vez que aparece un término técnico se
  define. "Nodo", "topic", "QoS", "TF", "costmap", "cinemática inversa" no son
  vocabulario común
- **Todo fragmento de código es ejecutable** contra el stack pinneado en
  `docs/stack-versions.md`. Si es un ejemplo de lo que NO hacer, se marca con `// ❌`
  / `# ❌` y se explica qué falla
- Ejemplos **paso a paso**: cada comando completo con su salida esperada, cada archivo
  con su ruta desde la raíz del workspace. Nunca "configura X" sin mostrar cómo
- Diagramas SVG cuando aporten (nunca ASCII art, nunca capturas de pantalla)
- Referencias a la documentación oficial (docs.ros.org, navigation.ros.org,
  moveit.picknik.ai, gazebosim.org) como fuente de verdad

### 2. **Prácticas** (`2-practicas/`)

Los ejercicios son **tutoriales guiados**, NO tareas con TODOs. El estudiante aprende
**descomentando código** y viendo los tests/el nodo funcionar.

```
2-practicas/ejercicio-01-nombre_py/
├── README.md
└── starter/                  # paquete ament_python, código comentado por pasos
2-practicas/ejercicio-02-nombre_cpp/
├── README.md
└── starter/                  # paquete ament_cmake, mismo concepto en rclcpp
```

Reglas:

- Todo paso termina con **una forma de verificarlo**: `colcon test`, `ros2 topic echo`,
  un mensaje concreto, o el comportamiento esperado en RViz2/Gazebo
- Los **tests van escritos en el starter** (Python: `pytest`+`launch_testing`; C++:
  `gtest`/`ament_cmake_gtest`) y fallan hasta que el estudiante descomenta
- ❌ No usar `// TODO:`/`# TODO:` en prácticas — eso es formato de proyecto
- ❌ **Sin carpeta `solution/`**: el código comentado ES la solución. `**/solution/`
  está en `.gitignore`
- Python pasa `ruff` + `mypy` sin avisos; C++ compila con
  `-Wall -Wextra -Wpedantic -Werror` y pasa `clang-format --dry-run --Werror`

### 3. **Proyecto** (`3-proyecto/`)

Cada semana añade **una capa nueva al mismo sistema del dominio del estudiante**. Nunca un proyecto desechable por semana.

El README del proyecto incluye:

1. Qué capa se añade esta semana y por qué va aquí
2. Requisitos verificables (compila/lintea, tests que deben existir y pasar,
   comportamiento observable en simulación)
3. Cómo verificarlo: `colcon build && colcon test`, y si aplica,
   `scripts/verificar-simulaciones.sh week-NN`
4. Criterios de calidad más allá de lo automatizable
5. Adaptación al dominio con ejemplos para al menos las misiones del catálogo de
   `docs/dominios.md`

**Política de dominio**: el estudiante declara su dominio/misión en la Semana 01 y no
cambia después; cada misión tiene una parte móvil y una de manipulación, así que sirve
para las 33 semanas. Ver `docs/dominios.md`.

### 4. **Recursos** (`4-recursos/`)

- **ebooks-free/**: guías gratuitas y legales (REP de ROS2, documentación oficial
  descargable)
- **videografia/**: ROSCon, charlas oficiales de Open Robotics/PickNik, tutoriales
  verificados
- **webgrafia/**: docs.ros.org primero, luego navigation.ros.org, moveit.picknik.ai,
  gazebosim.org y blogs de calidad

Cada recurso lleva una línea de por qué vale la pena, no solo el enlace.

### 5. **Glosario** (`5-glosario/`)

Términos A-Z **en español**, con el **término inglés/API entre paréntesis** cuando
exista (`calidad de servicio (Quality of Service, QoS)`, `mapa de costos (costmap)`).
Conecta la prosa española con la documentación oficial en inglés.

---

## 📝 Convenciones de Código

### Python (`rclpy`)

- Python 3.12.3 (el del sistema en Ubuntu 24.04, que es contra el que está compilado
  `rclpy`), `ament_python`, `package.xml` + `setup.py`
- Lint/format: `ruff` (reemplaza flake8+black+isort); tipado: `mypy` en modo estricto
  sobre el código propio (no sobre `rclpy`, que carece de stubs completos)
- Nomenclatura: `snake_case` para funciones/variables/archivos/paquetes; `PascalCase`
  para clases de nodo (`class OdometryFusionNode(Node): ...`)
- Todo nodo declara sus parámetros explícitamente (`self.declare_parameter(...)`) y su
  perfil de QoS cuando no usa el `QoSPresetProfiles` por defecto
- ✅ Type hints en toda función pública
- ❌ `except Exception:` desnudo — capturar la excepción concreta o dejar que se
  propague con contexto

### Python y `uv`

**Nunca `pip`**, ni en el material ni en el Dockerfile. `rclpy` y los paquetes ROS no
viven en PyPI, así que el reparto es:

| Qué | Cómo se instala | Por qué |
| --- | --- | --- |
| Paquetes ROS (`rclpy`, `cv_bridge`, `tf_transformations`...) | `apt` / `rosdep` | Están compilados contra el Python del sistema y ROS Jazzy |
| Tooling (`ruff`, `mypy`) | `uv tool install ruff mypy` | Aislado del sistema, versión pinneada |
| Dependencias no-ROS (`ultralytics`, versiones nuevas de `numpy`...) | `uv venv --system-site-packages` + `uv pip install` dentro del venv | Ve `rclpy` del sistema sin contaminarlo |
| Scripts sueltos | `uv run --with <paquete> script.py` | Sin instalar nada globalmente |

`colcon` sigue construyendo los paquetes `ament_python`; `uv` no sustituye a `colcon`.

### C++ (`rclcpp`)

- C++17 (estándar exigido por `rclcpp` en Jazzy), `ament_cmake`, CMake 3.28.3
- **Target-based**: `target_link_libraries`, `target_include_directories`. Nunca
  `CMAKE_CXX_FLAGS` global salvo en presets de configuración
- Warnings como errores: `-Wall -Wextra -Wpedantic -Werror`
- `.clang-format` de la raíz es la única verdad de formato
- Nomenclatura: `snake_case` para funciones/variables/archivos; `PascalCase` para tipos
  y clases de nodo; miembros privados con sufijo `_`
- ✅ `std::shared_ptr<Node>` vía `rclcpp::Node::make_shared`, nunca `new` crudo para nodos
- ✅ Callbacks con `std::bind`/lambda explícitos sobre el tipo de mensaje concreto
- ❌ `using namespace std;` en headers

### Interfaces (`rosidl`)

- Todo `.msg`/`.srv`/`.action` custom vive en un paquete `_interfaces` separado del
  paquete que lo consume (patrón oficial de ROS2)
- Nombres de campo en `snake_case`, nombres de tipo/acción en `PascalCase`

### Launch y configuración

- Todo launch file en **Python** (`generate_launch_description`), nunca XML/YAML salvo
  justificación explícita en el README de la semana
- Argumentos declarados con `DeclareLaunchArgument`, nunca hardcodeados
- Configuración por archivo YAML versionado, no por edición manual en runtime

### Placeholders

- `<tu-dominio>` para la misión del estudiante
- `<ruta-al-repo>` para rutas locales
- ❌ Nunca una ruta absoluta real de una máquina concreta en el material

---

## 🔐 Reglas de Seguridad y Rigor del Contenido

- ✅ Todo fragmento de código publicado se ejecuta contra el stack pinneado en
  `docs/stack-versions.md` (ROS2 Jazzy, Gazebo Harmonic, Nav2/MoveIt2 rama `jazzy`)
- ✅ Toda afirmación sobre una API se puede señalar en la documentación oficial
  (docs.ros.org, navigation.ros.org, moveit.picknik.ai). Nada de "creo que expone..."
- ✅ Toda semana con simulación corre **headless** (`gz sim -s` /
  `--headless-rendering`) antes de publicarse — verificado con
  `scripts/verificar-simulaciones.sh`
- ✅ Todo nodo que mueve un actuador (real o simulado) clampea a límites declarados; no
  confía en que el comando de entrada ya viene sano
- ✅ URDF/Xacro válida con `check_urdf`; árbol TF sin ciclos, verificado con
  `view_frames`
- ✅ Imágenes Docker con tag de fecha, nunca `:latest`
- ❌ Nunca inventar un topic, servicio, parámetro o plugin que no exista en la
  documentación oficial de la versión pinneada
- ❌ Nunca credenciales, IPs o tokens hardcodeados en ejemplos de nodos de hardware
- ❌ Nunca un ejemplo de control que no clampee límites presentado como listo para
  hardware real
- ❌ Nunca un plugin `pluginlib` escrito en Python

---

## 🎨 Recursos Visuales

- ✅ **SVG** para todos los diagramas (nunca ASCII art, nunca capturas de pantalla)
- 🌙 **Tema oscuro**, **sin degradados**, colores sólidos
- ✅ Paleta del bootcamp:

```
fondo             #0d1117      texto              #e6edf3
superficie        #161b22      texto secundario   #8b949e
superficie alta   #21262d      texto atenuado     #484f58
borde             #30363d      código             #79c0ff
acento python     #4b8bbe      acento c++         #00599c
éxito             #3fb950      advertencia        #d29922
error             #f85149      simulación (Gazebo)#a371f7
hardware opcional #f0883e
```

- `acento python`/`acento c++` se reservan para diagramas que comparan ambos lenguajes
  lado a lado (semanas 01-06 y donde haya ejercicio CORE en C++). `simulación` para todo lo que ocurre solo en
  Gazebo. `hardware opcional` exclusivamente en diagramas de la sección de hardware
- ✅ Tipografía sans-serif: `Inter, Roboto, "Segoe UI", system-ui, sans-serif`;
  `ui-monospace, "JetBrains Mono", Consolas, monospace` para código en el diagrama
- ✅ `viewBox` siempre, `role="img"`, `<title>` y `aria-label` descriptivo
- ✅ Ancho objetivo 800-880 px, texto mínimo 12 px, sin JS ni fuentes externas
- ✅ Nombrar en orden de lectura: `01-grafo-ros2.svg`, `02-arbol-tf.svg`
- ✅ Todo SVG debe estar enlazado desde al menos un `.md`; uno huérfano es un error que
  reporta `verificar-enlaces.sh`
- **El número de SVG depende de la necesidad de cada archivo de teoría**, nunca de
  cuántos diagramas tenga la semana equivalente en un repo hermano (`bc-cpp`,
  `bc-fastapi`...). Un archivo de teoría puede necesitar cero SVG o varios; ningún
  archivo lleva un diagrama solo para "no quedarse corto" frente al ejemplo

---

## 📖 Documentación

### README.md de Semana

Debe incluir, en este orden:

1. Título `# Semana NN — Tema` + blockquote gancho de una línea
2. `## 🎯 Objetivos de la Semana`
3. `## 📋 Prerrequisitos`
4. `## 🗂️ Estructura de la Semana` (árbol de archivos)
5. `## 📝 Contenidos` (tablas de teoría, prácticas y proyecto con duración y lenguaje)
6. `## ⏱️ Distribución del Tiempo (12 horas)` — la tabla suma exactamente 12 h; si suma
   más, se recorta alcance
7. `## 🎩 Trucos y atajos` (CLI de ROS2, `rqt`, RViz2, editor; mínimo cinco)
8. `## 📌 Entregables`
9. `## ✅ Verificación` (comandos `colcon`/simulación headless)
10. `## 🔧 Extensión Hardware (opcional)` — solo si aplica esa semana, siempre al final
    y en bloque `> [!NOTE]`, nunca mezclada con los pasos de simulación
11. `## 🔗 Navegación`, en tabla al pie, igual en todo documento del repo:

```markdown
## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 01](../week-01-…/README.md) | **Semana 02** | [Semana 03](../week-03-…/README.md) |

← [Volver al inicio del bootcamp](../../README.md)
```

Dentro de una semana, teoría, prácticas, recursos y glosario encadenan su propio
anterior/siguiente (p. ej. teoría 01 → teoría 02).

### Archivos de Teoría

```markdown
# Título del Tema

> Blockquote de una línea: por qué esto importa en robótica.

## 🎯 Objetivos

## 1. Qué problema resuelve

## 2. Cómo funciona en ROS2

## 3. Cómo se escribe (rclpy y/o rclcpp)

## 4. Antipatrones

## 5. Trucos

## 📚 Recursos Adicionales

## ✅ Checklist de Verificación
```

---

## 📊 Evaluación

Cada semana incluye **tres tipos de evidencias**:

1. **Conocimiento 🧠** (30%): cuestionario de autoevaluación con respuestas al final
2. **Desempeño 💪** (40%): ejercicios verificados por `colcon test` (y simulación
   headless cuando aplica) en cada starter
3. **Producto 📦** (30%): la capa semanal del proyecto del dominio

Mínimo **70%** en cada tipo. Al ser autoestudio, el cuestionario incluye sus respuestas
en una sección colapsable (`<details>`) al final de la rúbrica.

Penalizaciones estándar del Producto:

| Situación | Penalización |
| --------- | ------------ |
| No compila/lintea limpio (`ruff`/`mypy` o `-Werror`) | 0 en Producto |
| Simulación no levanta headless | 0 en Producto |
| Plugin `pluginlib` escrito en Python | 0 en Producto |
| Nodo de actuador sin clamp de límites | -20 |
| Sin nodo C++ CORE donde la semana lo exige sin justificación | -15 |
| Sin tests propios del proyecto | -15 |
| Código copiado de otra misión/dominio | 0 en Producto |

**Lo que no se automatiza** (legibilidad, elección de arquitectura del grafo, diseño de
interfaces) se evalúa con criterios observables escritos en la rúbrica.

---

## 🤖 Instrucciones para Copilot

### Límites de Respuesta

1. **Divide respuestas largas**: por carpetas — teoría → prácticas → proyecto →
   recursos → assets. Indica siempre qué parte se entregó y qué falta
2. **Una semana por tanda**, usando la Semana 01 como plantilla de calidad

### Generación de Contenido

1. **Profundidad sobre cobertura**: mejor tres conceptos bien explicados que veinte
   listados
2. **Siempre el porqué**: ninguna decisión de ROS2 sin el problema que resuelve
3. **Cero absoluto de robótica**: cada término se define la primera vez
4. **Verificable**: todo entregable compila/lintea y tiene tests o se verifica en
   simulación. Si no se puede verificar, replantear el entregable
5. **Progresión estricta**: ningún concepto se usa antes de su semana. Sin acciones
   antes de la 03, sin TF2/URDF antes de la 06, sin Gazebo antes de la 08, sin
   `pluginlib` ni `ros2_control` antes de la 10, sin fusión sensorial antes de la 12, sin
   SLAM/Nav2 antes de la 14, sin MoveIt2 antes de la 20
6. **Verificar antes de publicar**: `./scripts/verificar-simulaciones.sh week-NN` y
   `colcon build && colcon test` tienen que pasar
7. **No inventar topics, servicios, parámetros ni plugins.** Si hay duda, decirlo y
   enlazar la documentación oficial en vez de improvisar algo plausible

### Estado del stack

- **ROS2 Jazzy Jalisco** es la LTS objetivo (soporte hasta mayo 2029); el material se
  escribe contra ella
- **Gazebo Harmonic** (`gz-sim`) reemplaza a Gazebo Classic, que está en EOL: el
  bootcamp nunca enseña Classic
- **Nav2/MoveIt2** se usan en su rama `jazzy`; las versiones exactas de cada paquete
  viven en `docs/stack-versions.md`
- **`moveit_py`** es la API Python oficial de MoveIt2 desde Iron/Jazzy — se usa en el
  bootcamp en vez de `moveit_commander` (deprecado)

---

## 📚 Referencias Oficiales

- **ROS2 (Jazzy)**: https://docs.ros.org/en/jazzy/
- **Nav2**: https://docs.nav2.org/
- **MoveIt2**: https://moveit.picknik.ai/
- **Gazebo (Harmonic)**: https://gazebosim.org/docs/harmonic
- **`ros_gz` (puente ROS2↔Gazebo)**: https://github.com/gazebosim/ros_gz
- **REP (ROS Enhancement Proposals)**: https://ros.org/reps/rep-0000.html
- **Index de paquetes ROS2**: https://index.ros.org/

---

## 🔗 Enlaces Importantes

- **Repositorio**: https://github.com/ergrato-dev/bc-robotica
- **Documentación general**: [docs/README.md](../docs/README.md)
- **Primera semana**: [bootcamp/week-01-fundamentos_ros2_y_workspace/README.md](../bootcamp/week-01-fundamentos_ros2_y_workspace/README.md)

---

## ✅ Checklist para Nuevas Semanas

- [ ] Estructura de carpetas completa en `bootcamp/week-NN-slug/`
- [ ] `README.md` con las secciones obligatorias (incluida `🎩 Trucos y atajos`)
- [ ] Teoría en `1-teoria/`, un archivo por concepto (~250 líneas cada uno)
- [ ] Cada término técnico nuevo definido en su primera aparición
- [ ] Semanas 01-06: los dos ejercicios (`rclpy`/`rclcpp`) implementan el mismo
      concepto y son comparables
- [ ] Donde la tabla marca CORE: el ejercicio en C++ existe, compila y su justificación de
      "por qué C++ aquí" está escrita en el README
- [ ] Prácticas con patrón descomentar, tests escritos en el starter, sin `solution/`
- [ ] `./scripts/verificar-simulaciones.sh week-NN` pasa si la semana tiene simulación
- [ ] `colcon build && colcon test` pasa (Python y C++)
- [ ] Proyecto que añade una capa al sistema del dominio, con adaptación por misión
- [ ] Ningún concepto usado antes de la semana en que se enseña
- [ ] Sección de hardware opcional (si aplica) en bloque `> [!NOTE]` al final, nunca
      bloqueante
- [ ] Recursos en las tres subcarpetas, cada uno con su justificación
- [ ] Glosario A-Z con el término/API en inglés entre paréntesis
- [ ] `rubrica-evaluacion.md` con cuestionario + respuestas en `<details>`
- [ ] SVG con la paleta del bootcamp, todos enlazados
- [ ] Tuteo en todo el texto, sin voseo; cero `pip`/`npm`/MySQL
- [ ] Tabla de tiempos suma 12 h
- [ ] Navegación en tabla al pie de cada documento, enlaces correctos
- [ ] Fila de la semana actualizada en `bootcamp/README.md`
- [ ] `./scripts/verificar-enlaces.sh` sin errores
- [ ] Commit (`feat(week-NN): ...`) + push

---

## 💡 Notas Finales

- **Prioridad**: profundidad sobre cobertura
- **Enfoque**: escribir y simular robótica, no leer sobre robótica
- **Objetivo**: formar a alguien capaz de leer y extender Nav2/MoveIt2, no solo
  configurarlos
- **Filosofía**: si no corre en simulación verificable y no tiene un test, no es un
  entregable

---

_Última actualización: noviembre de 2026_
