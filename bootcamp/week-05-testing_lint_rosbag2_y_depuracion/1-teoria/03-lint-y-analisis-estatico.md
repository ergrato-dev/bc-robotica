# Lint y análisis estático

> Un test ejecuta tu código para ver si falla. El **análisis estático** lo lee sin ejecutarlo y encuentra fallos que un test tardaría en provocar: una variable que puede ser `None`, un `float` convertido a `int` sin avisar, una copia innecesaria. El **lint** añade las reglas de estilo, para que todo el código se lea igual. Las dos cosas se ejecutan en segundos y en cada commit.

## 🎯 Objetivos

- Usar `ruff` y `mypy` en Python, `clang-format` y `clang-tidy` en C++
- Configurar cada herramienta con su archivo por paquete
- Leer un aviso y saber qué regla lo dispara
- Convertir el lint en tests de `colcon test`

## 1. Las cuatro herramientas

| Herramienta | Lenguaje | Qué encuentra | Configuración |
|---|---|---|---|
| `ruff check` | Python | Imports sin usar, `== None`, `except:` desnudo, f-strings vacías... | `ruff.toml` |
| `ruff format` | Python | Formato: espacios, comillas, líneas largas | `ruff.toml` |
| `mypy` | Python | Errores de tipos: funciones sin tipos, `None` donde no toca | `mypy.ini` |
| `clang-format` | C++ | Formato | `.clang-format` |
| `clang-tidy` | C++ | Fallos probables, copias innecesarias, C++ antiguo | `.clang-tidy` + `compile_commands.json` |

En la imagen Docker del bootcamp ya están instaladas: `ruff` y `mypy` con
`uv tool install`, y `clang-format` y `clang-tidy` con `apt` (ver
[stack-versions](../../../docs/stack-versions.md)). Fuera de Docker:

```bash
uv tool install ruff==0.8.6
uv tool install mypy==1.13.0
sudo apt install clang-format clang-tidy
```

## 2. ruff

Desde la carpeta del paquete:

```bash
ruff check .
# ejercicio03_lint_py/battery_monitor.py:7:8: F401 [*] `os` imported but unused
# ejercicio03_lint_py/battery_monitor.py:25:19: E711 Comparison to `None` should be `cond is None`
# ejercicio03_lint_py/battery_monitor.py:55:5: E722 Do not use bare `except`
# ...
# Found 5 errors.
```

Cada línea es `archivo:línea:columna: CÓDIGO mensaje`. El código dice qué regla
saltó; buscando `ruff E722` en la web tienes la explicación completa. Las marcadas
con `[*]` las arregla solo `ruff check --fix .`.

```bash
ruff format --check .
# Would reformat: ejercicio03_lint_py/battery_monitor.py
# 1 file would be reformatted, 3 files already formatted
```

`--check` solo avisa; `ruff format .` reescribe los archivos. El formato no se
discute: lo decide la herramienta.

La configuración va en `ruff.toml`, en la carpeta del paquete:

```toml
target-version = "py312"  # el Python de Ubuntu 24.04, contra el que va rclpy

[lint]
# E/W: estilo (pycodestyle) · F: errores lógicos (pyflakes) · I: orden de
# imports · B: trampas habituales (bugbear) · UP: sintaxis moderna (pyupgrade)
select = ["E", "W", "F", "I", "B", "UP"]
```

## 3. mypy

`mypy` comprueba los **type hints**: las anotaciones `x: float` y `-> str` que
llevas usando desde la Semana 01. Con ellas sabe qué tipo tiene cada cosa y
avisa cuando no encaja:

```bash
mypy ejercicio03_lint_py
# ejercicio03_lint_py/battery_monitor.py:21: error: Function is missing a type annotation  [no-untyped-def]
# ejercicio03_lint_py/battery_monitor.py:36: error: Function is missing a return type annotation  [no-untyped-def]
# Found 2 errors in 1 file (checked 2 source files)
```

El bootcamp usa el **modo estricto** (`strict`): toda función lleva tipos. Una
función sin tipos es una función que `mypy` no revisa por dentro.

```ini
# mypy.ini
[mypy]
python_version = 3.12
strict = True
# Los paquetes de mensajes (std_msgs...) no traen información de tipos.
ignore_missing_imports = True
# rclpy trae tipos solo en parte: sin esto, cada llamada a get_logger() sería
# un error. Tu código sigue revisado en modo estricto.
disallow_untyped_calls = False

# rclpy reexporta try_shutdown sin declararlo; esto lo acepta.
[mypy-rclpy]
implicit_reexport = True
```

Un ejemplo de lo que encuentra: el Ejercicio 04 guarda la primera lectura en
`self._first: tuple[float, float] | None`, y desempaqueta
`first_s, first_percent = self._first` sin comprobar antes si es `None`. Al
ejecutarse, el nodo muere con `TypeError: cannot unpack non-iterable NoneType
object`. `mypy` lo marca sin ejecutar nada:

```text
battery_watchdog.py:48: error: "None" object is not iterable  [misc]
```

## 4. clang-format

Ya lo usas desde la Semana 01: el `.clang-format` de la raíz del repositorio es
la única referencia de formato. `clang-format` lo busca subiendo carpetas desde
cada archivo, así que en tu workspace va en `src/` (o más arriba):

```bash
cp <ruta-al-repo>/.clang-format src/
clang-format --dry-run --Werror src/ejercicio03_lint_cpp/src/battery_monitor.cpp
# src/battery_monitor.cpp:19:26: error: code should be clang-formatted [-Wclang-format-violations]
```

`--dry-run --Werror` solo comprueba; `clang-format -i <archivos>` los reescribe.

## 5. clang-tidy

`clang-tidy` analiza el código como lo haría un compilador, así que necesita
saber **cómo** se compila cada archivo: flags, includes, estándar de C++. Esa
información la escribe CMake en `compile_commands.json` si se lo pides:

```cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```

Tras `colcon build`, el archivo está en `build/<paquete>/compile_commands.json`, y
`-p` le dice a `clang-tidy` dónde buscarlo:

```bash
clang-tidy -p build/ejercicio03_lint_cpp --quiet src/ejercicio03_lint_cpp/src/battery_monitor.cpp
# .../battery_monitor.cpp:24:35: error: the parameter 'label' is copied for each invocation but only used as a const reference; consider making it a const reference [performance-unnecessary-value-param,-warnings-as-errors]
# .../battery_monitor.cpp:61:25: error: narrowing conversion from '_data_type' (aka 'float') to 'int' [bugprone-narrowing-conversions,-warnings-as-errors]
```

El nombre entre corchetes es el **chequeo** (check) que saltó. Los chequeos se
eligen en `.clang-tidy`, en la carpeta del paquete:

```yaml
Checks: >-
  -*,
  bugprone-*,
  performance-*,
  modernize-loop-convert,
  modernize-use-nullptr,
  readability-braces-around-statements
WarningsAsErrors: "*"
```

`-*` apaga todo y después se encienden familias. `bugprone-*` son fallos
probables; `performance-*`, copias y conversiones que cuestan tiempo. La
conversión `float` → `int` del ejemplo compila sin un warning con
`-Wall -Wextra -Wpedantic`: el compilador no la marca, `clang-tidy` sí.

## 6. El lint como test

Una herramienta que hay que acordarse de ejecutar acaba sin ejecutarse. Si es un
test, `colcon test` la ejecuta siempre.

**Python**: un archivo `test/test_lint.py` que lanza las herramientas y falla si
encuentran algo:

```python
def _run(*command: str) -> str:
    """Ejecuta una herramienta en PACKAGE_DIR y devuelve su salida si falla."""
    if shutil.which(command[0]) is None:
        pytest.fail(f"{command[0]} no está instalado: uv tool install {command[0]}")
    result = subprocess.run(command, cwd=PACKAGE_DIR, capture_output=True, text=True)
    return "" if result.returncode == 0 else result.stdout + result.stderr


def test_ruff_check() -> None:
    assert _run("ruff", "check", ".") == ""
```

Si falla, `colcon test-result --verbose` muestra la salida de `ruff` en el mensaje.

**C++**: `ament_add_test` registra un comando cualquiera como test (código de
salida 0 = aprobado):

```cmake
if(BUILD_TESTING)
  find_package(ament_cmake_test REQUIRED)
  find_program(CLANG_TIDY clang-tidy REQUIRED)
  ament_add_test(clang_tidy GENERATE_RESULT_FOR_RETURN_CODE_ZERO
    COMMAND ${CLANG_TIDY} -p ${CMAKE_BINARY_DIR} --quiet ${SOURCES})
endif()
```

`GENERATE_RESULT_FOR_RETURN_CODE_ZERO` hace que aparezca con su nombre en
`colcon test-result`.

> [!NOTE]
> `ros2 pkg create` añade tests de lint a los paquetes nuevos: en Python,
> `test_flake8.py`, `test_pep257.py` y `test_copyright.py`; en C++,
> `ament_lint_auto` con `ament_lint_common` (`cpplint`, `uncrustify`...). Hacen el
> mismo papel con otras herramientas. En el bootcamp se usan `ruff`, `mypy`,
> `clang-format` y `clang-tidy`, así que sustituye esos tests por los de esta
> sección.

## 7. Antipatrones

- ❌ **Silenciar el aviso en vez de entenderlo.** `# noqa`, `# type: ignore` o
  `// NOLINT` sin un comentario que explique por qué es correcto
- ❌ **Relajar la configuración para que pase.** Si `mypy.ini` acaba con
  `strict = False`, ya no revisa casi nada
- ❌ **`clang-tidy` sin `compile_commands.json`.** No encuentra los headers de
  ROS2 y llena la pantalla de errores que no son tuyos
- ❌ **Arreglar el formato a mano.** `ruff format .` y `clang-format -i` lo hacen
  en un segundo y sin discutir

## 📚 Recursos Adicionales

- [Ruff — documentación](https://docs.astral.sh/ruff/) y [lista de reglas](https://docs.astral.sh/ruff/rules/)
- [mypy — documentación](https://mypy.readthedocs.io/en/stable/)
- [clang-tidy — lista de chequeos](https://clang.llvm.org/extra/clang-tidy/checks/list.html)
- [ClangFormat](https://clang.llvm.org/docs/ClangFormat.html)

## ✅ Checklist de Verificación

- [ ] Sé qué encuentra cada una de las cuatro herramientas
- [ ] Sé buscar qué significa un código como `E722` o un chequeo como `bugprone-narrowing-conversions`
- [ ] Sé por qué `clang-tidy` necesita `compile_commands.json`
- [ ] Tengo el lint de mis paquetes como tests de `colcon test`

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · launch_testing](02-tests-de-integracion-con-launch-testing.md) | **03 · Lint y análisis estático** | [04 · rosbag2](04-grabar-y-reproducir-con-rosbag2.md) |

← [Volver a la Semana 05](../README.md)
