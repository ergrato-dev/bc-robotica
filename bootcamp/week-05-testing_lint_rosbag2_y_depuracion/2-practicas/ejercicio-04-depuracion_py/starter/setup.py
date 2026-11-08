from setuptools import find_packages, setup

package_name = "ejercicio04_depuracion_py"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="bc-robotica",
    maintainer_email="ergrato-dev@example.com",
    description="Ejercicio 04 - depuración (Semana 05)",
    license="CC-BY-NC-SA-4.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "battery_sim = ejercicio04_depuracion_py.battery_sim:main",
            "battery_watchdog = ejercicio04_depuracion_py.battery_watchdog:main",
        ],
    },
)
