"""Proyecto — Semana 01 — capa Python.

NOTA PARA EL APRENDIZ: adapta el topic y el contenido del mensaje a tu dominio
asignado (almacen, mesa_clasificacion, campus, mesa_ensamblado...). Ver la
tabla de adaptación en el README de este proyecto.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SensorStub(Node):
    def __init__(self) -> None:
        super().__init__("sensor_stub_py")

        # TODO: cambia "dominio/state" por el topic de tu misión
        # (ej. "almacen/state", "mesa_clasificacion/state").
        self._publisher = self.create_publisher(String, "dominio/state", 10)
        self._counter = 0
        self._timer = self.create_timer(1.0, self._on_timer)

    def _on_timer(self) -> None:
        # TODO: reemplaza este texto plano por el estado simulado real de tu
        # dominio. Por ahora basta con un contador — el mensaje custom llega
        # en la Semana 02.
        msg = String()
        msg.data = f"estado simulado #{self._counter}"
        self._publisher.publish(msg)
        self._counter += 1


def main() -> None:
    rclpy.init()
    node = SensorStub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
