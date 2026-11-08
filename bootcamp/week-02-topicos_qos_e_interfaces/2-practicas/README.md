# Prácticas — Semana 02

Cuatro ejercicios guiados:

| # | Ejercicio | Lenguaje | Qué construye |
|---|---|---|---|
| 01 | [`ejercicio-01-qos_py`](ejercicio-01-qos_py/README.md) | Python (`rclpy`) | Sensor `sensor_data`, estado latched y listener con el QoS correcto |
| 02 | [`ejercicio-02-qos_cpp`](ejercicio-02-qos_cpp/README.md) | C++ (`rclcpp`) | Los mismos tres nodos en C++, intercambiables con los de Python |
| 03 | [`ejercicio-03-interfaz_compartida`](ejercicio-03-interfaz_compartida/README.md) | Python + C++ | Paquete `_interfaces` con `SensorReading`, publisher Python y listener C++ |
| 04 | [`ejercicio-04-diagnosticar_qos_cli`](ejercicio-04-diagnosticar_qos_cli/README.md) | — (solo CLI) | Inspeccionar QoS, reproducir incompatibilidades y publicar un tipo propio |

Haz el 01 y el 02 en cualquier orden. El 03 necesita las teorías 04 y 05. El 04 va al
final, con los tres anteriores compilados en el mismo workspace.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Usar interfaces en Python y C++](../1-teoria/05-usar-interfaces-custom-en-python-y-cpp.md) | **Prácticas** | [Ejercicio 01](ejercicio-01-qos_py/README.md) |

← [Volver a la Semana 02](../README.md)
