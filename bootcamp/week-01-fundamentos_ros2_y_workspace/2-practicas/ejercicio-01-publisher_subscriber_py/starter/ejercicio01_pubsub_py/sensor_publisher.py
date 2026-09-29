"""Ejercicio 01, Semana 01 — publisher mínimo en rclpy.

Completa los pasos en orden. Cada paso tiene un test en test/test_pubsub.py
que falla hasta que descomentas el bloque correspondiente.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SensorPublisher(Node):
    def __init__(self) -> None:
        super().__init__("sensor_publisher")

        # ============================================
        # PASO 1: Crear el publisher
        # ============================================
        # Descomenta las siguientes líneas para el Paso 1:
        #
        # self._publisher = self.create_publisher(String, "sensor/state", 10)
        # self._counter = 0

        # ============================================
        # PASO 2: Crear el timer que dispara la publicación
        # ============================================
        # Descomenta las siguientes líneas para el Paso 2
        # (requiere el Paso 1 ya hecho):
        #
        # self._timer = self.create_timer(0.5, self._on_timer)

        pass  # elimina esta línea cuando completes el Paso 1

    def _on_timer(self) -> None:
        msg = String()
        msg.data = f"lectura #{self._counter}"
        self._publisher.publish(msg)
        self.get_logger().info(f"Publicado: {msg.data}")
        self._counter += 1


def main() -> None:
    rclpy.init()
    node = SensorPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
