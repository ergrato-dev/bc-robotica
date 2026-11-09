from glob import glob

from setuptools import find_packages, setup

package_name = "ejercicio03_urdf_xacro"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.launch.py")),
        # El modelo también va a share/: launch y tests lo buscan ahí.
        (f"share/{package_name}/urdf", glob("urdf/*.xacro")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="bc-robotica",
    maintainer_email="ergrato-dev@example.com",
    description="Ejercicio 03 - modelo URDF/xacro y robot_state_publisher (Semana 06)",
    license="CC-BY-NC-SA-4.0",
    tests_require=["pytest"],
)
