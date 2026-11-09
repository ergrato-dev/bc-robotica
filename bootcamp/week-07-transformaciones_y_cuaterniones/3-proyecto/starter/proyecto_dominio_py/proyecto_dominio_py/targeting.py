"""Geometría del objetivo visto desde el sensor, sin ROS (Semana 07).

Ejes del marco del sensor (REP 103): x hacia donde mira, y a su izquierda,
z hacia arriba.
"""


def bearing_and_range(x: float, y: float, z: float) -> tuple[float, float, float]:
    """Rumbo y elevación en radianes, y distancia en metros, de un punto del sensor.

    Rumbo: cuánto a la izquierda (+) o a la derecha (-) del eje x está el punto.
    Elevación: cuánto por encima (+) o por debajo (-) del plano xy del sensor.
    """
    # TODO (Requisito 2): el rumbo es el yaw que apuntaría al punto, la
    # elevación el ángulo sobre el plano xy del sensor (los dos con
    # math.atan2; añade import math) y la distancia, la norma de (x, y, z).
    raise NotImplementedError("Requisito 2: bearing_and_range")


def in_field_of_view(
    bearing: float,
    elevation: float,
    range_m: float,
    h_fov_rad: float,
    v_fov_rad: float,
    max_range_m: float,
) -> bool:
    """True si el punto cae dentro del campo de visión y del alcance del sensor."""
    return (
        abs(bearing) <= h_fov_rad / 2.0
        and abs(elevation) <= v_fov_rad / 2.0
        and range_m <= max_range_m
    )
