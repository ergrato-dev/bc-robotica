"""Bag de referencia: estados reales de tu misión, grabados y versionados.

Graba la bag una vez con los comandos del README del proyecto. Este test la
lee sin nada de ROS en marcha y comprueba invariantes que tu estado debe
cumplir siempre. Si un cambio futuro los rompe, la bag lo delata.
TODO: si renombraste el topic o el tipo, cambia STATE_TOPIC y el import.
"""

from pathlib import Path

import pytest
import rosbag2_py
from proyecto_dominio_interfaces.msg import DomainState
from rclpy.serialization import deserialize_message

from proyecto_dominio_py.sensor_stub import VALID_MODES

BAG = Path(__file__).parent / "data" / "state_bag"
STATE_TOPIC = "/dominio/state"


@pytest.fixture(scope="module")
def states() -> list[DomainState]:
    if not BAG.exists():
        pytest.fail(f"falta la bag de referencia {BAG}: grábala (README del proyecto)")
    reader = rosbag2_py.SequentialReader()
    reader.open(
        rosbag2_py.StorageOptions(uri=str(BAG)),
        rosbag2_py.ConverterOptions("cdr", "cdr"),
    )
    reader.set_filter(rosbag2_py.StorageFilter(topics=[STATE_TOPIC]))
    result: list[DomainState] = []
    while reader.has_next():
        _topic, data, _timestamp_ns = reader.read_next()
        result.append(deserialize_message(data, DomainState))
    return result


def test_al_menos_diez_estados(states: list[DomainState]) -> None:
    assert len(states) >= 10


def test_bateria_y_modo_validos(states: list[DomainState]) -> None:
    for msg in states:
        assert 0.0 <= msg.battery_percent <= 100.0
        assert msg.mode in VALID_MODES


def test_header_con_frame_y_en_orden(states: list[DomainState]) -> None:
    stamps = [msg.header.stamp.sec * 10**9 + msg.header.stamp.nanosec for msg in states]
    assert all(msg.header.frame_id for msg in states)
    assert stamps == sorted(stamps)
