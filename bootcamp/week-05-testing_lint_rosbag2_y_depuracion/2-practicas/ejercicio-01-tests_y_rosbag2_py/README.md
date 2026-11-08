# Ejercicio 01 — Tests y rosbag2 en Python (`rclpy`)

Un sensor de distancia simulado (`range_sim`) mete de vez en cuando lecturas
falsas: un reflejo de 9.9 m y un eco perdido de 0.0 m. El nodo `range_filter` las
quita con una mediana. Los dos nodos ya funcionan: tú escribes los tests que lo
demuestran, grabas el sensor en una bag y la lees desde código.

**Antes de empezar**: teorías [01](../../1-teoria/01-tests-con-pytest-y-gtest.md),
[02](../../1-teoria/02-tests-de-integracion-con-launch-testing.md) y
[04](../../1-teoria/04-grabar-y-reproducir-con-rosbag2.md) leídas.

## Preparar el workspace

Copia el starter dentro de `src/` de tu workspace (la carpeta que contiene `src/`):

```bash
cp -r <ruta-al-repo>/bootcamp/week-05-testing_lint_rosbag2_y_depuracion/2-practicas/ejercicio-01-tests_y_rosbag2_py/starter \
  src/ejercicio01_tests_rosbag2_py
```

Estructura:

```
src/ejercicio01_tests_rosbag2_py/
├── package.xml                         # rclpy, std_msgs, rosbag2_py + dependencias de test
├── setup.py                            # tres ejecutables
├── setup.cfg
├── resource/ejercicio01_tests_rosbag2_py
├── ejercicio01_tests_rosbag2_py/
│   ├── __init__.py
│   ├── filtering.py                    # filter_range: lógica pura, sin ROS
│   ├── range_sim.py                    # sensor con lecturas falsas
│   ├── range_filter.py                 # nodo que aplica filter_range
│   └── bag_summary.py                  # PASO 3
└── test/
    ├── test_filtering.py               # PASO 1
    ├── test_range_filter_launch.py     # PASO 2
    └── test_bag_summary.py             # test ya escrito del Paso 3
```

Verificación, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio01_tests_rosbag2_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio01_tests_rosbag2_py
colcon test-result --verbose
# build/ejercicio01_tests_rosbag2_py/pytest.xml: 2 tests, 0 errors, 2 failures, 0 skipped
```

Fallan los dos tests de `test_bag_summary.py`: esperan el Paso 3. Los de los
Pasos 1 y 2 aún no existen: están comentados y los activas tú.

## Paso 0: Ver los datos

En cada terminal, primero `source install/setup.bash`:

```bash
# Terminal 1
ros2 run ejercicio01_tests_rosbag2_py range_sim
```

```bash
# Terminal 2
ros2 topic echo /robot/range_raw_m --field data
# ...
# 1.9273798802338298
# ---
# 9.9
# ---
# 1.7392493292139823
# ---
# ...
# 0.0
# ---
```

Ahora arranca el filtro y mira su salida:

```bash
# Terminal 3
ros2 run ejercicio01_tests_rosbag2_py range_filter
```

```bash
# Terminal 2 (Ctrl+C al echo anterior)
ros2 topic echo /robot/range_m --field data
```

Ni un 9.9 ni un 0.0: los valores van y vienen entre 0.5 y 2.5. Parece que
funciona. Los pasos siguientes lo **demuestran**. Deja `range_sim` en marcha para
el Paso 3; cierra el resto.

## Paso 1: Tests unitarios con pytest

**Abre `test/test_filtering.py`** y descomenta el bloque del Paso 1: cinco tests de
`filter_range` (uno de ellos con `parametrize`, que cuenta como tres).

**Por qué**: `filter_range` no depende de ROS, así que se prueba en milisegundos
y cada caso límite (ventana vacía, todo fuera de rango) tiene su test.

✅ Verificación:

```bash
colcon test --packages-select ejercicio01_tests_rosbag2_py
colcon test-result --verbose
# build/ejercicio01_tests_rosbag2_py/pytest.xml: 7 tests, 0 errors, 2 failures, 0 skipped
```

Los cinco nuevos pasan; los dos fallos siguen siendo los del Paso 3.

**¿El test detecta fallos?** En `filtering.py`, cambia `median` por `mean` (en el
import y en la función), vuelve a compilar y a probar:

```text
- ejercicio01_tests_rosbag2_py.test.test_filtering test_mediana_ignora_un_reflejo
  <<< failure message
    assert 2.84 == 1.1
```

Deshaz el cambio antes de seguir.

## Paso 2: Test de integración con launch_testing

**Abre `test/test_range_filter_launch.py`** y descomenta el bloque del Paso 2. El
test arranca `range_sim` y `range_filter` como procesos, escucha 30 mensajes de
`robot/range_m` y comprueba que ninguno es un reflejo o un eco perdido. Después,
que los dos nodos terminan con código 0.

**Por qué**: el Paso 1 prueba la función, no que el nodo la use, que lea el topic
correcto o que arranque. Esto solo se ve con los procesos de verdad.

✅ Verificación (tarda unos segundos más: arranca dos nodos):

```bash
colcon test --packages-select ejercicio01_tests_rosbag2_py
colcon test-result --verbose
# build/ejercicio01_tests_rosbag2_py/pytest.xml: 8 tests, 0 errors, 2 failures, 0 skipped
```

**¿El test detecta fallos?** En `range_filter.py`, cambia el `window` por defecto
de `5` a `1` (una ventana de una lectura no filtra nada). Vuelve a probar: ahora
falla `test_range_filter_launch`. Los tests del Paso 1 siguen pasando, porque
`filter_range` está bien: el fallo está en cómo la usa el nodo. Deshaz el cambio.

## Paso 3: Grabar una bag y leerla desde código

Con `range_sim` en marcha en la terminal 1, graba unos 5 segundos y para con `Ctrl+C`:

```bash
# Terminal 2, desde la raíz del workspace
ros2 bag record -o rango_crudo --topics /robot/range_raw_m
# [INFO] [...] [rosbag2_recorder]: Subscribed to topic '/robot/range_raw_m'
# ...
```

```bash
ros2 bag info rango_crudo
# ...
# Messages:          46
# Topic information: Topic: /robot/range_raw_m | Type: std_msgs/msg/Float64 | Count: 46 | Serialization Format: cdr
```

El número depende de cuánto grabaste: 10 por segundo. **Guarda la carpeta
`rango_crudo`**: la usas en el Ejercicio 02.

Para `range_sim` (`Ctrl+C` en la terminal 1) y reproduce la bag con el filtro en
marcha:

```bash
# Terminal 1
ros2 run ejercicio01_tests_rosbag2_py range_filter
```

```bash
# Terminal 3
ros2 topic echo /robot/range_m --field data
```

```bash
# Terminal 2
ros2 bag play rango_crudo
```

El filtro procesa la bag como si fuera el sensor: en la terminal 3 aparecen
valores filtrados durante los segundos que dura la grabación.

Ahora léela desde código. **Abre `ejercicio01_tests_rosbag2_py/bag_summary.py`**,
descomenta el bloque del Paso 3 y **borra la línea
`raise NotImplementedError(...)`** marcada con `# elimina en el Paso 3`.

✅ Verificación:

```bash
colcon test --packages-select ejercicio01_tests_rosbag2_py
colcon test-result --verbose
# build/ejercicio01_tests_rosbag2_py/pytest.xml: 8 tests, 0 errors, 0 failures, 0 skipped

ros2 run ejercicio01_tests_rosbag2_py bag_summary rango_crudo /robot/range_raw_m
# mensajes: 46, min: 0.000, max: 9.900

ros2 run ejercicio01_tests_rosbag2_py bag_summary rango_crudo /otro
# la bag no tiene mensajes de /otro
# [ros2run]: Process exited with failure 1
```

`min: 0.000` y `max: 9.900` son el eco perdido y el reflejo: la bag guarda los
datos crudos, sin filtrar. `test_bag_summary.py` no usa tu grabación: escribe
su propia bag pequeña en una carpeta temporal, así el test no depende de nada
que haya fuera de él.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. En el Paso 2, el test de integración falló y los unitarios no. ¿Qué te dice
   eso sobre dónde estaba el fallo?
2. ¿Por qué el test de integración comprueba que los valores están entre 0.4 y
   2.6 y no compara con valores exactos?
3. ¿Qué topic de tu misión grabarías para reproducir un fallo que solo pasa a
   veces? ¿Cuántos segundos?

## Checklist

- [ ] Los 8 tests del paquete pasan
- [ ] Rompí `filter_range` y el Paso 1 lo detectó; rompí `window` y lo detectó el Paso 2
- [ ] Grabé `rango_crudo`, la reproduje con el filtro y la resumí con `bag_summary`
- [ ] Guardé la carpeta `rango_crudo` para el Ejercicio 02

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Prácticas](../README.md) | **Ejercicio 01** | [Ejercicio 02](../ejercicio-02-gtest_y_rosbag2_cpp/README.md) |

← [Volver a la Semana 05](../../README.md)
