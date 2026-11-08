# 📖 Glosario — Semana 02

Términos A-Z. El término/API en inglés va entre paréntesis cuando existe en la
documentación oficial.

- **Calidad de servicio (Quality of Service, QoS)**: conjunto de reglas sobre cómo se
  entregan los mensajes de un topic (reintentos, historial, plazos).
- **Callback de evento (event callback)**: función que ROS2 llama cuando ocurre algo
  en una conexión, por ejemplo un QoS incompatible (`incompatible_qos`).
- **Compatibilidad pedido-ofrecido (Request vs Offered, RxO)**: regla por la que un
  publisher y un subscriber solo conectan si lo ofrecido es igual o mejor que lo pedido.
- **Constante (constant)**: línea `TIPO NOMBRE=valor` de un `.msg`; no viaja en el
  mensaje, da nombre a un valor fijo (`STATUS_OK=0`).
- **Deadline (deadline)**: política QoS que fija el tiempo máximo entre dos mensajes.
- **Depth (depth)**: tamaño del búfer de mensajes con `KEEP_LAST`.
- **Durabilidad (durability)**: política QoS que decide si un subscriber que llega
  tarde recibe mensajes anteriores (`TRANSIENT_LOCAL`) o no (`VOLATILE`).
- **Fiabilidad (reliability)**: política QoS que decide si se reintentan los mensajes
  perdidos (`RELIABLE`) o no (`BEST_EFFORT`).
- **Frame (frame)**: sistema de coordenadas con nombre desde el que se mide un dato;
  va en `header.frame_id`.
- **Header (`std_msgs/Header`)**: cabecera con `stamp` (cuándo) y `frame_id` (desde
  dónde) que llevan casi todos los mensajes de sensores.
- **Historial (history)**: política QoS que decide cuántos mensajes se guardan:
  `KEEP_LAST` (los últimos `depth`) o `KEEP_ALL`.
- **Interfaz (interface)**: nombre común de los mensajes (`.msg`), servicios (`.srv`)
  y acciones (`.action`).
- **Latched (latched)**: patrón de publicar una vez con `TRANSIENT_LOCAL` para que los
  subscribers tardíos reciban el último valor.
- **Lifespan (lifespan)**: política QoS que fija la edad máxima de un mensaje antes de
  descartarlo.
- **Liveliness (liveliness)**: política QoS que define cómo se detecta que un
  publisher sigue vivo.
- **Paquete de interfaces (interface package)**: paquete `ament_cmake`, normalmente
  con sufijo `_interfaces`, que solo contiene `.msg`/`.srv`/`.action`.
- **Perfil QoS (QoS profile)**: combinación concreta de políticas QoS
  (`QoSProfile` en Python, `rclcpp::QoS` en C++).
- **Preset QoS (QoS preset profile)**: perfil predefinido con nombre, como
  `sensor_data` o `services_default`.
- **`rosidl` (ROS Interface Definition Language)**: sistema que genera el código de
  cada lenguaje a partir de los archivos de interfaz.
- **Secuencia acotada (bounded sequence)**: array con tamaño máximo (`float64[<=16]`).
- **Stamp (`header.stamp`)**: instante en que se tomó el dato, con el reloj del nodo.
- **Tipo de mensaje (message type)**: definición de los campos de un mensaje,
  identificada como `paquete/msg/Nombre`.
- **Typesupport (type support)**: código generado que convierte un mensaje en bytes
  para DDS y de vuelta.
- **Valor por defecto (default value)**: valor que toma un campo si no lo rellenas,
  escrito tras su nombre en el `.msg` (`string unit "m"`).

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Recursos](../4-recursos/README.md) | **Glosario** | [Rúbrica](../rubrica-evaluacion.md) |

← [Volver a la Semana 02](../README.md)
