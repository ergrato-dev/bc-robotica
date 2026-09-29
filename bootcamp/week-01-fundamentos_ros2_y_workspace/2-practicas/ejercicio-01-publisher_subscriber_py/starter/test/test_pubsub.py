"""Tests del Ejercicio 01. No los edites: pasan solos al completar los pasos
del starter (sensor_publisher.py, sensor_listener.py)."""

import time

import pytest
import rclpy
from std_msgs.msg import String

from ejercicio01_pubsub_py.sensor_listener import SensorListener
from ejercicio01_pubsub_py.sensor_publisher import SensorPublisher


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


def test_publisher_existe():
    """Paso 1: el nodo debe exponer un publisher sobre /sensor/state."""
    node = SensorPublisher()
    try:
        topic_names_and_types = dict(node.get_topic_names_and_types())
        assert "/sensor/state" in topic_names_and_types
        assert "std_msgs/msg/String" in topic_names_and_types["/sensor/state"]
    finally:
        node.destroy_node()


def test_publica_mensajes():
    """Paso 2: el timer debe disparar al menos un mensaje en 2 segundos."""
    pub_node = SensorPublisher()
    received = []

    probe = rclpy.create_node("probe_publica_mensajes")
    probe.create_subscription(String, "sensor/state", lambda m: received.append(m.data), 10)

    try:
        ok = _spin_until([pub_node, probe], lambda: len(received) >= 1, timeout_s=3.0)
        assert ok, "no se recibió ningún mensaje en /sensor/state en 3 segundos"
    finally:
        pub_node.destroy_node()
        probe.destroy_node()


def test_listener_recibe_mensajes_del_publisher():
    """Paso 3: el listener debe incrementar received_count al llegar mensajes."""
    pub_node = SensorPublisher()
    sub_node = SensorListener()

    try:
        ok = _spin_until(
            [pub_node, sub_node], lambda: sub_node.received_count >= 2, timeout_s=3.0
        )
        assert ok, "el listener no recibió al menos 2 mensajes en 3 segundos"
        assert sub_node.last_message is not None
        assert sub_node.last_message.startswith("lectura #")
    finally:
        pub_node.destroy_node()
        sub_node.destroy_node()
