"""Tests mínimos del proyecto. Actualízalos cuando renombres topic, servicio y tipos."""

import os
import time

import pytest
import rclpy
from proyecto_dominio_interfaces.msg import DomainState
from proyecto_dominio_interfaces.srv import SetMode
from proyecto_dominio_py.sensor_stub import STATE_QOS, SensorStub
from rclpy.parameter import Parameter


@pytest.fixture(autouse=True)
def ros_context():
    # Dominio DDS propio por proceso: colcon test corre paquetes en paralelo
    # y así los nodos de otros tests no se mezclan con los de este.
    rclpy.init(domain_id=os.getpid() % 100 + 1)
    yield
    rclpy.shutdown()


def _state_topic(node: SensorStub) -> str:
    topics = [
        name for name, _ in node.get_topic_names_and_types() if name.endswith("/state")
    ]
    assert len(topics) == 1, f"se esperaba un topic */state, hay: {topics}"
    return topics[0]


def test_publica_tipo_propio():
    node = SensorStub()
    try:
        types = dict(node.get_topic_names_and_types())[_state_topic(node)]
        # Si renombraste DomainState, actualiza este assert.
        assert "proyecto_dominio_interfaces/msg/DomainState" in types
    finally:
        node.destroy_node()


def test_estado_lleva_header():
    node = SensorStub()
    probe = rclpy.create_node("probe_state")
    received: list[DomainState] = []
    probe.create_subscription(
        DomainState, _state_topic(node), received.append, STATE_QOS
    )
    try:
        deadline = time.monotonic() + 3.0
        while time.monotonic() < deadline and not received:
            rclpy.spin_once(node, timeout_sec=0.05)
            rclpy.spin_once(probe, timeout_sec=0.05)
        assert received, "no llegó ningún estado en 3 segundos"
        assert received[0].header.frame_id != ""
        assert received[0].header.stamp.sec > 0
    finally:
        node.destroy_node()
        probe.destroy_node()


def test_servicio_cambia_modo_y_rechaza_desconocido():
    node = SensorStub()
    probe = rclpy.create_node("probe_set_mode")
    names = [
        n for n, _ in node.get_service_names_and_types() if n.endswith("/set_mode")
    ]
    assert len(names) == 1, "se esperaba un servicio */set_mode"
    # Si renombraste SetMode, actualiza el tipo del cliente.
    client = probe.create_client(SetMode, names[0])
    try:
        assert client.wait_for_service(timeout_sec=2.0)
        for mode, accepted in ((DomainState.MODE_IDLE, True), (99, False)):
            future = client.call_async(SetMode.Request(mode=mode))
            deadline = time.monotonic() + 3.0
            while not future.done() and time.monotonic() < deadline:
                rclpy.spin_once(node, timeout_sec=0.05)
                rclpy.spin_once(probe, timeout_sec=0.05)
            assert future.done(), "el servicio no respondió"
            assert future.result().accepted is accepted
    finally:
        node.destroy_node()
        probe.destroy_node()


def test_periodo_respeta_su_rango():
    node = SensorStub()
    try:
        bad = node.set_parameters([Parameter("publish_period_s", value=0.0)])[0]
        assert not bad.successful
        good = node.set_parameters([Parameter("publish_period_s", value=0.5)])[0]
        assert good.successful
        assert node.timer.timer_period_ns == 500_000_000
    finally:
        node.destroy_node()
