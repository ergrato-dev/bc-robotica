"""Tests del Ejercicio 04 (parte Python). No los edites: pasan solos al
completar los pasos de heartbeat.py."""

import os
import time

import pytest
import rclpy
from ejercicio04_parametros_py.heartbeat import Heartbeat
from rclpy.parameter import Parameter
from std_msgs.msg import String


@pytest.fixture(autouse=True)
def ros_context():
    # Dominio DDS propio por proceso: colcon test corre paquetes en paralelo
    # y así los nodos de otros tests no se mezclan con los de este.
    rclpy.init(domain_id=os.getpid() % 100 + 1)
    yield
    rclpy.shutdown()


def test_declara_parametros_con_descriptor():
    """Paso 1: los dos parámetros existen con sus valores por defecto."""
    node = Heartbeat()
    try:
        assert node.get_parameter("robot_name").value == "robot"
        assert node.get_parameter("period_s").value == pytest.approx(1.0)
        assert node.describe_parameter("robot_name").read_only
    finally:
        node.destroy_node()


def test_rechaza_valores_invalidos():
    """Paso 1: fuera de rango o de solo lectura, el cambio se rechaza."""
    node = Heartbeat()
    try:
        out_of_range = node.set_parameters([Parameter("period_s", value=10.0)])[0]
        assert not out_of_range.successful
        read_only = node.set_parameters([Parameter("robot_name", value="otro")])[0]
        assert not read_only.successful
    finally:
        node.destroy_node()


def test_publica_latido_con_nombre():
    """Paso 2: publica "<robot_name>: alive"."""
    node = Heartbeat()
    probe = rclpy.create_node("probe_heartbeat")
    received: list[String] = []
    probe.create_subscription(String, "robot/heartbeat", received.append, 10)
    try:
        deadline = time.monotonic() + 3.0
        while time.monotonic() < deadline and not received:
            rclpy.spin_once(node, timeout_sec=0.05)
            rclpy.spin_once(probe, timeout_sec=0.05)
        assert received, "no llegó ningún latido en 3 segundos"
        assert received[0].data == "robot: alive"
    finally:
        node.destroy_node()
        probe.destroy_node()


def test_cambio_de_periodo_en_marcha():
    """Paso 3: un period_s válido cambia el periodo del timer."""
    node = Heartbeat()
    try:
        assert node.set_parameters([Parameter("period_s", value=0.2)])[0].successful
        assert node.period_s == pytest.approx(0.2)
        assert node.timer.timer_period_ns == 200_000_000
    finally:
        node.destroy_node()
