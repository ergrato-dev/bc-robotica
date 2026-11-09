"""Ejercicio 01, Semana 06 — la geometría de la patrulla, sin ROS.

El robot recorre un círculo de radio `radius_m` centrado en el origen de odom,
en sentido antihorario, una vuelta cada `period_s` segundos, y mira siempre
hacia donde avanza. Sin ROS para poder probarlo con pytest en milisegundos.
"""

import math


def circle_pose(
    t_s: float, radius_m: float, period_s: float
) -> tuple[float, float, float]:
    """Posición (x, y) en metros y orientación yaw en radianes en el instante t_s."""
    # ============================================
    # PASO 1: la pose del robot en cada instante
    # ============================================
    # angle es cuánto ha girado el robot alrededor del centro. Su posición es
    # el punto del círculo en ese ángulo. Al avanzar en sentido antihorario,
    # el morro apunta 90° (pi/2) por delante del radio; atan2(sin, cos) deja
    # el resultado en (-pi, pi], el rango que usa ROS para un yaw.
    # Descomenta las siguientes líneas para el Paso 1:
    #
    # angle = 2.0 * math.pi * t_s / period_s
    # x = radius_m * math.cos(angle)
    # y = radius_m * math.sin(angle)
    # heading = angle + math.pi / 2.0
    # yaw = math.atan2(math.sin(heading), math.cos(heading))
    # return x, y, yaw
    raise NotImplementedError("completa el Paso 1")  # elimina en el Paso 1


def yaw_to_quaternion(yaw: float) -> tuple[float, float, float, float]:
    """Cuaternión (x, y, z, w) de un giro de `yaw` radianes alrededor del eje z.

    Fórmula para un giro solo en z (teoría 03, sección 4). La Semana 07
    explica el caso general.
    """
    return 0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0)
