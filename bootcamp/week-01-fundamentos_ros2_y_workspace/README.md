# Semana 01 — Fundamentos ROS2 y Workspace

> El primer nodo que escribas define cómo vas a pensar las próximas 32 semanas: todo en ROS2 es un grafo de piezas pequeñas que se hablan por nombre, no un programa monolítico.

## 🎯 Objetivos de la Semana

- Entender el grafo computacional de ROS2 (nodos, topics) y por qué no hay "maestro"
- Compilar y activar un workspace ROS2 con `colcon`
- Escribir un publisher/subscriber equivalente en `rclpy` **y** en `rclcpp`
- Medir, no asumir: comparar ambos con `ros2 topic hz`
- Inspeccionar el grafo con la CLI `ros2` y reconectar nodos con remapping y namespaces

## 📋 Prerrequisitos

- Programación previa en Python y/o C++ (este bootcamp no enseña sintaxis básica)
- Entorno configurado — ver [docs/setup/con-docker.md](../../docs/setup/con-docker.md)
- Ninguna experiencia previa en ROS2 o robótica
- Haber elegido tu misión/dominio del catálogo de [docs/dominios.md](../../docs/dominios.md)
  (o tenerla asignada)

## 🗂️ Estructura de la Semana

```
week-01-fundamentos_ros2_y_workspace/
├── README.md                       (este archivo)
├── rubrica-evaluacion.md
├── 0-assets/
│   ├── 01-grafo-ros2.svg
│   ├── 02-workspace-colcon-flujo.svg
│   ├── 03-ciclo-vida-nodo.svg
│   └── 04-remapping-y-namespaces.svg
├── 1-teoria/
│   ├── 01-que-es-ros2-y-el-grafo-computacional.md
│   ├── 02-workspace-colcon-y-paquetes.md
│   ├── 03-primer-nodo-rclpy.md
│   ├── 04-primer-nodo-rclcpp.md
│   └── 05-introspeccion-cli-nombres-y-remapping.md
├── 2-practicas/
│   ├── ejercicio-01-publisher_subscriber_py/
│   ├── ejercicio-02-publisher_subscriber_cpp/
│   ├── ejercicio-03-comparar_latencia/
│   └── ejercicio-04-explorar_grafo_cli/
├── 3-proyecto/
│   └── starter/ (proyecto_dominio_py/, proyecto_dominio_cpp/)
├── 4-recursos/
└── 5-glosario/
```

## 📝 Contenidos

### Teoría (3.5 h)

| Archivo | Tema |
|---|---|
| [`01-que-es-ros2-y-el-grafo-computacional.md`](1-teoria/01-que-es-ros2-y-el-grafo-computacional.md) | Qué es ROS2, nodos, topics, DDS |
| [`02-workspace-colcon-y-paquetes.md`](1-teoria/02-workspace-colcon-y-paquetes.md) | Workspace, `colcon`, `ament_python` vs `ament_cmake` |
| [`03-primer-nodo-rclpy.md`](1-teoria/03-primer-nodo-rclpy.md) | Nodo mínimo, publisher y subscriber en Python |
| [`04-primer-nodo-rclcpp.md`](1-teoria/04-primer-nodo-rclcpp.md) | Los mismos nodos en C++, comparados línea a línea |
| [`05-introspeccion-cli-nombres-y-remapping.md`](1-teoria/05-introspeccion-cli-nombres-y-remapping.md) | CLI `ros2`, nombres relativos/absolutos/privados, remapping y namespaces |

### Prácticas (6 h)

| Ejercicio | Lenguaje | Qué construye |
|---|---|---|
| 01 | `rclpy` | Publisher + subscriber sobre `/sensor/state` |
| 02 | `rclcpp` | El mismo publisher + subscriber, en C++ |
| 03 | — (CLI) | Medición comparada con `ros2 topic hz` |
| 04 | — (CLI) | Introspección, `ROS_DOMAIN_ID` y remapping entre tus nodos Python y C++ |

### Proyecto (2 h)

Arranque del workspace del dominio: dos paquetes (`proyecto_dominio_py`,
`proyecto_dominio_cpp`) con un nodo `sensor_stub` equivalente en ambos lenguajes. Ver
[3-proyecto/README.md](3-proyecto/README.md).

## ⏱️ Distribución del Tiempo (12 horas)

| Actividad | Horas |
|---|---|
| Teoría (01-05) | 3.5 |
| Ejercicios 01 y 02 (`rclpy` y `rclcpp`) | 3.5 |
| Ejercicio 03 (medición) | 1.0 |
| Ejercicio 04 (CLI y remapping) | 1.5 |
| Proyecto | 2.0 |
| Autoevaluación (rúbrica) | 0.5 |
| **Total** | **12.0** |

## 🎩 Trucos y atajos

- `ros2 doctor` — primer comando a correr si algo "no aparece" en el grafo
- `rqt_graph` — visualización gráfica; más rápido que leer `ros2 node info` a mano
- `colcon build --packages-select <paquete>` — compila solo lo que cambiaste, no todo
  el workspace
- `colcon build --symlink-install` — úsalo siempre en desarrollo con paquetes Python
- `ros2 topic hz /topic --window 20` — frecuencia media sobre los últimos 20 mensajes,
  más estable que mirar mensaje a mensaje

## 📌 Entregables

- Los cuatro ejercicios de `2-practicas/`: 01 y 02 con sus tests pasando, 03 y 04 con
  su checklist completo
- `3-proyecto/` con ambos paquetes compilando, tu misión/dominio elegido y documentado
- Respuestas de los Ejercicios 03 y 04 en el README de tu proyecto

## ✅ Verificación

Desde la raíz de tu workspace (la carpeta que contiene `src/`):

```bash
colcon build --symlink-install
source install/setup.bash
colcon test
colcon test-result --verbose
```

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Índice de semanas](../README.md) | **Semana 01** | [Semana 02](../week-02-topicos_qos_e_interfaces/README.md) |

← [Volver al inicio del bootcamp](../../README.md)
