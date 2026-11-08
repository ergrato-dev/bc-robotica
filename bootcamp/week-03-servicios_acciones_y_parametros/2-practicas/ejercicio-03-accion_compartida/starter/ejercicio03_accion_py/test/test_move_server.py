"""Tests del Ejercicio 03 (parte Python). No los edites: pasan solos al
completar los pasos de move_server.py."""

import os
import threading
import time

import pytest
import rclpy
from action_msgs.msg import GoalStatus
from ejercicio03_accion_py.move_server import MoveServer
from ejercicio03_interfaces.action import MoveDistance
from rclpy.action import ActionClient
from rclpy.action.graph import get_action_server_names_and_types_by_node
from rclpy.executors import MultiThreadedExecutor


@pytest.fixture
def setup():
    """Server + nodo de prueba con un ActionClient, girando en otro hilo."""
    # Dominio DDS propio por proceso: colcon test corre paquetes en paralelo
    # y así los nodos de otros tests no se mezclan con los de este.
    rclpy.init(domain_id=os.getpid() % 100 + 1)
    server = MoveServer()
    probe = rclpy.create_node("probe_move")
    client = ActionClient(probe, MoveDistance, "robot/move_distance")
    executor = MultiThreadedExecutor()
    executor.add_node(server)
    executor.add_node(probe)
    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()
    yield server, client
    executor.shutdown()
    thread.join(timeout=2.0)
    server.destroy_node()
    probe.destroy_node()
    rclpy.shutdown()


def _wait(future, timeout_s: float = 5.0):
    deadline = time.monotonic() + timeout_s
    while not future.done() and time.monotonic() < deadline:
        time.sleep(0.02)
    assert future.done(), f"sin respuesta en {timeout_s} s"
    return future.result()


def _send(client: ActionClient, distance_m: float, feedback: list | None = None):
    assert client.wait_for_server(timeout_sec=2.0), "no hay action server"
    goal = MoveDistance.Goal(distance_m=distance_m)
    callback = (
        (lambda msg: feedback.append(msg.feedback)) if feedback is not None else None
    )
    return _wait(client.send_goal_async(goal, feedback_callback=callback))


def test_server_anuncia_la_accion(setup):
    """Paso 1 (parte A): /robot/move_distance existe con su tipo."""
    server, _ = setup
    # Solo los action servers de move_server: el ActionClient del fixture
    # también haría aparecer el nombre en un listado general.
    actions = dict(
        get_action_server_names_and_types_by_node(server, "move_server", "/")
    )
    assert actions.get("/robot/move_distance") == [
        "ejercicio03_interfaces/action/MoveDistance"
    ]


def test_rechaza_distancia_invalida(setup):
    """Paso 1 (parte B): un goal negativo se rechaza."""
    _, client = setup
    handle = _send(client, -1.0)
    assert not handle.accepted


def test_completa_con_feedback(setup):
    """Paso 2: recorre 0.5 m, publica feedback y termina en SUCCEEDED."""
    _, client = setup
    feedback: list[MoveDistance.Feedback] = []
    handle = _send(client, 0.5, feedback)
    assert handle.accepted
    response = _wait(handle.get_result_async())
    assert response.status == GoalStatus.STATUS_SUCCEEDED
    assert response.result.traveled_m == pytest.approx(0.5)
    assert feedback, "no llegó ningún feedback"
    assert feedback[-1].remaining_m == pytest.approx(0.0)


def test_se_puede_cancelar(setup):
    """Paso 3: cancelar un goal largo lo termina en CANCELED antes de llegar."""
    _, client = setup
    handle = _send(client, 5.0)
    assert handle.accepted
    time.sleep(0.3)
    _wait(handle.cancel_goal_async())
    response = _wait(handle.get_result_async())
    assert response.status == GoalStatus.STATUS_CANCELED
    assert 0.0 < response.result.traveled_m < 5.0
