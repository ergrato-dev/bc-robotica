"""Paso 1 — to_frame con un buffer sin red: el escenario del Ejercicio 01."""

import math

import pytest
import tf2_ros
from geometry_msgs.msg import PointStamped, TransformStamped

from ejercicio03_point_transform_py.detection_relay import to_frame


def make_buffer() -> tf2_ros.Buffer:
    robot = TransformStamped()
    robot.header.frame_id, robot.child_frame_id = "odom", "base_link"
    robot.transform.translation.x = 2.0
    robot.transform.rotation.z = math.sin(math.pi / 4)
    robot.transform.rotation.w = math.cos(math.pi / 4)
    laser = TransformStamped()
    laser.header.frame_id, laser.child_frame_id = "base_link", "laser_link"
    laser.transform.translation.x = 0.20
    buffer = tf2_ros.Buffer()
    buffer.set_transform(robot, "test")
    buffer.set_transform_static(laser, "test")
    return buffer


def detection(frame_id: str) -> PointStamped:
    point = PointStamped()
    point.header.frame_id = frame_id
    point.point.x = 1.0
    return point


def test_la_deteccion_escrita_en_odom() -> None:
    result = to_frame(make_buffer(), detection("laser_link"), "odom")
    assert result.header.frame_id == "odom"
    p = result.point
    assert (p.x, p.y, p.z) == pytest.approx((2.0, 1.2, 0.0))


def test_en_base_link_solo_cuenta_el_laser() -> None:
    p = to_frame(make_buffer(), detection("laser_link"), "base_link").point
    assert (p.x, p.y, p.z) == pytest.approx((1.2, 0.0, 0.0))


def test_un_marco_desconocido_lanza_lookup_exception() -> None:
    with pytest.raises(tf2_ros.LookupException):
        to_frame(make_buffer(), detection("camera_link"), "odom")
