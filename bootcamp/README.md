# Bootcamp Robótica — Zero to Advanced

33 semanas · 12 h/semana · 396 horas. Autoestudio asincrónico sobre ROS2 Jazzy, en una ruta única: robot móvil autónomo, brazo manipulador, manipulación móvil y bloque avanzado, sobre un solo sistema de **tu dominio** que crece cada semana ([`docs/dominios.md`](../docs/dominios.md)).

La columna **Estado** dice la verdad sobre el repositorio: ✅ la semana está publicada al estándar de [`CLAUDE.md`](../CLAUDE.md), ⬜ todavía no se escribió. Las semanas sin publicar no llevan enlace. El contenido se escribe en orden.

---

## Índice de Semanas

### Fase 1 — Fundamentos ROS2 bilingüe (S01-06, 72 h)

| Semana | Tema | Estado |
|:--:|---|:--:|
| [01](week-01-fundamentos_ros2_y_workspace/README.md) | Grafo ROS2/DDS, `colcon`, `ament_python` vs `ament_cmake` | ✅ |
| 02 | QoS profiles, `.msg` custom (`rosidl`) | ⬜ |
| 03 | Servicios, acciones, parámetros | ⬜ |
| 04 | Executors, callback groups, component containers, lifecycle nodes | ⬜ |
| 05 | `pytest`/`gtest`, `launch_testing`, `ruff`/`mypy`/`clang-tidy`, `rosbag2`, `ros2 doctor` | ⬜ |
| 06 | Launch files, TF2, URDF/xacro | ⬜ |

### Fase 2 — Matemáticas, simulación y control (S07-12, 72 h)

| Semana | Tema | Estado |
|:--:|---|:--:|
| 07 | Matrices homogéneas, ángulos de Euler, cuaterniones, `tf_transformations` | ⬜ |
| 08 | `gz-sim`, SDF, `ros_gz_bridge`, spawn, teleop | ⬜ |
| 09 | `sensor_msgs` (LiDAR, cámara, IMU), plugins de sensor, RViz2 | ⬜ |
| 10 | `ros2_control`, hardware interface, `diff_drive_controller`, `joint_trajectory_controller` | ⬜ |
| 11 | `cv_bridge`, filtros, color/forma, calibración de cámara, ArUco | ⬜ |
| 12 | Odometría, ruido, `robot_localization` EKF | ⬜ |

### Fase 3 — Robot móvil autónomo (S13-18, 72 h)

| Semana | Tema | Estado |
|:--:|---|:--:|
| 13 | Cinemática diferencial, PID, pure pursuit | ⬜ |
| 14 | SLAM online/offline, guardar/cargar mapa | ⬜ |
| 15 | AMCL, costmaps 2D, capas | ⬜ |
| 16 | NavFn/Smac, DWB/RPP/MPPI, `nav2_simple_commander` | ⬜ |
| 17 | BT XML, BT.CPP, recovery, waypoints | ⬜ |
| 18 | Misión multi-objetivo, manejo de fallos, checkpoint móvil | ⬜ |

### Fase 4 — Manipulación (S19-24, 72 h)

| Semana | Tema | Estado |
|:--:|---|:--:|
| 19 | Brazo serie, DH, FK, IK numérica, Jacobiano | ⬜ |
| 20 | Arquitectura MoveIt2, Setup Assistant, planning scene | ⬜ |
| 21 | Planners OMPL, collision objects, restricciones | ⬜ |
| 22 | Point clouds, PCL, segmentación, calibración hand-eye | ⬜ |
| 23 | `GripperCommand`, grasp planning, MoveIt Task Constructor | ⬜ |
| 24 | Pipeline pick&place completo, fallos, checkpoint manipulación | ⬜ |

### Fase 5 — Avanzado (S25-30, 72 h)

| Semana | Tema | Estado |
|:--:|---|:--:|
| 25 | YOLO (`ultralytics`) vs clásico, benchmarking | ⬜ |
| 26 | Nav2 + MoveIt2 en un mismo robot, coordinación base-brazo | ⬜ |
| 27 | Namespaces, `ROS_DOMAIN_ID`, TF multi-robot, flotas | ⬜ |
| 28 | `ros2_tracing`, intra-process, zero-copy (loaned messages), kernel RT | ⬜ |
| 29 | SROS2, Docker multi-stage, CI con GitHub Actions | ⬜ |
| 30 | micro-ROS, agente, plataforma host (hardware opcional) | ⬜ |

### Fase 6 — Capstone (S31-33, 36 h)

| Semana | Tema | Estado |
|:--:|---|:--:|
| 31 | Diseño del sistema del dominio, ADR, interfaces | ⬜ |
| 32 | Sistema completo del dominio | ⬜ |
| 33 | Pulido, documentación, demo, hardware opcional | ⬜ |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Hardware opcional](../docs/hardware-opcional.md) | **Índice de semanas** | [Semana 01](week-01-fundamentos_ros2_y_workspace/README.md) |

← [Volver al inicio del bootcamp](../README.md)
