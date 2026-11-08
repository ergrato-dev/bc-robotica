# Primer nodo en C++ (`rclcpp`)

> `rclcpp` es la librería cliente oficial de ROS2 para C++. El mismo publisher de la teoría anterior, ahora en C++ — compáralos línea a línea: la API es deliberadamente paralela.

## 🎯 Objetivos

- Escribir un nodo `rclcpp` mínimo equivalente al de `rclpy`
- Entender `rclcpp::spin` y por qué usa `shared_ptr`
- Compilarlo con `ament_cmake` y ejecutarlo con `ros2 run`

## 1. Qué problema resuelve

Mismo problema que en Python: registrar un proceso en el grafo, crear
publishers/timers, mantenerlo vivo. La diferencia no es de fondo — es de lenguaje: C++
exige gestión explícita de memoria (resuelta con `shared_ptr`) y tipado estático en
tiempo de compilación en vez de en tiempo de ejecución.

**Por qué te importa C++ desde la Semana 01**: no es un añadido "para los que ya saben
C++". Nav2 y MoveIt2 (que vas a usar en las semanas 13-17) exponen sus puntos de
extensión — `pluginlib` — **solo** en C++, porque no existe binding Python. Aprender
`rclcpp` en paralelo a `rclpy` desde el día uno significa que cuando llegues a esas
semanas, la sintaxis de nodo ya te es familiar y solo tienes que aprender lo nuevo de
cada framework.

## 2. Cómo funciona: el ciclo de vida de un nodo

```cpp
#include "rclcpp/rclcpp.hpp"

class SensorPublisher : public rclcpp::Node {
public:
  SensorPublisher() : Node("sensor_publisher") {
    // aquí se crean publishers, subscribers, timers...
  }
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);                          // equivalente a rclpy.init()
  auto node = std::make_shared<SensorPublisher>();
  rclcpp::spin(node);                                 // equivalente a rclpy.spin(node)
  rclcpp::shutdown();                                  // equivalente a rclpy.shutdown()
  return 0;
}
```

Compara con la versión Python de la teoría anterior: el orden de los pasos —
`init → construir nodo → spin → shutdown`— es idéntico. Lo que cambia es la sintaxis:
herencia de `rclcpp::Node` con inicialización en la lista de constructor
(`Node("sensor_publisher")`), y `std::make_shared` en vez de una instancia directa,
porque `rclcpp::spin` necesita un `shared_ptr` (el nodo puede ser referenciado por
varios callbacks internos a la vez).

## 3. Cómo se escribe: publisher con timer

```cpp
#include <chrono>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class SensorPublisher : public rclcpp::Node {
public:
  SensorPublisher() : Node("sensor_publisher"), counter_{0} {
    publisher_ = create_publisher<std_msgs::msg::String>("sensor/state", 10);
    timer_ = create_wall_timer(500ms, std::bind(&SensorPublisher::on_timer, this));
  }

private:
  void on_timer() {
    auto msg = std_msgs::msg::String();
    msg.data = "lectura #" + std::to_string(counter_);
    publisher_->publish(msg);
    RCLCPP_INFO(get_logger(), "Publicado: %s", msg.data.c_str());
    counter_++;
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  int counter_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SensorPublisher>());
  rclcpp::shutdown();
  return 0;
}
```

Comparación directa con la versión Python:

| Concepto | `rclpy` | `rclcpp` |
|---|---|---|
| Crear publisher | `self.create_publisher(String, "sensor/state", 10)` | `create_publisher<std_msgs::msg::String>("sensor/state", 10)` |
| Crear timer | `self.create_timer(0.5, self._on_timer)` | `create_wall_timer(500ms, std::bind(&SensorPublisher::on_timer, this))` |
| Loguear | `self.get_logger().info(...)` | `RCLCPP_INFO(get_logger(), ...)` |
| Mantener vivo | `rclpy.spin(node)` | `rclcpp::spin(node)` |

`std::bind(&SensorPublisher::on_timer, this)` es la forma de pasar un método de la
clase como callback — en Python `self._on_timer` ya es un objeto invocable con `self`
ligado; en C++ hay que ligarlo explícitamente. Una lambda (`[this]() { on_timer(); }`)
hace lo mismo y es igual de válida — verás ambos estilos en el ecosistema ROS2.

### 3.2 El otro extremo: subscriber

El mismo `sensor_listener` de la teoría 03, en C++:

```cpp
#include <functional>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class SensorListener : public rclcpp::Node {
public:
  SensorListener() : Node("sensor_listener") {
    // std::placeholders::_1 es "el primer argumento que pasará ROS2": el mensaje.
    subscription_ = create_subscription<std_msgs::msg::String>(
        "sensor/state", 10,
        std::bind(&SensorListener::on_message, this, std::placeholders::_1));
  }

private:
  void on_message(const std_msgs::msg::String &msg) const {
    RCLCPP_INFO(get_logger(), "Recibido: %s", msg.data.c_str());
  }

  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SensorListener>());
  rclcpp::shutdown();
  return 0;
}
```

| Concepto | `rclpy` | `rclcpp` |
|---|---|---|
| Crear subscriber | `self.create_subscription(String, "sensor/state", cb, 10)` | `create_subscription<std_msgs::msg::String>("sensor/state", 10, cb)` |
| Orden de argumentos | tipo, topic, callback, depth | (tipo como plantilla), topic, depth, callback |
| Firma del callback | `def cb(self, msg: String) -> None` | `void cb(const std_msgs::msg::String &msg) const` |
| Guardar la referencia | `self._subscription = ...` | miembro `subscription_` |

Ojo al orden: en C++ el `depth` va **antes** del callback; en Python, después. Es el
error de compilación más frecuente al portar un nodo de un lenguaje al otro.

Recibir el mensaje por `const &` evita copiarlo. Con un `String` da igual; con una nube
de puntos de varios MB (Semana 22) es la diferencia entre llegar a la frecuencia o no.

Como el topic es el mismo, puedes **mezclar lenguajes**: publisher C++ y listener Python
se conectan sin cambiar nada, porque ambos hablan DDS por debajo:

```bash
# Terminal 1
ros2 run ejercicio02_pubsub_cpp sensor_publisher
# Terminal 2
ros2 run ejercicio01_pubsub_py sensor_listener
# [INFO] [...] [sensor_listener]: Recibido: lectura #3
```

## 4. Antipatrones

- ❌ **Guardar el nodo en un `rclcpp::Node` (valor) en vez de `shared_ptr<Node>`.**
  `rclcpp::spin` exige un `shared_ptr`; si intentas pasarle otra cosa, no compila
- ❌ **`new SensorPublisher()` crudo.** Siempre `std::make_shared<SensorPublisher>()` —
  gestión de memoria manual en nodos ROS2 no tiene ninguna ventaja y sí varias formas
  de fallar
- ❌ **Olvidar `rclcpp::shutdown()`.** A diferencia de Python, aquí no hay recolector de
  basura que limpie los recursos DDS por ti al terminar el proceso de forma poco
  ordenada
- ❌ **Capturar `this` por valor en una lambda que sobrevive al nodo.** Si el nodo se
  destruye y la lambda sigue viva (ej. guardada en otro sitio), acceder a `this` es
  comportamiento indefinido. En callbacks de timer/subscripción esto no pasa porque su
  ciclo de vida está ligado al nodo, pero es el error clásico al reusar lambdas fuera
  de ese contexto

## 5. Trucos

- `ros2 topic hz /sensor/state` funciona igual sin importar si el publisher es Python o
  C++ — ROS2 CLI no le importa el lenguaje del nodo, solo habla DDS
- `colcon build --packages-select mi_paquete_cpp --event-handlers console_direct+` —
  ver el output de compilación en vivo en vez de solo al final
- `RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 1000, "...")` — equivalente C++ al
  `throttle_duration_sec` de `rclpy`, limita la frecuencia de un log

## 📚 Recursos Adicionales

- [Writing a simple publisher and subscriber (C++) — ROS2 Jazzy docs](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html)
- [rclcpp API reference](https://docs.ros2.org/latest/api/rclcpp/)

## ✅ Checklist de Verificación

- [ ] Puedo escribir de memoria el esqueleto `init → Node → spin → shutdown` en C++
- [ ] Entiendo por qué `rclcpp::spin` necesita un `shared_ptr`, no un valor
- [ ] Comparé mi nodo `rclcpp` con el `rclpy` equivalente y ubico cada diferencia de
      sintaxis con lo que hace en Python

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Primer nodo rclpy](03-primer-nodo-rclpy.md) | **04 · Primer nodo rclcpp** | [05 · Introspección CLI y remapping](05-introspeccion-cli-nombres-y-remapping.md) |

← [Volver a la Semana 01](../README.md)
