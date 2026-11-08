"""Ejercicio 01, Semana 02 — publisher latched (TRANSIENT_LOCAL)."""

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String

# Perfil latched: compartido por el publisher y por qos_listener.py.
# depth=1 porque solo importa el último estado.
LATCHED_QOS = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
)


class StatusPublisher(Node):
    def __init__(self) -> None:
        super().__init__("status_publisher")

        # ============================================
        # PASO 3: Publicar una sola vez con QoS latched
        # ============================================
        # Con LATCHED_QOS el mensaje queda guardado y lo recibe cualquier
        # subscriber TRANSIENT_LOCAL que se conecte después.
        # Descomenta las siguientes líneas para el Paso 3:
        #
        # self._publisher = self.create_publisher(String, "robot/status", LATCHED_QOS)
        # self._publisher.publish(String(data="ready"))
        # self.get_logger().info("Estado publicado una vez: ready")


def main() -> None:
    rclpy.init()
    node = StatusPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
