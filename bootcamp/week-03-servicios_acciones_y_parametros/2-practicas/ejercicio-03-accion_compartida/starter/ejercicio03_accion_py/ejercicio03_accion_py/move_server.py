"""Ejercicio 03, Semana 03 — action server robot/move_distance (MoveDistance).

Simula un robot que avanza a velocidad constante: no hay motores ni simulador
todavía (Semana 08), solo el patrón goal -> feedback -> result.
"""

import time

import rclpy
from ejercicio03_interfaces.action import MoveDistance
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.node import Node

SPEED_MPS = 0.5  # velocidad simulada del robot
PERIOD_S = 0.1  # cada cuánto avanza y publica feedback
MAX_DISTANCE_M = 10.0  # goals más largos se rechazan


class MoveServer(Node):
    def __init__(self) -> None:
        super().__init__("move_server")

        # ============================================
        # PASO 1 (parte A): Crear el action server
        # ============================================
        # Cuatro callbacks: aceptar el goal, ejecutarlo, aceptar la cancelación.
        # ReentrantCallbackGroup deja que _on_cancel corra mientras _execute
        # sigue en su bucle (en otro hilo del MultiThreadedExecutor de main).
        # Descomenta las siguientes líneas para el Paso 1 (parte A):
        #
        # self._server = ActionServer(
        #     self,
        #     MoveDistance,
        #     "robot/move_distance",
        #     execute_callback=self._execute,
        #     goal_callback=self._on_goal,
        #     cancel_callback=self._on_cancel,
        #     callback_group=ReentrantCallbackGroup(),
        # )

    def _on_goal(self, goal_request: MoveDistance.Goal) -> GoalResponse:
        # ============================================
        # PASO 1 (parte B): Validar el goal
        # ============================================
        # Rechazar aquí es barato: el cliente lo sabe antes de que empiece nada.
        # Descomenta las siguientes líneas para el Paso 1 (parte B):
        #
        # if 0.0 < goal_request.distance_m <= MAX_DISTANCE_M:
        #     return GoalResponse.ACCEPT
        # self.get_logger().warn(f"Goal rechazado: {goal_request.distance_m} m")
        return GoalResponse.REJECT

    def _on_cancel(self, goal_handle: ServerGoalHandle) -> CancelResponse:
        # ============================================
        # PASO 3: Aceptar la cancelación
        # ============================================
        # Aceptarla solo pide parar; _execute decide cuándo y cómo (Paso 2).
        # Descomenta la siguiente línea para el Paso 3:
        #
        # return CancelResponse.ACCEPT
        return CancelResponse.REJECT  # elimina esta línea al completar el Paso 3

    def _execute(self, goal_handle: ServerGoalHandle) -> MoveDistance.Result:
        result = MoveDistance.Result()
        # ============================================
        # PASO 2: Ejecutar con feedback
        # ============================================
        # Cada PERIOD_S avanza SPEED_MPS * PERIOD_S metros y publica cuánto
        # falta. Antes de cada paso mira si piden cancelar: así el robot para
        # en menos de PERIOD_S. El resultado lleva lo recorrido en ambos casos.
        # Descomenta las siguientes líneas para el Paso 2:
        #
        # distance_m = goal_handle.request.distance_m
        # feedback = MoveDistance.Feedback()
        # while result.traveled_m < distance_m:
        #     if goal_handle.is_cancel_requested:
        #         goal_handle.canceled()
        #         self.get_logger().info(f"Cancelado a {result.traveled_m:.2f} m")
        #         return result
        #     time.sleep(PERIOD_S)
        #     step_m = SPEED_MPS * PERIOD_S
        #     result.traveled_m = min(distance_m, result.traveled_m + step_m)
        #     feedback.remaining_m = distance_m - result.traveled_m
        #     goal_handle.publish_feedback(feedback)
        # goal_handle.succeed()
        # self.get_logger().info(f"Completado: {result.traveled_m:.2f} m")
        return result


def main() -> None:
    rclpy.init()
    node = MoveServer()
    # Varios hilos: uno ejecuta el goal mientras otro atiende cancelaciones.
    # La Semana 04 explica executors y callback groups a fondo.
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        # try_shutdown: Ctrl+C ya cerró el contexto; shutdown() fallaría.
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
