"""Paso 2 — test de integración con launch_testing: dos procesos de verdad."""

# ============================================
# PASO 2: test de integración con launch_testing
# ============================================
# generate_test_description arranca range_sim y range_filter como procesos
# separados, igual que ros2 run. ReadyToTest avisa de que ya pueden empezar
# los tests. Las clases normales corren con los nodos vivos; la marcada con
# post_shutdown_test corre después de pararlos y revisa cómo terminaron.
# Descomenta las siguientes líneas para el Paso 2:
#
# import os
# import time
# import unittest
#
# import launch
# import launch_ros.actions
# import launch_testing.actions
# import launch_testing.asserts
# import pytest
# import rclpy
# from std_msgs.msg import Float64
#
# # Dominio DDS propio: colcon test corre paquetes en paralelo y así los nodos
# # de otros tests no se mezclan con los de este.
# DOMAIN_ID = os.getpid() % 100 + 1
# PACKAGE = "ejercicio01_tests_rosbag2_py"
#
#
# @pytest.mark.launch_test
# def generate_test_description() -> launch.LaunchDescription:
#     env = {"ROS_DOMAIN_ID": str(DOMAIN_ID)}
#     return launch.LaunchDescription(
#         [
#             launch_ros.actions.Node(
#                 package=PACKAGE, executable="range_sim", additional_env=env
#             ),
#             launch_ros.actions.Node(
#                 package=PACKAGE, executable="range_filter", additional_env=env
#             ),
#             launch_testing.actions.ReadyToTest(),
#         ]
#     )
#
#
# class TestRangeFilter(unittest.TestCase):
#     def test_salida_sin_reflejos_ni_ecos_perdidos(self) -> None:
#         rclpy.init(domain_id=DOMAIN_ID)
#         node = rclpy.create_node("probe_range")
#         received: list[float] = []
#         node.create_subscription(
#             Float64, "robot/range_m", lambda msg: received.append(msg.data), 10
#         )
#         try:
#             # 30 lecturas a 10 Hz son 3 s; 10 s de margen por si arranca lento.
#             deadline = time.monotonic() + 10.0
#             while len(received) < 30 and time.monotonic() < deadline:
#                 rclpy.spin_once(node, timeout_sec=0.1)
#         finally:
#             node.destroy_node()
#             rclpy.shutdown()
#         self.assertGreaterEqual(len(received), 30)
#         # El obstáculo real va de 0.5 a 2.5 m: ni 9.9 ni 0.0 deben pasar el filtro.
#         for value in received:
#             self.assertTrue(0.4 < value < 2.6, f"lectura sin filtrar: {value}")
#
#
# @launch_testing.post_shutdown_test()
# class TestShutdown(unittest.TestCase):
#     def test_los_nodos_salen_con_codigo_0(self, proc_info):
#         launch_testing.asserts.assertExitCodes(proc_info)
