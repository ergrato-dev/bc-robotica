"""Pasos 1 a 4 — tus cuaterniones contra tf_transformations."""

import math

import numpy as np
import pytest
import tf_transformations as tft

from ejercicio02_quaternions_py.quaternions import (
    heading_error,
    interpolate,
    orientation_from_rpy_degrees,
    quaternion_from_axis_angle,
    quaternion_multiply,
    quaternion_norm,
    rotate_vector,
    same_rotation,
)

Z_AXIS = (0.0, 0.0, 1.0)
X_AXIS = (1.0, 0.0, 0.0)


# Paso 1


def test_un_giro_en_z_coincide_con_quaternion_from_euler() -> None:
    ours = quaternion_from_axis_angle(Z_AXIS, 1.0)
    assert ours == pytest.approx(tft.quaternion_from_euler(0.0, 0.0, 1.0))


def test_el_eje_no_tiene_que_medir_uno() -> None:
    long_axis = quaternion_from_axis_angle((0.0, 0.0, 5.0), 1.0)
    assert long_axis == pytest.approx(quaternion_from_axis_angle(Z_AXIS, 1.0))


def test_multiplicar_coincide_con_tf_transformations() -> None:
    q1 = quaternion_from_axis_angle((1.0, 2.0, 3.0), 0.7)
    q2 = quaternion_from_axis_angle((-1.0, 0.0, 2.0), 1.9)
    assert quaternion_multiply(q1, q2) == pytest.approx(tft.quaternion_multiply(q1, q2))


def test_dos_cuartos_de_vuelta_son_media_vuelta() -> None:
    quarter = quaternion_from_axis_angle(Z_AXIS, math.pi / 2)
    half = quaternion_multiply(quarter, quarter)
    assert half == pytest.approx((0.0, 0.0, 1.0, 0.0), abs=1e-12)


def test_el_orden_de_los_giros_importa() -> None:
    qx = quaternion_from_axis_angle(X_AXIS, math.pi / 2)
    qz = quaternion_from_axis_angle(Z_AXIS, math.pi / 2)
    assert quaternion_multiply(qx, qz) != pytest.approx(quaternion_multiply(qz, qx))


# Paso 2


def test_un_cuarto_de_vuelta_en_z_lleva_x_a_y() -> None:
    quarter = quaternion_from_axis_angle(Z_AXIS, math.pi / 2)
    assert rotate_vector(quarter, X_AXIS) == pytest.approx((0.0, 1.0, 0.0))


def test_rotar_coincide_con_la_matriz_del_cuaternion() -> None:
    q = quaternion_from_axis_angle((0.3, -1.0, 0.5), 2.2)
    v = (0.4, 1.5, -0.7)
    expected = tft.quaternion_matrix(q)[:3, :3] @ np.array(v)
    assert rotate_vector(q, v) == pytest.approx(expected)


def test_q_y_menos_q_son_la_misma_rotacion() -> None:
    q = quaternion_from_axis_angle((0.3, -1.0, 0.5), 2.2)
    minus_q = (-q[0], -q[1], -q[2], -q[3])
    assert same_rotation(q, minus_q)
    assert not same_rotation(q, quaternion_from_axis_angle(Z_AXIS, 2.2))


# Paso 3


def test_noventa_grados_de_yaw() -> None:
    half_sqrt2 = math.sqrt(2.0) / 2.0
    expected = (0.0, 0.0, half_sqrt2, half_sqrt2)
    assert orientation_from_rpy_degrees(0.0, 0.0, 90.0) == pytest.approx(expected)


def test_el_error_de_rumbo_toma_el_giro_corto() -> None:
    current = tft.quaternion_from_euler(0.0, 0.0, 3.0)
    goal = tft.quaternion_from_euler(0.0, 0.0, -3.0)
    # Restando a secas saldría -6.0: casi una vuelta entera hacia la derecha.
    assert heading_error(current, goal) == pytest.approx(2.0 * math.pi - 6.0)


def test_en_gimbal_lock_euler_no_vuelve_igual() -> None:
    # Con pitch de 90°, roll y yaw giran alrededor del mismo eje: de los tres
    # números de ida solo se recupera la diferencia roll - yaw.
    rpy = (0.3, math.pi / 2, 0.2)
    back = tft.euler_from_quaternion(tft.quaternion_from_euler(*rpy))
    assert back == pytest.approx((0.1, math.pi / 2, 0.0), abs=1e-6)
    # Pero es la misma orientación: el cuaternión no pierde nada.
    assert np.allclose(tft.euler_matrix(*rpy), tft.euler_matrix(*back))


# Paso 4


def test_slerp_a_mitad_de_camino() -> None:
    start = quaternion_from_axis_angle(Z_AXIS, 0.0)
    end = quaternion_from_axis_angle(Z_AXIS, math.pi / 2)
    middle = interpolate(start, end, 0.5)
    assert middle == pytest.approx(quaternion_from_axis_angle(Z_AXIS, math.pi / 4))


@pytest.mark.parametrize("fraction", [0.0, 0.25, 0.6, 1.0])
def test_slerp_sigue_siendo_unitario(fraction: float) -> None:
    start = quaternion_from_axis_angle((1.0, 1.0, 0.0), 0.4)
    end = quaternion_from_axis_angle((0.0, -1.0, 1.0), 2.5)
    q = interpolate(start, end, fraction)
    assert quaternion_norm(q) == pytest.approx(1.0)
