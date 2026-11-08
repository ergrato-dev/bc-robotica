"""Tests mínimos del proyecto. Actualízalos cuando renombres topic, servicio y tipos."""

import os
import time

import pytest
import rclpy
from proyecto_dominio_interfaces.msg import DomainState
from proyecto_dominio_interfaces.srv import SetMode
from rclpy.parameter import Parameter

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


def _received_during(node: SensorStub, seconds: float) -> list[DomainState]:
    probe = rclpy.create_node("probe_state")
    received: list[DomainState] = []
    probe.create_subscription(
        DomainState, _state_topic(node), received.append, STATE_QOS
    )
    try:
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.05)
            rclpy.spin_once(probe, timeout_sec=0.05)
    finally:
        probe.destroy_node()
    return received


def test_publica_tipo_propio():
    node = SensorStub()
    try:
        node.trigger_configure()
        types = dict(node.get_topic_names_and_types())[_state_topic(node)]
        # Si renombraste DomainState, actualiza este assert.
        assert "proyecto_dominio_interfaces/msg/DomainState" in types
    finally:
        node.destroy_node()


def test_publica_solo_en_active_y_con_header():
    node = SensorStub()
    try:
        node.trigger_configure()
        assert not _received_during(node, 1.5), "publica sin estar activo"
        node.trigger_activate()
        received = _received_during(node, 3.0)
        assert received, "activo, pero no llegó ningún estado en 3 segundos"
        assert received[0].header.frame_id != ""
        assert received[0].header.stamp.sec > 0
    finally:
        node.destroy_node()


def test_servicio_cambia_modo_y_rechaza_desconocido():
    node = SensorStub()
    probe = rclpy.create_node("probe_set_mode")
    try:
        assert not [
            n for n, _ in node.get_service_names_and_types() if n.endswith("/set_mode")
        ], "el servicio existe antes de configure"
        node.trigger_configure()
        names = [
            n for n, _ in node.get_service_names_and_types() if n.endswith("/set_mode")
        ]
        assert len(names) == 1, "se esperaba un servicio */set_mode tras configure"
        # Si renombraste SetMode, actualiza el tipo del cliente.
        client = probe.create_client(SetMode, names[0])
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
        node.trigger_configure()
        node.trigger_activate()
        good = node.set_parameters([Parameter("publish_period_s", value=0.5)])[0]
        assert good.successful
        assert node.timer is not None
        assert node.timer.timer_period_ns == 500_000_000
    finally:
        node.destroy_node()


def test_cleanup_deja_el_nodo_como_al_arrancar():
    node = SensorStub()
    try:
        node.trigger_configure()
        node.trigger_cleanup()
        published = node.get_publisher_names_and_types_by_node("sensor_stub", "/")
        assert not [name for name, _ in published if name.endswith("/state")]
        assert not [
            n for n, _ in node.get_service_names_and_types() if n.endswith("/set_mode")
        ]
    finally:
        node.destroy_node()
