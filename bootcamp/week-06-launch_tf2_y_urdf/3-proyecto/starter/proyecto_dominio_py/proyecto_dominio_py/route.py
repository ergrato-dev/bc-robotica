"""La ruta simulada del robot, sin ROS: ida y vuelta por una recta.

Hasta que haya simulación (Semana 08), sensor_stub mueve el robot por aquí
para que el árbol TF tenga un odom -> base_link que cambia.
"""

import math


def route_pose(distance_m: float, length_m: float) -> tuple[float, float]:
    """(x, yaw) tras recorrer distance_m por una recta de length_m, ida y vuelta.

    A la ida avanza por +x mirando hacia delante (yaw 0); a la vuelta retrocede
    hacia el origen mirando hacia atrás (yaw pi).
    """
    lap = distance_m % (2.0 * length_m)
    if lap < length_m:
        return lap, 0.0
    return 2.0 * length_m - lap, math.pi


def yaw_to_quaternion(yaw: float) -> tuple[float, float, float, float]:
    """Cuaternión (x, y, z, w) de un giro de yaw radianes alrededor de z."""
    return 0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0)
