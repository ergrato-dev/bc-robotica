"""Paso 4 — tu calculadora contra tf2, con el mismo escenario.

tf2_ros.Buffer funciona sin nodo ni red: se le dan las transformaciones con
set_transform y se le pregunta con lookup_transform (teoría 05, sección 3).
Si tu calculadora y tf2 dan lo mismo, la calculadora es correcta.
"""

# ============================================
# PASO 4: comparar con tf2
# ============================================
# Descomenta las siguientes líneas para el Paso 4:
#
# import math
#
# import numpy as np
# import pytest
# import rclpy.time
# import tf2_geometry_msgs  # noqa: F401  registra PointStamped en Buffer.transform
# import tf2_ros
# from geometry_msgs.msg import PointStamped, TransformStamped
#
# from ejercicio01_transform_calculator_py.homogeneous import (
#     compose,
#     make_transform,
#     rot_z,
#     transform_point,
# )
#
#
# def planar_transform(
#     parent: str, child: str, x: float, y: float, yaw: float
# ) -> TransformStamped:
#     msg = TransformStamped()
#     msg.header.frame_id = parent
#     msg.child_frame_id = child
#     msg.transform.translation.x = x
#     msg.transform.translation.y = y
#     # Cuaternión de un giro solo en z (Semana 06); la teoría 04 explica por qué.
#     msg.transform.rotation.z = math.sin(yaw / 2.0)
#     msg.transform.rotation.w = math.cos(yaw / 2.0)
#     return msg
#
#
# def make_buffer() -> tf2_ros.Buffer:
#     buffer = tf2_ros.Buffer()
#     buffer.set_transform(planar_transform("odom", "base_link", 2.0, 0.0, 0.6), "test")
#     buffer.set_transform_static(
#         planar_transform("base_link", "laser_link", 0.20, 0.05, -0.3), "test"
#     )
#     return buffer
#
#
# def test_la_cadena_coincide_con_lookup_transform() -> None:
#     ours = compose(
#         make_transform(rot_z(0.6), [2.0, 0.0, 0.0]),
#         make_transform(rot_z(-0.3), [0.20, 0.05, 0.0]),
#     )
#     theirs = make_buffer().lookup_transform("odom", "laser_link", rclpy.time.Time())
#     t = theirs.transform.translation
#     assert ours[:3, 3] == pytest.approx([t.x, t.y, t.z])
#     # La rotación compuesta es un giro de 0.6 - 0.3 = 0.3 rad.
#     assert np.allclose(ours[:3, :3], rot_z(0.3))
#
#
# def test_el_punto_coincide_con_buffer_transform() -> None:
#     point = PointStamped()
#     point.header.frame_id = "laser_link"
#     point.point.x, point.point.y = 1.5, -0.4
#     theirs = make_buffer().transform(point, "odom").point
#     ours = transform_point(
#         compose(
#             make_transform(rot_z(0.6), [2.0, 0.0, 0.0]),
#             make_transform(rot_z(-0.3), [0.20, 0.05, 0.0]),
#         ),
#         [1.5, -0.4, 0.0],
#     )
#     assert ours == pytest.approx([theirs.x, theirs.y, theirs.z])
