"""Ejercicio 01, Semana 03 — server del servicio robot/enable (std_srvs/SetBool)."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_srvs.srv import SetBool


class EnableServer(Node):
    def __init__(self) -> None:
        super().__init__("enable_server")
        # Estado que protege el servicio: los motores arrancan deshabilitados.
        self.enabled = False

        # ============================================
        # PASO 1: Crear el servicio
        # ============================================
        # Mismo patrón que create_publisher: tipo, nombre relativo y la función
        # que atiende cada petición.
        # Descomenta la siguiente línea para el Paso 1:
        #
        # self._service = self.create_service(SetBool, "robot/enable", self._on_enable)

    def _on_enable(
        self, request: SetBool.Request, response: SetBool.Response
    ) -> SetBool.Response:
        # ============================================
        # PASO 2: Atender la petición
        # ============================================
        # Rellena la response que llega como argumento y devuélvela. Pedir el
        # estado que ya hay no es un error, pero se informa con success=False
        # para que el cliente sepa que no cambió nada.
        # Descomenta las siguientes líneas para el Paso 2:
        #
        # wanted = "habilitado" if request.data else "deshabilitado"
        # if request.data == self.enabled:
        #     response.success = False
        #     response.message = f"ya estaba {wanted}"
        # else:
        #     self.enabled = request.data
        #     response.success = True
        #     response.message = wanted
        # self.get_logger().info(f"Petición data={request.data}: {response.message}")
        return response


def main() -> None:
    rclpy.init()
    node = EnableServer()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        # try_shutdown: Ctrl+C ya cerró el contexto; shutdown() fallaría.
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
