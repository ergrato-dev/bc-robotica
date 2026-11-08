from setuptools import find_packages, setup

package_name = "ejercicio04_parametros_py"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        # Instala el YAML en share/ para poder pasarlo con --params-file.
        (f"share/{package_name}/config", ["config/heartbeat.yaml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="bc-robotica",
    maintainer_email="ergrato-dev@example.com",
    description="Ejercicio 04 - parametros en rclpy (Semana 03)",
    license="CC-BY-NC-SA-4.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "heartbeat = ejercicio04_parametros_py.heartbeat:main",
        ],
    },
)
