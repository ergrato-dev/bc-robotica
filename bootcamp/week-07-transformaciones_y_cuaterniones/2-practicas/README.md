# Prácticas — Semana 07

Tres ejercicios guiados, los tres en Python: desde esta semana Python es el
lenguaje por defecto, y C++ entra donde haga falta y con justificación escrita.
El lado C++ de esta matemática ya lo tienes: `tf2` de la Semana 06, resumido en
la teoría 05, sección 6.

| # | Ejercicio | Qué construye |
|---|---|---|
| 01 | [`ejercicio-01-calculadora_transformaciones_py`](ejercicio-01-calculadora_transformaciones_py/README.md) | Una calculadora de transformaciones homogéneas con NumPy, comprobada contra tf2 |
| 02 | [`ejercicio-02-euler_y_cuaterniones_py`](ejercicio-02-euler_y_cuaterniones_py/README.md) | Cuaterniones escritos a mano y comparados con `tf_transformations`; error de rumbo e interpolación |
| 03 | [`ejercicio-03-transformar_puntos_tf2_py`](ejercicio-03-transformar_puntos_tf2_py/README.md) | Un nodo que lleva cada detección del láser a `odom` con tf2, y su launch file |

El 01 necesita las teorías 01 y 02; el 02, la 03, la 04 y la 05; el 03, la 05. Los tres
usan el mismo escenario: el robot en `(2, 0)` de `odom` mirando hacia `+y` y un
láser 0.20 m por delante de su centro. Lo que el láser ve 1 m delante está en
`(2, 1.2)` de `odom`: lo calcularás tres veces, cada vez con una herramienta
distinta.

Antes de empezar, instala `tf_transformations` (teoría 05, sección 2):

```bash
sudo apt install ros-jazzy-tf-transformations
```

Como en semanas anteriores, cada ejercicio te pide romper el código a propósito
para ver caer el test que lo vigila, y dejarlo como estaba.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 — tf_transformations y tf2](../1-teoria/05-tf-transformations-y-tf2.md) | **Prácticas** | [Ejercicio 01](ejercicio-01-calculadora_transformaciones_py/README.md) |

← [Volver a la Semana 07](../README.md)
