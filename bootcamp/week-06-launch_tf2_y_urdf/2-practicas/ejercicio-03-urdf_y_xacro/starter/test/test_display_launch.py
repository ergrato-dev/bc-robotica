"""Paso 3 — display.launch.py publica el árbol TF del rover."""

import os
import time
import unittest

import launch
import launch_testing.actions
import launch_testing.asserts
import pytest
import rclpy
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener

# Dominio DDS propio: colcon test corre paquetes en paralelo.
DOMAIN_ID = os.getpid() % 100 + 1


@pytest.mark.launch_test
def generate_test_description() -> launch.LaunchDescription:
    launch_file = os.path.join(
        get_package_share_directory("ejercicio03_urdf_xacro"),
        "launch",
        "display.launch.py",
    )
    return launch.LaunchDescription(
        [
            SetEnvironmentVariable("ROS_DOMAIN_ID", str(DOMAIN_ID)),
            IncludeLaunchDescription(PythonLaunchDescriptionSource(launch_file)),
            launch_testing.actions.ReadyToTest(),
        ]
    )


class TestDisplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rclpy.init(domain_id=DOMAIN_ID)
        cls.node = rclpy.create_node("probe_tf")
        cls.buffer = Buffer()
        cls.listener = TransformListener(cls.buffer, cls.node)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.node.destroy_node()
        rclpy.shutdown()

    def _translation(self, target: str, source: str):
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            rclpy.spin_once(self.node, timeout_sec=0.1)
            if self.buffer.can_transform(target, source, Time()):
                return self.buffer.lookup_transform(
                    target, source, Time()
                ).transform.translation
        self.fail(f"sin TF de {target} a {source} en 10 s")

    def test_laser_fijo_sobre_el_chasis(self) -> None:
        t = self._translation("base_link", "laser_link")
        self.assertAlmostEqual(t.x, 0.15)
        self.assertAlmostEqual(t.z, 0.08)

    def test_ruedas_publicadas_gracias_a_joint_states(self) -> None:
        # Sin joint_state_publisher, las ruedas (continuous) no aparecerían.
        t = self._translation("base_link", "left_wheel_link")
        self.assertAlmostEqual(t.y, 0.17)


@launch_testing.post_shutdown_test()
class TestShutdown(unittest.TestCase):
    def test_los_nodos_salen_con_codigo_0(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
