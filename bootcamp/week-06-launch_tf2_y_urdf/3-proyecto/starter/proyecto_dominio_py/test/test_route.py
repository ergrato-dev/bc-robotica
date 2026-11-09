"""La ruta simulada: ida y vuelta, siempre dentro de la recta."""

import math

import pytest

from proyecto_dominio_py.route import route_pose, yaw_to_quaternion


def test_a_la_ida_avanza_mirando_hacia_delante() -> None:
    assert route_pose(3.0, length_m=10.0) == pytest.approx((3.0, 0.0))


def test_a_la_vuelta_retrocede_mirando_hacia_atras() -> None:
    assert route_pose(13.0, length_m=10.0) == pytest.approx((7.0, math.pi))


def test_tras_una_vuelta_completa_vuelve_al_origen() -> None:
    assert route_pose(20.0, length_m=10.0) == pytest.approx((0.0, 0.0))


@pytest.mark.parametrize("distance_m", [0.0, 4.2, 9.99, 10.0, 17.5, 123.4])
def test_nunca_sale_de_la_recta(distance_m: float) -> None:
    x, _ = route_pose(distance_m, length_m=10.0)
    assert 0.0 <= x <= 10.0


def test_cuaternion_de_media_vuelta() -> None:
    assert yaw_to_quaternion(math.pi) == pytest.approx((0.0, 0.0, 1.0, 0.0), abs=1e-12)
