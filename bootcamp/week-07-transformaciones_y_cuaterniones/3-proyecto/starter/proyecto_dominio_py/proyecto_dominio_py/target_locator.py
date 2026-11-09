"""Proyecto — Semana 07 — dónde está el objetivo de la misión visto desde el sensor.

El objetivo (la estantería, la válvula, la planta...) está quieto en un punto
conocido de odom. Cada periodo, este nodo lo escribe en el marco del sensor con
tf2 y decide si el sensor lo tiene delante: dentro de su campo de visión y a su
alcance. Es Python, como manda la política de la Fase 2: no hay ni frecuencia
fija ni punto de extensión que pida C++. Adapta los TODO a tu misión.
"""

import math

import rclpy
import tf2_geometry_msgs  # noqa: F401  registra PointStamped en Buffer.transform
import tf2_ros
from geometry_msgs.msg import PointStamped
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Bool

from proyecto_dominio_py.sensor_stub import ODOM_FRAME
from proyecto_dominio_py.targeting import bearing_and_range, in_field_of_view

# TODO: el link de tu sensor principal (Requisito 3 de la Semana 06).
SENSOR_FRAME = "sensor_link"
# TODO: renombra los topics con el prefijo de tu misión, como dominio/state.
TARGET_TOPIC = "dominio/target_in_sensor"
VISIBLE_TOPIC = "dominio/target_visible"
# TODO: dónde está el objetivo de tu misión en odom (tabla de adaptación).
DEFAULT_TARGET_XYZ = [6.0, 1.0, 0.5]


class TargetLocator(Node):
    def __init__(self) -> None:
        super().__init__("target_locator")
        target_xyz = self.declare_parameter("target_xyz", DEFAULT_TARGET_XYZ).value
        # TODO: el campo de visión y el alcance de tu sensor, de su hoja de datos.
        h_fov_deg = self.declare_parameter("h_fov_deg", 60.0).value
        v_fov_deg = self.declare_parameter("v_fov_deg", 45.0).value
        self._max_range_m = self.declare_parameter("max_range_m", 4.0).value
        period_s = self.declare_parameter("period_s", 0.2).value
        self._h_fov_rad = math.radians(h_fov_deg)
        self._v_fov_rad = math.radians(v_fov_deg)
        # El objetivo, escrito en odom. stamp a 0: Buffer.transform usará la
        # transformación más reciente que tenga.
        self._target = PointStamped()
        self._target.header.frame_id = ODOM_FRAME
        self._target.point.x, self._target.point.y, self._target.point.z = target_xyz
        self._buffer = tf2_ros.Buffer()
        self._listener = tf2_ros.TransformListener(self._buffer, self)
        self._target_pub = self.create_publisher(PointStamped, TARGET_TOPIC, 10)
        self._visible_pub = self.create_publisher(Bool, VISIBLE_TOPIC, 10)
        self._visible: bool | None = None
        self.create_timer(period_s, self._on_timer)

    def _on_timer(self) -> None:
        # TODO (Requisito 3): escribe self._target en SENSOR_FRAME con
        # self._buffer.transform, como to_frame en el Ejercicio 03. Si tf2 lanza
        # LookupException, ConnectivityException o ExtrapolationException (al
        # arrancar aún no hay TF), sal sin publicar. Si sale bien, publica el
        # punto en self._target_pub y pásalo a self._report_visibility.
        pass

    def _report_visibility(self, in_sensor: PointStamped) -> None:
        """Publica si el objetivo está a la vista y lo anota cuando cambia."""
        p = in_sensor.point
        bearing, elevation, range_m = bearing_and_range(p.x, p.y, p.z)
        visible = in_field_of_view(
            bearing,
            elevation,
            range_m,
            self._h_fov_rad,
            self._v_fov_rad,
            self._max_range_m,
        )
        self._visible_pub.publish(Bool(data=visible))
        if visible != self._visible:
            self._visible = visible
            state = "a la vista" if visible else "fuera de vista"
            self.get_logger().info(
                f"objetivo {state}: rumbo {math.degrees(bearing):.0f}°, "
                f"elevación {math.degrees(elevation):.0f}°, {range_m:.1f} m"
            )


def main() -> None:
    rclpy.init()
    node = TargetLocator()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
