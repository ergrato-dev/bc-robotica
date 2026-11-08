"""Ejercicio 01, Semana 05 — filtro de distancia.

Escucha robot/range_raw_m y publica en robot/range_m la mediana de las últimas
`window` lecturas, recortada a [min_range_m, max_range_m]. La lógica vive en
filtering.py; este archivo solo la conecta con ROS.
"""

from collections import deque

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64

from ejercicio01_tests_rosbag2_py.filtering import filter_range


class RangeFilter(Node):
    def __init__(self) -> None:
        super().__init__("range_filter")
        window = self.declare_parameter("window", 5).value
        self._min_m = self.declare_parameter("min_range_m", 0.05).value
        self._max_m = self.declare_parameter("max_range_m", 4.0).value
        # deque con maxlen: al llenarse, cada lectura nueva expulsa la más vieja.
        self._window: deque[float] = deque(maxlen=window)
        self.publisher = self.create_publisher(Float64, "robot/range_m", 10)
        self.create_subscription(Float64, "robot/range_raw_m", self._on_raw, 10)

    def _on_raw(self, msg: Float64) -> None:
        self._window.append(msg.data)
        filtered = filter_range(self._window, self._min_m, self._max_m)
        self.publisher.publish(Float64(data=filtered))


def main() -> None:
    rclpy.init()
    node = RangeFilter()
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
