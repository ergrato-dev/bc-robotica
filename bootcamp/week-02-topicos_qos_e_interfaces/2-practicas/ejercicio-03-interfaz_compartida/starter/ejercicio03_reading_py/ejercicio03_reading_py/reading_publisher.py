"""Ejercicio 03, Semana 02 — publisher Python de la interfaz propia SensorReading.

Requiere los Pasos 1 y 2 hechos en ejercicio03_interfaces y compilados.
"""

import rclpy
from ejercicio03_interfaces.msg import SensorReading
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

# Por encima de este valor la lectura se marca como aviso (STATUS_WARN).
WARN_THRESHOLD_M = 3.0


class ReadingPublisher(Node):
    def __init__(self) -> None:
        super().__init__("reading_publisher")
        self._value = 0.5

        # ============================================
        # PASO 3: Publicar SensorReading
        # ============================================
        # Descomenta las siguientes líneas para el Paso 3:
        #
        # self._publisher = self.create_publisher(SensorReading, "sensor/reading", 10)
        # self._timer = self.create_timer(0.5, self._on_timer)

    def _on_timer(self) -> None:
        msg = SensorReading()
        # unit ("m") e is_valid (True) llegan ya con su valor por defecto del .msg.
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "range_sensor"
        msg.sensor_id = "front"
        msg.value = self._value
        msg.status = (
            SensorReading.STATUS_OK
            if self._value < WARN_THRESHOLD_M
            else SensorReading.STATUS_WARN
        )
        self._publisher.publish(msg)
        self.get_logger().info(f"Publicado: {msg.value:.2f} {msg.unit}")
        self._value = 0.5 if self._value >= 3.5 else self._value + 0.25


def main() -> None:
    rclpy.init()
    node = ReadingPublisher()
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
