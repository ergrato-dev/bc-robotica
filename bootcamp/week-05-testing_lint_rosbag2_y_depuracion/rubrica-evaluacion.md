# Rúbrica de Evaluación — Semana 05

Evaluación en tres componentes. Mínimo **70%** en cada uno para aprobar la semana.

## 🧠 Conocimiento (30%)

Cuestionario de autoevaluación. Responde primero sin ver las respuestas.

1. ¿Qué diferencia hay entre un test unitario y uno de integración? Da un fallo
   que solo detecta el segundo.
2. ¿Por qué `filter_range` vive en un archivo aparte del nodo?
3. En gtest, ¿cuándo usas `ASSERT_*` en lugar de `EXPECT_*`? ¿Y por qué no
   `EXPECT_EQ` para comparar dos `double`?
4. ¿Qué tres partes tiene un archivo de `launch_testing` y cuándo corre cada una?
5. ¿Qué comprueba `assertExitCodes` y qué fallo de un `main` detecta?
6. ¿Por qué `clang-tidy` necesita `compile_commands.json`, y cómo se genera?
7. Nombra un fallo que `clang-tidy` encuentra y el compilador con
   `-Wall -Wextra -Wpedantic` no.
8. ¿Qué dos archivos hay dentro de la carpeta de una bag y qué guarda cada uno?
9. Un nodo no recibe nada y su log dice `offering incompatible QoS ... Last
   incompatible policy: RELIABILITY`. ¿Qué pasa y cómo lo arreglas?
10. ¿Cómo activas los mensajes `DEBUG` de un solo nodo, y por qué no de todos?

<details>
<summary>Ver respuestas</summary>

1. El unitario prueba una función sola, sin ROS; el de integración arranca los
   nodos como procesos. Solo el segundo detecta, por ejemplo, un topic mal
   escrito, un QoS incompatible o un nodo que muere al arrancar.
2. Porque así se prueba con pytest o gtest en milisegundos, sin arrancar nodos.
   Lo que queda dentro de un callback solo se puede probar arrancando el nodo.
3. `ASSERT_*` cuando seguir no tiene sentido si falla (por ejemplo, comprobar el
   tamaño antes de leer elementos). Con `double`, el redondeo hace que valores
   "iguales" difieran en el último decimal: se usa `EXPECT_DOUBLE_EQ` o
   `EXPECT_NEAR`.
4. `generate_test_description()` (al principio: qué procesos arrancar), las
   clases normales (tests activos, con los nodos en marcha tras `ReadyToTest`) y
   las clases con `post_shutdown_test` (tras parar los nodos).
5. Que todos los procesos terminaron con código 0. Detecta un nodo que termina
   con traceback, por ejemplo un `main` que no captura
   `ExternalShutdownException` al recibir SIGINT.
6. Para analizar cada archivo con las mismas flags, includes y estándar con los
   que se compila. Con `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)` en
   `CMakeLists.txt`; queda en `build/<paquete>/`.
7. Una conversión `float` → `int` implícita (`bugprone-narrowing-conversions`),
   o un parámetro copiado sin necesidad (`performance-unnecessary-value-param`).
8. El `.mcap` con los mensajes serializados y su instante, y `metadata.yaml` con
   el resumen: topics, tipos, QoS, duración y número de mensajes.
9. El publicador es best effort y el suscriptor pide reliable: no hay entrega
   posible. Se arregla haciendo que el suscriptor use un QoS compatible, en un
   sensor el mismo perfil (`qos_profile_sensor_data`).
10. `--ros-args --log-level <nodo>:=debug`. Con `--log-level debug` a secas se
    activan también los loggers del middleware y la salida se llena de líneas
    que no son tuyas.

</details>

## 💪 Desempeño (40%)

Verificado automáticamente por `colcon test` en cada `starter/`:

| Ejercicio | Verificación |
|---|---|
| 01 (`rclpy`) | `test_filtering` (5), `test_range_filter_launch`, `test_bag_summary` (2) |
| 02 (`rclcpp`) | `FilterRangeTest.*` (4), `BagToolsTest.LeeSoloElTopicPedidoEnOrden`, `BagToolsTest.FiltroReproducidoSinPicos` |
| 03 (Python + C++) | `test_ruff_check`, `test_ruff_format`, `test_mypy`, `clang_format`, `clang_tidy` |
| 04 (`rclpy`) | `test_watchdog_launch` |

Además, en los Ejercicios 01 y 02, haber roto el código a propósito y visto
fallar el test correspondiente (checklist de cada ejercicio).

```bash
colcon test --packages-select ejercicio01_tests_rosbag2_py ejercicio02_gtest_rosbag2_cpp \
  ejercicio03_lint_py ejercicio03_lint_cpp ejercicio04_depuracion_py
colcon test-result --verbose
```

## 📦 Producto (30%)

La capa del proyecto del dominio (`3-proyecto/`):

- [ ] `test_lint.py`, `clang_format` y `clang_tidy` pasan (incluidos los dos
      avisos corregidos en `on_set_mode`)
- [ ] `test_sensor_stub_launch.py` pasa con el topic de tu misión
- [ ] Bag de referencia versionada en `test/data/state_bag` y
      `test_state_bag.py` pasa, con un invariante propio de tu misión
- [ ] `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
- [ ] Respuestas de los cuatro ejercicios en el README del proyecto

### Penalizaciones (ver también `.github/copilot-instructions.md`)

| Situación | Penalización |
|---|---|
| No compila/lintea limpio | 0 en Producto |
| `# noqa`, `# type: ignore` o `// NOLINT` sin justificar | -10 |
| Configuración de lint relajada para que pase (`strict = False`, chequeos quitados) | -10 |
| Invariante de la bag que solo copia valores de la grabación | -10 |
| `time.sleep` fijo en lugar de esperar con plazo | -10 |
| Código copiado de otra misión/dominio | 0 en Producto |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica** | [Semana 06](../week-06-launch_tf2_y_urdf/README.md) |

← [Volver a la Semana 05](README.md)
