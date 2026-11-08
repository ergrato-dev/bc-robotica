"""Proyecto — Semana 02 — capa Python.

Evolución del sensor_stub de la Semana 01: publica un mensaje propio
(DomainState) con Header y un perfil QoS explícito. Adapta los TODO a tu misión.
"""

import rclpy

# TODO: si renombraste DomainState.msg, cambia el import.
from proyecto_dominio_interfaces.msg import DomainState
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy

# TODO: elige y justifica en tu README el QoS de tu estado (teoría 02, sección 5).
# Punto de partida: RELIABLE + VOLATILE, porque el estado se publica cada segundo
# (quien llega tarde recibe el siguiente) pero cada cambio de modo importa.
STATE_QOS = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE,
)


class SensorStub(Node):
    def __init__(self) -> None:
        super().__init__("sensor_stub")
        # TODO: cambia "dominio/state" por el topic de tu misión (relativo, sin "/").
        self._publisher = self.create_publisher(DomainState, "dominio/state", STATE_QOS)
        self._battery_percent = 100.0
        self._timer = self.create_timer(1.0, self._on_timer)

    def _on_timer(self) -> None:
        msg = DomainState()
        msg.header.stamp = self.get_clock().now().to_msg()
        # TODO: frame del robot de tu dominio; en la Semana 06 lo conectas con TF2.
        msg.header.frame_id = "base_link"
        # TODO: valores simulados con sentido en tu misión.
        msg.location = "pasillo_A"
        msg.pending_tasks = 3
        msg.battery_percent = self._battery_percent
        msg.mode = DomainState.MODE_WORKING
        self._publisher.publish(msg)
        # Batería simulada: baja 0.5 % por segundo y se "recarga" al llegar a 20 %.
        self._battery_percent = (
            100.0 if self._battery_percent <= 20.0 else self._battery_percent - 0.5
        )


def main() -> None:
    rclpy.init()
    node = SensorStub()
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
