"""Ejercicio 01, Semana 01 — subscriber mínimo en rclpy."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SensorListener(Node):
    def __init__(self) -> None:
        super().__init__("sensor_listener")
        self.received_count = 0
        self.last_message: str | None = None

        # ============================================
        # PASO 3: Crear la subscripción
        # ============================================
        # Descomenta las siguientes líneas para el Paso 3:
        #
        # self._subscription = self.create_subscription(
        #     String, "sensor/state", self._on_message, 10
        # )

        pass  # elimina esta línea cuando completes el Paso 3

    def _on_message(self, msg: String) -> None:
        self.received_count += 1
        self.last_message = msg.data
        self.get_logger().info(f"Recibido: {msg.data}")


def main() -> None:
    rclpy.init()
    node = SensorListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
