# 📖 Glosario — Semana 01

Términos A-Z. El término/API en inglés va entre paréntesis cuando existe en la
documentación oficial.

- **Acción (action)**: comunicación para tareas largas, con feedback de progreso y
  posibilidad de cancelar. Se detalla en la Semana 03.
- **`ament_cmake`**: tipo de build de un paquete ROS2 escrito en C++, basado en CMake.
- **`ament_python`**: tipo de build de un paquete ROS2 escrito en Python, basado en
  `setuptools`.
- **CLI (Command Line Interface)**: interfaz de línea de comandos; en ROS2, el comando
  `ros2` y sus subcomandos (`node`, `topic`, `interface`...) para inspeccionar el grafo.
- **Callback (callback)**: función que entregas a ROS2 para que la llame cuando ocurre
  algo (llega un mensaje, vence un timer).
- **`colcon`**: herramienta de build que compila/instala todos los paquetes de un
  workspace ROS2, sin importar su lenguaje.
- **Daemon de la CLI (`ros2 daemon`)**: proceso en segundo plano que guarda una copia
  del grafo para que los comandos `ros2` respondan rápido. Se reinicia con
  `ros2 daemon stop`.
- **DDS (Data Distribution Service)**: estándar de transporte que usa ROS2 por debajo;
  permite que los nodos se descubran entre sí sin un proceso central.
- **Espacio de nombres (namespace)**: prefijo que agrupa nodos y topics (`/robot1/...`);
  permite tener varias copias del mismo sistema en un grafo.
- **Executor (executor)**: el objeto que decide cómo y cuándo se procesan los
  callbacks de un nodo (single-threaded vs multi-threaded). Se detalla en la Semana 04.
- **Grafo computacional (computation graph)**: la red de nodos y sus conexiones
  (topics, servicios, acciones) en un sistema ROS2 en marcha.
- **Nombre absoluto, relativo y privado (fully qualified, relative, private name)**:
  `/chatter` ignora el namespace; `chatter` se cuelga del namespace; `~/chatter` se
  cuelga del nombre del nodo.
- **Nodo (node)**: un proceso (o parte de uno) que aparece en el grafo con un nombre
  único.
- **Paquete (package)**: la unidad de distribución de código en ROS2 — tiene un
  `package.xml` y es lo que `colcon` compila/instala.
- **QoS (Quality of Service)**: configuración de cómo se entregan los mensajes de un
  topic (confiabilidad, historial...). Se detalla a fondo en la Semana 02.
- **`rclcpp`**: la librería cliente oficial de ROS2 para C++.
- **`rclpy`**: la librería cliente oficial de ROS2 para Python.
- **Reasignación de nombres (remapping)**: cambiar al arrancar un nodo el nombre de un
  topic, del nodo (`__node`) o su namespace (`__ns`) con `--ros-args -r origen:=destino`,
  sin tocar el código.
- **`ROS_DOMAIN_ID`**: variable de entorno que aísla grupos de nodos en la misma red —
  evita que dos grafos distintos en la misma WiFi se mezclen.
- **Servicio (service)**: comunicación síncrona de petición/respuesta. Se detalla en la
  Semana 03.
- **Subscriber (subscriber)**: la pieza de un nodo que recibe los mensajes de un topic
  y llama a su callback por cada uno.
- **Spin (spin)**: el bucle que mantiene vivo un nodo, procesando sus callbacks
  pendientes (`rclpy.spin()` / `rclcpp::spin()`).
- **Topic (topic)**: un canal con nombre y tipo de mensaje fijo, al que cualquier nodo
  puede publicar o suscribirse.
- **Workspace (workspace)**: el directorio raíz que contiene `src/`, `build/`,
  `install/` y `log/` de tu proyecto ROS2.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Recursos](../4-recursos/README.md) | **Glosario** | [Rúbrica](../rubrica-evaluacion.md) |

← [Volver a la Semana 01](../README.md)
