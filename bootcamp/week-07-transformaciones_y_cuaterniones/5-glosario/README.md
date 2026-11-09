# 📖 Glosario — Semana 07

Términos A-Z. El término/API en inglés va entre paréntesis cuando existe en la
documentación oficial.

- **Ángulos de Euler (Euler angles)**: tres giros seguidos alrededor de ejes
  dados que describen una orientación. En ROS: roll, pitch y yaw (teoría 03).
- **Bloqueo de cardán (gimbal lock)**: con pitch de ±90°, roll y yaw giran
  alrededor del mismo eje y se pierde un grado de libertad.
- **Componer (compose)**: aplicar una transformación tras otra. Con matrices o
  cuaterniones es un producto, y el orden importa.
- **Conjugado (conjugate)**: el cuaternión `(-x, -y, -z, w)`, el mismo eje con el
  giro al revés. En uno unitario es también su inverso.
- **Convención (convention)**: el orden y los ejes (fijos o móviles) de unos
  ángulos de Euler. La de ROS es `'sxyz'`: roll, pitch y yaw sobre ejes fijos.
- **Coordenadas homogéneas (homogeneous coordinates)**: un punto o vector 3D con
  una cuarta coordenada, 1 para puntos y 0 para direcciones.
- **Cuaternión (quaternion)**: cuatro números `(x, y, z, w)` que, si miden 1,
  representan un giro: `(u · sin(θ/2), cos(θ/2))` para un ángulo θ alrededor del
  eje `u`.
- **Cuaternión unitario (unit quaternion)**: el que mide 1. Solo estos son giros.
- **Doble cobertura (double cover)**: `q` y `-q` representan el mismo giro.
- **Eje-ángulo (axis-angle)**: un giro escrito como un eje unitario y un ángulo
  alrededor de él. Todo giro en 3D tiene esta forma.
- **Matriz de rotación (rotation matrix)**: matriz 3x3 ortonormal con
  determinante 1. Sus columnas son los ejes del marco hijo vistos desde el padre.
- **Matriz homogénea (homogeneous transformation matrix)**: matriz 4x4 con una
  rotación y una traslación, `T_a_b`, que lleva puntos del marco `b` al `a`.
- **Normalizar un ángulo (angle normalization / wrapping)**: dejarlo en
  `(-π, π]` con `atan2(sin(a), cos(a))`.
- **NumPy (NumPy)**: biblioteca de cálculo numérico con arrays de Python. `@` es
  el producto de matrices.
- **Ortonormal (orthonormal)**: con columnas de longitud 1 y perpendiculares
  entre sí. Por eso su inversa es su traspuesta.
- **Pitch (pitch)**: cabeceo, giro alrededor del eje y: morro arriba o abajo.
- **Producto de Hamilton (Hamilton product)**: la multiplicación de cuaterniones
  que compone dos giros.
- **Producto escalar (dot product)**: suma de los productos componente a
  componente. Entre dos cuaterniones unitarios, ±1 si son el mismo giro.
- **Roll (roll)**: alabeo, giro alrededor del eje x: inclinarse a un lado.
- **Rotación (rotation)**: giro alrededor de un eje que pasa por el origen, sin
  desplazar nada.
- **Rumbo (bearing)**: ángulo horizontal hacia un punto desde el eje x de un
  marco; positivo a la izquierda.
- **Slerp (spherical linear interpolation)**: interpolación entre dos
  cuaterniones por el arco más corto, a ritmo de giro constante.
- **`tf_transformations` (tf_transformations)**: biblioteca de Python de ROS 2
  para convertir y operar entre Euler, cuaterniones y matrices 4x4.
- **Traslación (translation)**: desplazamiento del origen de un marco respecto a
  otro, sin giro.
- **Traspuesta (transpose)**: la matriz con filas y columnas intercambiadas
  (`R.T`). En una rotación, deshace el giro.
- **Yaw (yaw)**: guiñada, giro alrededor del eje z: la orientación de un robot
  sobre el suelo.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Webgrafía](../4-recursos/webgrafia/README.md) | **Glosario** | [Rúbrica](../rubrica-evaluacion.md) |

← [Volver a la Semana 07](../README.md)
