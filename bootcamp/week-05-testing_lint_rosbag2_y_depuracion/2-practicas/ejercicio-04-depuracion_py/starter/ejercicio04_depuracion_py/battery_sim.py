"""Ejercicio 04, Semana 05 — batería simulada. Este nodo funciona: no lo toques.

Publica en robot/battery_percent, a 2 Hz, una batería que empieza en 100 % y
pierde 0.5 % en cada lectura (1 % por segundo). Usa el QoS de sensores
(best effort): si se pierde una lectura, la siguiente llega medio segundo después.
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import Float32


class BatterySim(Node):
    def __init__(self) -> None:
        super().__init__("battery_sim")
        self.publisher = self.create_publisher(
            Float32, "robot/battery_percent", qos_profile_sensor_data
        )
        self.timer = self.create_timer(0.5, self._on_timer)
        self._percent = 100.0

    def _on_timer(self) -> None:
        self._percent = max(self._percent - 0.5, 0.0)
        self.publisher.publish(Float32(data=self._percent))


def main() -> None:
    rclpy.init()
    node = BatterySim()
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
