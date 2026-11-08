# Prácticas — Semana 03

Cuatro ejercicios guiados:

| # | Ejercicio | Lenguaje | Qué construye |
|---|---|---|---|
| 01 | [`ejercicio-01-servicio_py`](ejercicio-01-servicio_py/README.md) | Python (`rclpy`) | Server y cliente de `robot/enable` (`std_srvs/SetBool`) |
| 02 | [`ejercicio-02-servicio_cpp`](ejercicio-02-servicio_cpp/README.md) | C++ (`rclcpp`) | El mismo servicio en C++; cada cliente contra el server del otro lenguaje |
| 03 | [`ejercicio-03-accion_compartida`](ejercicio-03-accion_compartida/README.md) | Python + C++ | Acción `MoveDistance`: server Python con feedback y cancelación, cliente C++ |
| 04 | [`ejercicio-04-parametros`](ejercicio-04-parametros/README.md) | Python + C++ | Nodo `heartbeat` con descriptor, post-set callback y un YAML para los dos |

Haz el 01 antes que el 02: el Paso 5 del 02 usa los nodos del 01. El 03 necesita
las teorías 03 y 04; el 04, la teoría 05.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Parámetros](../1-teoria/05-parametros.md) | **Prácticas** | [Ejercicio 01](ejercicio-01-servicio_py/README.md) |

← [Volver a la Semana 03](../README.md)
