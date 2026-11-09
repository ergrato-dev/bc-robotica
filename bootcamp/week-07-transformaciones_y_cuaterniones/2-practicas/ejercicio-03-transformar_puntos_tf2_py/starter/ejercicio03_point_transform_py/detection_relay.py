"""Ejercicio 03, Semana 07 — llevar una detección del marco del láser a odom.

Un detector publica lo que ve en el marco de su sensor (laser_link). Para
decidir algo con esa posición (ir hacia ella, recordarla) hace falta escrita
en un marco que no se mueva con el robot: este nodo la reescribe en
`target_frame` con tf2.
"""

import rclpy
import tf2_geometry_msgs  # noqa: F401  registra PointStamped en Buffer.transform
import tf2_ros
from geometry_msgs.msg import PointStamped
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


def to_frame(
    buffer: tf2_ros.Buffer, point: PointStamped, target_frame: str
) -> PointStamped:
    """El mismo punto, escrito en `target_frame`."""
    # ============================================
    # PASO 1: transformar un punto con tf2
    # ============================================
    # Buffer.transform busca la transformación de point.header.frame_id a
    # target_frame en el instante point.header.stamp (0 = la más reciente) y
    # la aplica: es el transform_point del Ejercicio 01 con la matriz que
    # devolvería lookup_transform. Si no la encuentra, lanza una excepción.
    # Descomenta las siguientes líneas para el Paso 1:
    #
    # result: PointStamped = buffer.transform(point, target_frame)
    # return result
    raise NotImplementedError("completa el Paso 1")  # elimina en el Paso 1


class DetectionRelay(Node):
    def __init__(self) -> None:
        super().__init__("detection_relay")
        self._target_frame = self.declare_parameter("target_frame", "odom").value
        # ============================================
        # PASO 2: el nodo
        # ============================================
        # El listener llena el buffer con /tf y /tf_static en su propio hilo;
        # la suscripción recibe cada detección y la publica ya transformada.
        # Descomenta las siguientes líneas para el Paso 2:
        #
        # self._buffer = tf2_ros.Buffer()
        # self._listener = tf2_ros.TransformListener(self._buffer, self)
        # self._publisher = self.create_publisher(PointStamped, "detection", 10)
        # self.create_subscription(
        #     PointStamped, "laser/detection", self._on_detection, 10
        # )

    def _on_detection(self, msg: PointStamped) -> None:
        # Al arrancar, la primera detección puede llegar antes que las
        # transformaciones; y un frame_id mal escrito no existe nunca. En los
        # dos casos se avisa y se descarta esa detección, sin tirar el nodo.
        # Descomenta las siguientes líneas para el Paso 2:
        #
        # try:
        #     point = to_frame(self._buffer, msg, self._target_frame)
        #     self._publisher.publish(point)
        # except (
        #     tf2_ros.LookupException,
        #     tf2_ros.ConnectivityException,
        #     tf2_ros.ExtrapolationException,
        # ) as error:
        #     source = msg.header.frame_id
        #     self.get_logger().warning(
        #         f"no puedo llevar {source} a {self._target_frame}: {error}"
        #     )
        pass  # elimina en el Paso 2


def main() -> None:
    rclpy.init()
    node = DetectionRelay()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
