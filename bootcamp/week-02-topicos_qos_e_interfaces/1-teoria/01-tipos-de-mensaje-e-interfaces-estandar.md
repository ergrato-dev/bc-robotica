# Tipos de mensaje e interfaces estándar

> `std_msgs/String` te sirvió para arrancar, pero un robot no se describe con texto libre: una distancia necesita su unidad, su instante de medida y el sensor que la tomó. Los tipos de mensaje son el contrato entre nodos.

## 🎯 Objetivos

- Leer la definición de cualquier tipo de mensaje con `ros2 interface show`
- Conocer los tipos primitivos de ROS2 y cómo se traducen a Python y a C++
- Saber qué paquetes estándar existen (`geometry_msgs`, `sensor_msgs`...) antes de inventar uno
- Rellenar un `std_msgs/Header` (`stamp` y `frame_id`) y entender por qué casi todo sensor lo lleva

## 1. Qué problema resuelve

En la Semana 01 publicaste `"lectura #7"` en un `std_msgs/String`. Para el nodo que lo
recibe, eso no es un dato: tendría que "parsear" el texto, adivinar la unidad y no
sabría cuándo se midió.

Un **tipo de mensaje** (message type) define los campos que viajan por un topic, cada
uno con su tipo de dato. Publisher y subscriber deben usar exactamente el mismo tipo
(teoría 03 de la Semana 01): por eso el tipo funciona como un **contrato**. Si el
contrato es pobre (`String`), cada consumidor lo interpreta a su manera.

En ROS2, los mensajes (`.msg`), servicios (`.srv`, Semana 03) y acciones (`.action`,
Semana 03) se llaman en conjunto **interfaces**. Esta semana usas las estándar (esta
teoría) y escribes las tuyas (teorías 04 y 05).

## 2. Cómo funciona: nombre completo y campos

Toda interfaz se identifica por `paquete/tipo_de_interfaz/Nombre`:

```text
sensor_msgs/msg/Range
│           │   └── nombre del tipo (PascalCase)
│           └────── msg = mensaje (srv = servicio, action = acción)
└────────────────── paquete que lo define
```

La definición es un archivo de texto con una línea por campo: `tipo nombre`. Un campo
puede ser **primitivo** o **compuesto** (otro mensaje, que a su vez tiene campos).

### 2.1 Tipos primitivos y su traducción

| En el `.msg` | Python (`rclpy`) | C++ (`rclcpp`) | Ejemplo de uso |
|---|---|---|---|
| `bool` | `bool` | `bool` | `is_valid` |
| `int32` / `int64` | `int` | `int32_t` / `int64_t` | contador |
| `uint8` | `int` | `uint8_t` | código de estado |
| `float32` | `float` | `float` | distancia de un sensor barato |
| `float64` | `float` | `double` | posición, velocidad |
| `string` | `str` | `std::string` | `frame_id`, identificador |
| `float64[3]` (tamaño fijo) | `numpy.ndarray` de 3 | `std::array<double, 3>` | vector 3D |
| `float64[]` (sin límite) | `array.array('d')` | `std::vector<double>` | lecturas de un barrido |
| `float64[<=10]` (acotado) | `array.array('d')` | secuencia acotada (máx. 10) | hasta 10 lecturas |
| `string<=32` (acotado) | `str` | `std::string` | nombre corto |

Python no comprueba los rangos al escribir el campo: si asignas `300` a un `uint8`,
el error salta al publicar (`AssertionError` en rclpy). En C++, `uint8_t` desborda en
silencio. Elige el tipo pensando en el rango real del dato.

### 2.2 Constantes

Una línea con `=` define una **constante**, no un campo: no viaja en el mensaje, es un
nombre para un valor fijo.

```text
uint8 ULTRASOUND=0
uint8 INFRARED=1
uint8 radiation_type
```

Se usan como `Range.ULTRASOUND` en Python y `sensor_msgs::msg::Range::ULTRASOUND` en
C++. Así nadie escribe un `0` mágico.

## 3. Paquetes estándar: búscalos antes de inventar

| Paquete | Para qué | Tipos que verás pronto |
|---|---|---|
| `std_msgs` | Prototipos y `Header` | `Header`, `String` (solo pruebas) |
| `builtin_interfaces` | Tiempo | `Time`, `Duration` |
| `geometry_msgs` | Geometría | `Point`, `Pose`, `Twist` (velocidad, Semana 08) |
| `sensor_msgs` | Sensores | `Range`, `LaserScan` (Semana 09), `Imu`, `Image`, `BatteryState` |
| `nav_msgs` | Navegación | `Odometry` (Semana 12), `OccupancyGrid` (Semana 14) |

La documentación de `std_msgs` lo dice expresamente: tipos como `String` o `Float64`
no tienen significado y sirven para prototipos. Para datos con significado, usa un tipo
semántico o crea el tuyo.

### 3.1 El `Header`: cuándo y dónde

```bash
ros2 interface show std_msgs/msg/Header
```

Las líneas de campo (sin los comentarios) son:

```text
builtin_interfaces/Time stamp
	int32 sec
	uint32 nanosec
string frame_id
```

- `stamp` — **cuándo** se tomó el dato (segundos + nanosegundos). No cuándo se
  publicó: si procesas una imagen 80 ms, el `stamp` sigue siendo el de la captura
- `frame_id` — **desde dónde** se midió: el nombre del sistema de coordenadas del
  sensor (frame). En la Semana 06 conectas estos nombres con TF2; por ahora basta con
  un nombre fijo y descriptivo (`"range_sensor"`)

Con `stamp` y `frame_id` vacíos, ningún nodo de las semanas siguientes (RViz2, TF2,
Nav2) puede usar tu dato.

## 4. Cómo se usa, paso a paso

### 4.1 Explorar desde la terminal

```bash
ros2 interface list | grep sensor_msgs/msg
# sensor_msgs/msg/BatteryState
# sensor_msgs/msg/Image
# ...
# sensor_msgs/msg/Range
# ...

ros2 interface show sensor_msgs/msg/Range
```

Quitando los comentarios y el desglose del `Header`, quedan estos campos y constantes:

```text
std_msgs/Header header
uint8 ULTRASOUND=0
uint8 INFRARED=1
uint8 radiation_type
float32 field_of_view
float32 min_range
float32 max_range
float32 range
float32 variance
```

`ros2 interface proto sensor_msgs/msg/Range` imprime un mensaje vacío en YAML, listo
para copiar en `ros2 topic pub`.

### 4.2 Rellenar un `Range` en Python

```python
from rclpy.node import Node
from sensor_msgs.msg import Range


def build_range(node: Node, distance_m: float) -> Range:
    msg = Range()
    # stamp: el reloj del nodo, no time.time(). Así funciona igual con tiempo
    # simulado (Semana 08), donde el reloj lo marca Gazebo.
    msg.header.stamp = node.get_clock().now().to_msg()
    msg.header.frame_id = "range_sensor"
    msg.radiation_type = Range.ULTRASOUND
    msg.field_of_view = 0.5  # rad, unos 29°
    msg.min_range = 0.02  # m
    msg.max_range = 4.0  # m
    msg.range = distance_m
    return msg
```

### 4.3 El mismo mensaje en C++

```cpp
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/range.hpp"

sensor_msgs::msg::Range build_range(rclcpp::Node& node, float distance_m) {
  sensor_msgs::msg::Range msg;
  // node.now() devuelve rclcpp::Time, que se convierte solo a builtin_interfaces/Time.
  msg.header.stamp = node.now();
  msg.header.frame_id = "range_sensor";
  msg.radiation_type = sensor_msgs::msg::Range::ULTRASOUND;
  msg.field_of_view = 0.5F;
  msg.min_range = 0.02F;
  msg.max_range = 4.0F;
  msg.range = distance_m;
  return msg;
}
```

Fíjate en la regla del include: el tipo `Range` (PascalCase) vive en
`sensor_msgs/msg/range.hpp` (snake_case). `BatteryState` estaría en
`battery_state.hpp`. La misma regla aplica a tus tipos propios (teoría 05).

### 4.4 Unidades: siempre SI

La convención de ROS (REP 103) es el Sistema Internacional: metros, radianes,
segundos, kilogramos. `field_of_view = 0.5` son radianes, no grados. Si tu sensor da
centímetros, conviertes **antes** de publicar.

## 5. Antipatrones

- ❌ **JSON dentro de un `std_msgs/String`.** Pierdes el contrato: el compilador no
  avisa si un campo cambia de nombre y cada consumidor parsea a su manera
- ❌ **`stamp` con `time.time()` o `std::chrono`.** Rompe en simulación, donde el reloj
  del sistema y el de ROS no coinciden. Usa siempre el reloj del nodo
- ❌ **`frame_id` vacío "porque aún no hay TF".** Pon un nombre ya; en la Semana 06 lo
  conectas. Cambiar un nombre es más fácil que añadirlo después en diez nodos
- ❌ **Grados, centímetros o milisegundos en un campo.** Unidades SI siempre
- ❌ **Inventar `MyDistance.msg` cuando existe `sensor_msgs/Range`.** RViz2 y el resto
  del ecosistema ya entienden los tipos estándar; los tuyos, no

## 6. Trucos

- `ros2 interface package sensor_msgs` — todos los tipos de un paquete
- `ros2 interface proto <tipo>` — YAML de ejemplo para `ros2 topic pub`
- `ros2 topic echo /topic --field header.stamp` — ver solo el timestamp
- En Python, `print(msg)` muestra todos los campos: útil en un test, nunca en un nodo
  (usa el logger)

## 📚 Recursos Adicionales

- [Interfaces — ROS2 Jazzy concepts](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Interfaces.html)
- [common_interfaces (std_msgs, sensor_msgs, geometry_msgs...) — GitHub](https://github.com/ros2/common_interfaces/tree/jazzy)
- [REP 103 — Standard Units of Measure and Coordinate Conventions](https://www.ros.org/reps/rep-0103.html)

## ✅ Checklist de Verificación

- [ ] Sé leer `paquete/msg/Tipo` y encontrar su definición con `ros2 interface show`
- [ ] Sé a qué tipo de Python y de C++ corresponde `float64[]` y `float32`
- [ ] Rellené un `Header` con el reloj del nodo y un `frame_id`
- [ ] Sé por qué no conviene usar `std_msgs/String` para datos con significado

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 02](../README.md) | **01 · Tipos de mensaje** | [02 · Políticas QoS](02-qos-politicas-y-compatibilidad.md) |

← [Volver a la Semana 02](../README.md)
