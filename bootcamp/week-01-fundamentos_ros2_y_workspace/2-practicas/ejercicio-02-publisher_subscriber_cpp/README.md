# Ejercicio 02 — Publisher/Subscriber en C++ (`rclcpp`)

El mismo ejercicio del `rclpy`, ahora en C++. Mismo topic (`/sensor/state`), mismo tipo
de mensaje (`std_msgs/String`) — para que compruebes que un nodo Python y uno C++ se
hablan sin ningún adaptador.

> En C++, a diferencia de Python, los **miembros de la clase ya están declarados** en
> el starter (declarar un `shared_ptr` vacío no rompe la compilación). Lo que
> descomentas es la **inicialización** en el constructor. Si comentaras la declaración
> del miembro, el archivo no compilaría en absoluto — eso lo tienes que evitar siempre
> que edites un starter C++.

## Abrir el starter

```bash
cd bootcamp/week-01-fundamentos_ros2_y_workspace/2-practicas/ejercicio-02-publisher_subscriber_cpp/starter
```

Estructura:

```
starter/
├── package.xml
├── CMakeLists.txt
├── include/ejercicio02_pubsub_cpp/
│   ├── sensor_publisher.hpp    # PASO 1 y 2
│   └── sensor_listener.hpp     # PASO 3
├── src/
│   ├── sensor_publisher_main.cpp   # solo main(): no se toca
│   └── sensor_listener_main.cpp    # solo main(): no se toca
└── test/
    └── test_pubsub.cpp          # tests ya escritos (gtest), fallan hasta completar los pasos
```

## Paso 1: El publisher crea su canal

**Abre `include/ejercicio02_pubsub_cpp/sensor_publisher.hpp`** y descomenta la línea de inicialización de
`publisher_` en el constructor (Paso 1).

**Verifica**:

```bash
colcon build --packages-select ejercicio02_pubsub_cpp --cmake-args -DCMAKE_BUILD_TYPE=Debug
source install/setup.bash
colcon test --packages-select ejercicio02_pubsub_cpp
colcon test-result --verbose
```

Debe pasar `PublisherTest.PublisherExiste`. Los demás siguen fallando.

## Paso 2: El timer publica periódicamente

**Descomenta la línea de `timer_`** en el mismo archivo (Paso 2).

**Verifica**: debe pasar `PublisherTest.PublicaMensajes`.

## Paso 3: El listener se suscribe y cuenta mensajes

**Abre `include/ejercicio02_pubsub_cpp/sensor_listener.hpp`** y descomenta la línea de `subscription_` (Paso 3).

**Verifica**: debe pasar `ListenerTest.RecibeMensajesDelPublisher`. Con esto, los tres
tests del starter pasan.

## Correr los nodos de verdad

```bash
# Terminal 1
ros2 run ejercicio02_pubsub_cpp sensor_publisher

# Terminal 2 (puedes mezclar: el listener Python del Ejercicio 01 también funciona aquí)
ros2 run ejercicio02_pubsub_cpp sensor_listener

# Terminal 3
ros2 topic hz /sensor/state
```

## Checklist

- [ ] Los tres tests de `test/test_pubsub.cpp` pasan
- [ ] Compila sin warnings con `-Wall -Wextra -Wpedantic -Werror`
- [ ] Probé el publisher C++ con el listener Python del Ejercicio 01 (o viceversa) y
      funcionan igual — mismo topic, mismo tipo, dos lenguajes

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01](../ejercicio-01-publisher_subscriber_py/README.md) | **Ejercicio 02** | [Ejercicio 03](../ejercicio-03-comparar_latencia/README.md) |

← [Volver a la Semana 01](../../README.md)
