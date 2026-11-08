# 📖 Glosario — Semana 05

Términos A-Z. El término/API en inglés va entre paréntesis cuando existe en la
documentación oficial.

- **Análisis estático (static analysis)**: revisar el código sin ejecutarlo para
  encontrar fallos probables. `mypy` y `clang-tidy` lo hacen.
- **Bag (bag)**: grabación de los mensajes de uno o varios topics, con el instante
  de cada uno. Es una carpeta con un archivo `.mcap` (o `.db3`) y `metadata.yaml`.
- **CDR (Common Data Representation)**: formato binario en el que ROS2 serializa
  los mensajes, tanto en la red como en una bag.
- **Chequeo (check)**: cada regla de `clang-tidy`, como
  `bugprone-narrowing-conversions`. Se agrupan en familias (`bugprone-*`,
  `performance-*`...).
- **compile_commands.json (compilation database)**: archivo que CMake escribe con
  el comando exacto de compilación de cada `.cpp`. `clang-tidy` lo necesita.
- **CTest (CTest)**: herramienta de CMake que ejecuta los tests de un paquete
  `ament_cmake`. `colcon test` la usa por debajo.
- **Fixture (fixture)**: recurso que pytest prepara antes de un test y limpia
  después, como `tmp_path`.
- **Invariante (invariant)**: propiedad que debe cumplirse siempre, en cualquier
  dato: "la batería está entre 0 y 100".
- **Lint (lint)**: comprobar reglas de estilo y errores típicos del código. `ruff`
  es un linter.
- **MCAP (MCAP)**: formato de archivo por defecto de las bags en Jazzy.
- **Nivel de log (logging severity level)**: gravedad de un mensaje de log:
  `DEBUG`, `INFO`, `WARN`, `ERROR` o `FATAL`.
- **Serializar (serialize)**: convertir un mensaje en bytes; deserializar es lo
  contrario.
- **Test de integración (integration test)**: test que arranca varios nodos como
  procesos reales y comprueba lo que ocurre entre ellos. En ROS2,
  `launch_testing`.
- **Test unitario (unit test)**: test de una función o clase sola, sin ROS en
  marcha. `pytest` o `gtest`.
- **Traceback (traceback)**: cadena de llamadas que Python imprime cuando una
  excepción no se captura. Se lee de abajo arriba.
- **Type hint (type hint)**: anotación de tipo en Python (`x: float`,
  `-> str`). `mypy` la usa para comprobar el código.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Webgrafía](../4-recursos/webgrafia/README.md) | **Glosario** | [Rúbrica](../rubrica-evaluacion.md) |

← [Volver a la Semana 05](../README.md)
