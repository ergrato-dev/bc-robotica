"""Ejercicio 03, Semana 07 — el robot quieto, su láser y el relé de detecciones.

ros2 launch ejercicio03_point_transform_py relay.launch.py target_frame:=base_link
"""

from launch import LaunchDescription

# ============================================
# PASO 3: el escenario en un launch file
# ============================================
# Descomenta las siguientes líneas para el Paso 3:
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration
# from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    # Descomenta las siguientes líneas para el Paso 3:
    #
    # target_arg = DeclareLaunchArgument(
    #     "target_frame",
    #     default_value="odom",
    #     description="Marco en el que se publican las detecciones",
    # )
    # # El escenario del Ejercicio 01: el robot en (2, 0) de odom mirando hacia
    # # +y. Está quieto, así que aquí basta una transformación estática; en tu
    # # proyecto odom -> base_link la publica sensor_stub en /tf.
    # robot_tf = Node(
    #     package="tf2_ros",
    #     executable="static_transform_publisher",
    #     arguments=[
    #         "--x", "2.0", "--yaw", "1.5707963267948966",
    #         "--frame-id", "odom", "--child-frame-id", "base_link",
    #     ],
    # )  # fmt: skip
    # laser_tf = Node(
    #     package="tf2_ros",
    #     executable="static_transform_publisher",
    #     arguments=[
    #         "--x", "0.20",
    #         "--frame-id", "base_link", "--child-frame-id", "laser_link",
    #     ],
    # )  # fmt: skip
    # relay = Node(
    #     package="ejercicio03_point_transform_py",
    #     executable="detection_relay",
    #     parameters=[{"target_frame": LaunchConfiguration("target_frame")}],
    # )
    # return LaunchDescription([target_arg, robot_tf, laser_tf, relay])
    return LaunchDescription([])  # elimina en el Paso 3
