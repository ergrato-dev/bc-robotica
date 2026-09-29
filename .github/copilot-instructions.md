# 🤖 Instrucciones para GitHub Copilot

## 📋 Contexto del Bootcamp

Este es un **Bootcamp Robótica Zero to Hero**: 19 semanas sobre **ROS2 (Jazzy Jalisco)**
desde cero absoluto en robótica hasta un robot móvil autónomo con SLAM+Nav2 (Track A) o
un brazo manipulador con visión y pick&place (Track B). No es un curso de "instalar ROS
y correr un ejemplo": forma a alguien capaz de diseñar, simular, depurar y entregar un
sistema robótico completo, con percepción, navegación o manipulación, y con Python y C++
como herramientas igual de reales.

### 📊 Datos del Bootcamp

- **Duración**: 19 semanas (~4.5 meses)
- **Dedicación semanal**: 10 horas
- **Total de horas**: 190 horas
- **Modalidad**: autoestudio asincrónico con verificación automática (`colcon test` +
  simulación headless en Gazebo)
- **Nivel de entrada**: cero absoluto en robótica, **con programación previa en Python
  y/o C++** (no se enseña sintaxis básica de ningún lenguaje)
- **Nivel de salida**: capaz de diseñar, simular y depurar un sistema ROS2 completo —
  Track A (navegación autónoma) o Track B (manipulación con visión)
- **Lenguajes objetivo**: **Python (`rclpy`) y C++ (`rclcpp`), ambos de primera clase**.
  Ver [Política Python/C++](#-política-pythonc)
- **Toolchain**: ROS2 Jazzy, Ubuntu 24.04, Gazebo Harmonic, Nav2, MoveIt2, `colcon`,
  Docker
- **Sistema operativo**: Docker (`osrf/ros:jazzy-desktop-full`) como entorno obligatorio.
  Ver `docs/setup/`
- **Idioma del código**: inglés (identificadores, nombres de paquetes/topics). La prosa
  es española

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
- ✅ (Track A) Cartografiar con `slam_toolbox`, localizar con AMCL y navegar de forma
  autónoma con Nav2, incluida la escritura de un plugin de costmap/controller en C++
- ✅ (Track B) Planificar y ejecutar movimientos con MoveIt2, detectar objetos y ejecutar
  un pipeline de pick&place completo, incluido un planning adapter en C++
- ✅ Escribir el nodo correcto en el lenguaje correcto: Python para prototipar y
  orquestar, C++ donde el framework lo exige o hay presupuesto de latencia real
- ✅ Documentar y demostrar un sistema robótico con evidencia reproducible (`ros2 bag`,
  tests, video)

---

## 📚 Estructura del Bootcamp

### Distribución por Fases

#### **Fase 1 · Fundamentos ROS2 bilingüe (Semanas 1-5)** — 50 horas

- Grafo ROS2/DDS, workspace `colcon`, primer nodo
- Topics, QoS, interfaces custom
- Servicios, acciones, parámetros
- Executors, composición, testing y lint dual
- Launch files, TF2, URDF básico

#### **Fase 2 · Simulación y percepción (Semanas 6-10)** — 50 horas

- Gazebo Harmonic, `ros_gz`, spawn y teleop
- Sensores simulados (LiDAR, cámara, IMU), RViz2
- Visión clásica con OpenCV
- Odometría y fusión sensorial (EKF)
- Detección avanzada (deep learning opcional)

#### **Fase 3 · Puente común: cinemática (Semanas 11-12)** — 20 horas

- Cinemática de robot diferencial y de brazo serie
- Checkpoint de integración y elección definitiva de track + dominio

#### **Fase 4 · Especialización — Track A o B (Semanas 13-17)** — 50 horas

- **Track A** (SLAM + Nav2): cartografiado, AMCL, planners/controllers, behavior trees,
  misión autónoma
- **Track B** (MoveIt2 + visión): planning scene, OMPL, percepción para manipulación,
  grasping, pipeline pick&place

#### **Fase 5 · Capstone (Semanas 18-19)** — 20 horas

- Integración final del sistema del dominio
- Documentación, demo, hardware opcional

### Contenido Semana a Semana

| Semana | Carpeta | Tema | Ej.1 (rclpy) | Ej.2 CORE (rclcpp) |
| --- | --- | --- | --- | --- |
| 01 | `bootcamp/week-01-fundamentos_ros2_y_workspace` | Grafo ROS2/DDS, `colcon`, `ament_python` vs `ament_cmake` | publisher/subscriber | mismo nodo; comparar latencia (`ros2 topic hz`) |
| 02 | `bootcamp/week-02-topicos_qos_e_interfaces` | QoS profiles, `.msg` custom (`rosidl`) | pub/sub con QoS | mismo nodo; interfaz compartida agnóstica de lenguaje |
| 03 | `bootcamp/week-03-servicios_acciones_y_parametros` | Servicios, acciones, parámetros | server + cliente | mismo servicio; cliente obligatorio en el lenguaje contrario al server |
| 04 | `bootcamp/week-04-executors_composicion_y_calidad` | Executors, component containers, lifecycle, testing/lint dual | acción `long_task` | acción `run_diagnostic` — CORE, justificación de executor |
| 05 | `bootcamp/week-05-launch_tf2_urdf_cierre_fase1` | Launch files, TF2, URDF/xacro básico | TF broadcaster | TF listener; checklist de paridad que cierra la fase |
| 06 | `bootcamp/week-06-gazebo_harmonic_y_spawn` | `gz-sim`, `ros_gz_bridge`, spawn, teleop | scripts de teleop | nodo puente de comandos (primer hot-path de control) |
| 07 | `bootcamp/week-07-sensores_simulados_lidar_camara_imu` | `sensor_msgs`, plugins de sensor, RViz2 | — | — |
| 08 | `bootcamp/week-08-vision_clasica_opencv` | `cv_bridge`, filtros, color/forma, ArUco | detección clásica | — (nota: `cv_bridge` existe igual en C++) |
| 09 | `bootcamp/week-09-odometria_fusion_sensorial_ekf` | `robot_localization` EKF | — | nodo de fusión CORE, frecuencia fija justificada |
| 10 | `bootcamp/week-10-deteccion_avanzada_deep_learning` | YOLOv8 (`ultralytics`) vs clásico, benchmarking | inferencia + comparación | — (semana "opcional avanzada" en esfuerzo) |
| 11 | `bootcamp/week-11-cinematica_moviles_y_brazos` | Cinemática diferencial y de brazo serie | prototipo NumPy | mismo cálculo como servicio ROS2 de baja latencia |
| 12 | `bootcamp/week-12-checkpoint_integracion_y_eleccion_track` | Integración, elección de track y dominio | — | — |
| 13 A | `bootcamp/track-a/week-13-slam_toolbox_y_cartografiado` | SLAM online/offline, guardar/cargar mapa | orquestar `slam_toolbox` | — |
| 14 A | `bootcamp/track-a/week-14-amcl_localizacion_y_costmaps` | AMCL, costmaps | localizar desde pose desconocida | plugin de costmap layer (`nav2_costmap_2d::Layer`) |
| 15 A | `bootcamp/track-a/week-15-planners_controllers_nav2` | NavFn/Smac, DWB/RPP, `nav2_simple_commander` | enviar goals, reintentos | plugin de controller (`nav2_core::Controller`) |
| 16 A | `bootcamp/track-a/week-16-behavior_trees_y_recovery` | BT XML, recovery, waypoints | BT con `py_trees_ros` | nodo BT nativo (BT.CPP) |
| 17 A | `bootcamp/track-a/week-17-mision_autonoma_integracion_y_rendimiento` | Misión multi-objetivo, fallos | orquestación de misión | benchmarking `rclpy` vs `rclcpp` + informe |
| 13 B | `bootcamp/track-b/week-13-moveit2_fundamentos_y_planning_scene` | Arquitectura MoveIt2, Setup Assistant | `moveit_py` | `MoveGroupInterface` en C++ |
| 14 B | `bootcamp/track-b/week-14-planificacion_ompl_y_colisiones` | Planners OMPL, collision objects | definir escena | plugin `planning_request_adapter` |
| 15 B | `bootcamp/track-b/week-15-percepcion_para_manipulacion` | Eye-in-hand, pose 3D, hand-eye | — | nodo C++ detección→pose (latencia real) |
| 16 B | `bootcamp/track-b/week-16-grasping_y_control_gripper` | `GripperCommand`, grasp planning | secuencia orquestada | controller de gripper con feedback, C++ |
| 17 B | `bootcamp/track-b/week-17-pick_and_place_integracion_y_rendimiento` | Pipeline completo, fallos | orquestación `moveit_py` | benchmarking `rclpy` vs `rclcpp` + informe |
| 18 | `week-18-proyecto_final_implementacion` (por track) | Sistema completo del dominio | — | al menos un nodo C++ justificado |
| 19 | `week-19-proyecto_final_entrega_y_demo` (por track) | Pulido, documentación, demo | — | — |

---

## 🔀 Política Python/C++

No es una alternancia arbitraria. Tres reglas fijas:

1. **Semanas 01-05**: todo concepto de comunicación se enseña **dos veces**, en `rclpy`
   y en `rclcpp`, replicando el propio patrón de los tutoriales oficiales de ROS2.
   Ningún lenguaje es "el principal" en esta fase.
2. **Semanas 06-12**: Python por defecto (prototipado, scripting, ecosistema Python-first
   como OpenCV/`ultralytics`), salvo que el nodo esté en un bucle de control a
   frecuencia fija (odometría/EKF semana 09, cinemática como servicio semana 11) — ahí
   C++ se justifica por rendimiento, nunca por dogma.
3. **Semanas 13-17 (ambos tracks)**: Python para orquestación de alto nivel
   (`nav2_simple_commander`, `moveit_py` — las APIs oficiales para eso). **C++
   obligatorio** donde el propio framework lo exige (plugins vía `pluginlib`, que no
   tiene binding Python) o donde hay presupuesto de latencia real (percepción→acción en
   Track B). El capstone exige al menos un nodo C++ con justificación escrita.

**Regla dura**: ningún plugin `pluginlib` se escribe en Python — no está soportado por
el framework, no es una elección pedagógica.

---

## 🗂️ Estructura de Carpetas

Semanas 01-12, planas en `bootcamp/`. Semanas 13-19, anidadas por track:

```
bootcamp/
├── week-01-fundamentos_ros2_y_workspace/   … week-12-checkpoint_integracion_y_eleccion_track/
├── track-a/
│   └── week-13-slam_toolbox_y_cartografiado/  … week-19-proyecto_final_entrega_y_demo/
└── track-b/
    └── week-13-moveit2_fundamentos_y_planning_scene/  … week-19-proyecto_final_entrega_y_demo/
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
├── 3-proyecto/                # Capa semanal del proyecto del track/dominio
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
- **`docs/`**: documentación transversal (setup, `stack-versions.md`, `tracks.md`,
  `hardware-opcional.md`, `dependency-security-policy.md`)
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

Cada semana añade **una capa nueva al mismo sistema del track y dominio del
estudiante**. Nunca un proyecto desechable por semana.

El README del proyecto incluye:

1. Qué capa se añade esta semana y por qué va aquí
2. Requisitos verificables (compila/lintea, tests que deben existir y pasar,
   comportamiento observable en simulación)
3. Cómo verificarlo: `colcon build && colcon test`, y si aplica,
   `scripts/verificar-simulaciones.sh week-NN`
4. Criterios de calidad más allá de lo automatizable
5. Adaptación al dominio con ejemplos para al menos las misiones del catálogo de
   `docs/tracks.md`

**Política de tracks + dominio**: el estudiante declara su dominio/misión en la Semana
01 y su track (A/B) en la Semana 12; ninguno cambia después. Ver `docs/tracks.md`.

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

- Python 3.12.3, `ament_python`, `package.xml` + `setup.py`
- Lint/format: `ruff` (reemplaza flake8+black+isort); tipado: `mypy` en modo estricto
  sobre el código propio (no sobre `rclpy`, que carece de stubs completos)
- Nomenclatura: `snake_case` para funciones/variables/archivos/paquetes; `PascalCase`
  para clases de nodo (`class OdometryFusionNode(Node): ...`)
- Todo nodo declara sus parámetros explícitamente (`self.declare_parameter(...)`) y su
  perfil de QoS cuando no usa el `QoSPresetProfiles` por defecto
- ✅ Type hints en toda función pública
- ❌ `except Exception:` desnudo — capturar la excepción concreta o dejar que se
  propague con contexto

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

- `<tu-track>` / `<tu-dominio>` para el track y la misión del estudiante
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
  lado a lado (semanas 01-05, 13-17). `simulación` para todo lo que ocurre solo en
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
6. `## ⏱️ Distribución del Tiempo (10 horas)`
7. `## 🎩 Trucos y atajos` (CLI de ROS2, `rqt`, RViz2, editor; mínimo cinco)
8. `## 📌 Entregables`
9. `## ✅ Verificación` (comandos `colcon`/simulación headless)
10. `## 🔧 Extensión Hardware (opcional)` — solo si aplica esa semana, siempre al final
    y en bloque `> [!NOTE]`, nunca mezclada con los pasos de simulación
11. `## 🔗 Navegación` (anterior / actual / siguiente)

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
3. **Producto 📦** (30%): la capa semanal del proyecto del track/dominio

Mínimo **70%** en cada tipo. Al ser autoestudio, el cuestionario incluye sus respuestas
en una sección colapsable (`<details>`) al final de la rúbrica.

Penalizaciones estándar del Producto:

| Situación | Penalización |
| --------- | ------------ |
| No compila/lintea limpio (`ruff`/`mypy` o `-Werror`) | 0 en Producto |
| Simulación no levanta headless | 0 en Producto |
| Plugin `pluginlib` escrito en Python | 0 en Producto |
| Nodo de actuador sin clamp de límites | -20 |
| Sin nodo C++ CORE donde la semana lo exige (13-17) sin justificación | -15 |
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
   antes de la 03, sin TF2/URDF antes de la 05, sin Gazebo antes de la 06, sin fusión
   sensorial antes de la 09, sin cinemática antes de la 11, sin SLAM/Nav2 ni MoveIt2
   antes de la 13, sin plugins `pluginlib` antes de su semana específica (14 en ambos
   tracks)
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
  Track B en vez de `moveit_commander` (deprecado)

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

- [ ] Estructura de carpetas completa (en `bootcamp/` o en `bootcamp/track-{a,b}/`
      según corresponda)
- [ ] `README.md` con las secciones obligatorias (incluida `🎩 Trucos y atajos`)
- [ ] Teoría en `1-teoria/`, un archivo por concepto (~250 líneas cada uno)
- [ ] Cada término técnico nuevo definido en su primera aparición
- [ ] Semanas 01-05: los dos ejercicios (`rclpy`/`rclcpp`) implementan el mismo
      concepto y son comparables
- [ ] Semanas 13-17: el ejercicio CORE en C++ existe, compila y su justificación de
      "por qué C++ aquí" está escrita en el README
- [ ] Prácticas con patrón descomentar, tests escritos en el starter, sin `solution/`
- [ ] `./scripts/verificar-simulaciones.sh week-NN` pasa si la semana tiene simulación
- [ ] `colcon build && colcon test` pasa (Python y C++)
- [ ] Proyecto que añade una capa al sistema del track/dominio, con adaptación por
      misión
- [ ] Ningún concepto usado antes de la semana en que se enseña
- [ ] Sección de hardware opcional (si aplica) en bloque `> [!NOTE]` al final, nunca
      bloqueante
- [ ] Recursos en las tres subcarpetas, cada uno con su justificación
- [ ] Glosario A-Z con el término/API en inglés entre paréntesis
- [ ] `rubrica-evaluacion.md` con cuestionario + respuestas en `<details>`
- [ ] SVG con la paleta del bootcamp, todos enlazados
- [ ] Navegación anterior/siguiente correcta
- [ ] `./scripts/verificar-enlaces.sh` sin errores

---

## 💡 Notas Finales

- **Prioridad**: profundidad sobre cobertura
- **Enfoque**: escribir y simular robótica, no leer sobre robótica
- **Objetivo**: formar a alguien capaz de leer y extender Nav2/MoveIt2, no solo
  configurarlos
- **Filosofía**: si no corre en simulación verificable y no tiene un test, no es un
  entregable

---

_Última actualización: septiembre de 2026_
