# Ejercicio 02 — Ángulos de Euler, cuaterniones y `tf_transformations`

Primero escribes a mano las dos operaciones básicas de los cuaterniones,
construir y componer, y las usas para girar vectores y comparar orientaciones.
Cada resultado se comprueba contra `tf_transformations`. Después usas la
biblioteca para lo que harás en tus nodos: pasar de grados a un cuaternión,
calcular cuánto tiene que girar el robot y moverse suavemente entre dos
orientaciones.

**Antes de empezar**: teorías [03](../../1-teoria/03-angulos-de-euler.md),
[04](../../1-teoria/04-cuaterniones.md) y
[05](../../1-teoria/05-tf-transformations-y-tf2.md) leídas, y
`ros-jazzy-tf-transformations` instalado.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-07-transformaciones_y_cuaterniones/2-practicas/ejercicio-02-euler_y_cuaterniones_py/starter \
  src/ejercicio02_quaternions_py
```

Estructura:

```
src/ejercicio02_quaternions_py/
├── package.xml                         # python3-numpy, tf_transformations
├── setup.py
├── setup.cfg
├── resource/ejercicio02_quaternions_py
├── ejercicio02_quaternions_py/
│   ├── __init__.py
│   └── quaternions.py                  # PASOS 1 a 4
└── test/
    └── test_quaternions.py             # tests ya escritos de los cuatro pasos
```

Todos los cuaterniones van como tuplas `(x, y, z, w)`, el orden de ROS.
Verificación, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio02_quaternions_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio02_quaternions_py
colcon test-result --test-result-base build/ejercicio02_quaternions_py
# Summary: 16 tests, 0 errors, 15 failures, 0 skipped
```

El único que pasa es `test_en_gimbal_lock_euler_no_vuelve_igual`: usa solo
`tf_transformations` y es la sección 4 de la teoría 03 convertida en test. Léelo
antes de empezar.

## Paso 1: Construir y componer

**Abre `ejercicio02_quaternions_py/quaternions.py`**. Descomenta los bloques del
Paso 1 en `quaternion_from_axis_angle` y `quaternion_multiply`, y borra sus dos
líneas `# elimina en el Paso 1`.

**Por qué**: con estas dos funciones se construye cualquier orientación. La
primera es la fórmula de la teoría 04, sección 3: el eje se divide por su
longitud para que no tenga que medir 1. La segunda es el producto de Hamilton de
la sección 4, con `w` al final.

✅ Verificación:

```bash
colcon test --packages-select ejercicio02_quaternions_py
colcon test-result --test-result-base build/ejercicio02_quaternions_py
# Summary: 16 tests, 0 errors, 10 failures, 0 skipped
```

`test_multiplicar_coincide_con_tf_transformations` compara tu producto con
`tft.quaternion_multiply` en dos giros con ejes inclinados: si un signo de la
fórmula está mal, falla aquí.

## Paso 2: Girar y comparar

Descomenta los bloques del Paso 2 en `rotate_vector` y `same_rotation`, y borra
sus líneas `# elimina en el Paso 2`.

**Por qué**: `rotate_vector` es `q · (v, 0) · q*` (teoría 04, sección 5), solo
con lo del Paso 1. `same_rotation` compara con el producto escalar en valor
absoluto, porque `q` y `-q` son el mismo giro (sección 6).

✅ Verificación:

```bash
colcon test --packages-select ejercicio02_quaternions_py
colcon test-result --test-result-base build/ejercicio02_quaternions_py
# Summary: 16 tests, 0 errors, 7 failures, 0 skipped
```

`test_rotar_coincide_con_la_matriz_del_cuaternion` gira el mismo vector con tu
función y con la matriz de `tft.quaternion_matrix`: dos caminos, mismo
resultado.

## Paso 3: `tf_transformations` para lo de cada día

Descomenta la línea `# import tf_transformations` del principio del archivo y los
bloques del Paso 3 en `orientation_from_rpy_degrees` y `heading_error`. Borra sus
líneas `# elimina en el Paso 3`.

**Por qué**: a partir de aquí, la biblioteca. `orientation_from_rpy_degrees`
convierte la entrada de una persona (grados) en radianes **en la frontera**,
antes de llamar a `quaternion_from_euler`. `heading_error` saca el yaw de dos
orientaciones y normaliza su diferencia con `atan2(sin, cos)` (teoría 03,
sección 5): es el error que un controlador de rumbo necesita en la Semana 13.

✅ Verificación:

```bash
colcon test --packages-select ejercicio02_quaternions_py
colcon test-result --test-result-base build/ejercicio02_quaternions_py
# Summary: 16 tests, 0 errors, 5 failures, 0 skipped
```

`test_el_error_de_rumbo_toma_el_giro_corto` pasa con 0.283 rad: restando a secas
saldría -6.0, casi una vuelta entera en sentido contrario.

## Paso 4: Interpolar

Descomenta el bloque del Paso 4 en `interpolate` y borra su línea
`# elimina en el Paso 4`.

**Por qué**: `quaternion_slerp` recorre el arco más corto entre dos
orientaciones y el resultado sigue midiendo 1 (teoría 04, sección 7). Es lo que
usarás para girar una cámara o una muñeca sin tirones.

✅ Verificación:

```bash
colcon test --packages-select ejercicio02_quaternions_py
colcon test-result --test-result-base build/ejercicio02_quaternions_py
# Summary: 16 tests, 0 errors, 0 failures, 0 skipped
```

Comprueba los mismos números en la terminal:

```bash
python3 -c "import math, tf_transformations as t; print(t.quaternion_slerp([0, 0, 0, 1], t.quaternion_from_euler(0, 0, math.pi / 2), 0.5))"
# [0.         0.         0.38268343 0.92387953]
```

A mitad de camino entre 0° y 90° de yaw, 45°: `(0, 0, sin 22.5°, cos 22.5°)`.

**¿El test detecta fallos?** En `same_rotation`, cambia
`abs(abs(dot) - 1.0) < tol` por `abs(dot - 1.0) < tol`: sin el valor absoluto
del producto escalar.

```bash
colcon test --packages-select ejercicio02_quaternions_py
colcon test-result --test-result-base build/ejercicio02_quaternions_py --verbose
# - ejercicio02_quaternions_py.test.test_quaternions test_q_y_menos_q_son_la_misma_rotacion
# Summary: 16 tests, 0 errors, 1 failure, 0 skipped
```

Solo falla el test de `-q`: el error es invisible mientras nadie te devuelva el
cuaternión con el signo cambiado. Deshaz el cambio. Prueba también a quitar el
`atan2` de `heading_error` (`return error`): cae
`test_el_error_de_rumbo_toma_el_giro_corto`. Deshazlo.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué el cuaternión usa `θ/2`? Pista: compón dos veces un giro de 180° y
   mira el signo del resultado.
2. ¿Qué devolvería `heading_error` sin `atan2` si tu robot mira con yaw 3.0 y el
   objetivo está en yaw -3.0? ¿Hacia dónde giraría?
3. ¿Qué orientación de tu robot (o de su sensor) podría acercarse al bloqueo de
   cardán?

## Checklist

- [ ] Los 16 tests del paquete pasan
- [ ] Mi producto de Hamilton coincide con `tft.quaternion_multiply`
- [ ] Comparo cuaterniones con el producto escalar
- [ ] Rompí `same_rotation` y `heading_error`, y los tests lo detectaron

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01](../ejercicio-01-calculadora_transformaciones_py/README.md) | **Ejercicio 02** | [Ejercicio 03](../ejercicio-03-transformar_puntos_tf2_py/README.md) |

← [Volver a la Semana 07](../../README.md)
