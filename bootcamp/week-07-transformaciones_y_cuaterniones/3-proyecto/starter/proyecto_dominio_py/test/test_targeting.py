"""Requisito 2 — rumbo, elevación y distancia del objetivo, sin ROS."""

import math

import pytest

from proyecto_dominio_py.targeting import bearing_and_range, in_field_of_view

FOV_60 = math.radians(60.0)
FOV_45 = math.radians(45.0)


def test_justo_delante() -> None:
    assert bearing_and_range(2.0, 0.0, 0.0) == pytest.approx((0.0, 0.0, 2.0))


def test_a_la_izquierda_el_rumbo_es_positivo() -> None:
    bearing, elevation, range_m = bearing_and_range(0.0, 3.0, 0.0)
    assert (bearing, elevation, range_m) == pytest.approx((math.pi / 2, 0.0, 3.0))


def test_por_encima_la_elevacion_es_positiva() -> None:
    bearing, elevation, range_m = bearing_and_range(1.0, 0.0, 1.0)
    assert (bearing, elevation) == pytest.approx((0.0, math.pi / 4))
    assert range_m == pytest.approx(math.sqrt(2.0))


def test_detras_el_rumbo_es_media_vuelta() -> None:
    bearing, _, _ = bearing_and_range(-1.0, 0.0, 0.0)
    assert abs(bearing) == pytest.approx(math.pi)


def test_dentro_del_campo_de_vision() -> None:
    assert in_field_of_view(math.radians(20), 0.1, 3.0, FOV_60, FOV_45, 4.0)


@pytest.mark.parametrize(
    ("bearing", "elevation", "range_m"),
    [(math.radians(35), 0.0, 1.0), (0.0, math.radians(30), 1.0), (0.0, 0.0, 4.5)],
)
def test_fuera_por_angulo_o_por_alcance(
    bearing: float, elevation: float, range_m: float
) -> None:
    assert not in_field_of_view(bearing, elevation, range_m, FOV_60, FOV_45, 4.0)
