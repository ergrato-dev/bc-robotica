"""bringup.launch.py con cada capa: arranca sola hasta active y completa TF.

Corre dos veces, una con impl:=py y otra con impl:=cpp: las dos capas tienen
que ser intercambiables.
TODO: si renombraste el topic de estado o sensor_link, cambia las constantes.
"""

import math
import os
import time
import unittest

import launch
import launch_testing
import launch_testing.actions
import launch_testing.asserts
import pytest
import rclpy
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from proyecto_dominio_interfaces.msg import DomainState
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener

from proyecto_dominio_py.sensor_stub import (
    BASE_FRAME,
    ODOM_FRAME,
    ROUTE_LENGTH_M,
    STATE_QOS,
)

DOMAIN_ID = os.getpid() % 100 + 1
STATE_TOPIC = "/dominio/state"
SENSOR_FRAME = "sensor_link"


@pytest.mark.launch_test
@launch_testing.parametrize("impl", ["py", "cpp"])
def generate_test_description(impl: str) -> launch.LaunchDescription:
    launch_file = os.path.join(
        get_package_share_directory("proyecto_dominio_py"),
        "launch",
        "bringup.launch.py",
    )
    return launch.LaunchDescription(
        [
            SetEnvironmentVariable("ROS_DOMAIN_ID", str(DOMAIN_ID)),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(launch_file),
                launch_arguments={"impl": impl}.items(),
            ),
            launch_testing.actions.ReadyToTest(),
        ]
    )


class TestBringup(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rclpy.init(domain_id=DOMAIN_ID)
        cls.node = rclpy.create_node("probe_bringup")
        cls.buffer = Buffer()
        cls.listener = TransformListener(cls.buffer, cls.node)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.node.destroy_node()
        rclpy.shutdown()

    def _spin_until(self, done, seconds: float) -> None:
        deadline = time.monotonic() + seconds
        while not done() and time.monotonic() < deadline:
            rclpy.spin_once(self.node, timeout_sec=0.1)

    def test_publica_sin_transiciones_manuales(self) -> None:
        received: list[DomainState] = []
        self.node.create_subscription(
            DomainState, STATE_TOPIC, received.append, STATE_QOS
        )
        self._spin_until(lambda: len(received) >= 2, 10.0)
        self.assertGreaterEqual(len(received), 2, "sensor_stub no llegó a active")
        self.assertEqual(received[-1].header.frame_id, BASE_FRAME)

    def test_arbol_completo_de_odom_al_sensor(self) -> None:
        # odom -> base_link lo pone sensor_stub; base_link -> sensor, el URDF.
        def ready() -> bool:
            return self.buffer.can_transform(ODOM_FRAME, SENSOR_FRAME, Time())

        self._spin_until(ready, 10.0)
        self.assertTrue(ready(), f"sin TF {ODOM_FRAME} -> {SENSOR_FRAME}")
        t = self.buffer.lookup_transform(ODOM_FRAME, SENSOR_FRAME, Time())
        robot = self.buffer.lookup_transform(ODOM_FRAME, BASE_FRAME, Time())
        self.assertTrue(0.0 <= robot.transform.translation.x <= ROUTE_LENGTH_M)
        # El sensor va montado en el robot: nunca lejos de base_link.
        offset = t.transform.translation
        base = robot.transform.translation
        self.assertLess(math.dist((offset.x, offset.y), (base.x, base.y)), 2.0)


@launch_testing.post_shutdown_test()
class TestShutdown(unittest.TestCase):
    def test_salen_con_codigo_0(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
