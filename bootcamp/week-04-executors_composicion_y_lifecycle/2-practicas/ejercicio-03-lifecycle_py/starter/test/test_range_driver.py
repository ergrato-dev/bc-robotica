"""Tests del Ejercicio 03. No los edites: pasan solos al completar los pasos de
range_driver.py. Llaman a las transiciones directamente (trigger_*), lo mismo
que hace `ros2 lifecycle set` a través de un servicio."""

import os
import time

import pytest
import rclpy
from ejercicio03_lifecycle_py.range_driver import RangeDriver
from rclpy.lifecycle import TransitionCallbackReturn
from rclpy.parameter import Parameter
from std_msgs.msg import Float64

TOPIC = "/robot/range_m"


@pytest.fixture(autouse=True)
def ros_context():
    # Dominio DDS propio por proceso: colcon test corre paquetes en paralelo
    # y así los nodos de otros tests no se mezclan con los de este.
    rclpy.init(domain_id=os.getpid() % 100 + 1)
    yield
    rclpy.shutdown()


def _received_during(node: RangeDriver, seconds: float) -> list[Float64]:
    probe = rclpy.create_node("probe_range")
    received: list[Float64] = []
    probe.create_subscription(Float64, TOPIC, received.append, 10)
    try:
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.02)
            rclpy.spin_once(probe, timeout_sec=0.02)
    finally:
        probe.destroy_node()
    return received


def test_configure_crea_el_publisher():
    """Paso 1: tras configure existe el publisher (aún inactivo)."""
    node = RangeDriver()
    try:
        assert node.count_publishers(TOPIC) == 0
        assert node.trigger_configure() == TransitionCallbackReturn.SUCCESS
        assert node.count_publishers(TOPIC) == 1, "configure no creó el publisher"
    finally:
        node.destroy_node()


def test_configure_falla_con_rate_invalido():
    """Paso 1: rate_hz <= 0 hace fallar configure."""
    node = RangeDriver(parameter_overrides=[Parameter("rate_hz", value=0.0)])
    try:
        assert node.trigger_configure() == TransitionCallbackReturn.FAILURE
        assert node.count_publishers(TOPIC) == 0
    finally:
        node.destroy_node()


def test_publica_solo_en_active():
    """Paso 2: inactive no publica; active sí; deactivate vuelve a parar."""
    node = RangeDriver()
    try:
        node.trigger_configure()
        assert not _received_during(node, 1.0), "publica sin estar activo"
        assert node.trigger_activate() == TransitionCallbackReturn.SUCCESS
        received = _received_during(node, 2.0)
        assert received, "activo, pero no llegó ninguna lectura en 2 segundos"
        assert 0.5 <= received[0].data <= 2.5
        assert node.trigger_deactivate() == TransitionCallbackReturn.SUCCESS
        assert node.timer is None, "deactivate no destruyó el timer"
    finally:
        node.destroy_node()


def test_cleanup_libera_el_publisher():
    """Paso 3: cleanup deshace configure."""
    node = RangeDriver()
    try:
        node.trigger_configure()
        assert node.count_publishers(TOPIC) == 1, "configure no creó el publisher"
        assert node.trigger_cleanup() == TransitionCallbackReturn.SUCCESS
        assert node.count_publishers(TOPIC) == 0, "cleanup no destruyó el publisher"
        assert node.publisher is None
    finally:
        node.destroy_node()
