"""Pasos 1 a 3 — la calculadora, sin ROS.

El escenario de todos los tests: el robot está en (2, 0) de odom mirando hacia
+y (yaw de 90°) y lleva un láser 0.20 m por delante de su centro.
"""

import math
from collections.abc import Callable

import numpy as np
import pytest

from ejercicio01_transform_calculator_py.homogeneous import (
    Matrix,
    compose,
    invert_transform,
    make_transform,
    rot_x,
    rot_y,
    rot_z,
    transform_point,
    transform_vector,
)


def odom_base() -> Matrix:
    return make_transform(rot_z(math.pi / 2), [2.0, 0.0, 0.0])


def base_laser() -> Matrix:
    return make_transform(np.eye(3), [0.20, 0.0, 0.0])


# Paso 1


def test_rot_z_lleva_x_a_y() -> None:
    assert rot_z(math.pi / 2) @ [1.0, 0.0, 0.0] == pytest.approx([0.0, 1.0, 0.0])


def test_rot_y_lleva_z_a_x() -> None:
    assert rot_y(math.pi / 2) @ [0.0, 0.0, 1.0] == pytest.approx([1.0, 0.0, 0.0])


@pytest.mark.parametrize("rot", [rot_x, rot_y, rot_z])
def test_las_rotaciones_son_ortonormales(rot: Callable[[float], Matrix]) -> None:
    rotation = rot(0.7)
    assert np.allclose(rotation.T @ rotation, np.eye(3))
    assert np.linalg.det(rotation) == pytest.approx(1.0)


def test_el_orden_de_los_giros_importa() -> None:
    assert not np.allclose(
        rot_z(math.pi / 2) @ rot_x(math.pi / 2), rot_x(math.pi / 2) @ rot_z(math.pi / 2)
    )


# Paso 2


def test_la_ultima_fila_es_fija() -> None:
    assert odom_base()[3] == pytest.approx([0.0, 0.0, 0.0, 1.0])


def test_un_punto_delante_del_robot_en_odom() -> None:
    # 1 m delante del robot: el robot mira hacia +y, así que en odom es +y.
    point_odom = transform_point(odom_base(), [1.0, 0.0, 0.0])
    assert point_odom == pytest.approx([2.0, 1.0, 0.0])


def test_las_direcciones_no_se_trasladan() -> None:
    # "Hacia delante" del robot es +y en odom, esté donde esté el robot.
    forward_odom = transform_vector(odom_base(), [1.0, 0.0, 0.0])
    assert forward_odom == pytest.approx([0.0, 1.0, 0.0])


# Paso 3


def test_la_inversa_deshace_la_transformacion() -> None:
    assert np.allclose(invert_transform(odom_base()) @ odom_base(), np.eye(4))


def test_el_origen_de_odom_visto_desde_el_robot() -> None:
    # El origen de odom queda 2 m a la izquierda del robot (y positiva).
    base_odom = invert_transform(odom_base())
    assert transform_point(base_odom, [0.0, 0.0, 0.0]) == pytest.approx([0.0, 2.0, 0.0])


def test_encadenar_odom_base_laser() -> None:
    odom_laser = compose(odom_base(), base_laser())
    # Lo que el láser ve 1 m delante está 1.20 m delante del centro del robot.
    point_odom = transform_point(odom_laser, [1.0, 0.0, 0.0])
    assert point_odom == pytest.approx([2.0, 1.2, 0.0])


def test_encadenar_nada_es_la_identidad() -> None:
    assert np.allclose(compose(), np.eye(4))
