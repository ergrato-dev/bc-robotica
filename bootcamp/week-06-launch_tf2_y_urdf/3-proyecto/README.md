# Proyecto — Semana 06

## Qué capa se añade esta semana

Tu robot gana **cuerpo, posición y un arranque de una sola orden**:

- **Modelo URDF/xacro** en un paquete nuevo, `proyecto_dominio_description`: el
  chasis, el sensor principal de tu misión y las ruedas, publicados por
  `robot_state_publisher`
- **`odom → base_link` en TF**: `sensor_stub` recorre una ruta simulada de ida y
  vuelta y publica dónde está el robot, con el mismo `stamp` que su estado. La
  capa Python ya lo hace; en la C++ lo escribes tú
- **`bringup.launch.py`**: incluye el modelo, arranca la capa elegida con
  `impl:=py` o `impl:=cpp` y la lleva sola hasta `active` con eventos de lifecycle

```
src/
├── .clang-format
├── proyecto_dominio_interfaces/        # sin cambios
├── proyecto_dominio_description/       # nuevo
│   ├── CMakeLists.txt                  # instala urdf/ y launch/
│   ├── urdf/robot.urdf.xacro           # TODO: tu robot (Requisitos 2 y 3)
│   └── launch/description.launch.py    # robot_state_publisher + joint_state_publisher
├── proyecto_dominio_py/
│   ├── launch/bringup.launch.py        # nuevo
│   ├── proyecto_dominio_py/
│   │   ├── route.py                    # nuevo: route_pose, yaw_to_quaternion
│   │   └── sensor_stub.py              # publica odom -> base_link
│   └── test/
│       ├── test_route.py               # nuevo
│       ├── test_description.py         # nuevo: check_urdf y estructura del modelo
│       ├── test_bringup_launch.py      # nuevo: launch_testing con impl py y cpp
│       └── data/state_bag/             # tu bag de la Semana 05
└── proyecto_dominio_cpp/
    ├── include/proyecto_dominio_cpp/
    │   ├── route.hpp                   # nuevo: la misma ruta que route.py
    │   └── sensor_stub.hpp             # TODO: odom -> base_link (Requisito 4)
    └── test/test_route.cpp             # nuevo
```

## Por qué va aquí

Hasta ahora `sensor_stub` decía `frame_id: base_link`, pero `base_link` no existía
en ningún árbol. Desde esta semana el estado de tu robot tiene un sitio en el
mundo. En la Semana 08 Gazebo cargará este mismo URDF y la simulación sustituirá a
la ruta simulada; en la Semana 14 Nav2 leerá este mismo árbol. Y `bringup.launch.py`
es el punto de entrada que irá incluyendo cada capa nueva.

## Requisitos verificables

1. `colcon build --symlink-install` compila los cuatro paquetes sin errores ni warnings
2. `robot.urdf.xacro` describe **tu** robot: nombre, medidas del chasis y dos
   ruedas motrices `continuous` con eje y, una a cada lado, hechas con una macro.
   `test_description.py` pasa
3. El sensor principal de tu misión tiene su link con nombre propio y su
   posición real sobre el chasis (tabla de adaptación), y `SENSOR_FRAME` está
   actualizado en `test_description.py` y `test_bringup_launch.py`
4. `sensor_stub` en C++ publica `odom → base_link` igual que la capa Python:
   `test_bringup_launch.py` pasa con `impl` igual a `py` y a `cpp`
5. `ros2 launch proyecto_dominio_py bringup.launch.py` deja `sensor_stub` en
   `active` sin ninguna orden más, con las dos capas
6. `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
7. El README de tu repositorio responde las preguntas de los tres ejercicios e
   incluye el checklist de paridad del Ejercicio 02 relleno

## Cómo verificarlo, paso a paso

Copia los cuatro paquetes del `starter/` a `src/`, reemplazando los de la Semana
05 (este starter es su evolución; vuelve a aplicar tus renombrados):

```bash
cp -r <ruta-al-repo>/bootcamp/week-06-launch_tf2_y_urdf/3-proyecto/starter/* src/
```

`cp -r` sobrescribe los archivos pero no borra carpetas: tu bag de referencia de
la Semana 05 sigue en `src/proyecto_dominio_py/test/data/state_bag`. Compila y
prueba:

```bash
colcon build --symlink-install
# Summary: 4 packages finished [...]
source install/setup.bash
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result --verbose
```

Con el starter sin tocar fallan dos tests, y es lo esperado:

```text
- proyecto_dominio_py.test.test_bringup_launch test_bringup_launch
- proyecto_dominio_py.test.test_description test_dos_ruedas_motrices
    AssertionError: Requisito 2: añade las ruedas (joints continuous)
```

`test_bringup_launch` corre dos veces (con `impl:=py` y con `impl:=cpp`); la
pasada de Python es correcta, la de C++ falla en
`test_arbol_completo_de_odom_al_sensor[cpp]` con `sin TF odom -> sensor_link`
(el detalle está en `build/proyecto_dominio_py/pytest.xml`): la capa C++ aún no
publica `odom → base_link`. Si además fallan los tres tests de
`test_state_bag`, falta la bag: cópiala de tu repositorio de la Semana 05.

**Requisito 2**: añade la macro de las ruedas a `robot.urdf.xacro`, como en el
Paso 2 del Ejercicio 03, con las medidas de tu robot. Valídalo:

```bash
xacro src/proyecto_dominio_description/urdf/robot.urdf.xacro > /tmp/robot.urdf
check_urdf /tmp/robot.urdf
# robot name is: <tu-robot>
# ---------- Successfully Parsed XML ---------------
# root Link: base_link has 3 child(ren)
#     child(1):  left_wheel_link
#     child(2):  right_wheel_link
#     child(3):  sensor_link
```

**Requisito 4**: en `sensor_stub.hpp`, sigue el `TODO (Requisito 4)` de `on_timer`.
Necesitas un `std::unique_ptr<tf2_ros::TransformBroadcaster>` creado en el
constructor, avanzar `distance_m_`, llamar a `route_pose` y rellenar un
`TransformStamped` con el mismo `stamp` que el estado (teoría 04, sección 3.1).
`CMakeLists.txt` y `package.xml` ya traen `tf2_ros` y `geometry_msgs`.

**Requisito 5**, comprobado a mano:

```bash
# Terminal 1
ros2 launch proyecto_dominio_py bringup.launch.py impl:=cpp
# [INFO] [robot_state_publisher-1]: process started with pid [71]
# [INFO] [joint_state_publisher-2]: process started with pid [72]
# [INFO] [sensor_stub-3]: process started with pid [73]
# ...
```

```bash
# Terminal 2
ros2 lifecycle get /sensor_stub
# active [3]
ros2 run tf2_ros tf2_echo odom sensor_link
# At time 1794193059.955210502
# - Translation: [9.750, 0.000, 0.100]
# - Rotation: in Quaternion (xyzw) [0.000, 0.000, 1.000, 0.000]
# ...
```

Tus números serán otros: en ese instante el robot volvía hacia el origen (yaw π,
cuaternión `(0, 0, 1, 0)`) y el sensor iba montado 0.25 m por delante del centro,
así que quedaba 0.25 m más cerca del origen que `base_link`. Prueba también
`impl:=java`: el launch se niega a arrancar.

Con todo hecho:

```bash
colcon build --symlink-install
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result
# Summary: 42 tests, 0 errors, 0 failures, 0 skipped
```

Son 28 de Python (los 12 de la Semana 05, 10 de la ruta, 5 del modelo y 1 de
bringup) y 14 de C++ (8 de gtest, los 2 de lint y los 4 que CTest anota en su
resumen).

## Criterios de calidad

- Las medidas del URDF salen de propiedades xacro, no de números repetidos
- Todo link tiene `<inertial>` con masa e inercia calculadas con las fórmulas de
  la teoría 05, no inventadas
- El `stamp` de `odom → base_link` y el del estado son el mismo en las dos capas
- Ningún nodo publica en `/tf` algo que no se mueve

## Adaptación al dominio

Además de los renombrados de semanas anteriores, adapta el modelo y la ruta:

| Misión | Sensor principal y montaje (Requisito 3) | Ruta simulada (`ROUTE_LENGTH_M`) |
|---|---|---|
| 📦 Almacén | `camera_link` delante, a la altura de las etiquetas de las cajas | Un pasillo entre estantes |
| 🔬 Laboratorio | `camera_link` en un mástil, mirando a la mesa | La distancia entre dos mesas |
| 🔦 Inspección industrial | `thermal_camera_link` en lo alto, con `pitch` hacia las válvulas | El tramo entre dos waypoints |
| 🧹 Oficina | `laser_link` bajo y delante, para detectar objetos en el suelo | El largo de una habitación |
| 🌾 Agrícola | `camera_link` delante con `pitch` hacia el surco | El largo de un surco |
| 📚 Biblioteca | `camera_link` lateral (`yaw` de 90°) mirando a la estantería | Un pasillo de estanterías |

Escribe en tu README por qué el sensor va donde lo pusiste y qué medidas tomaste
del robot de referencia de tu misión.

## Checklist

- [ ] Mi robot tiene nombre, medidas, sensor y ruedas propios, y `check_urdf` lo acepta
- [ ] La capa C++ publica `odom → base_link` y `test_bringup_launch` pasa en las dos capas
- [ ] `bringup.launch.py` deja `sensor_stub` en `active` sin teclear transiciones
- [ ] `colcon test` pasa en los dos paquetes de nodos
- [ ] Respondí las preguntas de los tres ejercicios y rellené el checklist de paridad

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03](../2-practicas/ejercicio-03-urdf_y_xacro/README.md) | **Proyecto** | [Recursos](../4-recursos/README.md) |

← [Volver a la Semana 06](../README.md)
