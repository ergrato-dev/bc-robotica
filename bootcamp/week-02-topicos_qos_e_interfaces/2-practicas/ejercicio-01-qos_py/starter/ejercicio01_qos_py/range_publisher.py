"""Ejercicio 01, Semana 02 — publisher de sensor con QoS sensor_data.

Completa los pasos en orden. Cada paso tiene un test en test/test_qos.py
que falla hasta que descomentas el bloque correspondiente.
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Range


class RangePublisher(Node):
    def __init__(self) -> None:
        super().__init__("range_publisher")
        self._distance_m = 1.0

        # ============================================
        # PASO 1: Publisher con el preset de sensores
        # ============================================
        # qos_profile_sensor_data = KEEP_LAST 5, BEST_EFFORT, VOLATILE.
        # Impacto: si el subscriber pide RELIABLE, no se conectan (teoría 02).
        # Descomenta las siguientes líneas para el Paso 1:
        #
        # self._publisher = self.create_publisher(
        #     Range, "sensor/range", qos_profile_sensor_data
        # )
        # self._timer = self.create_timer(0.1, self._on_timer)  # 10 Hz

    def _on_timer(self) -> None:
        msg = Range()

        # ============================================
        # PASO 2: Rellenar el Header
        # ============================================
        # stamp = cuándo se midió (reloj del nodo, válido también en simulación).
        # frame_id = desde qué sensor; TF2 lo usará en la Semana 06.
        # Descomenta las siguientes líneas para el Paso 2:
        #
        # msg.header.stamp = self.get_clock().now().to_msg()
        # msg.header.frame_id = "range_sensor"

        msg.radiation_type = Range.ULTRASOUND
        msg.field_of_view = 0.5  # rad
        msg.min_range = 0.02  # m
        msg.max_range = 4.0  # m
        msg.range = self._distance_m
        self._publisher.publish(msg)
        # Distancia simulada: sube de 1.0 a 3.0 m y vuelve a empezar.
        self._distance_m = 1.0 if self._distance_m >= 3.0 else self._distance_m + 0.1


def main() -> None:
    rclpy.init()
    node = RangePublisher()
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
