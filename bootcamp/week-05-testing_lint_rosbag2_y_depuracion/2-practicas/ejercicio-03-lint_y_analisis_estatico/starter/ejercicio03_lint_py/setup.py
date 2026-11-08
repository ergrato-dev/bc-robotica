from setuptools import find_packages, setup

package_name = "ejercicio03_lint_py"

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
    description="Ejercicio 03 - ruff y mypy (Semana 05)",
    license="CC-BY-NC-SA-4.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "battery_monitor = ejercicio03_lint_py.battery_monitor:main",
        ],
    },
)
