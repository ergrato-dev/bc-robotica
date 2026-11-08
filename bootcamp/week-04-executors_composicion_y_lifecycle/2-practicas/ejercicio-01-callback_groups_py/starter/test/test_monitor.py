"""Tests del Ejercicio 01. No los edites: pasan solos al completar el Paso 1."""

import os
import threading
import time

import pytest
import rclpy
from ejercicio01_callback_groups_py.monitor import Monitor
from rclpy.executors import MultiThreadedExecutor
from std_srvs.srv import Trigger


@pytest.fixture(autouse=True)
def ros_context():
    # Dominio DDS propio por proceso: colcon test corre paquetes en paralelo
    # y así los nodos de otros tests no se mezclan con los de este.
    rclpy.init(domain_id=os.getpid() % 100 + 1)
    yield
    rclpy.shutdown()


def test_usa_grupos_propios():
    """Paso 1: el timer y el servicio tienen cada uno su grupo."""
    node = Monitor()
    try:
        assert node.timer_group is not None, "falta crear el grupo del timer"
        assert node.service_group is not None, "falta crear el grupo del servicio"
        assert node.timer_group is not node.service_group
        assert node.timer.callback_group is node.timer_group
    finally:
        node.destroy_node()


def test_timer_sigue_durante_la_comprobacion():
    """Paso 1: con executor multihilo, el timer avanza mientras el servicio
    trabaja. El test ya usa MultiThreadedExecutor: solo faltan los grupos."""
    node = Monitor()
    probe = rclpy.create_node("probe_monitor")
    client = probe.create_client(Trigger, "robot/slow_check")
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    executor.add_node(probe)
    spinner = threading.Thread(target=executor.spin, daemon=True)
    spinner.start()
    try:
        assert client.wait_for_service(timeout_sec=2.0)
        future = client.call_async(Trigger.Request())
        deadline = time.monotonic() + 3.0
        while not future.done() and time.monotonic() < deadline:
            time.sleep(0.05)
        assert future.done(), "el servicio no respondió en 3 segundos"
        ticks = int(future.result().message.rsplit(":", 1)[1])
        # 0.5 s a 10 Hz son unos 5 ticks; 3 deja margen a una máquina lenta.
        assert ticks >= 3, f"el timer estuvo bloqueado: {ticks} ticks"
    finally:
        executor.shutdown()
        node.destroy_node()
        probe.destroy_node()
