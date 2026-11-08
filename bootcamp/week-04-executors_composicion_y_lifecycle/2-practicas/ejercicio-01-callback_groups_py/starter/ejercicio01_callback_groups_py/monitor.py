"""Ejercicio 01, Semana 04 — un timer que no se para durante un servicio lento.

El timer cuenta ticks a 10 Hz. El servicio robot/slow_check tarda 0.5 s y
responde cuántos ticks hubo mientras trabajaba: 0 significa que el timer
estuvo bloqueado todo ese tiempo.
"""

import time

import rclpy
from rclpy.callback_groups import CallbackGroup, MutuallyExclusiveCallbackGroup
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.node import Node
from std_srvs.srv import Trigger

TICK_PERIOD_S = 0.1
# Simula un trabajo pesado (leer un archivo grande, calibrar un sensor...).
SLOW_CHECK_S = 0.5


class Monitor(Node):
    def __init__(self) -> None:
        super().__init__("monitor")
        self.ticks = 0
        # None = el grupo por defecto del nodo, que es MutuallyExclusive:
        # nunca corren dos de sus callbacks a la vez.
        self.timer_group: CallbackGroup | None = None
        self.service_group: CallbackGroup | None = None

        # ============================================
        # PASO 1: Un grupo para cada callback
        # ============================================
        # Dos grupos MutuallyExclusive distintos: dentro de cada grupo los
        # callbacks siguen en fila, pero el timer y el servicio ya no se
        # esperan entre sí. Un executor multihilo puede correrlos a la vez.
        # Descomenta las siguientes líneas para el Paso 1:
        #
        # self.timer_group = MutuallyExclusiveCallbackGroup()
        # self.service_group = MutuallyExclusiveCallbackGroup()

        self.timer = self.create_timer(
            TICK_PERIOD_S, self._on_tick, callback_group=self.timer_group
        )
        self.service = self.create_service(
            Trigger,
            "robot/slow_check",
            self._on_slow_check,
            callback_group=self.service_group,
        )

    def _on_tick(self) -> None:
        self.ticks += 1

    def _on_slow_check(
        self, request: Trigger.Request, response: Trigger.Response
    ) -> Trigger.Response:
        start = self.ticks
        # time.sleep bloquea el hilo que ejecuta este callback.
        time.sleep(SLOW_CHECK_S)
        response.success = True
        response.message = f"ticks durante la comprobación: {self.ticks - start}"
        self.get_logger().info(response.message)
        return response


def main() -> None:
    rclpy.init()
    node = Monitor()
    executor = rclpy.executors.SingleThreadedExecutor()  # elimina en el Paso 2

    # ============================================
    # PASO 2: Executor multihilo
    # ============================================
    # Con un solo hilo, los grupos del Paso 1 no sirven de nada: solo hay un
    # hilo para correr callbacks. MultiThreadedExecutor crea varios (por
    # defecto, tantos como núcleos de CPU).
    # Descomenta la siguiente línea para el Paso 2:
    #
    # executor = MultiThreadedExecutor()

    executor.add_node(node)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        # try_shutdown: Ctrl+C ya cerró el contexto; shutdown() fallaría.
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
