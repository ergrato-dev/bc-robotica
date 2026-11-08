"""Lógica pura del filtro de distancia, sin nada de ROS.

Separarla del nodo permite probarla con pytest en milisegundos, sin arrancar
procesos ni esperar mensajes.
"""

from collections.abc import Sequence
from statistics import median


def filter_range(window: Sequence[float], min_m: float, max_m: float) -> float:
    """Mediana de las últimas lecturas, recortada al rango que mide el sensor.

    La mediana descarta un pico aislado (un reflejo que da 9.9 m, un eco perdido
    que da 0.0 m) sin retrasar tanto la señal como una media.
    """
    if not window:
        raise ValueError("la ventana de lecturas está vacía")
    return min(max(median(window), min_m), max_m)
