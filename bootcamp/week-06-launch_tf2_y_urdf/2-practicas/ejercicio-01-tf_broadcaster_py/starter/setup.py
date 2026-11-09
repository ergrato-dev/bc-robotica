from glob import glob

from setuptools import find_packages, setup

package_name = "ejercicio01_tf_broadcaster_py"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        # Los launch files se instalan en share/: ros2 launch los busca ahí.
        (f"share/{package_name}/launch", glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="bc-robotica",
    maintainer_email="ergrato-dev@example.com",
    description="Ejercicio 01 - broadcaster TF2 y launch file en rclpy (Semana 06)",
    license="CC-BY-NC-SA-4.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "patrol_broadcaster = ejercicio01_tf_broadcaster_py.patrol_broadcaster:main",
        ],
    },
)
