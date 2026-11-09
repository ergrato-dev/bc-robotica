# Semana 07 — Transformaciones y cuaterniones

> En la Semana 06 tf2 te daba la posición de las cosas en el marco que pedías, sin que vieras cómo. Esta semana abres la caja: matrices de rotación, matrices homogéneas, ángulos de Euler y cuaterniones. Es la matemática con la que trabajan tf2, Gazebo, Nav2 y MoveIt2, y empieza la Fase 2.

## 🎯 Objetivos de la Semana

- Escribir y leer matrices de rotación, y saber por qué el orden de los giros importa
- Encadenar e invertir transformaciones con matrices homogéneas 4x4, con la notación `T_a_b`
- Usar roll, pitch y yaw con la convención de ROS, y reconocer el bloqueo de cardán
- Construir, componer, comparar e interpolar orientaciones con cuaterniones
- Calcular con `tf_transformations` y transformar mensajes con tf2 en Python
- Decir dónde está el objetivo de tu misión visto desde el sensor de tu robot

## 📋 Prerrequisitos

- [Semana 06](../week-06-launch_tf2_y_urdf/README.md) completada:
  launch files, TF2 y URDF
- Tu proyecto del dominio publicando `odom → base_link` desde las dos capas y
  arrancando con `bringup.launch.py`
- Matemáticas de bachillerato: seno, coseno y multiplicar una matriz por un vector

## 🗂️ Estructura de la Semana

```
week-07-transformaciones_y_cuaterniones/
├── README.md                       (este archivo)
├── rubrica-evaluacion.md
├── 0-assets/
│   ├── 01-rotacion-de-un-marco.svg
│   ├── 02-cadena-de-matrices.svg
│   ├── 03-roll-pitch-yaw.svg
│   ├── 04-cuaternion-eje-angulo.svg
│   └── 05-mapa-de-conversiones.svg
├── 1-teoria/
│   ├── 01-rotaciones-y-matrices.md
│   ├── 02-matrices-homogeneas.md
│   ├── 03-angulos-de-euler.md
│   ├── 04-cuaterniones.md
│   └── 05-tf-transformations-y-tf2.md
├── 2-practicas/
│   ├── ejercicio-01-calculadora_transformaciones_py/
│   ├── ejercicio-02-euler_y_cuaterniones_py/
│   └── ejercicio-03-transformar_puntos_tf2_py/
├── 3-proyecto/
│   └── starter/ (proyecto_dominio_interfaces/, proyecto_dominio_description/,
│                 proyecto_dominio_py/, proyecto_dominio_cpp/)
├── 4-recursos/
└── 5-glosario/
```

## 📝 Contenidos

### Teoría (4.0 h)

| Archivo | Tema |
|---|---|
| [`01-rotaciones-y-matrices.md`](1-teoria/01-rotaciones-y-matrices.md) | Rotación en 2D y 3D, columnas como ejes, inversa como traspuesta, orden de los giros, NumPy |
| [`02-matrices-homogeneas.md`](1-teoria/02-matrices-homogeneas.md) | Matriz 4x4, puntos y vectores, notación `T_a_b`, encadenar, invertir, el árbol TF como producto |
| [`03-angulos-de-euler.md`](1-teoria/03-angulos-de-euler.md) | Roll, pitch y yaw, la convención de ROS, bloqueo de cardán, normalizar ángulos |
| [`04-cuaterniones.md`](1-teoria/04-cuaterniones.md) | Eje-ángulo, producto de Hamilton, girar vectores, `q` y `-q`, slerp, orden `xyzw` |
| [`05-tf-transformations-y-tf2.md`](1-teoria/05-tf-transformations-y-tf2.md) | `tf_transformations`, mensaje a matriz y vuelta, `tf2_ros.Buffer` sin red, `buffer.transform`, lo mismo en C++ |

### Prácticas (5.5 h)

Los tres en Python: desde esta semana es el lenguaje por defecto.

| Ejercicio | Qué construye |
|---|---|
| 01 | Calculadora de transformaciones homogéneas con NumPy, comparada con tf2 |
| 02 | Cuaterniones a mano contra `tf_transformations`; error de rumbo y slerp |
| 03 | Nodo que lleva las detecciones del láser a `odom` con tf2, y su launch file |

### Proyecto (2.0 h)

Tu robot sabe dónde tiene el objetivo de su misión: `target_locator` lo escribe
en el marco del sensor con tf2 y dice si está a la vista.
Ver [3-proyecto/README.md](3-proyecto/README.md).

## ⏱️ Distribución del Tiempo (12 horas)

| Actividad | Horas |
|---|---|
| Teoría (01-05) | 4.0 |
| Ejercicio 01 (calculadora de transformaciones) | 2.0 |
| Ejercicio 02 (Euler y cuaterniones) | 2.0 |
| Ejercicio 03 (transformar puntos con tf2) | 1.5 |
| Proyecto | 2.0 |
| Autoevaluación (rúbrica) | 0.5 |
| **Total** | **12.0** |

## 🎩 Trucos y atajos

- `ros2 run tf2_ros tf2_echo <padre> <hijo>` — la transformación como cuaternión, como RPY en radianes y grados, y como matriz 4x4
- `python3 -c "import tf_transformations as t; print(t.quaternion_from_euler(0, 0, 1.5708))"` — calculadora de cuaterniones en la terminal
- `np.set_printoptions(precision=3, suppress=True)` — matrices legibles, sin `6.1e-17`
- `math.atan2(math.sin(e), math.cos(e))` — cualquier diferencia de ángulos, en `(-π, π]`
- `abs(np.dot(q1, q2))` cerca de 1 — dos cuaterniones son el mismo giro, aunque cambie el signo
- `T_a_b @ T_b_c` — si los subíndices de dentro no se tocan, el producto está mal

## 📌 Entregables

- Los tres ejercicios de `2-practicas/` con sus tests pasando y sus checklists completos
- `3-proyecto/` con `target_locator` publicando el objetivo de tu misión en el
  marco de tu sensor, y `colcon test` pasando
- Respuestas de los tres ejercicios en el README de tu proyecto

## ✅ Verificación

Desde la raíz de tu workspace (la carpeta que contiene `src/`):

```bash
sudo apt install ros-jazzy-tf-transformations
colcon build --symlink-install
source install/setup.bash
colcon test
colcon test-result --verbose
```

Esta semana no hay simulación: `scripts/verificar-simulaciones.sh week-07` no
encuentra mundos de Gazebo y termina sin error. Gazebo llega en la Semana 08.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 06](../week-06-launch_tf2_y_urdf/README.md) | **Semana 07** | Semana 08 (pendiente de publicar) |

← [Volver al inicio del bootcamp](../../README.md)
