"""Ejercicio 01, Semana 06 — broadcaster TF de la patrulla.

Publica en /tf la transformación odom -> base_link: dónde está el robot dentro
del marco odom en cada instante. La geometría vive en geometry.py.
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

# ============================================
# PASO 2: un broadcaster TF en rclpy
# ============================================
# TransformBroadcaster publica TransformStamped en /tf. Cada mensaje dice:
# "en el instante stamp, child_frame_id está en esta posición y orientación
# respecto a frame_id".
# Descomenta las siguientes líneas para el Paso 2:
#
# from geometry_msgs.msg import TransformStamped
# from tf2_ros import TransformBroadcaster
#
# from ejercicio01_tf_broadcaster_py.geometry import circle_pose, yaw_to_quaternion


class PatrolBroadcaster(Node):
    def __init__(self) -> None:
        super().__init__("patrol_broadcaster")
        self._radius_m = self.declare_parameter("radius_m", 1.5).value
        self._period_s = self.declare_parameter("period_s", 20.0).value
        self._start = self.get_clock().now()
        # Descomenta las siguientes líneas para el Paso 2:
        #
        # self._broadcaster = TransformBroadcaster(self)
        # # 20 Hz: quien consulte TF entre dos mensajes interpola, y a esta
        # # velocidad el error de interpolar es de milímetros.
        # self.create_timer(0.05, self._on_timer)

    def _on_timer(self) -> None:
        # Descomenta las siguientes líneas para el Paso 2:
        #
        # now = self.get_clock().now()
        # t_s = (now - self._start).nanoseconds / 1e9
        # x, y, yaw = circle_pose(t_s, self._radius_m, self._period_s)
        # msg = TransformStamped()
        # # stamp: el instante en que la pose es válida. TF lo usa para
        # # interpolar y para descartar datos viejos.
        # msg.header.stamp = now.to_msg()
        # msg.header.frame_id = "odom"
        # msg.child_frame_id = "base_link"
        # msg.transform.translation.x = x
        # msg.transform.translation.y = y
        # # El robot se mueve en el suelo: z = 0 siempre.
        # qx, qy, qz, qw = yaw_to_quaternion(yaw)
        # msg.transform.rotation.x = qx
        # msg.transform.rotation.y = qy
        # msg.transform.rotation.z = qz
        # msg.transform.rotation.w = qw
        # self._broadcaster.sendTransform(msg)
        pass  # elimina en el Paso 2


def main() -> None:
    rclpy.init()
    node = PatrolBroadcaster()
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
