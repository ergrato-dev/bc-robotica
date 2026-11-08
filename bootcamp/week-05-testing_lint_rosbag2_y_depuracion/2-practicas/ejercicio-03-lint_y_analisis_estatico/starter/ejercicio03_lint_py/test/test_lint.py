"""ruff y mypy como tests: colcon test falla si el código no está limpio.

No los edites: pasan solos al completar los Pasos 1 y 2.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

# La carpeta del paquete, donde están ruff.toml y mypy.ini.
PACKAGE_DIR = Path(__file__).resolve().parent.parent


def _run(*command: str) -> str:
    """Ejecuta una herramienta en PACKAGE_DIR y devuelve su salida si falla."""
    if shutil.which(command[0]) is None:
        pytest.fail(f"{command[0]} no está instalado: uv tool install {command[0]}")
    result = subprocess.run(command, cwd=PACKAGE_DIR, capture_output=True, text=True)
    return "" if result.returncode == 0 else result.stdout + result.stderr


def test_ruff_check() -> None:
    assert _run("ruff", "check", ".") == ""


def test_ruff_format() -> None:
    assert _run("ruff", "format", "--check", ".") == ""


def test_mypy() -> None:
    assert _run("mypy", "ejercicio03_lint_py") == ""
