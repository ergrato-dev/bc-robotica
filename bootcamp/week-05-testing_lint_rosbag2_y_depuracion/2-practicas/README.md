# Prácticas — Semana 05

Cuatro ejercicios guiados:

| # | Ejercicio | Lenguaje | Qué construye |
|---|---|---|---|
| 01 | [`ejercicio-01-tests_y_rosbag2_py`](ejercicio-01-tests_y_rosbag2_py/README.md) | Python (`rclpy`) | Filtro de distancia probado con `pytest` y `launch_testing`; grabación y lectura de una bag |
| 02 | [`ejercicio-02-gtest_y_rosbag2_cpp`](ejercicio-02-gtest_y_rosbag2_cpp/README.md) | C++ (`rclcpp`) | El mismo filtro en C++ con `gtest`; lectura de una bag con `rosbag2_cpp` y reproducción de la bag del 01 |
| 03 | [`ejercicio-03-lint_y_analisis_estatico`](ejercicio-03-lint_y_analisis_estatico/README.md) | Python y C++ | Un monitor de batería limpio para `ruff`, `mypy`, `clang-format` y `clang-tidy` |
| 04 | [`ejercicio-04-depuracion_py`](ejercicio-04-depuracion_py/README.md) | Python (`rclpy`) | Dos nodos que no se hablan: tres fallos encontrados con el método de depuración |

Haz el 01 antes que el 02: el 02 reproduce la bag que grabas en el 01. El 01 y
el 02 necesitan las teorías 01, 02 y 04; el 03, la teoría 03; el 04, la teoría 05.

Los ejercicios 01 y 02 piden comprobar que tus tests **detectan fallos**:
rompes el código a propósito, miras el test caer y lo dejas como estaba.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Depuración](../1-teoria/05-depuracion-y-ros2-doctor.md) | **Prácticas** | [Ejercicio 01](ejercicio-01-tests_y_rosbag2_py/README.md) |

← [Volver a la Semana 05](../README.md)
