"""Publica el modelo del robot en TF: robot_state_publisher + joint_state_publisher.

ros2 launch proyecto_dominio_description description.launch.py
"""

from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    model = PathJoinSubstitution(
        [FindPackageShare("proyecto_dominio_description"), "urdf", "robot.urdf.xacro"]
    )
    # value_type=str: el URDF es texto XML, no YAML.
    robot_description = ParameterValue(Command(["xacro ", model]), value_type=str)
    return LaunchDescription(
        [
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[{"robot_description": robot_description}],
            ),
            # Ruedas a 0 rad hasta que haya motores simulados (Semana 10).
            Node(package="joint_state_publisher", executable="joint_state_publisher"),
        ]
    )
