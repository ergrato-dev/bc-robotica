"""Paso 1 — tests unitarios de filter_range con pytest. Sin ROS: puro Python."""

# ============================================
# PASO 1: tests unitarios
# ============================================
# Cada función test_* es un test. pytest la ejecuta y la da por buena si
# ningún assert falla. parametrize repite el mismo test con varios datos.
# Descomenta las siguientes líneas para el Paso 1:
#
# import pytest
#
# from ejercicio01_tests_rosbag2_py.filtering import filter_range
#
#
# def test_mediana_ignora_un_reflejo() -> None:
#     assert filter_range([1.0, 1.1, 9.9, 1.2, 1.0], 0.05, 4.0) == 1.1
#
#
# @pytest.mark.parametrize(
#     ("window", "expected"),
#     [
#         ([5.0, 6.0, 7.0], 4.0),  # todo por encima del máximo: se recorta a 4.0
#         ([0.0, 0.01, 0.02], 0.05),  # todo por debajo del mínimo: se recorta a 0.05
#         ([2.0], 2.0),  # una sola lectura: la mediana es ella misma
#     ],
# )
# def test_recorta_al_rango_del_sensor(window: list[float], expected: float) -> None:
#     assert filter_range(window, 0.05, 4.0) == expected
#
#
# def test_ventana_vacia_es_un_error() -> None:
#     with pytest.raises(ValueError):
#         filter_range([], 0.05, 4.0)
