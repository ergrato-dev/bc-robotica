"""Ejercicio 01, Semana 06 — la patrulla entera con una sola orden.

ros2 launch ejercicio01_tf_broadcaster_py patrol.launch.py radius_m:=2.0
"""

from launch import LaunchDescription

# ============================================
# PASO 3: un launch file con argumento y TF estática
# ============================================
# Descomenta las siguientes líneas para el Paso 3:
#
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration
# from launch_ros.actions import Node
# from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
    # Descomenta las siguientes líneas para el Paso 3:
    #
    # # Un argumento se declara para que ros2 launch lo enseñe con
    # # --show-args y para que tenga un valor por defecto.
    # radius_arg = DeclareLaunchArgument(
    #     "radius_m",
    #     default_value="1.5",
    #     description="Radio del círculo de la patrulla, en metros",
    # )
    # # ParameterValue(..., value_type=float): sin él, radius_m:=2 llegaría
    # # como entero y el nodo, que declaró un float, se negaría a arrancar.
    # radius_m = ParameterValue(LaunchConfiguration("radius_m"), value_type=float)
    # patrol = Node(
    #     package="ejercicio01_tf_broadcaster_py",
    #     executable="patrol_broadcaster",
    #     parameters=[{"radius_m": radius_m}],
    # )
    # # El láser va atornillado 0.20 m por delante y 0.15 m por encima del
    # # centro del robot: no se mueve respecto a base_link, así que es una
    # # transformación estática (/tf_static), publicada una sola vez.
    # laser_tf = Node(
    #     package="tf2_ros",
    #     executable="static_transform_publisher",
    #     arguments=[
    #         "--x", "0.20", "--z", "0.15",
    #         "--frame-id", "base_link", "--child-frame-id", "laser_link",
    #     ],
    # )  # fmt: skip
    # return LaunchDescription([radius_arg, patrol, laser_tf])
    return LaunchDescription([])  # elimina en el Paso 3
