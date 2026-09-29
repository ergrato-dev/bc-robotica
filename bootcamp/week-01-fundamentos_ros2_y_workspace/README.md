# Semana 01 — Fundamentos ROS2 y Workspace

> El primer nodo que escribas define cómo vas a pensar los próximos 18: todo en ROS2 es un grafo de piezas pequeñas que se hablan por nombre, no un programa monolítico.

## 🎯 Objetivos de la Semana

- Entender el grafo computacional de ROS2 (nodos, topics) y por qué no hay "maestro"
- Compilar y activar un workspace ROS2 con `colcon`
- Escribir un publisher/subscriber equivalente en `rclpy` **y** en `rclcpp`
- Medir, no asumir: comparar ambos con `ros2 topic hz`

## 📋 Prerrequisitos

- Programación previa en Python y/o C++ (este bootcamp no enseña sintaxis básica)
- Entorno configurado — ver [docs/setup/con-docker.md](../../docs/setup/con-docker.md)
- Ninguna experiencia previa en ROS2 o robótica

## 🗂️ Estructura de la Semana

```
week-01-fundamentos_ros2_y_workspace/
├── README.md                       (este archivo)
├── rubrica-evaluacion.md
├── 0-assets/
│   └── 01-grafo-ros2.svg
├── 1-teoria/
│   ├── 01-que-es-ros2-y-el-grafo-computacional.md
│   ├── 02-workspace-colcon-y-paquetes.md
│   ├── 03-primer-nodo-rclpy.md
│   └── 04-primer-nodo-rclcpp.md
├── 2-practicas/
│   ├── ejercicio-01-publisher_subscriber_py/
│   ├── ejercicio-02-publisher_subscriber_cpp/
│   └── ejercicio-03-comparar_latencia/
├── 3-proyecto/
│   └── starter/ (proyecto_dominio_py/, proyecto_dominio_cpp/)
├── 4-recursos/
└── 5-glosario/
```

## 📝 Contenidos

### Teoría (≈2.5 h)

| Archivo | Tema |
|---|---|
| `01-que-es-ros2-y-el-grafo-computacional.md` | Qué es ROS2, nodos, topics, DDS |
| `02-workspace-colcon-y-paquetes.md` | Workspace, `colcon`, `ament_python` vs `ament_cmake` |
| `03-primer-nodo-rclpy.md` | Nodo mínimo y publisher en Python |
| `04-primer-nodo-rclcpp.md` | El mismo nodo y publisher en C++, comparado línea a línea |

### Prácticas (≈5 h)

| Ejercicio | Lenguaje | Qué construye |
|---|---|---|
| 01 | `rclpy` | Publisher + subscriber sobre `/sensor/state` |
| 02 | `rclcpp` | El mismo publisher + subscriber, en C++ |
| 03 | — (CLI) | Medición comparada con `ros2 topic hz` |

### Proyecto (≈2.5 h)

Arranque del workspace del dominio: dos paquetes (`proyecto_dominio_py`,
`proyecto_dominio_cpp`) con un nodo `sensor_stub` equivalente en ambos lenguajes. Ver
[3-proyecto/README.md](3-proyecto/README.md).

## ⏱️ Distribución del Tiempo (10 horas)

| Actividad | Horas |
|---|---|
| Teoría | 2.5 |
| Prácticas (Ejercicios 01-03) | 5.0 |
| Proyecto | 2.5 |

## 🎩 Trucos y atajos

- `ros2 doctor` — primer comando a correr si algo "no aparece" en el grafo
- `rqt_graph` — visualización gráfica; más rápido que leer `ros2 node info` a mano
- `colcon build --packages-select <paquete>` — compila solo lo que cambiaste, no todo
  el workspace
- `colcon build --symlink-install` — úsalo siempre en desarrollo con paquetes Python
- `ros2 topic hz /topic --window 20` — frecuencia media sobre los últimos 20 mensajes,
  más estable que mirar mensaje a mensaje

## 📌 Entregables

- Los tres ejercicios de `2-practicas/` con sus tests pasando
- `3-proyecto/` con ambos paquetes compilando, tu misión/dominio elegido y documentado
- Respuestas del Ejercicio 03 en el README de tu proyecto

## ✅ Verificación

```bash
colcon build --symlink-install
source install/setup.bash
colcon test
colcon test-result --verbose
```

## 🔗 Navegación

- **Anterior**: — (primera semana)
- **Actual**: Semana 01 — Fundamentos ROS2 y Workspace
- **Siguiente**: Semana 02 — Tópicos, QoS e Interfaces (pendiente de publicar)
