"""Ejercicio 04, Semana 03 — latido configurable con parámetros.

Publica "<robot_name>: alive" en robot/heartbeat cada period_s segundos.
"""

import rclpy
from rcl_interfaces.msg import FloatingPointRange, ParameterDescriptor
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import String


class Heartbeat(Node):
    def __init__(self) -> None:
        super().__init__("heartbeat")
        self._publisher = self.create_publisher(String, "robot/heartbeat", 10)
        self.robot_name = ""
        self.period_s = 0.0

        # ============================================
        # PASO 1: Declarar los parámetros
        # ============================================
        # Nombre, valor por defecto y descriptor. El descriptor documenta el
        # parámetro y ROS2 hace cumplir sus restricciones: read_only impide
        # cambiarlo en marcha; el rango rechaza valores fuera de [0.1, 5.0].
        # Descomenta las siguientes líneas para el Paso 1:
        #
        # self.declare_parameter(
        #     "robot_name",
        #     "robot",
        #     ParameterDescriptor(description="Nombre en cada latido", read_only=True),
        # )
        # self.declare_parameter(
        #     "period_s",
        #     1.0,
        #     ParameterDescriptor(
        #         description="Segundos entre latidos",
        #         floating_point_range=[FloatingPointRange(from_value=0.1, to_value=5.0)],
        #     ),
        # )

        # ============================================
        # PASO 2: Leer los parámetros y usarlos
        # ============================================
        # El valor ya incluye lo que llegue por -p o --params-file.
        # Descomenta las siguientes líneas para el Paso 2:
        #
        # self.robot_name = self.get_parameter("robot_name").value
        # self.period_s = self.get_parameter("period_s").value
        # self.timer = self.create_timer(self.period_s, self._on_timer)

        # ============================================
        # PASO 3: Reaccionar a cambios en marcha
        # ============================================
        # La post-set callback se llama después de que un `ros2 param set`
        # haya pasado las validaciones; aquí solo se aplica el cambio.
        # Descomenta la siguiente línea para el Paso 3:
        #
        # self.add_post_set_parameters_callback(self._on_parameters_set)

    def _on_timer(self) -> None:
        self._publisher.publish(String(data=f"{self.robot_name}: alive"))

    def _on_parameters_set(self, parameters: list[Parameter]) -> None:
        for parameter in parameters:
            if parameter.name == "period_s":
                self.period_s = parameter.value
                # El timer de rclpy permite cambiar el periodo sin recrearlo.
                self.timer.timer_period_ns = int(self.period_s * 1e9)
                self.get_logger().info(f"Nuevo periodo: {self.period_s} s")


def main() -> None:
    rclpy.init()
    node = Heartbeat()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
