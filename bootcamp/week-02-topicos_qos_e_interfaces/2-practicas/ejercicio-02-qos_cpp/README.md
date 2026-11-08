# Ejercicio 02 — Perfiles QoS en C++ (`rclcpp`)

Los mismos tres nodos del Ejercicio 01, en C++: mismos nombres, mismos topics y mismo
QoS. Al final mezclas lenguajes y compruebas que la compatibilidad QoS no depende del
lenguaje.

> Igual que en la Semana 01: los **miembros** de cada clase ya están declarados; lo
> que descomentas es su **inicialización** en el constructor. No comentes nunca una
> declaración de miembro: el archivo dejaría de compilar.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-02-topicos_qos_e_interfaces/2-practicas/ejercicio-02-qos_cpp/starter \
  src/ejercicio02_qos_cpp
```

Estructura:

```
src/ejercicio02_qos_cpp/
├── package.xml
├── CMakeLists.txt
├── include/ejercicio02_qos_cpp/
│   ├── range_publisher.hpp    # PASO 1 y 2
│   ├── status_publisher.hpp   # PASO 3
│   └── qos_listener.hpp       # PASO 4
├── src/                       # solo main() de cada nodo: no se tocan
└── test/
    └── test_qos.cpp           # tests ya escritos (gtest)
```

El `CMakeLists.txt` crea un ejecutable por nodo con un `foreach`: los tres comparten
dependencias, así que la lista se escribe una vez.

Todos los pasos se verifican igual, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio02_qos_cpp
source install/setup.bash
colcon test --packages-select ejercicio02_qos_cpp
colcon test-result --verbose
```

## Paso 1: Publisher con el preset de sensores

**Abre `include/ejercicio02_qos_cpp/range_publisher.hpp`** y descomenta el bloque del
Paso 1. `rclcpp::SensorDataQoS()` es el equivalente de `qos_profile_sensor_data`.

**Verifica**: pasa `RangePublisherTest.EsBestEffort`.

## Paso 2: Rellenar el `Header`

**Descomenta el bloque del Paso 2** dentro de `on_timer()`.

**Verifica**: pasa `RangePublisherTest.LlevaHeader`.

## Paso 3: Estado latched

**Abre `include/ejercicio02_qos_cpp/status_publisher.hpp`**. La función
`latched_qos()` ya devuelve `rclcpp::QoS(1).reliable().transient_local()`; descomenta
el bloque del Paso 3 en el constructor.

`latched_qos()` es una función `inline` en el header (y no una variable global) para
que el publisher, el listener y el test usen el mismo perfil sin duplicarlo.

**Verifica**: pasa `StatusPublisherTest.LlegaASuscriptorTardio`.

## Paso 4: Listener con el QoS de cada publisher

**Abre `include/ejercicio02_qos_cpp/qos_listener.hpp`** y descomenta el bloque del
Paso 4.

**Verifica**: pasa `QosListenerTest.RecibeAmbosTopics`. Con esto, los cuatro tests
pasan.

## Paso 5: Mezclar lenguajes

Con los Ejercicios 01 y 02 compilados en el mismo workspace. En cada terminal nueva,
primero `source install/setup.bash`:

```bash
# Terminal 1: sensor en Python
ros2 run ejercicio01_qos_py range_publisher

# Terminal 2: estado en C++
ros2 run ejercicio02_qos_cpp status_publisher

# Terminal 3: listener en C++, arrancado el último
ros2 run ejercicio02_qos_cpp qos_listener
# [INFO] [...] [qos_listener]: Estado del robot: ready
# [INFO] [...] [qos_listener]: range_sensor: 1.30 m
```

**Verifica**: el listener C++ recibe del publisher Python y el estado latched C++.
Prueba también la combinación inversa (listener Python del Ejercicio 01).

## Checklist

- [ ] Los cuatro tests de `test/test_qos.cpp` pasan
- [ ] Compila sin warnings con `-Wall -Wextra -Wpedantic -Werror`
- [ ] Mezclé publishers y listeners de los dos lenguajes y todo conecta

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01](../ejercicio-01-qos_py/README.md) | **Ejercicio 02** | [Ejercicio 03](../ejercicio-03-interfaz_compartida/README.md) |

← [Volver a la Semana 02](../../README.md)
