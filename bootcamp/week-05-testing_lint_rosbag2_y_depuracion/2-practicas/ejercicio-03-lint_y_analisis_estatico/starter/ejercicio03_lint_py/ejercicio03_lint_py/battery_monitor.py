"""Ejercicio 03, Semana 05 — monitor de batería con fallos de lint a propósito.

Escucha robot/battery_percent y escribe en el log si la batería está baja.
Funciona, pero ruff y mypy encuentran seis problemas. Cada línea marcada con
"elimina" tiene encima su versión corregida, comentada.
"""
import os  # elimina en el Paso 1

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float32

# Descomenta la versión corregida (formato: espacios alrededor de "="):
# LOW_PERCENT = 20.0
LOW_PERCENT=20.0  # elimina en el Paso 1


# Descomenta la versión corregida (mypy: función sin tipos):
# def classify(percent: float | None) -> str:
def classify(percent):  # elimina en el Paso 2
    """Nivel de batería en palabras."""
    # Descomenta la versión corregida (E711: con None se compara con "is"):
    # if percent is None:
    if percent == None:  # elimina en el Paso 1
        return "desconocido"
    if percent < LOW_PERCENT:
        return "baja"
    # Descomenta la versión corregida (mypy: sin este return, devuelve None):
    # return "ok"


class BatteryMonitor(Node):
    # Descomenta la versión corregida (mypy: falta el tipo de retorno):
    # def __init__(self) -> None:
    def __init__(self):  # elimina en el Paso 2
        super().__init__("battery_monitor")
        self.create_subscription(Float32, "robot/battery_percent", self._on_battery, 10)
        # Descomenta la versión corregida (F541: f-string sin nada que formatear):
        # self.get_logger().info("monitor listo")
        self.get_logger().info(f"monitor listo")  # elimina en el Paso 1

    def _on_battery(self, msg: Float32) -> None:
        self.get_logger().info(f"batería {classify(msg.data)} ({msg.data:.0f} %)")


def main() -> None:
    rclpy.init()
    node = BatteryMonitor()
    try:
        rclpy.spin(node)
    # E722: un except desnudo atrapa también los errores de programación.
    # Descomenta la versión corregida:
    # except (KeyboardInterrupt, ExternalShutdownException):
    except:  # elimina en el Paso 1
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
