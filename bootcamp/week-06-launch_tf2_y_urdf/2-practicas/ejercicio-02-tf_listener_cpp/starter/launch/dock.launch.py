"""Ejercicio 02, Semana 06 — patrulla (Python) + dock + monitor (C++).

ros2 launch ejercicio02_tf_listener_cpp dock.launch.py
"""

from launch import LaunchDescription

# ============================================
# PASO 3: incluir un launch file de otro paquete
# ============================================
# Descomenta las siguientes líneas para el Paso 3:
#
# from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
# from launch_ros.actions import Node
# from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    # Descomenta las siguientes líneas para el Paso 3:
    #
    # radius_arg = DeclareLaunchArgument(
    #     "radius_m", default_value="1.5", description="Radio de la patrulla, en metros"
    # )
    # # FindPackageShare busca la carpeta share/ del paquete instalado: el
    # # launch file funciona desde cualquier carpeta y en cualquier máquina.
    # patrol = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         PathJoinSubstitution(
    #             [
    #                 FindPackageShare("ejercicio01_tf_broadcaster_py"),
    #                 "launch",
    #                 "patrol.launch.py",
    #             ]
    #         )
    #     ),
    #     # El argumento de este launch se reenvía al incluido.
    #     launch_arguments={"radius_m": LaunchConfiguration("radius_m")}.items(),
    # )
    # # El dock está fijo en el suelo, a 3 m del origen de odom: TF estática.
    # dock_tf = Node(
    #     package="tf2_ros",
    #     executable="static_transform_publisher",
    #     arguments=["--x", "3.0", "--frame-id", "odom", "--child-frame-id", "dock"],
    # )
    # monitor = Node(package="ejercicio02_tf_listener_cpp", executable="dock_monitor")
    # return LaunchDescription([radius_arg, patrol, dock_tf, monitor])
    return LaunchDescription([])  # elimina en el Paso 3
