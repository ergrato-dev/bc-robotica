# Usar interfaces custom en Python y C++

> El `.msg` de la teoría 04 todavía no hace nada. Esta teoría lo conecta: un publisher Python y un subscriber C++ que se entienden porque comparten el mismo contrato, sin que ninguno sepa en qué lenguaje está escrito el otro.

## 🎯 Objetivos

- Declarar la dependencia de un paquete de interfaces en un paquete `ament_python` y en uno `ament_cmake`
- Importar e incluir un tipo propio (regla de nombres del header)
- Usar constantes y valores por defecto del `.msg` en ambos lenguajes
- Publicar un tipo propio desde la CLI con `ros2 topic pub`

## 1. Qué problema resuelve

Generar el código no basta: cada paquete que use el tipo tiene que **declarar** que
depende del paquete de interfaces. Si no lo hace, `colcon` puede compilarlo antes que
las interfaces (y el include no existe todavía) o Python no encuentra el módulo al
arrancar.

## 2. Cómo funciona: dependencias en tres sitios

| Dónde | `ament_python` | `ament_cmake` | Para qué |
|---|---|---|---|
| `package.xml` | `<exec_depend>ejemplo_interfaces</exec_depend>` | `<depend>ejemplo_interfaces</depend>` | `colcon` compila primero las interfaces; `rosdep` sabe qué instalar |
| `CMakeLists.txt` | — | `find_package(ejemplo_interfaces REQUIRED)` | CMake encuentra los headers y librerías generados |
| Target | — | `ament_target_dependencies(mi_nodo ... ejemplo_interfaces)` | Enlaza el ejecutable contra el tipo |

Python no compila, por eso solo necesita la dependencia de ejecución
(`exec_depend`). C++ la necesita para compilar **y** ejecutar: `depend` cubre ambas.

## 3. Publisher en Python, paso a paso

Paquete `ejemplo_reading_py` (ament_python). En `package.xml`, junto a `rclpy`:

```xml
<exec_depend>ejemplo_interfaces</exec_depend>
```

Nodo `ejemplo_reading_py/reading_publisher.py`:

```python
import rclpy
from rclpy.node import Node

# El módulo Python generado se llama como el paquete; el tipo, como el .msg.
from ejemplo_interfaces.msg import SensorReading


class ReadingPublisher(Node):
    def __init__(self) -> None:
        super().__init__("reading_publisher")
        self._publisher = self.create_publisher(SensorReading, "sensor/reading", 10)
        self._value = 0.5
        self._timer = self.create_timer(0.5, self._on_timer)

    def _on_timer(self) -> None:
        msg = SensorReading()
        # unit e is_valid ya valen "m" y True: son los valores por defecto del .msg.
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "range_sensor"
        msg.sensor_id = "front"
        msg.value = self._value
        # Constante del .msg en lugar de un 0 mágico.
        msg.status = SensorReading.STATUS_OK if self._value < 3.0 else SensorReading.STATUS_WARN
        self._publisher.publish(msg)
        self._value = 0.5 if self._value > 3.5 else self._value + 0.25


def main() -> None:
    rclpy.init()
    node = ReadingPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## 4. Subscriber en C++, paso a paso

Paquete `ejemplo_reading_cpp` (ament_cmake). En `package.xml`:

```xml
<depend>ejemplo_interfaces</depend>
```

En `CMakeLists.txt`:

```cmake
find_package(ejemplo_interfaces REQUIRED)

add_executable(reading_listener src/reading_listener.cpp)
ament_target_dependencies(reading_listener rclcpp ejemplo_interfaces)
```

Nodo `src/reading_listener.cpp`:

```cpp
#include "rclcpp/rclcpp.hpp"

#include <functional>
#include <memory>
// Regla del header: tipo SensorReading -> archivo sensor_reading.hpp
#include "ejemplo_interfaces/msg/sensor_reading.hpp"

using ejemplo_interfaces::msg::SensorReading;

class ReadingListener : public rclcpp::Node {
 public:
  ReadingListener() : Node("reading_listener") {
    subscription_ = create_subscription<SensorReading>(
        "sensor/reading", 10, std::bind(&ReadingListener::on_reading, this, std::placeholders::_1));
  }

 private:
  void on_reading(const SensorReading& msg) {
    if (msg.status != SensorReading::STATUS_OK) {
      RCLCPP_WARN(get_logger(), "%s fuera de rango: %.2f %s", msg.sensor_id.c_str(), msg.value,
                  msg.unit.c_str());
      return;
    }
    RCLCPP_INFO(get_logger(), "%s: %.2f %s", msg.sensor_id.c_str(), msg.value, msg.unit.c_str());
  }

  rclcpp::Subscription<SensorReading>::SharedPtr subscription_;
};

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ReadingListener>());
  rclcpp::shutdown();
  return 0;
}
```

`using ejemplo_interfaces::msg::SensorReading;` en un `.cpp` es correcto: acorta un
nombre largo sin contaminar a nadie. En un header, escribe el nombre completo.

### 4.1 Traducción de nombres entre lenguajes

| Concepto | Python | C++ |
|---|---|---|
| Importar | `from ejemplo_interfaces.msg import SensorReading` | `#include "ejemplo_interfaces/msg/sensor_reading.hpp"` |
| Tipo | `SensorReading` | `ejemplo_interfaces::msg::SensorReading` |
| Constante | `SensorReading.STATUS_OK` | `SensorReading::STATUS_OK` |
| Campo `string` | `msg.unit` (`str`) | `msg.unit` (`std::string`) |
| Campo `float64` | `msg.value` (`float`) | `msg.value` (`double`) |

## 5. Compilar y probar entre lenguajes

Desde la raíz del workspace (con los tres paquetes en `src/`):

```bash
colcon build --symlink-install
# Starting >>> ejemplo_interfaces
# Finished <<< ejemplo_interfaces [...]
# Starting >>> ejemplo_reading_py
# Starting >>> ejemplo_reading_cpp
# ...
# Summary: 3 packages finished [...]
source install/setup.bash
```

`colcon` compiló primero `ejemplo_interfaces` porque los otros dos lo declaran en su
`package.xml`. Ahora, en dos terminales:

```bash
# Terminal 1
ros2 run ejemplo_reading_py reading_publisher

# Terminal 2
ros2 run ejemplo_reading_cpp reading_listener
# [INFO] [...] [reading_listener]: front: 1.25 m
# [INFO] [...] [reading_listener]: front: 1.50 m
```

Y sin el publisher, desde la CLI (los campos que omites toman su valor por defecto):

```bash
ros2 topic pub --once /sensor/reading ejemplo_interfaces/msg/SensorReading \
  "{sensor_id: 'cli', value: 9.0, status: 1}"
# En la terminal 2:
# [WARN] [...] [reading_listener]: cli fuera de rango: 9.00 m
```

## 6. Errores típicos y su causa

| Mensaje | Causa | Arreglo |
|---|---|---|
| `ModuleNotFoundError: No module named 'ejemplo_interfaces'` | Terminal sin `source` tras compilar un paquete nuevo | `source install/setup.bash` |
| `fatal error: ejemplo_interfaces/msg/sensor_reading.hpp: No such file or directory` | Falta `find_package` o el paquete en `ament_target_dependencies` | Añadir las dos líneas de la sección 4 |
| `fatal error: ejemplo_interfaces/msg/SensorReading.hpp` | Include con el nombre del tipo en vez de snake_case | `sensor_reading.hpp` |
| `The message type 'ejemplo_interfaces/msg/SensorReading' is invalid` (CLI) | La terminal de la CLI no tiene el `source` | `source install/setup.bash` |
| El listener no recibe y no hay `[WARN]` | Nodo compilado contra una versión vieja del `.msg` | `colcon build --packages-up-to <paquete>` |

## 7. Antipatrones

- ❌ **Copiar el `.msg` a cada paquete que lo usa.** Dos copias divergen; con una
  dependencia hay un solo contrato
- ❌ **`depend` del paquete de interfaces solo en CMake y no en `package.xml`.**
  `colcon` puede compilar en el orden equivocado y el error aparece "a veces"
- ❌ **Comparar `msg.status == 1`.** Usa la constante: si alguien reordena los valores,
  el número deja de significar lo mismo

## 8. Trucos

- `colcon list --topological-order` — en qué orden compilará `colcon` tu workspace
- `colcon build --packages-up-to ejemplo_reading_cpp` — compila solo ese paquete y lo
  que necesita
- `ros2 interface proto ejemplo_interfaces/msg/SensorReading` — YAML completo para
  copiar en `ros2 topic pub`

## 📚 Recursos Adicionales

- [Creating custom msg and srv files (sección "Test the new interfaces") — ROS2 Jazzy](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html)
- [Implementing custom interfaces — ROS2 Jazzy](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Single-Package-Define-And-Use-Interface.html) (léelo para entender por qué este bootcamp prefiere el paquete aparte)

## ✅ Checklist de Verificación

- [ ] Sé qué dependencia declarar en un paquete Python y en uno C++
- [ ] Sé el nombre del header que corresponde a un tipo `PascalCase`
- [ ] Hice hablar un publisher Python con un subscriber C++ mediante un tipo propio
- [ ] Publiqué mi tipo desde la CLI con `ros2 topic pub --once`

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Interfaces custom](04-interfaces-custom-con-rosidl.md) | **05 · Usar interfaces en Python y C++** | [Prácticas](../2-practicas/README.md) |

← [Volver a la Semana 02](../README.md)
