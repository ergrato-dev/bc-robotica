"""Test de integración: sensor_stub arrancado como proceso, igual que con ros2 run.

Lo lleva de unconfigured a active con el mismo servicio que usa ros2 lifecycle
(/sensor_stub/change_state) y comprueba que solo publica en active.
TODO: si renombraste el topic de estado, cambia STATE_TOPIC.
"""

import os
import time
import unittest

import launch
import launch_ros.actions
import launch_testing.actions
import launch_testing.asserts
import pytest
import rclpy
from lifecycle_msgs.msg import Transition
from lifecycle_msgs.srv import ChangeState
from proyecto_dominio_interfaces.msg import DomainState

from proyecto_dominio_py.sensor_stub import STATE_QOS

# Dominio DDS propio: colcon test corre paquetes en paralelo y así los nodos
# de otros tests no se mezclan con los de este.
DOMAIN_ID = os.getpid() % 100 + 1
STATE_TOPIC = "/dominio/state"


@pytest.mark.launch_test
def generate_test_description() -> launch.LaunchDescription:
    return launch.LaunchDescription(
        [
            launch_ros.actions.Node(
                package="proyecto_dominio_py",
                executable="sensor_stub",
                additional_env={"ROS_DOMAIN_ID": str(DOMAIN_ID)},
            ),
            launch_testing.actions.ReadyToTest(),
        ]
    )


class TestArranqueEnOrden(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rclpy.init(domain_id=DOMAIN_ID)
        cls.node = rclpy.create_node("probe_lifecycle")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.node.destroy_node()
        rclpy.shutdown()

    def _transition(self, transition_id: int) -> bool:
        client = self.node.create_client(ChangeState, "/sensor_stub/change_state")
        try:
            self.assertTrue(client.wait_for_service(timeout_sec=10.0))
            request = ChangeState.Request(transition=Transition(id=transition_id))
            future = client.call_async(request)
            rclpy.spin_until_future_complete(self.node, future, timeout_sec=5.0)
            return future.result() is not None and future.result().success
        finally:
            self.node.destroy_client(client)

    def _received_during(self, seconds: float) -> list[DomainState]:
        received: list[DomainState] = []
        subscription = self.node.create_subscription(
            DomainState, STATE_TOPIC, received.append, STATE_QOS
        )
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            rclpy.spin_once(self.node, timeout_sec=0.1)
        self.node.destroy_subscription(subscription)
        return received

    def test_publica_solo_en_active(self) -> None:
        self.assertEqual(self._received_during(1.5), [], "publica en unconfigured")
        self.assertTrue(self._transition(Transition.TRANSITION_CONFIGURE))
        self.assertEqual(self._received_during(1.5), [], "publica en inactive")
        self.assertTrue(self._transition(Transition.TRANSITION_ACTIVATE))
        self.assertGreater(len(self._received_during(2.5)), 0, "mudo en active")


@launch_testing.post_shutdown_test()
class TestShutdown(unittest.TestCase):
    def test_sale_con_codigo_0(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
