"""Ejercicio 01, Semana 03 — cliente del servicio robot/enable.

Uso: ros2 run ejercicio01_servicio_py enable_client true|false
"""

import sys

import rclpy
from rclpy.node import Node
from rclpy.task import Future
from rclpy.utilities import remove_ros_args
from std_srvs.srv import SetBool


class EnableClient(Node):
    def __init__(self) -> None:
        super().__init__("enable_client")

        # ============================================
        # PASO 3: Crear el cliente
        # ============================================
        # Tipo y nombre tienen que coincidir con los del server, como en un topic.
        # Descomenta la siguiente línea para el Paso 3:
        #
        # self._client = self.create_client(SetBool, "robot/enable")

    def send(self, enable: bool) -> Future:
        """Envía la petición sin bloquear; el resultado llega en el Future."""
        # ============================================
        # PASO 4: Llamada asíncrona
        # ============================================
        # wait_for_service evita mandar la petición a un server que aún no
        # existe; call_async devuelve enseguida un Future que se completa
        # cuando llega la response.
        # Descomenta las siguientes líneas para el Paso 4:
        #
        # if not self._client.wait_for_service(timeout_sec=2.0):
        #     raise RuntimeError("el servicio robot/enable no está disponible")
        # return self._client.call_async(SetBool.Request(data=enable))
        raise NotImplementedError("Paso 4")  # elimina esta línea al completarlo


def main() -> None:
    rclpy.init()
    # remove_ros_args quita los --ros-args; queda [programa, true|false].
    args = remove_ros_args(sys.argv)
    enable = len(args) > 1 and args[1].lower() == "true"
    node = EnableClient()
    try:
        future = node.send(enable)
        # Hace spin solo hasta que llega la response; luego el programa termina.
        rclpy.spin_until_future_complete(node, future, timeout_sec=5.0)
        result = future.result()
        if result is None:
            node.get_logger().error("sin respuesta en 5 segundos")
        else:
            node.get_logger().info(
                f"success={result.success} message='{result.message}'"
            )
    except RuntimeError as error:
        node.get_logger().error(str(error))
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
