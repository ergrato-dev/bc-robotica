# Ejercicio 03 — Lint y análisis estático

Dos versiones de un monitor de batería, una en Python y otra en C++. Las dos
compilan y funcionan, pero tienen fallos que solo ven las herramientas de la
teoría 03. Cada paquete trae su lint como tests de `colcon test`: los ejecutas,
lees cada aviso y lo corriges.

**Antes de empezar**: [teoría 03](../../1-teoria/03-lint-y-analisis-estatico.md)
leída. Comprueba que tienes las herramientas (en la imagen Docker del bootcamp ya
vienen):

```bash
ruff --version
# ruff 0.8.6
mypy --version
# mypy 1.13.0 (compiled: yes)
clang-tidy --version | head -1
# Ubuntu LLVM version 18.1.3
clang-format --version
# Ubuntu clang-format version 18.1.3 (1ubuntu1)
```

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-05-testing_lint_rosbag2_y_depuracion/2-practicas/ejercicio-03-lint_y_analisis_estatico/starter/* src/
cp <ruta-al-repo>/.clang-format src/
```

El segundo `cp` pone el `.clang-format` del bootcamp en `src/`: `clang-format` lo
encuentra subiendo carpetas desde cada archivo, así que vale para todos tus
paquetes.

Estructura:

```
src/
├── .clang-format
├── ejercicio03_lint_py/
│   ├── package.xml
│   ├── setup.py
│   ├── setup.cfg
│   ├── ruff.toml                       # reglas de ruff
│   ├── mypy.ini                        # mypy en modo estricto
│   ├── resource/ejercicio03_lint_py
│   ├── ejercicio03_lint_py/
│   │   ├── __init__.py
│   │   └── battery_monitor.py          # PASOS 1 y 2
│   └── test/
│       └── test_lint.py                # ruff check, ruff format y mypy como tests
└── ejercicio03_lint_cpp/
    ├── package.xml
    ├── CMakeLists.txt                  # tests clang_format y clang_tidy
    ├── .clang-tidy                     # chequeos de clang-tidy
    └── src/
        └── battery_monitor.cpp         # PASO 3
```

Verificación:

```bash
colcon build --packages-select ejercicio03_lint_py ejercicio03_lint_cpp --symlink-install
colcon test --packages-select ejercicio03_lint_py ejercicio03_lint_cpp
colcon test-result
# build/ejercicio03_lint_cpp/Testing/.../Test.xml: 2 tests, 0 errors, 2 failures, 0 skipped
# build/ejercicio03_lint_cpp/test_results/ejercicio03_lint_cpp/clang_format.xml: 1 test, 1 error, 0 failures, 0 skipped
# build/ejercicio03_lint_cpp/test_results/ejercicio03_lint_cpp/clang_tidy.xml: 1 test, 1 error, 0 failures, 0 skipped
# build/ejercicio03_lint_py/pytest.xml: 3 tests, 0 errors, 3 failures, 0 skipped
```

Todo compila sin un warning y todo falla en el lint. Es lo esperado.

En los pasos, cada línea con un fallo lleva el comentario `elimina en el Paso N`
y encima su versión corregida, comentada. **Antes de descomentar**, ejecuta la
herramienta, lee el aviso y piensa la corrección; después compárala con la del
archivo.

## Paso 1: ruff

Desde la carpeta del paquete:

```bash
cd src/ejercicio03_lint_py
ruff check .
# ejercicio03_lint_py/battery_monitor.py:7:8: F401 [*] `os` imported but unused
# ejercicio03_lint_py/battery_monitor.py:10:29: F401 [*] `rclpy.executors.ExternalShutdownException` imported but unused
# ejercicio03_lint_py/battery_monitor.py:25:19: E711 Comparison to `None` should be `cond is None`
# ejercicio03_lint_py/battery_monitor.py:41:32: F541 [*] f-string without any placeholders
# ejercicio03_lint_py/battery_monitor.py:55:5: E722 Do not use bare `except`
# Found 5 errors.
ruff format --check .
# Would reformat: ejercicio03_lint_py/battery_monitor.py
# 1 file would be reformatted, 3 files already formatted
```

Aplica las correcciones marcadas `elimina en el Paso 1` en `battery_monitor.py`:
borra `import os`, y en cada uno de los otros cuatro sitios descomenta la versión
corregida y borra la línea marcada.

El segundo F401 (`ExternalShutdownException` sin usar) no tiene corrección
propia: desaparece al arreglar el `except:` desnudo, que pasa a capturar
exactamente esa excepción. Un aviso puede ser la pista de otro fallo.

✅ Verificación:

```bash
ruff check .
# All checks passed!
ruff format --check .
# 4 files already formatted
```

## Paso 2: mypy

```bash
mypy ejercicio03_lint_py
# ejercicio03_lint_py/battery_monitor.py:21: error: Function is missing a type annotation  [no-untyped-def]
# ejercicio03_lint_py/battery_monitor.py:36: error: Function is missing a return type annotation  [no-untyped-def]
# ejercicio03_lint_py/battery_monitor.py:36: note: Use "-> None" if function does not return a value
# Found 2 errors in 1 file (checked 2 source files)
```

Los números de línea cambian según cuánto hayas borrado en el Paso 1.

Aplica las correcciones `elimina en el Paso 2`: los tipos de `classify` y de
`__init__`. Después **ejecuta `mypy` otra vez antes de seguir**:

```bash
mypy ejercicio03_lint_py
# ejercicio03_lint_py/battery_monitor.py:...: error: Missing return statement  [return]
```

Con tipos, `mypy` ya revisa `classify` por dentro y encuentra un fallo que antes
no veía: si la batería no es `None` ni baja, la función no devuelve nada, y el
log diría `batería None`. Descomenta el `return "ok"` del final de `classify`.

✅ Verificación:

```bash
mypy ejercicio03_lint_py
# Success: no issues found in 2 source files
cd ../..
colcon test --packages-select ejercicio03_lint_py
colcon test-result
# build/ejercicio03_lint_py/pytest.xml: 3 tests, 0 errors, 0 failures, 0 skipped
```

## Paso 3: clang-format y clang-tidy

Desde la raíz del workspace, y con el paquete ya compilado (necesita
`compile_commands.json`):

```bash
clang-format --dry-run --Werror src/ejercicio03_lint_cpp/src/battery_monitor.cpp
# src/ejercicio03_lint_cpp/src/battery_monitor.cpp:19:26: error: code should be clang-formatted [-Wclang-format-violations]
# ...
clang-tidy -p build/ejercicio03_lint_cpp --quiet src/ejercicio03_lint_cpp/src/battery_monitor.cpp
# .../battery_monitor.cpp:24:35: error: the parameter 'label' is copied for each invocation but only used as a const reference; consider making it a const reference [performance-unnecessary-value-param,-warnings-as-errors]
# .../battery_monitor.cpp:33:22: error: statement should be inside braces [readability-braces-around-statements,-warnings-as-errors]
# .../battery_monitor.cpp:40:3: error: use range-based for loop instead [modernize-loop-convert,-warnings-as-errors]
# .../battery_monitor.cpp:61:25: error: narrowing conversion from '_data_type' (aka 'float') to 'int' [bugprone-narrowing-conversions,-warnings-as-errors]
```

`clang-tidy` escribe antes una línea como `36367 warnings generated.`: son avisos
dentro de los headers de ROS2, que `--quiet` y el filtro de headers ocultan. Solo
cuentan las líneas con `error:`. Los números de línea exactos pueden variar un
poco.

Aplica las correcciones `elimina en el Paso 3` de `battery_monitor.cpp`.

**Fíjate en el último**: `const int percent = msg.data;` convierte `float` a `int`
y pierde los decimales (99.9 % se vuelve 99 %). Compila sin un solo warning con
`-Wall -Wextra -Wpedantic -Werror`. Solo `clang-tidy` lo ve.

✅ Verificación:

```bash
colcon build --packages-select ejercicio03_lint_cpp --symlink-install
colcon test --packages-select ejercicio03_lint_py ejercicio03_lint_cpp
colcon test-result
# Summary: 7 tests, 0 errors, 0 failures, 0 skipped
```

Son 3 tests de Python y 2 de C++ (`clang_format` y `clang_tidy`); `colcon
test-result` cuenta además los 2 que CTest anota en su propio resumen.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. Elige dos avisos de este ejercicio y explica qué fallo real podrían causar en
   un robot.
2. ¿Por qué `mypy` no encontró el `return` que faltaba hasta que `classify` tuvo
   tipos?
3. ¿Qué aviso de `clang-tidy` no habría encontrado nunca el compilador?

## Checklist

- [ ] Los 3 tests de `ejercicio03_lint_py` y los 2 de `ejercicio03_lint_cpp` pasan
- [ ] Leí cada aviso antes de mirar la corrección
- [ ] Sé configurar `ruff.toml`, `mypy.ini` y `.clang-tidy` para mis paquetes

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02](../ejercicio-02-gtest_y_rosbag2_cpp/README.md) | **Ejercicio 03** | [Ejercicio 04](../ejercicio-04-depuracion_py/README.md) |

← [Volver a la Semana 05](../../README.md)
