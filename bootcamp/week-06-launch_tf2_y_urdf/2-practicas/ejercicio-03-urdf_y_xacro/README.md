# Ejercicio 03 — Modelo URDF/xacro de un rover

En los ejercicios 01 y 02 escribiste a mano dónde va el láser. Aquí describes un
robot entero, un rover de dos ruedas motrices y una rueda loca, en un archivo
xacro. `check_urdf` lo valida y `robot_state_publisher` publica su árbol TF. No
hay código Python ni C++: el modelo y su launch file son el ejercicio.

**Antes de empezar**: teorías [01](../../1-teoria/01-launch-files-en-python.md) y
[05](../../1-teoria/05-urdf-y-xacro.md) leídas.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-06-launch_tf2_y_urdf/2-practicas/ejercicio-03-urdf_y_xacro/starter \
  src/ejercicio03_urdf_xacro
```

Estructura:

```
src/ejercicio03_urdf_xacro/
├── package.xml                         # xacro, robot_state_publisher, joint_state_publisher
├── setup.py                            # instala urdf/ y launch/ en share/
├── setup.cfg
├── resource/ejercicio03_urdf_xacro
├── ejercicio03_urdf_xacro/__init__.py  # vacío: el paquete no tiene código
├── urdf/
│   └── rover.urdf.xacro                # PASOS 1 y 2
├── launch/
│   └── display.launch.py               # PASO 3
└── test/
    ├── test_urdf.py                    # tests ya escritos de los Pasos 1 y 2
    └── test_display_launch.py          # test ya escrito del Paso 3
```

Verificación, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio03_urdf_xacro --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio03_urdf_xacro
colcon test-result --test-result-base build/ejercicio03_urdf_xacro
# Summary: 6 tests, 0 errors, 6 failures, 0 skipped
```

Fallan los seis: el modelo solo tiene las propiedades y las macros de inercia, y
el launch file está vacío.

## Paso 1: El chasis y el láser

**Abre `urdf/rover.urdf.xacro`**. El bloque del Paso 1 está entre dos comentarios
XML: **borra las dos líneas marcadas con `(borra esta línea)`** (la que abre el
comentario con `<!-- PASO 1` y la que lo cierra con `PASO 1 ... -->`).

Lee lo que acabas de activar: `base_link` es una caja con `visual`, `collision` e
`inertial`; `laser_link`, un cilindro; `laser_joint`, un joint `fixed` con su
`origin`. Las medidas salen de las propiedades del principio del archivo.

**Por qué**: el chasis es la raíz del árbol y el láser cuelga de él, como en el
Ejercicio 01, pero ahora con forma y masa.

✅ Verificación (con `--symlink-install` no hace falta recompilar para un archivo
que ya existía):

```bash
xacro src/ejercicio03_urdf_xacro/urdf/rover.urdf.xacro > /tmp/rover.urdf
check_urdf /tmp/rover.urdf
# robot name is: rover
# ---------- Successfully Parsed XML ---------------
# root Link: base_link has 1 child(ren)
#     child(1):  laser_link
colcon test --packages-select ejercicio03_urdf_xacro
colcon test-result --test-result-base build/ejercicio03_urdf_xacro
# Summary: 6 tests, 0 errors, 4 failures, 0 skipped
```

Pasan `test_check_urdf_acepta_el_modelo` y `test_todo_link_tiene_masa`. Abre
`/tmp/rover.urdf`: las expresiones `${...}` ya son números. El láser quedó a
`z = 0.08`: la mitad de la altura del chasis más 3 cm.

## Paso 2: Las ruedas con una macro

En el mismo archivo, **borra las dos líneas marcadas con `(borra esta línea)`**
del bloque del Paso 2.

Una macro `wheel` escribe link y joint de una rueda con dos parámetros: `prefix`
(`left`/`right`) y `side` (`1`/`-1`). Las dos llamadas generan las dos ruedas.
Además se añade la rueda loca (`caster_link`), una esfera con joint `fixed`.

**Por qué**: las dos ruedas son iguales salvo el lado. Con la macro, cambiar el
radio de la rueda es cambiar una propiedad, no dos bloques de XML.

✅ Verificación:

```bash
xacro src/ejercicio03_urdf_xacro/urdf/rover.urdf.xacro > /tmp/rover.urdf
check_urdf /tmp/rover.urdf
# robot name is: rover
# ---------- Successfully Parsed XML ---------------
# root Link: base_link has 4 child(ren)
#     child(1):  caster_link
#     child(2):  laser_link
#     child(3):  left_wheel_link
#     child(4):  right_wheel_link
colcon test --packages-select ejercicio03_urdf_xacro
colcon test-result --test-result-base build/ejercicio03_urdf_xacro
# Summary: 6 tests, 0 errors, 1 failure, 0 skipped
```

Solo falla `test_display_launch`: espera el Paso 3. Busca `left_wheel_joint` en
`/tmp/rover.urdf`:

```xml
<joint name="left_wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child link="left_wheel_link"/>
  <origin rpy="0 0 0" xyz="0.08 0.16999999999999998 -0.05"/>
  <axis xyz="0 1 0"/>
</joint>
```

`0.16999999999999998` es `0.30 / 2 + 0.04 / 2` calculado en coma flotante: 0.17 m.

**¿El test detecta fallos?** Cambia la segunda llamada a
`<xacro:wheel prefix="right" side="1"/>`: las dos ruedas quedan en el mismo lado.
`check_urdf` lo acepta (el XML es válido), pero `test_ruedas_a_cada_lado` falla.
Deshaz el cambio.

## Paso 3: Publicar el modelo

**Abre `launch/display.launch.py`**, descomenta los dos bloques del Paso 3 y
**borra la línea `return LaunchDescription([])`** marcada con
`# elimina en el Paso 3`.

**Por qué**: `Command` ejecuta xacro al lanzar, `robot_state_publisher` recibe el
URDF y publica el árbol, y `joint_state_publisher` da el ángulo de las ruedas.

✅ Verificación:

```bash
colcon build --packages-select ejercicio03_urdf_xacro --symlink-install
# Terminal 1
ros2 launch ejercicio03_urdf_xacro display.launch.py
# [INFO] [robot_state_publisher-1]: process started with pid [189]
# [INFO] [joint_state_publisher-2]: process started with pid [190]
# [robot_state_publisher-1] [WARN] [...] [kdl_parser]: The root link base_link has an inertia specified in the URDF, but KDL does not support a root link with an inertia.  As a workaround, you can add an extra dummy link to your URDF.
# [robot_state_publisher-1] [INFO] [...] [robot_state_publisher]: Robot initialized
# [joint_state_publisher-2] [INFO] [...] [joint_state_publisher]: Waiting for robot_description to be published on the robot_description topic...
# [joint_state_publisher-2] [INFO] [...] [joint_state_publisher]: Got description, configuring robot
```

El aviso de KDL es el de la teoría 05: no afecta a las transformaciones.

```bash
# Terminal 2
ros2 run tf2_ros tf2_echo base_link left_wheel_link
# At time 1794193274.495629613
# - Translation: [0.080, 0.170, -0.050]
# - Rotation: in Quaternion (xyzw) [0.000, 0.000, 0.000, 1.000]
# ...
ros2 topic echo /joint_states --once
# ...
# name:
# - left_wheel_joint
# - right_wheel_joint
# position:
# - 0.0
# - 0.0
# ...
```

La rueda tiene un `At time` real (no `0.0`): es dinámica, la publica
`robot_state_publisher` cada vez que llega un `/joint_states`. Comprueba los tests:

```bash
colcon test --packages-select ejercicio03_urdf_xacro
colcon test-result --test-result-base build/ejercicio03_urdf_xacro
# Summary: 6 tests, 0 errors, 0 failures, 0 skipped
```

**¿El test detecta fallos?** Quita el `joint_publisher` de la lista que devuelve
el launch file. Las ruedas desaparecen de TF (nadie da su ángulo) y
`test_display_launch` falla, mientras el láser, `fixed`, sigue en `/tf_static`.
Deshaz el cambio.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué `check_urdf` aceptó las dos ruedas en el mismo lado? ¿Qué comprueba
   y qué no?
2. Sin `joint_state_publisher`, ¿por qué el láser sigue en TF y las ruedas no?
3. ¿Qué piezas de tu robot serían `fixed`, cuáles `continuous` y cuáles
   `revolute`?

## Checklist

- [ ] Los 6 tests del paquete pasan
- [ ] `check_urdf` muestra `base_link` con cuatro hijos
- [ ] Vi una transformación estática (láser) y una dinámica (rueda) con `tf2_echo`
- [ ] Rompí el modelo y el launch file, y los tests lo detectaron

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02](../ejercicio-02-tf_listener_cpp/README.md) | **Ejercicio 03** | [Proyecto](../../3-proyecto/README.md) |

← [Volver a la Semana 06](../../README.md)
