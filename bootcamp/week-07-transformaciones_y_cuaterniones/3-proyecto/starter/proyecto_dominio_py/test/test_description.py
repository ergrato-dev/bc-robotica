"""El modelo del robot: URDF válido, con el sensor de tu misión y sus ruedas.

TODO: si renombraste sensor_link en robot.urdf.xacro, cambia SENSOR_FRAME.
"""

import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import xacro
from ament_index_python.packages import get_package_share_directory

MODEL = (
    Path(get_package_share_directory("proyecto_dominio_description"))
    / "urdf"
    / "robot.urdf.xacro"
)
SENSOR_FRAME = "sensor_link"


@pytest.fixture(scope="module")
def urdf_xml() -> str:
    return xacro.process_file(str(MODEL)).toxml()


@pytest.fixture(scope="module")
def robot(urdf_xml: str) -> ET.Element:
    return ET.fromstring(urdf_xml)


def test_check_urdf_acepta_el_modelo(urdf_xml: str, tmp_path: Path) -> None:
    assert shutil.which("check_urdf"), "falta check_urdf (paquete urdfdom)"
    urdf_file = tmp_path / "robot.urdf"
    urdf_file.write_text(urdf_xml)
    result = subprocess.run(
        ["check_urdf", str(urdf_file)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_base_link_es_la_raiz(robot: ET.Element) -> None:
    children = {joint.find("child").get("link") for joint in robot.findall("joint")}
    links = {link.get("name") for link in robot.findall("link")}
    # La raíz es el único link que no es hijo de ninguna articulación.
    assert links - children == {"base_link"}


def test_el_sensor_cuelga_fijo_del_robot(robot: ET.Element) -> None:
    joints = [
        j for j in robot.findall("joint") if j.find("child").get("link") == SENSOR_FRAME
    ]
    assert len(joints) == 1, f"falta la articulación de {SENSOR_FRAME}"
    assert joints[0].get("type") == "fixed"


def test_dos_ruedas_motrices(robot: ET.Element) -> None:
    wheels = [j for j in robot.findall("joint") if j.get("type") == "continuous"]
    assert len(wheels) >= 2, "Requisito 2: añade las ruedas (joints continuous)"
    sides = []
    for joint in wheels:
        axis = joint.find("axis")
        assert axis is not None and axis.get("xyz") == "0 1 0", joint.get("name")
        sides.append(float(joint.find("origin").get("xyz").split()[1]))
    # REP 103: y positivo es la izquierda. Al menos una rueda a cada lado.
    assert min(sides) < 0 < max(sides)


def test_todo_link_tiene_masa(robot: ET.Element) -> None:
    for link in robot.findall("link"):
        mass = link.find("inertial/mass")
        assert mass is not None, f"{link.get('name')} sin <inertial>"
        assert float(mass.get("value", "0")) > 0
