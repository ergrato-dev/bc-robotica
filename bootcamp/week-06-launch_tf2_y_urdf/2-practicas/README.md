# Prácticas — Semana 06

Tres ejercicios guiados:

| # | Ejercicio | Lenguaje | Qué construye |
|---|---|---|---|
| 01 | [`ejercicio-01-tf_broadcaster_py`](ejercicio-01-tf_broadcaster_py/README.md) | Python (`rclpy`) | Un robot que patrulla en círculo publicado en TF, su launch file con argumento y TF estática, y un test que lo arranca |
| 02 | [`ejercicio-02-tf_listener_cpp`](ejercicio-02-tf_listener_cpp/README.md) | C++ (`rclcpp`) | Un monitor que pregunta a TF dónde está el dock; un launch file que incluye la patrulla del 01; el checklist de paridad que cierra la Fase 1 |
| 03 | [`ejercicio-03-urdf_y_xacro`](ejercicio-03-urdf_y_xacro/README.md) | URDF/xacro + launch | El modelo de un rover de dos ruedas, validado con `check_urdf` y publicado con `robot_state_publisher` |

Haz el 01 antes que el 02: el launch file del 02 incluye el del 01, así que los
dos paquetes van en el mismo workspace. El 01 necesita las teorías 01, 03 y 04;
el 02, además, la 02; el 03, las teorías 01 y 05.

Como en la Semana 05, cada ejercicio te pide romper el código a propósito para
ver caer el test que lo vigila, y dejarlo como estaba.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · URDF y xacro](../1-teoria/05-urdf-y-xacro.md) | **Prácticas** | [Ejercicio 01](ejercicio-01-tf_broadcaster_py/README.md) |

← [Volver a la Semana 06](../README.md)
