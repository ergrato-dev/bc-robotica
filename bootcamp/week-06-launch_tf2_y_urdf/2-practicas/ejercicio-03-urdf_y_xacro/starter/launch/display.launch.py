"""Ejercicio 03, Semana 06 — publica el modelo del rover en TF.

ros2 launch ejercicio03_urdf_xacro display.launch.py
"""

from launch import LaunchDescription

# ============================================
# PASO 3: robot_state_publisher y joint_state_publisher
# ============================================
# Descomenta las siguientes líneas para el Paso 3:
#
# from launch.substitutions import Command, PathJoinSubstitution
# from launch_ros.actions import Node
# from launch_ros.parameter_descriptions import ParameterValue
# from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    # Descomenta las siguientes líneas para el Paso 3:
    #
    # model = PathJoinSubstitution(
    #     [FindPackageShare("ejercicio03_urdf_xacro"), "urdf", "rover.urdf.xacro"]
    # )
    # # Command ejecuta xacro al lanzar y devuelve el URDF ya expandido.
    # # value_type=str: es texto XML, que launch no debe intentar leer como YAML.
    # robot_description = ParameterValue(Command(["xacro ", model]), value_type=str)
    # # robot_state_publisher lee el URDF: publica las articulaciones fixed en
    # # /tf_static y, con cada /joint_states, las móviles en /tf.
    # state_publisher = Node(
    #     package="robot_state_publisher",
    #     executable="robot_state_publisher",
    #     parameters=[{"robot_description": robot_description}],
    # )
    # # Sin motores todavía (Semana 10), alguien tiene que decir el ángulo de
    # # las ruedas: joint_state_publisher publica 0 rad en /joint_states.
    # joint_publisher = Node(
    #     package="joint_state_publisher", executable="joint_state_publisher"
    # )
    # return LaunchDescription([state_publisher, joint_publisher])
    return LaunchDescription([])  # elimina en el Paso 3
