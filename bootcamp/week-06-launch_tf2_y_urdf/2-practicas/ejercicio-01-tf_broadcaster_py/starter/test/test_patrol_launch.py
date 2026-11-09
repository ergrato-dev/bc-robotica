"""Paso 4 — la patrulla arrancada desde su launch file, comprobada por TF."""

# ============================================
# PASO 4: probar un launch file con launch_testing y un listener TF
# ============================================
# El test no arranca los nodos uno a uno: incluye patrol.launch.py tal cual,
# con radius_m:=2.0, igual que harías desde la terminal. Después escucha /tf y
# /tf_static con un Buffer y pregunta dónde está cada marco.
# Descomenta las siguientes líneas para el Paso 4:
#
# import math
# import os
# import time
# import unittest
#
# import launch
# import launch_testing.actions
# import launch_testing.asserts
# import pytest
# import rclpy
# from ament_index_python.packages import get_package_share_directory
# from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from rclpy.time import Time
# from tf2_ros import Buffer, TransformListener
#
# # Dominio DDS propio: colcon test corre paquetes en paralelo.
# DOMAIN_ID = os.getpid() % 100 + 1
# PACKAGE = "ejercicio01_tf_broadcaster_py"
#
#
# @pytest.mark.launch_test
# def generate_test_description() -> launch.LaunchDescription:
#     launch_file = os.path.join(
#         get_package_share_directory(PACKAGE), "launch", "patrol.launch.py"
#     )
#     return launch.LaunchDescription(
#         [
#             # IncludeLaunchDescription no admite additional_env: la variable
#             # se fija para todo lo que se lance después.
#             SetEnvironmentVariable("ROS_DOMAIN_ID", str(DOMAIN_ID)),
#             IncludeLaunchDescription(
#                 PythonLaunchDescriptionSource(launch_file),
#                 launch_arguments={"radius_m": "2.0"}.items(),
#             ),
#             launch_testing.actions.ReadyToTest(),
#         ]
#     )
#
#
# class TestPatrol(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         rclpy.init(domain_id=DOMAIN_ID)
#         cls.node = rclpy.create_node("probe_tf")
#         cls.buffer = Buffer()
#         cls.listener = TransformListener(cls.buffer, cls.node)
#
#     @classmethod
#     def tearDownClass(cls) -> None:
#         cls.node.destroy_node()
#         rclpy.shutdown()
#
#     def _lookup(self, target: str, source: str):
#         # Time() vacío = "la transformación más reciente que tengas".
#         deadline = time.monotonic() + 10.0
#         while time.monotonic() < deadline:
#             rclpy.spin_once(self.node, timeout_sec=0.1)
#             if self.buffer.can_transform(target, source, Time()):
#                 return self.buffer.lookup_transform(target, source, Time())
#         self.fail(f"sin TF de {target} a {source} en 10 s")
#
#     def test_el_robot_esta_sobre_el_circulo_del_argumento(self) -> None:
#         t = self._lookup("odom", "base_link").transform.translation
#         self.assertAlmostEqual(math.hypot(t.x, t.y), 2.0, places=3)
#         self.assertAlmostEqual(t.z, 0.0)
#
#     def test_el_laser_cuelga_de_base_link(self) -> None:
#         t = self._lookup("base_link", "laser_link").transform.translation
#         self.assertAlmostEqual(t.x, 0.20)
#         self.assertAlmostEqual(t.z, 0.15)
#
#     def test_la_cadena_odom_laser_se_mueve(self) -> None:
#         first = self._lookup("odom", "laser_link").transform.translation
#         deadline = time.monotonic() + 1.0
#         while time.monotonic() < deadline:
#             rclpy.spin_once(self.node, timeout_sec=0.1)
#         second = self._lookup("odom", "laser_link").transform.translation
#         self.assertGreater(math.hypot(second.x - first.x, second.y - first.y), 0.1)
#
#
# @launch_testing.post_shutdown_test()
# class TestShutdown(unittest.TestCase):
#     def test_los_nodos_salen_con_codigo_0(self, proc_info):
#         launch_testing.asserts.assertExitCodes(proc_info)
