"""Tests del Ejercicio 01. No los edites: pasan solos al completar los pasos
del starter (range_publisher.py, status_publisher.py, qos_listener.py)."""

import time

import pytest
import rclpy
from ejercicio01_qos_py.qos_listener import QosListener
from ejercicio01_qos_py.range_publisher import RangePublisher
from ejercicio01_qos_py.status_publisher import LATCHED_QOS, StatusPublisher
from rclpy.qos import DurabilityPolicy, ReliabilityPolicy, qos_profile_sensor_data
from sensor_msgs.msg import Range
from std_msgs.msg import String


@pytest.fixture(autouse=True)
def ros_context():
    rclpy.init()
    yield
    rclpy.shutdown()


def _spin_until(node_list: list, condition, timeout_s: float = 3.0) -> bool:
    """Hace spin_once sobre varios nodos hasta que condition() es True o hay timeout."""
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        for n in node_list:
            rclpy.spin_once(n, timeout_sec=0.05)
        if condition():
            return True
    return False


def test_range_publisher_es_best_effort():
    """Paso 1: /sensor/range existe y se ofrece con BEST_EFFORT."""
    node = RangePublisher()
    try:
        infos = node.get_publishers_info_by_topic("/sensor/range")
        assert len(infos) == 1, "no hay publisher en /sensor/range"
        assert infos[0].qos_profile.reliability == ReliabilityPolicy.BEST_EFFORT
    finally:
        node.destroy_node()


def test_range_lleva_header():
    """Paso 2: cada Range lleva stamp y frame_id."""
    pub_node = RangePublisher()
    probe = rclpy.create_node("probe_range_header")
    received: list[Range] = []
    probe.create_subscription(
        Range, "sensor/range", received.append, qos_profile_sensor_data
    )
    try:
        ok = _spin_until([pub_node, probe], lambda: len(received) >= 1)
        assert ok, "no llegó ningún Range en 3 segundos"
        assert received[0].header.frame_id == "range_sensor"
        assert received[0].header.stamp.sec > 0, "header.stamp sigue a cero"
    finally:
        pub_node.destroy_node()
        probe.destroy_node()


def test_status_llega_a_suscriptor_tardio():
    """Paso 3: un subscriber que arranca después recibe el 'ready' guardado."""
    pub_node = StatusPublisher()
    infos = pub_node.get_publishers_info_by_topic("/robot/status")
    assert len(infos) == 1, "no hay publisher en /robot/status"
    assert infos[0].qos_profile.durability == DurabilityPolicy.TRANSIENT_LOCAL

    # Deja pasar tiempo para que el publish del constructor ya sea "pasado".
    _spin_until([pub_node], lambda: False, timeout_s=0.5)

    probe = rclpy.create_node("probe_status_tardio")
    received: list[String] = []
    probe.create_subscription(String, "robot/status", received.append, LATCHED_QOS)
    try:
        ok = _spin_until([pub_node, probe], lambda: len(received) >= 1)
        assert ok, "el subscriber tardío no recibió el estado guardado"
        assert received[0].data == "ready"
    finally:
        pub_node.destroy_node()
        probe.destroy_node()


def test_listener_recibe_ambos_topics():
    """Paso 4: el listener recibe Range (BEST_EFFORT) y el estado latched."""
    range_node = RangePublisher()
    status_node = StatusPublisher()
    listener = QosListener()
    try:
        ok = _spin_until(
            [range_node, status_node, listener],
            lambda: listener.range_count >= 2 and listener.status == "ready",
        )
        assert ok, (
            f"range_count={listener.range_count}, status={listener.status!r}: "
            "revisa el QoS de cada subscripción"
        )
        assert listener.last_frame_id == "range_sensor"
    finally:
        range_node.destroy_node()
        status_node.destroy_node()
        listener.destroy_node()
