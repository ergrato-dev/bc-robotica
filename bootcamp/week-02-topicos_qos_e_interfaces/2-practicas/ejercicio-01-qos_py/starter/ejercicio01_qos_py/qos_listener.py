"""Ejercicio 01, Semana 02 — subscriber que pide el mismo QoS que cada publisher."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Range
from std_msgs.msg import String

from ejercicio01_qos_py.status_publisher import LATCHED_QOS


class QosListener(Node):
    def __init__(self) -> None:
        super().__init__("qos_listener")
        # Estado público para que los tests lo lean sin depender de los logs.
        self.range_count = 0
        self.last_frame_id: str | None = None
        self.status: str | None = None

        # ============================================
        # PASO 4: Suscribirse con el QoS de cada publisher
        # ============================================
        # Si usaras 10 (RELIABLE) en sensor/range, no recibirías nada: el
        # publisher ofrece BEST_EFFORT. Si usaras 10 (VOLATILE) en robot/status,
        # te perderías el "ready" publicado antes de que arrancaras.
        # Descomenta las siguientes líneas para el Paso 4:
        #
        # self._range_sub = self.create_subscription(
        #     Range, "sensor/range", self._on_range, qos_profile_sensor_data
        # )
        # self._status_sub = self.create_subscription(
        #     String, "robot/status", self._on_status, LATCHED_QOS
        # )

    def _on_range(self, msg: Range) -> None:
        self.range_count += 1
        self.last_frame_id = msg.header.frame_id
        # throttle: a 10 Hz, un log por segundo basta.
        self.get_logger().info(
            f"{msg.header.frame_id}: {msg.range:.2f} m", throttle_duration_sec=1.0
        )

    def _on_status(self, msg: String) -> None:
        self.status = msg.data
        self.get_logger().info(f"Estado del robot: {msg.data}")


def main() -> None:
    rclpy.init()
    node = QosListener()
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
