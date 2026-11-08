# Ejercicio 02 — gtest y rosbag2 en C++ (`rclcpp`)

El mismo filtro de distancia del Ejercicio 01, ahora en C++. Escribes sus tests
con gtest, lees una bag con `rosbag2_cpp` y reproduces la bag que grabaste en el
Ejercicio 01 con este nodo: la bag no sabe en qué lenguaje está quien la escucha.

**Antes de empezar**: [Ejercicio 01](../ejercicio-01-tests_y_rosbag2_py/README.md)
completado y la carpeta `rango_crudo` guardada en la raíz de tu workspace.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-05-testing_lint_rosbag2_y_depuracion/2-practicas/ejercicio-02-gtest_y_rosbag2_cpp/starter \
  src/ejercicio02_gtest_rosbag2_cpp
```

Estructura:

```
src/ejercicio02_gtest_rosbag2_cpp/
├── package.xml                         # rclcpp, std_msgs, rosbag2_cpp, rosbag2_storage
├── CMakeLists.txt                      # PASO 1
├── include/ejercicio02_gtest_rosbag2_cpp/
│   ├── filtering.hpp                   # filter_range: lógica pura, sin ROS
│   └── bag_tools.hpp                   # declaración de read_ranges
├── src/
│   ├── bag_tools.cpp                   # PASO 2
│   └── range_filter_main.cpp           # nodo range_filter
└── test/
    ├── test_filtering.cpp              # PASO 1
    └── test_bag_tools.cpp              # tests ya escritos del Paso 2
```

`filter_range` y `read_ranges` van en la biblioteca `range_tools`. El ejecutable
`range_filter` y los tests enlazan la misma biblioteca: pruebas lo que se ejecuta.

Verificación:

```bash
colcon build --packages-select ejercicio02_gtest_rosbag2_cpp --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio02_gtest_rosbag2_cpp
colcon test-result --verbose
# build/ejercicio02_gtest_rosbag2_cpp/test_results/ejercicio02_gtest_rosbag2_cpp/test_bag_tools.gtest.xml: 2 tests, 0 errors, 2 failures, 0 skipped
```

Fallan los dos tests de `test_bag_tools.cpp`: esperan el Paso 2.

## Paso 1: Tests unitarios con gtest

Dos cambios, porque en C++ un test hay que escribirlo **y** registrarlo:

1. **Abre `test/test_filtering.cpp`** y descomenta el bloque del Paso 1: cuatro
   tests de `filter_range`
2. **Abre `CMakeLists.txt`** y descomenta el bloque del Paso 1, dentro de
   `if(BUILD_TESTING)`: `ament_add_gtest` compila el archivo y lo apunta para
   `colcon test`

**Por qué**: sin el paso 2, el archivo existe pero nadie lo compila. Un test que
no se ejecuta pasa siempre.

✅ Verificación:

```bash
colcon build --packages-select ejercicio02_gtest_rosbag2_cpp --symlink-install
colcon test --packages-select ejercicio02_gtest_rosbag2_cpp
colcon test-result --verbose
# .../test_bag_tools.gtest.xml: 2 tests, 0 errors, 2 failures, 0 skipped
# .../test_filtering.gtest.xml: 4 tests, 0 errors, 0 failures, 0 skipped
```

`VentanaParPromediaLasDosCentrales` comprueba que, con un número par de lecturas,
la mediana es la media de las dos centrales: igual que `statistics.median` en
Python. Así los dos filtros dan el mismo resultado con los mismos datos.

**¿El test detecta fallos?** En `filtering.hpp`, cambia `window.size() % 2 == 1`
por `window.size() % 2 == 0`: un error de una sola cifra que intercambia los casos
par e impar. Vuelve a compilar y probar:

```text
- ejercicio02_gtest_rosbag2_cpp.FilterRangeTest MedianaIgnoraUnReflejo (.../test/test_filtering.cpp:18)
- ejercicio02_gtest_rosbag2_cpp.FilterRangeTest VentanaParPromediaLasDosCentrales (.../test/test_filtering.cpp:27)
```

`colcon test-result --verbose` dice el test y la línea exacta del `EXPECT` que
falló. Deshaz el cambio.

Un cambio que no compila no sirve para esta prueba: con `-Werror`, quitar el uso
de `max_m` da un error de parámetro sin usar y el test ni siquiera se ejecuta.

## Paso 2: Leer una bag con rosbag2_cpp

**Abre `src/bag_tools.cpp`**, descomenta el bloque del Paso 2 y **borra las tres
líneas** marcadas con `// elimina esta línea al completar el Paso 2`.

`read_ranges` abre la bag, filtra un topic y devuelve sus valores en orden. Los
tests de `test_bag_tools.cpp` escriben su propia bag con `rosbag2_cpp::Writer` y:

- `LeeSoloElTopicPedidoEnOrden`: comprueba que `read_ranges` ignora el otro topic
  y respeta el orden
- `FiltroReproducidoSinPicos`: pasa las lecturas de la bag por la misma ventana
  deslizante de 5 que usa el nodo, y comprueba que el reflejo y el eco perdido no
  llegan a la salida

✅ Verificación:

```bash
colcon build --packages-select ejercicio02_gtest_rosbag2_cpp --symlink-install
colcon test --packages-select ejercicio02_gtest_rosbag2_cpp
colcon test-result --verbose
# .../test_bag_tools.gtest.xml: 2 tests, 0 errors, 0 failures, 0 skipped
# .../test_filtering.gtest.xml: 4 tests, 0 errors, 0 failures, 0 skipped
# Summary: 8 tests, 0 errors, 0 failures, 0 skipped
```

Son 6 tests de gtest. `colcon test-result` suma 2 más: CTest, la herramienta de
CMake que ejecuta los tests, anota en su propio resumen un resultado por cada
ejecutable de test (`test_filtering` y `test_bag_tools`).

## Paso 3: Reproducir la bag del Ejercicio 01

Desde la raíz del workspace (donde está `rango_crudo`):

```bash
# Terminal 1
ros2 run ejercicio02_gtest_rosbag2_cpp range_filter
```

```bash
# Terminal 2
ros2 topic echo /robot/range_m --field data
```

```bash
# Terminal 3
ros2 bag play rango_crudo --rate 2.0
```

✅ Verificación: en la terminal 2 aparecen valores filtrados, sin 9.9 ni 0.0, y la
reproducción dura la mitad que la grabación (`--rate 2.0`). Es la misma bag que
filtró el nodo Python: los dos filtros reciben exactamente los mismos datos.

Prueba también `ros2 bag play rango_crudo --loop` (vuelve a empezar hasta que
pulses `Ctrl+C`) y `--start-paused` (pulsa espacio en la terminal 3 para arrancar).

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Qué diferencia hay entre `EXPECT_EQ` y `ASSERT_EQ`? ¿Por qué
   `FiltroReproducidoSinPicos` usa `ASSERT_EQ` para el tamaño y `EXPECT_*` para
   los valores?
2. Si la bag de `rango_crudo` hubiera mostrado una lectura rara en el robot,
   ¿cómo la usarías para comprobar si el fallo está en el filtro Python o en el C++?

## Checklist

- [ ] Los 6 tests de gtest pasan
- [ ] Rompí `filter_range` y los tests del Paso 1 lo detectaron
- [ ] Reproduje `rango_crudo` con el filtro C++ a doble velocidad

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01](../ejercicio-01-tests_y_rosbag2_py/README.md) | **Ejercicio 02** | [Ejercicio 03](../ejercicio-03-lint_y_analisis_estatico/README.md) |

← [Volver a la Semana 05](../../README.md)
