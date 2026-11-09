"""Paso 1 — la geometría de la patrulla, sin ROS."""

import math

import pytest

from ejercicio01_tf_broadcaster_py.geometry import circle_pose, yaw_to_quaternion


def test_empieza_en_el_eje_x_mirando_hacia_y() -> None:
    x, y, yaw = circle_pose(0.0, radius_m=2.0, period_s=20.0)
    assert (x, y) == pytest.approx((2.0, 0.0))
    assert yaw == pytest.approx(math.pi / 2)


def test_un_cuarto_de_vuelta() -> None:
    x, y, yaw = circle_pose(5.0, radius_m=2.0, period_s=20.0)
    assert (x, y) == pytest.approx((0.0, 2.0), abs=1e-9)
    assert yaw == pytest.approx(math.pi)


@pytest.mark.parametrize("t_s", [0.0, 3.3, 7.1, 12.9, 19.9])
def test_siempre_sobre_el_circulo(t_s: float) -> None:
    x, y, _ = circle_pose(t_s, radius_m=1.5, period_s=20.0)
    assert math.hypot(x, y) == pytest.approx(1.5)


def test_el_yaw_queda_en_el_rango_de_ros() -> None:
    for step in range(200):
        _, _, yaw = circle_pose(step * 0.1, radius_m=1.0, period_s=20.0)
        assert -math.pi < yaw <= math.pi


def test_cuaternion_sin_giro() -> None:
    assert yaw_to_quaternion(0.0) == pytest.approx((0.0, 0.0, 0.0, 1.0))


def test_cuaternion_es_unitario() -> None:
    # Un cuaternión de rotación siempre mide 1; tf2 rechaza los que no.
    for yaw in (0.3, -1.2, math.pi):
        assert math.hypot(*yaw_to_quaternion(yaw)) == pytest.approx(1.0)
