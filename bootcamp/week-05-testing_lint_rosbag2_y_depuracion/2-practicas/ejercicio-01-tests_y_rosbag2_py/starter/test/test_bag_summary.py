"""Paso 3 — summarize contra una bag escrita por el propio test."""

from pathlib import Path

import pytest
import rosbag2_py
from rclpy.serialization import serialize_message
from std_msgs.msg import Float64

from ejercicio01_tests_rosbag2_py.bag_summary import summarize

RAW_TOPIC = "/robot/range_raw_m"


def _write_bag(uri: Path, values: list[float]) -> None:
    """Escribe una bag MCAP con `values` en RAW_TOPIC y uno de ruido en otro topic."""
    writer = rosbag2_py.SequentialWriter()
    writer.open(
        rosbag2_py.StorageOptions(uri=str(uri), storage_id="mcap"),
        rosbag2_py.ConverterOptions("cdr", "cdr"),
    )
    for topic in (RAW_TOPIC, "/otro_topic"):
        writer.create_topic(
            rosbag2_py.TopicMetadata(
                id=0,
                name=topic,
                type="std_msgs/msg/Float64",
                serialization_format="cdr",
            )
        )
    writer.write("/otro_topic", serialize_message(Float64(data=100.0)), 0)
    for i, value in enumerate(values):
        writer.write(
            RAW_TOPIC, serialize_message(Float64(data=value)), (i + 1) * 100_000_000
        )
    del writer  # cerrar el writer termina de escribir el archivo


def test_resume_solo_el_topic_pedido(tmp_path: Path) -> None:
    bag = tmp_path / "bag"
    _write_bag(bag, [1.5, 9.9, 0.0, 2.0])
    summary = summarize(str(bag), RAW_TOPIC)
    assert (summary.count, summary.min_m, summary.max_m) == (4, 0.0, 9.9)


def test_topic_ausente_es_un_error(tmp_path: Path) -> None:
    bag = tmp_path / "bag"
    _write_bag(bag, [1.5])
    with pytest.raises(ValueError):
        summarize(str(bag), "/no_existe")
