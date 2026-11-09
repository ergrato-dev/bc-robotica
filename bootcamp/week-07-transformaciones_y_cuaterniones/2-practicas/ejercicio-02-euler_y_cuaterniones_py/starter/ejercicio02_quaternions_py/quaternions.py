"""Ejercicio 02, Semana 07 — cuaterniones a mano y con tf_transformations.

Todos los cuaterniones van en el orden de ROS: (x, y, z, w), con w al final
(teoría 04, sección 6). Los Pasos 1 y 2 se escriben a mano para entender qué
hace cada fórmula; los Pasos 3 y 4 usan tf_transformations, la biblioteca que
usarás de verdad.
"""

import math

# tf_transformations se usa desde el Paso 3.
# Descomenta la siguiente línea para el Paso 3:
# import tf_transformations

Quaternion = tuple[float, float, float, float]
Vector = tuple[float, float, float]


def quaternion_norm(q: Quaternion) -> float:
    """Lo que mide el cuaternión. Uno que representa una rotación mide 1."""
    return math.sqrt(sum(c * c for c in q))


def quaternion_conjugate(q: Quaternion) -> Quaternion:
    """El conjugado: el mismo eje con el giro al revés. En un cuaternión unitario
    es también su inverso."""
    x, y, z, w = q
    return -x, -y, -z, w


def quaternion_from_axis_angle(axis: Vector, angle: float) -> Quaternion:
    """Cuaternión de un giro de `angle` radianes alrededor de `axis`."""
    # ============================================
    # PASO 1: construir y componer cuaterniones
    # ============================================
    # El eje se normaliza (que mida 1) y se escala por sin(angle/2); w es
    # cos(angle/2). Con axis = (0, 0, 1) sale la fórmula de la Semana 06.
    # Descomenta las siguientes líneas para el Paso 1:
    #
    # norm = math.sqrt(axis[0] ** 2 + axis[1] ** 2 + axis[2] ** 2)
    # s = math.sin(angle / 2.0) / norm
    # return axis[0] * s, axis[1] * s, axis[2] * s, math.cos(angle / 2.0)
    raise NotImplementedError("completa el Paso 1")  # elimina en el Paso 1


def quaternion_multiply(q1: Quaternion, q2: Quaternion) -> Quaternion:
    """Producto de Hamilton q1 * q2: primero se aplica q2 y después q1."""
    # Es el producto de la teoría 04, sección 3, con w al final. Igual que con
    # las matrices, q1 * q2 y q2 * q1 no son lo mismo.
    # Descomenta las siguientes líneas para el Paso 1:
    #
    # x1, y1, z1, w1 = q1
    # x2, y2, z2, w2 = q2
    # return (
    #     w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
    #     w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
    #     w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
    #     w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
    # )
    raise NotImplementedError("completa el Paso 1")  # elimina en el Paso 1


def rotate_vector(q: Quaternion, v: Vector) -> Vector:
    """El vector `v` girado por `q`: q * (v, 0) * conjugado(q)."""
    # ============================================
    # PASO 2: usar y comparar cuaterniones
    # ============================================
    # El vector se mete en un cuaternión con w = 0, se multiplica por los dos
    # lados y se saca la parte (x, y, z) (teoría 04, sección 4).
    # Descomenta las siguientes líneas para el Paso 2:
    #
    # pure = (v[0], v[1], v[2], 0.0)
    # x, y, z, _ = quaternion_multiply(
    #     quaternion_multiply(q, pure), quaternion_conjugate(q)
    # )
    # return x, y, z
    raise NotImplementedError("completa el Paso 2")  # elimina en el Paso 2


def same_rotation(q1: Quaternion, q2: Quaternion, tol: float = 1e-9) -> bool:
    """True si q1 y q2 giran lo mismo, aunque sus componentes sean distintas."""
    # q y -q son la misma rotación (teoría 04, sección 5): se compara el
    # producto escalar en valor absoluto, no componente a componente.
    # Descomenta las siguientes líneas para el Paso 2:
    #
    # dot = sum(a * b for a, b in zip(q1, q2, strict=True))
    # return abs(abs(dot) - 1.0) < tol
    raise NotImplementedError("completa el Paso 2")  # elimina en el Paso 2


def orientation_from_rpy_degrees(
    roll_deg: float, pitch_deg: float, yaw_deg: float
) -> Quaternion:
    """Cuaternión a partir de roll, pitch y yaw en grados, como los escribe alguien."""
    # ============================================
    # PASO 3: tf_transformations
    # ============================================
    # quaternion_from_euler quiere radianes y, por defecto, la convención de
    # ROS ('sxyz', teoría 03, sección 2). Devuelve una tupla (x, y, z, w).
    # Descomenta las siguientes líneas para el Paso 3:
    #
    # x, y, z, w = tf_transformations.quaternion_from_euler(
    #     math.radians(roll_deg), math.radians(pitch_deg), math.radians(yaw_deg)
    # )
    # return float(x), float(y), float(z), float(w)
    raise NotImplementedError("completa el Paso 3")  # elimina en el Paso 3


def heading_error(current: Quaternion, goal: Quaternion) -> float:
    """Cuánto debe girar en yaw el robot para mirar como `goal`, en (-pi, pi]."""
    # Restar dos yaw puede dar casi una vuelta entera (3.0 - (-3.0) = 6.0);
    # atan2(sin, cos) lo deja en el giro corto (teoría 03, sección 5).
    # Descomenta las siguientes líneas para el Paso 3:
    #
    # _, _, yaw_current = tf_transformations.euler_from_quaternion(current)
    # _, _, yaw_goal = tf_transformations.euler_from_quaternion(goal)
    # error = yaw_goal - yaw_current
    # return math.atan2(math.sin(error), math.cos(error))
    raise NotImplementedError("completa el Paso 3")  # elimina en el Paso 3


def interpolate(q1: Quaternion, q2: Quaternion, fraction: float) -> Quaternion:
    """La orientación a `fraction` (0 a 1) del camino de q1 a q2, a ritmo constante."""
    # ============================================
    # PASO 4: interpolar orientaciones
    # ============================================
    # slerp recorre el arco más corto entre las dos orientaciones y el
    # resultado sigue midiendo 1 (teoría 04, sección 7).
    # Descomenta las siguientes líneas para el Paso 4:
    #
    # x, y, z, w = tf_transformations.quaternion_slerp(q1, q2, fraction)
    # return float(x), float(y), float(z), float(w)
    raise NotImplementedError("completa el Paso 4")  # elimina en el Paso 4
