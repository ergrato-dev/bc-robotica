# Ejercicio 03 — Una interfaz propia compartida por Python y C++

Creas el tipo `SensorReading` en un paquete de interfaces, lo publicas desde Python y
lo recibes en C++. Es el patrón que usarás todo el bootcamp: un paquete `_interfaces`
del que dependen nodos de cualquier lenguaje.

**Antes de empezar**: teorías [04](../../1-teoria/04-interfaces-custom-con-rosidl.md) y
[05](../../1-teoria/05-usar-interfaces-custom-en-python-y-cpp.md) leídas.

## Preparar el workspace

El starter trae **tres paquetes**. Cópialos dentro de `src/`:

```bash
cp -r <ruta-al-repo>/bootcamp/week-02-topicos_qos_e_interfaces/2-practicas/ejercicio-03-interfaz_compartida/starter/* src/
ls src/
# ejercicio03_interfaces  ejercicio03_reading_cpp  ejercicio03_reading_py  ...
```

```
src/
├── ejercicio03_interfaces/         # ament_cmake: solo el tipo
│   ├── package.xml                 # PASO 1 (parte A)
│   ├── CMakeLists.txt              # PASO 1 (parte B)
│   └── msg/SensorReading.msg       # PASO 2
├── ejercicio03_reading_py/         # ament_python: publisher
│   └── ejercicio03_reading_py/reading_publisher.py   # PASO 3
└── ejercicio03_reading_cpp/        # ament_cmake: listener
    └── include/ejercicio03_reading_cpp/reading_listener.hpp   # PASO 4
```

> ⚠️ **Hasta terminar el Paso 2, no compiles el workspace entero.** El listener C++
> usa campos (`sensor_id`, `value`...) que todavía no existen y `colcon build` fallaría
> en `ejercicio03_reading_cpp`. Por eso los Pasos 1 y 2 usan `--packages-select`.

## Paso 1: Registrar el paquete como paquete de interfaces

**Por qué**: sin `rosidl_generate_interfaces` el paquete compila pero no contiene
ningún tipo; sin `<member_of_group>`, el tipo no se genera para todos los lenguajes.

**Parte A — `ejercicio03_interfaces/package.xml`**: las cuatro dependencias están
dentro de un comentario XML. Borra la línea que abre el comentario (`<!-- ====...`),
las líneas de explicación hasta `...que las rodean):` incluida, y la línea `-->` del
final. Debe quedar así:

```xml
  <buildtool_depend>ament_cmake</buildtool_depend>

  <buildtool_depend>rosidl_default_generators</buildtool_depend>
  <depend>std_msgs</depend>
  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>

  <export>
```

**Parte B — `ejercicio03_interfaces/CMakeLists.txt`**: descomenta el bloque del Paso 1.

**Verifica**:

```bash
colcon build --packages-select ejercicio03_interfaces
source install/setup.bash
ros2 interface list | grep ejercicio03
# ejercicio03_interfaces/msg/SensorReading
```

El tipo existe, pero vacío: `ros2 interface show ejercicio03_interfaces/msg/SensorReading`
solo muestra comentarios.

## Paso 2: Los campos del mensaje

**Abre `ejercicio03_interfaces/msg/SensorReading.msg`** y quita el `# ` inicial de cada
línea del bloque del Paso 2 (no toques los comentarios que van **después** de cada
campo: son documentación).

**Verifica**:

```bash
colcon build --packages-select ejercicio03_interfaces
ros2 interface show ejercicio03_interfaces/msg/SensorReading
```

Debes ver `string sensor_id`, `float64 value`, `string unit "m"`, `bool is_valid true`,
las tres constantes `STATUS_*` y `uint8 status`. Desde aquí ya puedes compilar todo:

```bash
colcon build --symlink-install
source install/setup.bash
```

## Paso 3: Publisher Python

**Por qué**: comprobar que el tipo generado se importa como cualquier mensaje estándar.

**Abre `ejercicio03_reading_py/ejercicio03_reading_py/reading_publisher.py`** y
descomenta el bloque del Paso 3.

**Verifica**:

```bash
colcon test --packages-select ejercicio03_reading_py
colcon test-result --verbose
```

Pasan `test_interfaz_tiene_campos_y_constantes` (este ya pasaba tras el Paso 2) y
`test_publisher_publica_sensor_reading`.

## Paso 4: Listener C++

**Abre `ejercicio03_reading_cpp/include/ejercicio03_reading_cpp/reading_listener.hpp`**
y descomenta el bloque del Paso 4.

**Verifica**:

```bash
colcon build --packages-select ejercicio03_reading_cpp
colcon test --packages-select ejercicio03_reading_cpp
colcon test-result --verbose
```

Pasa `ReadingListenerTest.RecibeYClasificaLecturas`.

## Paso 5: Python habla con C++

```bash
# Terminal 1
ros2 run ejercicio03_reading_py reading_publisher
# [INFO] [...] [reading_publisher]: Publicado: 0.50 m

# Terminal 2
ros2 run ejercicio03_reading_cpp reading_listener
# [INFO] [...] [reading_listener]: front: 1.25 m
# ...
# [WARN] [...] [reading_listener]: front fuera de rango: 3.00 m
```

**Verifica**: a partir de 3.00 m el listener C++ imprime `[WARN]`. El publisher
Python decide el `status` con la constante `STATUS_WARN` y el listener C++ lo compara
con la misma constante: un solo `.msg`, dos lenguajes.

## Paso 6: Cambiar el contrato

Añade al final de `SensorReading.msg` un campo nuevo:

```text
float32 temperature_c       # temperatura del sensor, en grados Celsius
```

Recompila **solo** las interfaces (`colcon build --packages-select ejercicio03_interfaces`)
y vuelve a ejecutar los nodos del Paso 5 sin recompilar los otros dos paquetes.

**Verifica**: anota qué pasa en tu informe. Después recompila con
`colcon build --packages-up-to ejercicio03_reading_cpp ejercicio03_reading_py` y
comprueba que todo vuelve a funcionar. Deja el campo o quítalo, pero recompila siempre
todo lo que use el tipo.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué `ejercicio03_reading_py` usa `<exec_depend>` y `ejercicio03_reading_cpp`
   usa `<depend>` para la misma interfaz?
2. ¿Qué observaste en el Paso 6 antes de recompilar los consumidores? ¿Por qué es
   peligroso en un robot con nodos compilados en momentos distintos?
3. ¿Qué ganas usando `SensorReading.STATUS_WARN` en lugar de escribir `1`?

## Checklist

- [ ] `ros2 interface show` muestra todos los campos y constantes de `SensorReading`
- [ ] Los tests de `ejercicio03_reading_py` y `ejercicio03_reading_cpp` pasan
- [ ] El publisher Python y el listener C++ se comunican, con `[WARN]` desde 3.00 m
- [ ] Hice el Paso 6 y respondí las tres preguntas

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02](../ejercicio-02-qos_cpp/README.md) | **Ejercicio 03** | [Ejercicio 04](../ejercicio-04-diagnosticar_qos_cli/README.md) |

← [Volver a la Semana 02](../../README.md)
