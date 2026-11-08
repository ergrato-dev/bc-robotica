"""Ejercicio 04, Semana 05 — vigilante de batería con tres fallos.

Escucha robot/battery_percent, calcula cuánto ha bajado por segundo desde la
primera lectura y escribe en el log cuánto tiempo le queda al robot. Así como está, no escribe nada. Encuentra
cada fallo con las herramientas de la teoría 05 antes de mirar la corrección.
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import Float32

# ============================================
# PASO 1: el topic
# ============================================
# Descomenta la siguiente línea para el Paso 1:
# TOPIC = "robot/battery_percent"
TOPIC = "robot/batery_percent"  # elimina en el Paso 1

# ============================================
# PASO 2: el QoS
# ============================================
# Descomenta la siguiente línea para el Paso 2:
# QOS: QoSProfile = rclpy.qos.qos_profile_sensor_data
QOS = QoSProfile(depth=10)  # elimina en el Paso 2


class BatteryWatchdog(Node):
    def __init__(self) -> None:
        super().__init__("battery_watchdog")
        # Primera lectura: (segundos, porcentaje). None hasta que llega.
        self._first: tuple[float, float] | None = None
        self.create_subscription(Float32, TOPIC, self._on_battery, QOS)

    def _on_battery(self, msg: Float32) -> None:
        now_s = self.get_clock().now().nanoseconds / 1e9
        # debug: solo se ve con --log-level battery_watchdog:=debug.
        self.get_logger().debug(f"lectura: {msg.data:.1f} %")
        # ============================================
        # PASO 3: la primera lectura
        # ============================================
        # Descomenta las siguientes líneas para el Paso 3:
        #
        # if self._first is None:
        #     self._first = (now_s, msg.data)
        #     return
        first_s, first_percent = self._first
        drop_per_s = (first_percent - msg.data) / (now_s - first_s)
        if drop_per_s > 0.0:
            remaining_s = msg.data / drop_per_s
            self.get_logger().info(
                f"batería {msg.data:.1f} %, tiempo restante: {remaining_s:.0f} s"
            )


def main() -> None:
    rclpy.init()
    node = BatteryWatchdog()
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
