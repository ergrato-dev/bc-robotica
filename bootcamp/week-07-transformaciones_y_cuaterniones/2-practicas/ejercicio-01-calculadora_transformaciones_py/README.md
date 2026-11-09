# Ejercicio 01 — Calculadora de transformaciones con NumPy

Escribes, función a función, lo que tf2 hace por dentro: rotaciones, matrices
homogéneas, transformar puntos y direcciones, invertir y encadenar. Al final la
comparas con tf2 en el mismo escenario: si dan lo mismo, la calculadora es
correcta y ya sabes qué hace tf2 cuando le pides `odom → laser_link`.

**Antes de empezar**: teorías [01](../../1-teoria/01-rotaciones-y-matrices.md) y
[02](../../1-teoria/02-matrices-homogeneas.md) leídas.

## Preparar el workspace

Copia el starter dentro de `src/` de tu workspace (la carpeta que contiene `src/`):

```bash
cp -r <ruta-al-repo>/bootcamp/week-07-transformaciones_y_cuaterniones/2-practicas/ejercicio-01-calculadora_transformaciones_py/starter \
  src/ejercicio01_transform_calculator_py
```

Estructura:

```
src/ejercicio01_transform_calculator_py/
├── package.xml                           # python3-numpy; tf2 solo para el test del Paso 4
├── setup.py
├── setup.cfg
├── resource/ejercicio01_transform_calculator_py
├── ejercicio01_transform_calculator_py/
│   ├── __init__.py
│   └── homogeneous.py                    # PASOS 1, 2 y 3
└── test/
    ├── test_homogeneous.py               # tests ya escritos de los Pasos 1 a 3
    └── test_contra_tf2.py                # PASO 4
```

Verificación, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio01_transform_calculator_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio01_transform_calculator_py
colcon test-result --test-result-base build/ejercicio01_transform_calculator_py
# Summary: 13 tests, 0 errors, 12 failures, 0 skipped
```

Solo pasa `test_las_rotaciones_son_ortonormales[rot_x]`: `rot_x` viene escrita
como modelo. Todos los tests usan el escenario de la teoría 02: el robot en
`(2, 0)` de `odom` mirando hacia `+y` y un láser 0.20 m por delante del centro.

## Paso 1: Las rotaciones básicas

**Abre `ejercicio01_transform_calculator_py/homogeneous.py`**. Lee `rot_x`, que
ya está escrita. Descomenta los bloques del Paso 1 en `rot_y` y `rot_z` y
**borra las dos líneas `raise NotImplementedError(...)`** marcadas con
`# elimina en el Paso 1`.

**Por qué**: con estas tres funciones se escribe cualquier rotación (teoría 01,
sección 3). La fila y la columna del eje de giro son las de la identidad; el
signo cambiado de `rot_y` sale de la regla de la mano derecha.

✅ Verificación:

```bash
colcon test --packages-select ejercicio01_transform_calculator_py
colcon test-result --test-result-base build/ejercicio01_transform_calculator_py
# Summary: 13 tests, 0 errors, 7 failures, 0 skipped
```

Pasan los seis tests del Paso 1. `test_el_orden_de_los_giros_importa` comprueba
que `rot_z @ rot_x` no es `rot_x @ rot_z`: es la sección 5 de la teoría 01.

## Paso 2: La matriz homogénea

En el mismo archivo, descomenta los bloques del Paso 2 en `make_transform`,
`transform_point` y `transform_vector`, y borra sus tres líneas
`# elimina en el Paso 2`.

**Por qué**: `make_transform` monta la 4x4 (teoría 02, sección 2).
`transform_point` añade un 1 al punto y `transform_vector` un 0 a la dirección:
el mismo producto da resultados distintos porque la cuarta coordenada decide si
la traslación cuenta. `result: Matrix = ...` le dice a mypy de qué tipo es el
producto; sin la anotación lo trataría como `Any`.

✅ Verificación:

```bash
colcon test --packages-select ejercicio01_transform_calculator_py
colcon test-result --test-result-base build/ejercicio01_transform_calculator_py
# Summary: 13 tests, 0 errors, 4 failures, 0 skipped
```

`test_un_punto_delante_del_robot_en_odom` da `(2, 1, 0)` y
`test_las_direcciones_no_se_trasladan` da `(0, 1, 0)` con la misma matriz.

## Paso 3: Invertir y encadenar

Descomenta los bloques del Paso 3 en `invert_transform` y `compose`, y borra sus
líneas `# elimina en el Paso 3`.

**Por qué**: `invert_transform` usa la forma cerrada de la teoría 02, sección 4:
trasponer la rotación y girar la traslación antes de cambiarle el signo.
`compose(T_a_b, T_b_c)` multiplica en el orden del árbol, de la raíz a la hoja,
y devuelve `T_a_c`.

✅ Verificación:

```bash
colcon test --packages-select ejercicio01_transform_calculator_py
colcon test-result --test-result-base build/ejercicio01_transform_calculator_py
# Summary: 13 tests, 0 errors, 0 failures, 0 skipped
```

`test_el_origen_de_odom_visto_desde_el_robot` da `(0, 2, 0)`: el origen de
`odom` queda 2 m a la izquierda del robot.

## Paso 4: Comparar con tf2

**Abre `test/test_contra_tf2.py`** y descomenta el bloque del Paso 4.

**Por qué**: hasta aquí los tests comprobaban números calculados a mano. Este
compara tu calculadora con tf2 en un escenario distinto (yaw 0.6 y un láser
girado -0.3 rad): `tf2_ros.Buffer` funciona sin nodo ni red, le das las
transformaciones con `set_transform` y le preguntas con `lookup_transform` y
`transform` (teoría 05, sección 5). Si tu `compose` coincide con
`lookup_transform` y tu `transform_point` con `buffer.transform`, has escrito lo
mismo que tf2.

✅ Verificación (no hace falta recompilar: con `--symlink-install` el test ya
apunta a tu archivo):

```bash
colcon test --packages-select ejercicio01_transform_calculator_py
colcon test-result --test-result-base build/ejercicio01_transform_calculator_py
# Summary: 15 tests, 0 errors, 0 failures, 0 skipped
```

**¿El test detecta fallos?** En `compose`, cambia `result = result @ transform`
por `result = transform @ result`: multiplicar de la hoja a la raíz.

```bash
colcon test --packages-select ejercicio01_transform_calculator_py
colcon test-result --test-result-base build/ejercicio01_transform_calculator_py --verbose
# - ejercicio01_transform_calculator_py.test.test_contra_tf2 test_la_cadena_coincide_con_lookup_transform
# - ejercicio01_transform_calculator_py.test.test_contra_tf2 test_el_punto_coincide_con_buffer_transform
# - ejercicio01_transform_calculator_py.test.test_homogeneous test_encadenar_odom_base_laser
# Summary: 15 tests, 0 errors, 3 failures, 0 skipped
```

Fallan los tres tests que encadenan, y los dos que comparan con tf2 lo
confirman con otro escenario. Deshaz el cambio. Prueba también, en
`invert_transform`, `make_transform(rotation.T, -translation)`: caen
`test_la_inversa_deshace_la_transformacion` y
`test_el_origen_de_odom_visto_desde_el_robot`. Deshazlo.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué `transform_point` y `transform_vector` dan resultados distintos con
   la misma matriz? Pon un ejemplo de tu robot de cada tipo de dato.
2. ¿Por qué `-translation` sin girar solo falla cuando hay rotación?
3. tf2 te da `T_odom_base` y `T_odom_dock`. Escribe con `compose` e
   `invert_transform` la expresión de `T_base_dock`.

## Checklist

- [ ] Los 15 tests del paquete pasan
- [ ] Sé leer las columnas de una matriz de rotación como ejes
- [ ] Mi calculadora coincide con `lookup_transform` y `buffer.transform`
- [ ] Rompí `compose` e `invert_transform`, y los tests lo detectaron

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Prácticas](../README.md) | **Ejercicio 01** | [Ejercicio 02](../ejercicio-02-euler_y_cuaterniones_py/README.md) |

← [Volver a la Semana 07](../../README.md)
