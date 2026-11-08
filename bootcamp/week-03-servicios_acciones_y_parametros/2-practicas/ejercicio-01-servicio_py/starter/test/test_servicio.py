"""Tests del Ejercicio 01. No los edites: pasan solos al completar los pasos
del starter (enable_server.py y enable_client.py)."""

import os

import pytest
import rclpy
from ejercicio01_servicio_py.enable_client import EnableClient
from ejercicio01_servicio_py.enable_server import EnableServer
from rclpy.executors import SingleThreadedExecutor
from std_srvs.srv import SetBool


@pytest.fixture(autouse=True)
def ros_context():
    # Dominio DDS propio por proceso: colcon test corre paquetes en paralelo
    # y así los nodos de otros tests no se mezclan con los de este.
    rclpy.init(domain_id=os.getpid() % 100 + 1)
    yield
    rclpy.shutdown()


def _call(executor: SingleThreadedExecutor, client, data: bool) -> SetBool.Response:
    future = client.call_async(SetBool.Request(data=data))
    executor.spin_until_future_complete(future, timeout_sec=3.0)
    assert future.done(), "el server no respondió en 3 segundos"
    return future.result()


def test_server_anuncia_el_servicio():
    """Paso 1: /robot/enable existe con tipo std_srvs/srv/SetBool."""
    node = EnableServer()
    try:
        services = dict(node.get_service_names_and_types())
        assert "/robot/enable" in services, f"servicios: {list(services)}"
        assert services["/robot/enable"] == ["std_srvs/srv/SetBool"]
    finally:
        node.destroy_node()


def test_server_cambia_estado_una_vez():
    """Paso 2: la primera petición cambia el estado; la repetida no."""
    server = EnableServer()
    probe = rclpy.create_node("probe_enable")
    client = probe.create_client(SetBool, "robot/enable")
    executor = SingleThreadedExecutor()
    executor.add_node(server)
    executor.add_node(probe)
    try:
        assert client.wait_for_service(timeout_sec=2.0)
        first = _call(executor, client, True)
        assert first.success and first.message == "habilitado"
        assert server.enabled
        again = _call(executor, client, True)
        assert not again.success and again.message == "ya estaba habilitado"
    finally:
        server.destroy_node()
        probe.destroy_node()


def test_cliente_recibe_respuesta():
    """Pasos 3 y 4: EnableClient.send() devuelve un Future con la response."""
    server = EnableServer()
    client = EnableClient()
    executor = SingleThreadedExecutor()
    executor.add_node(server)
    executor.add_node(client)
    try:
        future = client.send(True)
        executor.spin_until_future_complete(future, timeout_sec=3.0)
        assert future.done(), "no llegó la response en 3 segundos"
        assert future.result().success
    finally:
        server.destroy_node()
        client.destroy_node()
