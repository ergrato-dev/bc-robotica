"""Ejercicio 01, Semana 05 — sensor de distancia simulado con lecturas malas.

Publica en robot/range_raw_m, a 10 Hz, un obstáculo que se acerca y se aleja
entre 0.5 y 2.5 m. Cada 7 lecturas mete un reflejo (9.9 m) y cada 11, un eco
perdido (0.0 m): los fallos típicos de un sensor de ultrasonidos real.
Es determinista (sin azar), así los tests y las bags siempre ven lo mismo.
"""

import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64

REFLECTION_M = 9.9
LOST_ECHO_M = 0.0


def raw_reading(n: int) -> float:
    """Lectura número n del sensor simulado."""
    if n % 7 == 0:
        return REFLECTION_M
    if n % 11 == 0:
        return LOST_ECHO_M
    return 1.5 + math.sin(n / 10.0)


class RangeSim(Node):
    def __init__(self) -> None:
        super().__init__("range_sim")
        self.publisher = self.create_publisher(Float64, "robot/range_raw_m", 10)
        self.timer = self.create_timer(0.1, self._on_timer)
        self._readings = 0

    def _on_timer(self) -> None:
        self._readings += 1
        self.publisher.publish(Float64(data=raw_reading(self._readings)))


def main() -> None:
    rclpy.init()
    node = RangeSim()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        # try_shutdown: Ctrl+C ya cerró el contexto; shutdown() fallaría.
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
