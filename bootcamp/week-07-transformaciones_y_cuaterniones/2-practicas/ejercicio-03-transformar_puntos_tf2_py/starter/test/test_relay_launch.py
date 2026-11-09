"""Pasos 2 y 3 — relay.launch.py publica en odom lo que el láser ve."""

import os
import time
import unittest

import launch
import launch_testing.actions
import launch_testing.asserts
import pytest
import rclpy
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PointStamped
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

# Dominio DDS propio: colcon test corre paquetes en paralelo.
DOMAIN_ID = os.getpid() % 100 + 1


@pytest.mark.launch_test
def generate_test_description() -> launch.LaunchDescription:
    launch_file = os.path.join(
        get_package_share_directory("ejercicio03_point_transform_py"),
        "launch",
        "relay.launch.py",
    )
    return launch.LaunchDescription(
        [
            SetEnvironmentVariable("ROS_DOMAIN_ID", str(DOMAIN_ID)),
            IncludeLaunchDescription(PythonLaunchDescriptionSource(launch_file)),
            launch_testing.actions.ReadyToTest(),
        ]
    )


class TestRelay(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rclpy.init(domain_id=DOMAIN_ID)
        cls.node = rclpy.create_node("probe_detection")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.node.destroy_node()
        rclpy.shutdown()

    def test_la_deteccion_sale_en_odom(self) -> None:
        received: list[PointStamped] = []
        self.node.create_subscription(PointStamped, "detection", received.append, 10)
        publisher = self.node.create_publisher(PointStamped, "laser/detection", 10)
        seen = PointStamped()
        seen.header.frame_id = "laser_link"
        seen.point.x = 1.0
        # Se publica varias veces: las primeras pueden llegar antes que la TF
        # o antes de que el relé se suscriba.
        deadline = time.monotonic() + 10.0
        while not received and time.monotonic() < deadline:
            publisher.publish(seen)
            rclpy.spin_once(self.node, timeout_sec=0.2)
        self.assertTrue(received, "nada en /detection en 10 s")
        out = received[0]
        self.assertEqual(out.header.frame_id, "odom")
        self.assertAlmostEqual(out.point.x, 2.0, places=6)
        self.assertAlmostEqual(out.point.y, 1.2, places=6)


@launch_testing.post_shutdown_test()
class TestShutdown(unittest.TestCase):
    def test_los_nodos_salen_con_codigo_0(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
