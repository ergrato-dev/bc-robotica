"""Proyecto — Semana 03 — capa Python.

Evolución del sensor_stub de la Semana 02: además de publicar el estado, ofrece
un servicio para cambiar de modo y un parámetro para el periodo de publicación.
Adapta los TODO a tu misión.
"""

import rclpy

# TODO: si renombraste DomainState.msg o SetMode.srv, cambia los imports.
from proyecto_dominio_interfaces.msg import DomainState
from proyecto_dominio_interfaces.srv import SetMode
from rcl_interfaces.msg import FloatingPointRange, ParameterDescriptor
from rclpy.node import Node
from rclpy.parameter import Parameter
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

# Modos que acepta el servicio. TODO: los MODE_* de tu tipo.
VALID_MODES = (
    DomainState.MODE_IDLE,
    DomainState.MODE_WORKING,
    DomainState.MODE_CHARGING,
)


class SensorStub(Node):
    def __init__(self) -> None:
        super().__init__("sensor_stub")
        # TODO: cambia "dominio/state" por el topic de tu misión (relativo, sin "/").
        self._publisher = self.create_publisher(DomainState, "dominio/state", STATE_QOS)
        self._battery_percent = 100.0
        self._mode = DomainState.MODE_WORKING

        # Rango: más rápido que 0.1 s satura la red sin aportar; más lento que
        # 10 s y un nodo que arranque tarde espera demasiado. TODO: ajústalo.
        self.declare_parameter(
            "publish_period_s",
            1.0,
            ParameterDescriptor(
                description="Segundos entre dos estados publicados",
                floating_point_range=[
                    FloatingPointRange(from_value=0.1, to_value=10.0)
                ],
            ),
        )
        self.timer = self.create_timer(
            self.get_parameter("publish_period_s").value, self._on_timer
        )
        self.add_post_set_parameters_callback(self._on_parameters_set)

        # TODO: cambia "dominio/set_mode" por el servicio de tu misión.
        self._service = self.create_service(
            SetMode, "dominio/set_mode", self._on_set_mode
        )

    def _on_timer(self) -> None:
        msg = DomainState()
        msg.header.stamp = self.get_clock().now().to_msg()
        # TODO: frame del robot de tu dominio; en la Semana 06 lo conectas con TF2.
        msg.header.frame_id = "base_link"
        # TODO: valores simulados con sentido en tu misión.
        msg.location = "pasillo_A"
        msg.pending_tasks = 3
        msg.battery_percent = self._battery_percent
        msg.mode = self._mode
        self._publisher.publish(msg)
        # Batería simulada: baja 0.5 % por estado y se "recarga" al llegar a 20 %.
        self._battery_percent = (
            100.0 if self._battery_percent <= 20.0 else self._battery_percent - 0.5
        )

    def _on_set_mode(
        self, request: SetMode.Request, response: SetMode.Response
    ) -> SetMode.Response:
        if request.mode not in VALID_MODES:
            response.accepted = False
            response.message = f"modo desconocido: {request.mode}"
            return response
        self._mode = request.mode
        response.accepted = True
        response.message = f"modo {request.mode}"
        self.get_logger().info(f"Nuevo modo: {request.mode}")
        return response

    def _on_parameters_set(self, parameters: list[Parameter]) -> None:
        for parameter in parameters:
            if parameter.name == "publish_period_s":
                self.timer.timer_period_ns = int(parameter.value * 1e9)


def main() -> None:
    rclpy.init()
    node = SensorStub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
