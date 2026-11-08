"""Test mínimo del proyecto: el publisher existe. Amplíalo cuando renombres
el topic a tu dominio."""

import os

import pytest
import rclpy
from proyecto_dominio_py.sensor_stub import SensorStub


@pytest.fixture(autouse=True)
def ros_context():
    # Dominio DDS propio por proceso: colcon test corre paquetes en paralelo
    # y así los nodos de otros tests no se mezclan con los de este.
    rclpy.init(domain_id=os.getpid() % 100 + 1)
    yield
    rclpy.shutdown()


def test_publisher_existe():
    node = SensorStub()
    try:
        topics = dict(node.get_topic_names_and_types())
        # Si ya renombraste el topic en sensor_stub.py, actualiza este assert.
        assert any(t.endswith("/state") for t in topics)
    finally:
        node.destroy_node()
