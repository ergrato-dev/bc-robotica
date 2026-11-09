"""Ejercicio 01, Semana 07 — calculadora de transformaciones homogéneas con NumPy.

Notación de la teoría 02: `T_a_b` es la transformación del marco `b` dentro
del marco `a`. Lleva un punto escrito en `b` a ese mismo punto escrito en `a`:
`p_a = T_a_b @ p_b`. Sin ROS, para probarlo con pytest en milisegundos.
"""

import math

import numpy as np
from numpy.typing import ArrayLike, NDArray

Matrix = NDArray[np.float64]


def rot_x(angle: float) -> Matrix:
    """Matriz 3x3 de un giro de `angle` radianes alrededor del eje x (roll)."""
    c, s = math.cos(angle), math.sin(angle)
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, c, -s],
            [0.0, s, c],
        ]
    )


def rot_y(angle: float) -> Matrix:
    """Matriz 3x3 de un giro de `angle` radianes alrededor del eje y (pitch)."""
    # ============================================
    # PASO 1: las otras dos rotaciones básicas
    # ============================================
    # El eje del giro se queda quieto: aquí la fila y la columna de y son las
    # de la identidad. Fíjate en el signo: en rot_y el -s va abajo a la
    # izquierda, al revés que en rot_x y rot_z (teoría 01, sección 3).
    # Descomenta las siguientes líneas para el Paso 1:
    #
    # c, s = math.cos(angle), math.sin(angle)
    # return np.array(
    #     [
    #         [c, 0.0, s],
    #         [0.0, 1.0, 0.0],
    #         [-s, 0.0, c],
    #     ]
    # )
    raise NotImplementedError("completa el Paso 1")  # elimina en el Paso 1


def rot_z(angle: float) -> Matrix:
    """Matriz 3x3 de un giro de `angle` radianes alrededor del eje z (yaw)."""
    # Descomenta las siguientes líneas para el Paso 1:
    #
    # c, s = math.cos(angle), math.sin(angle)
    # return np.array(
    #     [
    #         [c, -s, 0.0],
    #         [s, c, 0.0],
    #         [0.0, 0.0, 1.0],
    #     ]
    # )
    raise NotImplementedError("completa el Paso 1")  # elimina en el Paso 1


def make_transform(rotation: ArrayLike, translation: ArrayLike) -> Matrix:
    """Matriz homogénea 4x4 a partir de una rotación 3x3 y una traslación (x, y, z)."""
    # ============================================
    # PASO 2: la matriz homogénea y cómo se usa
    # ============================================
    # Arriba a la izquierda la rotación, en la última columna la traslación,
    # y la última fila (0, 0, 0, 1) fija para que se puedan multiplicar.
    # Descomenta las siguientes líneas para el Paso 2:
    #
    # transform = np.eye(4)
    # transform[:3, :3] = rotation
    # transform[:3, 3] = translation
    # return transform
    raise NotImplementedError("completa el Paso 2")  # elimina en el Paso 2


def transform_point(transform: Matrix, point: ArrayLike) -> Matrix:
    """El punto (x, y, z) escrito en el marco hijo, escrito en el marco padre."""
    # Un punto lleva un 1 como cuarta coordenada: le afecta la traslación.
    # Descomenta las siguientes líneas para el Paso 2:
    #
    # homogeneous = np.append(np.asarray(point, dtype=np.float64), 1.0)
    # result: Matrix = transform @ homogeneous
    # return result[:3]
    raise NotImplementedError("completa el Paso 2")  # elimina en el Paso 2


def transform_vector(transform: Matrix, vector: ArrayLike) -> Matrix:
    """Una dirección (velocidad, eje) del marco hijo, escrita en el marco padre."""
    # Una dirección lleva un 0: gira con el marco pero no se traslada.
    # Descomenta las siguientes líneas para el Paso 2:
    #
    # homogeneous = np.append(np.asarray(vector, dtype=np.float64), 0.0)
    # result: Matrix = transform @ homogeneous
    # return result[:3]
    raise NotImplementedError("completa el Paso 2")  # elimina en el Paso 2


def invert_transform(transform: Matrix) -> Matrix:
    """T_b_a a partir de T_a_b, sin invertir la matriz 4x4 entera."""
    # ============================================
    # PASO 3: invertir y encadenar
    # ============================================
    # La inversa de una rotación es su traspuesta, y la traslación hay que
    # girarla y cambiarla de signo (teoría 02, sección 4).
    # Descomenta las siguientes líneas para el Paso 3:
    #
    # rotation = transform[:3, :3]
    # translation = transform[:3, 3]
    # return make_transform(rotation.T, -rotation.T @ translation)
    raise NotImplementedError("completa el Paso 3")  # elimina en el Paso 3


def compose(*transforms: Matrix) -> Matrix:
    """Encadena transformaciones de padre a hijo: compose(T_a_b, T_b_c) es T_a_c."""
    # Se multiplican en el orden del árbol, de la raíz hacia la hoja. Sin
    # argumentos, la identidad: no mover nada.
    # Descomenta las siguientes líneas para el Paso 3:
    #
    # result = np.eye(4)
    # for transform in transforms:
    #     result = result @ transform
    # return result
    raise NotImplementedError("completa el Paso 3")  # elimina en el Paso 3
