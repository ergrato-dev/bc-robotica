"""Tests del publisher Python del Ejercicio 03. No los edites."""

import time

import pytest
import rclpy
from ejercicio03_interfaces.msg import SensorReading
from ejercicio03_reading_py.reading_publisher import ReadingPublisher


@pytest.fixture(autouse=True)
def ros_context():
    rclpy.init()
    yield
    rclpy.shutdown()


def test_interfaz_tiene_campos_y_constantes():
    """Paso 2: SensorReading tiene sus campos, valores por defecto y constantes."""
    msg = SensorReading()
    assert msg.unit == "m"
    assert msg.is_valid is True
    assert SensorReading.STATUS_WARN == 1


def test_publisher_publica_sensor_reading():
    """Paso 3: llega un SensorReading con header y estado coherente."""
    pub_node = ReadingPublisher()
    probe = rclpy.create_node("probe_reading")
    received: list[SensorReading] = []
    probe.create_subscription(SensorReading, "sensor/reading", received.append, 10)
    try:
        deadline = time.monotonic() + 3.0
        while time.monotonic() < deadline and not received:
            rclpy.spin_once(pub_node, timeout_sec=0.05)
            rclpy.spin_once(probe, timeout_sec=0.05)
        assert received, "no llegó ningún SensorReading en 3 segundos"
        msg = received[0]
        assert msg.sensor_id == "front"
        assert msg.header.frame_id == "range_sensor"
        assert msg.status == SensorReading.STATUS_OK
    finally:
        pub_node.destroy_node()
        probe.destroy_node()
