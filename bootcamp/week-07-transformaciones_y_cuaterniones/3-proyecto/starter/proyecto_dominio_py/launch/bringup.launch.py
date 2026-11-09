"""Bringup del proyecto: el robot entero con una orden, ya en active.

Modelo, sensor_stub (la capa elegida) y, desde la Semana 07, target_locator.

ros2 launch proyecto_dominio_py bringup.launch.py impl:=cpp
"""

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    EmitEvent,
    GroupAction,
    IncludeLaunchDescription,
    RegisterEventHandler,
)
from launch.conditions import IfCondition
from launch.events import matches_action
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    EqualsSubstitution,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import LifecycleNode, Node
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from launch_ros.substitutions import FindPackageShare
from lifecycle_msgs.msg import Transition

# impl elige qué capa corre: las dos son intercambiables (mismo nodo, topic,
# servicio y TF), así que el resto del sistema no nota la diferencia.
IMPLEMENTATIONS = {"py": "proyecto_dominio_py", "cpp": "proyecto_dominio_cpp"}


def _sensor_stub(impl: str, package: str) -> GroupAction:
    """sensor_stub de `package`, llevado solo de unconfigured a active."""
    node = LifecycleNode(
        package=package,
        executable="sensor_stub",
        name="sensor_stub",
        namespace="",
        output="screen",
    )

    def change_state(transition_id: int) -> EmitEvent:
        # matches_action: el evento va a este nodo y a ningún otro.
        return EmitEvent(
            event=ChangeState(
                lifecycle_node_matcher=matches_action(node),
                transition_id=transition_id,
            )
        )

    # Cuando el nodo llega a inactive (configure terminó bien), se activa.
    # Si configure falla, el nodo se queda en unconfigured y nunca publica.
    activate_when_inactive = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=node,
            goal_state="inactive",
            entities=[change_state(Transition.TRANSITION_ACTIVATE)],
        )
    )
    return GroupAction(
        [node, activate_when_inactive, change_state(Transition.TRANSITION_CONFIGURE)],
        # Solo se lanza el grupo cuyo impl coincide con el argumento.
        condition=IfCondition(EqualsSubstitution(LaunchConfiguration("impl"), impl)),
    )


def generate_launch_description() -> LaunchDescription:
    impl_arg = DeclareLaunchArgument(
        "impl",
        default_value="py",
        choices=list(IMPLEMENTATIONS),
        description="Capa de sensor_stub que se arranca",
    )
    description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("proyecto_dominio_description"),
                    "launch",
                    "description.launch.py",
                ]
            )
        )
    )
    stubs = [_sensor_stub(impl, package) for impl, package in IMPLEMENTATIONS.items()]
    # Solo existe en Python: lee TF, así que vale con cualquiera de las capas.
    target_locator = Node(
        package="proyecto_dominio_py",
        executable="target_locator",
        output="screen",
    )
    return LaunchDescription([impl_arg, description, *stubs, target_locator])
