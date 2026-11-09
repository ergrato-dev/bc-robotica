"""Pasos 1 y 2 — el modelo expandido por xacro es un URDF válido y completo."""

import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import xacro
from ament_index_python.packages import get_package_share_directory

MODEL = (
    Path(get_package_share_directory("ejercicio03_urdf_xacro"))
    / "urdf"
    / "rover.urdf.xacro"
)


@pytest.fixture(scope="module")
def urdf_xml() -> str:
    # Lo mismo que hace `xacro rover.urdf.xacro` en la terminal.
    return xacro.process_file(str(MODEL)).toxml()


@pytest.fixture(scope="module")
def robot(urdf_xml: str) -> ET.Element:
    return ET.fromstring(urdf_xml)


def test_check_urdf_acepta_el_modelo(urdf_xml: str, tmp_path: Path) -> None:
    assert shutil.which("check_urdf"), "falta check_urdf (paquete urdfdom)"
    urdf_file = tmp_path / "rover.urdf"
    urdf_file.write_text(urdf_xml)
    result = subprocess.run(
        ["check_urdf", str(urdf_file)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_estan_todos_los_links(robot: ET.Element) -> None:
    links = {link.get("name") for link in robot.findall("link")}
    assert links == {
        "base_link",
        "laser_link",
        "left_wheel_link",
        "right_wheel_link",
        "caster_link",
    }


def test_las_ruedas_giran_sobre_el_eje_y(robot: ET.Element) -> None:
    for side in ("left", "right"):
        joint = robot.find(f"joint[@name='{side}_wheel_joint']")
        assert joint is not None, f"falta {side}_wheel_joint"
        # continuous: gira sin límite, como una rueda.
        assert joint.get("type") == "continuous"
        axis = joint.find("axis")
        assert axis is not None and axis.get("xyz") == "0 1 0"


def test_ruedas_a_cada_lado(robot: ET.Element) -> None:
    y = {}
    for side in ("left", "right"):
        origin = robot.find(f"joint[@name='{side}_wheel_joint']/origin")
        assert origin is not None
        y[side] = float(origin.get("xyz", "0 0 0").split()[1])
    # REP 103: y positivo es la izquierda del robot.
    assert y["left"] > 0 > y["right"]
    assert y["left"] == pytest.approx(-y["right"])


def test_todo_link_tiene_masa(robot: ET.Element) -> None:
    links = robot.findall("link")
    assert links, "el modelo no tiene links"
    for link in links:
        mass = link.find("inertial/mass")
        assert mass is not None, f"{link.get('name')} sin <inertial>"
        assert float(mass.get("value", "0")) > 0
