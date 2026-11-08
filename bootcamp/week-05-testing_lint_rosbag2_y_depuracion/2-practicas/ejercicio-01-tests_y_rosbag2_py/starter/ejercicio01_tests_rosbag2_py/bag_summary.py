"""Ejercicio 01, Semana 05 — resumen de un topic Float64 grabado en una bag.

Uso:
  ros2 run ejercicio01_tests_rosbag2_py bag_summary <carpeta_bag> <topic>
"""

import sys
from dataclasses import dataclass


@dataclass
class BagSummary:
    count: int
    min_m: float
    max_m: float


def summarize(bag_uri: str, topic: str) -> BagSummary:
    """Lee la bag mensaje a mensaje y resume los valores de `topic`."""
    # ============================================
    # PASO 3: leer una bag con rosbag2_py
    # ============================================
    # SequentialReader abre la bag (MCAP o SQLite: lo detecta solo) y entrega
    # los mensajes en orden de tiempo como (topic, bytes, timestamp_ns). Los
    # bytes van serializados en CDR; deserialize_message los convierte de nuevo
    # en un Float64.
    # Descomenta las siguientes líneas para el Paso 3:
    #
    # import rosbag2_py
    # from rclpy.serialization import deserialize_message
    # from std_msgs.msg import Float64
    #
    # reader = rosbag2_py.SequentialReader()
    # reader.open(
    #     rosbag2_py.StorageOptions(uri=bag_uri),
    #     rosbag2_py.ConverterOptions("cdr", "cdr"),
    # )
    # values: list[float] = []
    # while reader.has_next():
    #     name, data, _timestamp_ns = reader.read_next()
    #     if name == topic:
    #         values.append(deserialize_message(data, Float64).data)
    # if not values:
    #     raise ValueError(f"la bag no tiene mensajes de {topic}")
    # return BagSummary(len(values), min(values), max(values))
    raise NotImplementedError("completa el Paso 3")  # elimina en el Paso 3


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("uso: bag_summary <carpeta_bag> <topic>")
    try:
        summary = summarize(sys.argv[1], sys.argv[2])
    except ValueError as error:
        sys.exit(str(error))
    print(
        f"mensajes: {summary.count}, min: {summary.min_m:.3f}, max: {summary.max_m:.3f}"
    )


if __name__ == "__main__":
    main()
