"""Test de integración del Ejercicio 04. No lo edites: pasa al completar los tres pasos."""

import os
import unittest

import launch
import launch_ros.actions
import launch_testing.actions
import launch_testing.asserts
import pytest

# Dominio DDS propio: colcon test corre paquetes en paralelo y así los nodos
# de otros tests no se mezclan con los de este.
ENV = {"ROS_DOMAIN_ID": str(os.getpid() % 100 + 1)}
WATCHDOG = launch_ros.actions.Node(
    package="ejercicio04_depuracion_py",
    executable="battery_watchdog",
    additional_env=ENV,
)


@pytest.mark.launch_test
def generate_test_description() -> launch.LaunchDescription:
    return launch.LaunchDescription(
        [
            launch_ros.actions.Node(
                package="ejercicio04_depuracion_py",
                executable="battery_sim",
                additional_env=ENV,
            ),
            WATCHDOG,
            launch_testing.actions.ReadyToTest(),
        ]
    )


class TestWatchdog(unittest.TestCase):
    def test_estima_el_tiempo_restante(self, proc_output):
        # Espera a que el watchdog escriba esa frase en su salida (log incluido).
        proc_output.assertWaitFor("tiempo restante", process=WATCHDOG, timeout=15)


@launch_testing.post_shutdown_test()
class TestShutdown(unittest.TestCase):
    def test_los_nodos_salen_con_codigo_0(self, proc_info):
        # Un traceback deja al nodo con código de salida 1: este test lo detecta.
        launch_testing.asserts.assertExitCodes(proc_info)
