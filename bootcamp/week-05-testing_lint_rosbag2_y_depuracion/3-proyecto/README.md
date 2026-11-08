# Proyecto — Semana 05

## Qué capa se añade esta semana

`sensor_stub` no cambia. Lo que cambia es que, a partir de ahora, **cualquier
cambio que lo rompa lo detecta `colcon test`**:

- **Lint como tests** en las dos capas: `ruff`, `ruff format` y `mypy` en Python;
  `clang-format` y `clang-tidy` en C++
- **Test de integración** con `launch_testing`: arranca `sensor_stub` como
  proceso, lo lleva de `unconfigured` a `active` con el servicio de lifecycle y
  comprueba que solo publica en `active`
- **Bag de referencia**: unos segundos del estado real de tu misión, grabados en
  `test/data/state_bag` y versionados. Un test comprueba sobre ella las
  propiedades que tu estado debe cumplir siempre

```
src/
├── .clang-format                  # copia del de la raíz del bootcamp
├── proyecto_dominio_interfaces/   # sin cambios
├── proyecto_dominio_py/
│   ├── ruff.toml                  # nuevo
│   ├── mypy.ini                   # nuevo
│   └── test/
│       ├── test_sensor_stub.py         # de semanas anteriores
│       ├── test_lint.py                # nuevo
│       ├── test_sensor_stub_launch.py  # nuevo: launch_testing
│       ├── test_state_bag.py           # nuevo: lee la bag de referencia
│       └── data/state_bag/             # la grabas tú (Requisito 4)
└── proyecto_dominio_cpp/
    ├── .clang-tidy                # nuevo
    └── CMakeLists.txt             # tests clang_format y clang_tidy
```

## Por qué va aquí

A partir de la Semana 06 el sistema crece cada semana: launch files, TF,
simulación, Nav2. Cada capa nueva puede romper una anterior sin que lo notes
hasta que el robot no arranca. Con los tests de esta semana, `colcon test` te
avisa en el momento. Y la bag de referencia es el primer dato real de tu misión:
en la Semana 08 grabarás las de la simulación igual.

## Requisitos verificables

1. `colcon build --symlink-install` compila los tres paquetes sin errores ni warnings
2. `test_lint.py` pasa: tu código Python está limpio para `ruff` y `mypy` estricto
3. Los tests `clang_format` y `clang_tidy` de `proyecto_dominio_cpp` pasan. El
   código de la Semana 04 tiene **dos avisos de `clang-tidy`** en `on_set_mode`
   (marcados con un `TODO`): corrígelos
4. Existe `proyecto_dominio_py/test/data/state_bag` con al menos 10 estados de
   tu topic, grabados con `sensor_stub` en `active`, y `test_state_bag.py` pasa
5. `test_sensor_stub_launch.py` pasa, adaptado a tu topic
6. Añadiste a `test_state_bag.py` **al menos un invariante propio de tu
   misión** (ejemplos en la tabla de adaptación)
7. `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
8. El README de tu repositorio responde las preguntas de los cuatro ejercicios

## Cómo verificarlo, paso a paso

Copia los tres paquetes del `starter/` a `src/`, reemplazando los de la Semana 04
(este starter es su evolución; vuelve a aplicar tus renombrados), y el
`.clang-format` si no lo copiaste en el Ejercicio 03:

```bash
cp -r <ruta-al-repo>/bootcamp/week-05-testing_lint_rosbag2_y_depuracion/3-proyecto/starter/* src/
cp <ruta-al-repo>/.clang-format src/
colcon build --symlink-install
# Summary: 3 packages finished [...]
source install/setup.bash
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result --verbose
```

Con el starter sin tocar fallan dos cosas, y es lo esperado:

```text
- clang_tidy
    .../sensor_stub.hpp:123:60: error: the const qualified parameter 'request' is copied for each invocation; consider making it a reference [performance-unnecessary-value-param,-warnings-as-errors]
    .../sensor_stub.hpp:124:55: error: the parameter 'response' is copied for each invocation but only used as a const reference; consider making it a const reference [performance-unnecessary-value-param,-warnings-as-errors]
...
- proyecto_dominio_py.test.test_state_bag test_al_menos_diez_estados
    failed on setup with "Failed: falta la bag de referencia .../test/data/state_bag: grábala (README del proyecto)"
```

**Requisito 3**: pasa `request` y `response` por referencia constante
(`const std::shared_ptr<...>&`). `std::bind` sigue funcionando igual.

**Requisito 4**, grabar la bag de referencia (en cada terminal, antes,
`source install/setup.bash`):

```bash
# Terminal 1
ros2 run proyecto_dominio_py sensor_stub
```

```bash
# Terminal 2, desde la raíz del workspace
ros2 lifecycle set /sensor_stub configure
# Transitioning successful
ros2 lifecycle set /sensor_stub activate
# Transitioning successful
mkdir -p src/proyecto_dominio_py/test/data
ros2 bag record -o src/proyecto_dominio_py/test/data/state_bag --topics /dominio/state
# Ctrl+C tras unos 15 segundos
ros2 bag info src/proyecto_dominio_py/test/data/state_bag
# ...
# Messages:          13
# Topic information: Topic: /dominio/state | Type: proyecto_dominio_interfaces/msg/DomainState | Count: 13 | Serialization Format: cdr
```

Con `publish_period_s` en 1.0 sale un estado por segundo; el recorder tarda un
momento en suscribirse, así que 15 s de grabación dan algo más de 10 estados.
La bag pesa unos 9 KiB: va en git con el resto del paquete.

Con los dos arreglados:

```bash
colcon build --symlink-install
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result
# Summary: 22 tests, 0 errors, 0 failures, 0 skipped
```

Son 12 tests de Python (5 anteriores, 3 de lint, 1 de integración y 3 de la bag)
y 7 de C++ (5 de gtest y los 2 de lint); `colcon test-result` cuenta además los
3 que CTest anota en su propio resumen.

## Criterios de calidad

- Ninguna línea con `# noqa`, `# type: ignore` o `// NOLINT` sin un comentario
  que justifique por qué el código es correcto
- La configuración de lint es la del starter: si la cambias, explica por qué en
  tu README
- Los invariantes de la bag son propiedades de tu misión, no valores exactos
  copiados de una grabación
- Los tests de integración esperan con plazo, nunca con un `time.sleep` fijo

## Adaptación al dominio

Además de los renombrados de semanas anteriores (`STATE_TOPIC` en los dos tests
nuevos, el import de tu tipo en `test_state_bag.py`), escribe el invariante del
Requisito 6:

| Misión | Invariante de ejemplo para `test_state_bag.py` |
|---|---|
| 📦 Almacén | El pasillo (`location`) siempre empieza por `pasillo_` |
| 🔬 Laboratorio | Las muestras pendientes nunca superan la capacidad de la gradilla |
| 🔦 Inspección industrial | La temperatura de la cámara térmica está en el rango del sensor |
| 🧹 Oficina | El porcentaje de zona limpia nunca baja entre dos estados seguidos |
| 🌾 Agrícola | El número de surco nunca es negativo ni mayor que los del campo |
| 📚 Biblioteca | Los libros por devolver nunca superan la capacidad del carro |

Escribe en tu README qué invariante elegiste y qué fallo real detectaría.

## Checklist

- [ ] Corregí los dos avisos de `clang-tidy` del código de la Semana 04
- [ ] Grabé la bag de referencia de mi misión y está en git
- [ ] Añadí un invariante propio a `test_state_bag.py`
- [ ] `colcon test` pasa en los dos paquetes de nodos
- [ ] Respondí las preguntas de los cuatro ejercicios en mi README

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04](../2-practicas/ejercicio-04-depuracion_py/README.md) | **Proyecto** | [Recursos](../4-recursos/README.md) |

← [Volver a la Semana 05](../README.md)
