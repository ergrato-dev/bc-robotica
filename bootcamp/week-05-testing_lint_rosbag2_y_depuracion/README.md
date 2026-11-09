# Semana 05 — Testing, lint, rosbag2 y depuración

> Tu sistema ya arranca en orden y habla por topics, servicios y acciones. Antes de que crezca (launch files, TF, simulación, Nav2), necesita una red de seguridad: tests que avisen cuando algo se rompe, herramientas que lean el código por ti, grabaciones para repetir lo que pasó y un método para encontrar el fallo cuando "no llega nada".

## 🎯 Objetivos de la Semana

- Escribir tests unitarios con `pytest` y `gtest`, y de integración con `launch_testing`
- Comprobar que un test de verdad detecta fallos rompiendo el código a propósito
- Mantener el código limpio con `ruff`, `mypy`, `clang-format` y `clang-tidy`, ejecutados como tests
- Grabar, inspeccionar y reproducir topics con `ros2 bag`, y leer bags desde Python y C++
- Depurar un sistema con `ros2 node info`, `ros2 topic info -v`, `ros2 doctor` y los niveles de log

## 📋 Prerrequisitos

- [Semana 04](../week-04-executors_composicion_y_lifecycle/README.md) completada:
  executors, componentes y nodos lifecycle
- Tu proyecto del dominio de la Semana 04 compilando (esta semana lo cubres de tests)

## 🗂️ Estructura de la Semana

```
week-05-testing_lint_rosbag2_y_depuracion/
├── README.md                       (este archivo)
├── rubrica-evaluacion.md
├── 0-assets/
│   ├── 01-tres-niveles-de-test.svg
│   ├── 02-ciclo-de-launch-testing.svg
│   ├── 03-grabar-y-reproducir.svg
│   └── 04-metodo-de-depuracion.svg
├── 1-teoria/
│   ├── 01-tests-con-pytest-y-gtest.md
│   ├── 02-tests-de-integracion-con-launch-testing.md
│   ├── 03-lint-y-analisis-estatico.md
│   ├── 04-grabar-y-reproducir-con-rosbag2.md
│   └── 05-depuracion-y-ros2-doctor.md
├── 2-practicas/
│   ├── ejercicio-01-tests_y_rosbag2_py/
│   ├── ejercicio-02-gtest_y_rosbag2_cpp/
│   ├── ejercicio-03-lint_y_analisis_estatico/
│   └── ejercicio-04-depuracion_py/
├── 3-proyecto/
│   └── starter/ (proyecto_dominio_interfaces/, proyecto_dominio_py/, proyecto_dominio_cpp/)
├── 4-recursos/
└── 5-glosario/
```

## 📝 Contenidos

### Teoría (3.5 h)

| Archivo | Tema |
|---|---|
| [`01-tests-con-pytest-y-gtest.md`](1-teoria/01-tests-con-pytest-y-gtest.md) | Niveles de test, lógica separada del nodo, `pytest`, `gtest`, `colcon test-result` |
| [`02-tests-de-integracion-con-launch-testing.md`](1-teoria/02-tests-de-integracion-con-launch-testing.md) | `launch_testing`: arranque, tests activos, `proc_output`, códigos de salida |
| [`03-lint-y-analisis-estatico.md`](1-teoria/03-lint-y-analisis-estatico.md) | `ruff`, `mypy`, `clang-format`, `clang-tidy` y el lint como test |
| [`04-grabar-y-reproducir-con-rosbag2.md`](1-teoria/04-grabar-y-reproducir-con-rosbag2.md) | `ros2 bag record/info/play`, MCAP, `rosbag2_py` y `rosbag2_cpp` |
| [`05-depuracion-y-ros2-doctor.md`](1-teoria/05-depuracion-y-ros2-doctor.md) | Método de las cuatro preguntas, `ros2 doctor`, QoS incompatible, logs, tracebacks |

### Prácticas (6.5 h)

| Ejercicio | Lenguaje | Qué construye |
|---|---|---|
| 01 | `rclpy` | Tests de un filtro de distancia con `pytest` y `launch_testing`; grabación de una bag |
| 02 | `rclcpp` | El mismo filtro con `gtest`; lectura de bags con `rosbag2_cpp` y reproducción de la del 01 |
| 03 | `rclpy` + `rclcpp` | Monitor de batería limpio para `ruff`, `mypy`, `clang-format` y `clang-tidy` |
| 04 | `rclpy` | Dos nodos que no se hablan: tres fallos encontrados con el método de depuración |

### Proyecto (1.5 h)

`sensor_stub` gana lint como tests en las dos capas, un test de integración que
lo arranca en orden y una bag de referencia de tu misión. Ver
[3-proyecto/README.md](3-proyecto/README.md).

## ⏱️ Distribución del Tiempo (12 horas)

| Actividad | Horas |
|---|---|
| Teoría (01-05) | 3.5 |
| Ejercicio 01 (`pytest`, `launch_testing` y `rosbag2_py`) | 2.0 |
| Ejercicio 02 (`gtest` y `rosbag2_cpp`) | 1.5 |
| Ejercicio 03 (lint y análisis estático) | 1.5 |
| Ejercicio 04 (depuración) | 1.5 |
| Proyecto | 1.5 |
| Autoevaluación (rúbrica) | 0.5 |
| **Total** | **12.0** |

## 🎩 Trucos y atajos

- `colcon test-result --verbose` — solo los tests que fallan, con su mensaje
- `colcon test --packages-select <paquete> --pytest-args -k <nombre>` — un solo test de Python
- `ruff check --fix . && ruff format .` — arregla lo que se puede arreglar solo
- `ros2 bag info <bag>` — antes de usar una bag, mira `Count` por topic
- `ros2 doctor --report` — adjúntalo cuando pidas ayuda en un foro
- `--ros-args --log-level <nodo>:=debug` — los `DEBUG` de un solo nodo

## 📌 Entregables

- Los cuatro ejercicios de `2-practicas/` con sus tests pasando y sus checklists
  completos
- `3-proyecto/` con lint, test de integración y bag de referencia pasando en
  `colcon test`
- Respuestas de los cuatro ejercicios en el README de tu proyecto

## ✅ Verificación

Desde la raíz de tu workspace (la carpeta que contiene `src/`):

```bash
colcon build --symlink-install
source install/setup.bash
colcon test
colcon test-result --verbose
```

Cada test usa su propio dominio DDS (`ROS_DOMAIN_ID`), así que `colcon test` puede
correr paquetes en paralelo sin que sus nodos se mezclen.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 04](../week-04-executors_composicion_y_lifecycle/README.md) | **Semana 05** | [Semana 06](../week-06-launch_tf2_y_urdf/README.md) |

← [Volver al inicio del bootcamp](../../README.md)
