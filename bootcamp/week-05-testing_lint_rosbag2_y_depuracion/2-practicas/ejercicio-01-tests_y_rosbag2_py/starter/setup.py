from setuptools import find_packages, setup

package_name = "ejercicio01_tests_rosbag2_py"

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
    description="Ejercicio 01 - pytest, launch_testing y rosbag2 en rclpy (Semana 05)",
    license="CC-BY-NC-SA-4.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "range_sim = ejercicio01_tests_rosbag2_py.range_sim:main",
            "range_filter = ejercicio01_tests_rosbag2_py.range_filter:main",
            "bag_summary = ejercicio01_tests_rosbag2_py.bag_summary:main",
        ],
    },
)
