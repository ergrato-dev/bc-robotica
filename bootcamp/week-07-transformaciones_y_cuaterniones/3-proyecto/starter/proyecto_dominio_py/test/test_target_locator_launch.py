"""Requisito 3 — target_locator escribe el objetivo en el marco del sensor.

Comprobación de ida y vuelta: el punto que publica, escrito en el marco del
sensor, devuelto a odom con la TF de ese mismo instante, tiene que ser el
objetivo. Da igual dónde esté el robot en su ruta. Los topics, el marco del
sensor y el objetivo salen de target_locator.py: si los adaptas allí, este
test los sigue.
"""

import os
import time
import unittest

import launch
import launch_testing.actions
import launch_testing.asserts
import pytest
import rclpy
import tf2_geometry_msgs  # noqa: F401  registra PointStamped en Buffer.transform
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PointStamped
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from rclpy.time import Time
from std_msgs.msg import Bool
from tf2_ros import Buffer, TransformListener

from proyecto_dominio_py.sensor_stub import ODOM_FRAME
from proyecto_dominio_py.target_locator import (
    DEFAULT_TARGET_XYZ,
    SENSOR_FRAME,
    TARGET_TOPIC,
    VISIBLE_TOPIC,
)

DOMAIN_ID = os.getpid() % 100 + 1


@pytest.mark.launch_test
def generate_test_description() -> launch.LaunchDescription:
    launch_file = os.path.join(
        get_package_share_directory("proyecto_dominio_py"),
        "launch",
        "bringup.launch.py",
    )
    return launch.LaunchDescription(
        [
            SetEnvironmentVariable("ROS_DOMAIN_ID", str(DOMAIN_ID)),
            IncludeLaunchDescription(PythonLaunchDescriptionSource(launch_file)),
            launch_testing.actions.ReadyToTest(),
        ]
    )


class TestTargetLocator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rclpy.init(domain_id=DOMAIN_ID)
        cls.node = rclpy.create_node("probe_target")
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

    def test_ida_y_vuelta_devuelve_el_objetivo(self) -> None:
        received: list[PointStamped] = []
        self.node.create_subscription(PointStamped, TARGET_TOPIC, received.append, 10)
        self._spin_until(lambda: len(received) >= 3, 15.0)
        self.assertGreaterEqual(len(received), 3, f"nada en {TARGET_TOPIC} en 15 s")
        in_sensor = received[-1]
        self.assertEqual(in_sensor.header.frame_id, SENSOR_FRAME)
        stamp = Time.from_msg(in_sensor.header.stamp)
        self._spin_until(
            lambda: self.buffer.can_transform(ODOM_FRAME, SENSOR_FRAME, stamp), 5.0
        )
        back = self.buffer.transform(in_sensor, ODOM_FRAME).point
        target_x, target_y, target_z = DEFAULT_TARGET_XYZ
        self.assertAlmostEqual(back.x, target_x, places=6)
        self.assertAlmostEqual(back.y, target_y, places=6)
        self.assertAlmostEqual(back.z, target_z, places=6)

    def test_publica_si_el_objetivo_esta_a_la_vista(self) -> None:
        received: list[Bool] = []
        self.node.create_subscription(Bool, VISIBLE_TOPIC, received.append, 10)
        self._spin_until(lambda: bool(received), 15.0)
        self.assertTrue(received, f"nada en {VISIBLE_TOPIC} en 15 s")


@launch_testing.post_shutdown_test()
class TestShutdown(unittest.TestCase):
    def test_salen_con_codigo_0(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
