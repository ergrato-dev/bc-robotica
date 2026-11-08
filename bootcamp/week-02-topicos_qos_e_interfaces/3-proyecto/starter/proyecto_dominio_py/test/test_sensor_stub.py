"""Tests mínimos del proyecto. Actualízalos cuando renombres topic y tipo."""

import os
import time

import pytest
import rclpy
from proyecto_dominio_interfaces.msg import DomainState
from proyecto_dominio_py.sensor_stub import STATE_QOS, SensorStub


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
