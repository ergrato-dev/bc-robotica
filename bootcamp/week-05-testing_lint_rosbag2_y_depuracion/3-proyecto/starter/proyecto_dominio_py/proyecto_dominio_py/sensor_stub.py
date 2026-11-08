"""Proyecto — Semana 05 — capa Python.

Nodo lifecycle de la Semana 04: no publica ni atiende el servicio hasta que
alguien lo configura y lo activa. Esta semana el nodo no cambia; lo cubren
tests de lint, de integración (launch_testing) y una bag de referencia.
Adapta los TODO a tu misión.
"""

from typing import Any

import rclpy

# TODO: si renombraste DomainState.msg o SetMode.srv, cambia los imports.
from proyecto_dominio_interfaces.msg import DomainState
from proyecto_dominio_interfaces.srv import SetMode
from rcl_interfaces.msg import FloatingPointRange, ParameterDescriptor
from rclpy.executors import ExternalShutdownException
from rclpy.lifecycle import Node as LifecycleNode
from rclpy.lifecycle import Publisher, State, TransitionCallbackReturn
from rclpy.parameter import Parameter
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from rclpy.service import Service
from rclpy.timer import Timer

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


class SensorStub(LifecycleNode):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("sensor_stub", **kwargs)
        # El parámetro existe desde el arranque: así se puede fijar con -p o
        # YAML antes de configurar, y consultar en cualquier estado.
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
        self.add_post_set_parameters_callback(self._on_parameters_set)
        self.publisher: Publisher | None = None
        self.service: Service | None = None
        self.timer: Timer | None = None
        self._battery_percent: float
        self._mode: int
        self._reset_state()

    # --- Transiciones --------------------------------------------------------

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        # TODO: cambia "dominio/state" y "dominio/set_mode" por los de tu misión.
        self.publisher = self.create_lifecycle_publisher(
            DomainState, "dominio/state", STATE_QOS
        )
        # El servicio responde ya en inactive: se puede elegir el modo antes
        # de empezar a publicar.
        self.service = self.create_service(
            SetMode, "dominio/set_mode", self._on_set_mode
        )
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        self.timer = self.create_timer(
            self.get_parameter("publish_period_s").value, self._on_timer
        )
        # Activa el publisher lifecycle; sin esta llamada no sale nada.
        return super().on_activate(state)

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        self._destroy_timer()
        return super().on_deactivate(state)

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        if self.publisher is not None:
            self.destroy_publisher(self.publisher)
            self.publisher = None
        if self.service is not None:
            self.destroy_service(self.service)
            self.service = None
        # Volver a unconfigured es volver al principio: batería y modo también.
        self._reset_state()
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        self._destroy_timer()
        return self.on_cleanup(state)

    # --- Callbacks -----------------------------------------------------------

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
        assert self.publisher is not None
        self.publisher.publish(msg)
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
            # Sin timer (no active), el valor nuevo se usará en el próximo activate.
            if parameter.name == "publish_period_s" and self.timer is not None:
                self.timer.timer_period_ns = int(parameter.value * 1e9)

    # --- Utilidades ----------------------------------------------------------

    def _reset_state(self) -> None:
        self._battery_percent = 100.0
        self._mode = DomainState.MODE_WORKING

    def _destroy_timer(self) -> None:
        if self.timer is not None:
            self.destroy_timer(self.timer)
            self.timer = None


def main() -> None:
    rclpy.init()
    node = SensorStub()
    # Executor de un hilo (el de rclpy.spin): todos los callbacks son cortos,
    # así que nunca hay uno esperando a otro el tiempo suficiente para notarse.
    # TODO: justifica en tu README el executor de tu misión.
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
