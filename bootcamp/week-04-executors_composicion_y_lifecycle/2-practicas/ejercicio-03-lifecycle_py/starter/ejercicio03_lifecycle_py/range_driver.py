"""Ejercicio 03, Semana 04 — driver de un sensor de distancia como nodo lifecycle.

Simula un sensor que mide la distancia al obstáculo de delante y la publica en
robot/range_m. Como nodo lifecycle, no publica nada hasta que alguien lo
configura y lo activa:

  unconfigured --configure--> inactive --activate--> active
"""

import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.lifecycle import Node as LifecycleNode
from rclpy.lifecycle import Publisher, State, TransitionCallbackReturn
from rclpy.timer import Timer
from std_msgs.msg import Float64


class RangeDriver(LifecycleNode):
    def __init__(self, **kwargs) -> None:
        # **kwargs deja pasar parameter_overrides, como hacen los tests.
        super().__init__("range_driver", **kwargs)
        # Se declara en __init__ para poder fijarlo con -p antes de configurar.
        self.declare_parameter("rate_hz", 5.0)
        self.publisher: Publisher | None = None
        self.timer: Timer | None = None
        self._readings = 0

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        # ============================================
        # PASO 1: configure — validar y reservar recursos
        # ============================================
        # Aquí iría abrir el puerto serie del sensor. Si la configuración no
        # sirve, FAILURE deja el nodo en unconfigured y nada queda a medias.
        # El publisher es "lifecycle": solo entrega mensajes en active.
        # Descomenta las siguientes líneas para el Paso 1:
        #
        # rate_hz = self.get_parameter("rate_hz").value
        # if rate_hz <= 0.0:
        #     self.get_logger().error(f"rate_hz debe ser > 0, llegó {rate_hz}")
        #     return TransitionCallbackReturn.FAILURE
        # self.publisher = self.create_lifecycle_publisher(Float64, "robot/range_m", 10)
        # self.get_logger().info(f"Configurado a {rate_hz} Hz")
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        # ============================================
        # PASO 2 (parte A): activate — empezar a trabajar
        # ============================================
        # super().on_activate activa los publishers lifecycle; sin esa
        # llamada, publish() descarta los mensajes sin avisar.
        # Descomenta las siguientes líneas para el Paso 2:
        #
        # period_s = 1.0 / self.get_parameter("rate_hz").value
        # self.timer = self.create_timer(period_s, self._on_timer)
        # self.get_logger().info("Activo")
        # return super().on_activate(state)
        return TransitionCallbackReturn.SUCCESS  # elimina en el Paso 2

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        # ============================================
        # PASO 2 (parte B): deactivate — parar sin soltar recursos
        # ============================================
        # El timer se destruye; el publisher sigue creado pero inactivo, listo
        # para un activate inmediato.
        # Descomenta las siguientes líneas para el Paso 2:
        #
        # if self.timer is not None:
        #     self.destroy_timer(self.timer)
        #     self.timer = None
        # self.get_logger().info("Inactivo")
        # return super().on_deactivate(state)
        return TransitionCallbackReturn.SUCCESS  # elimina en el Paso 2

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        # ============================================
        # PASO 3: cleanup y shutdown — soltar lo reservado en configure
        # ============================================
        # Vuelve a unconfigured: aquí se cerraría el puerto serie. shutdown
        # llama a lo mismo porque puede llegar desde cualquier estado.
        # Descomenta las siguientes líneas para el Paso 3:
        #
        # if self.publisher is not None:
        #     self.destroy_publisher(self.publisher)
        #     self.publisher = None
        # self.get_logger().info("Recursos liberados")
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        if self.timer is not None:
            self.destroy_timer(self.timer)
            self.timer = None
        return self.on_cleanup(state)

    def _on_timer(self) -> None:
        # Distancia simulada: un obstáculo que se acerca y se aleja entre 0.5 y
        # 2.5 m. Sin el sensor real, basta para ver datos que cambian.
        self._readings += 1
        distance_m = 1.5 + math.sin(self._readings / 10.0)
        assert self.publisher is not None
        self.publisher.publish(Float64(data=distance_m))


def main() -> None:
    rclpy.init()
    node = RangeDriver()
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
