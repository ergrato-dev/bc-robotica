# Ejercicio 04 — El mismo driver lifecycle en C++ (`rclcpp`)

`range_driver` otra vez: mismo nombre de nodo, parámetro, topic y transiciones
que en el Ejercicio 03, ahora en C++. Además es componente, como los nodos de
Nav2: un nodo lifecycle cargado en un container.

**Antes de empezar**: Ejercicios 02 y 03 completados.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-04-executors_composicion_y_lifecycle/2-practicas/ejercicio-04-lifecycle_cpp/starter \
  src/ejercicio04_lifecycle_cpp
```

Estructura:

```
src/ejercicio04_lifecycle_cpp/
├── package.xml                          # + rclcpp_lifecycle, lifecycle_msgs
├── CMakeLists.txt                       # completo: registro como en el Ejercicio 02
├── include/ejercicio04_lifecycle_cpp/
│   └── range_driver.hpp                 # PASOS 1, 2 y 3
├── src/
│   └── range_driver_component.cpp       # completo: la macro de registro
└── test/
    └── test_range_driver.cpp            # gtest ya escrito
```

Verificación:

```bash
colcon build --packages-select ejercicio04_lifecycle_cpp
source install/setup.bash
colcon test --packages-select ejercicio04_lifecycle_cpp
colcon test-result --verbose
```

En C++ las transiciones se piden con `node->configure()`, `node->activate()`...
y devuelven el estado en el que queda el nodo. Antes del primer paso, los cuatro
tests fallan.

## Paso 1: `on_configure`

**Abre `include/ejercicio04_lifecycle_cpp/range_driver.hpp`** y descomenta el
bloque del Paso 1. En un `LifecycleNode`, `create_publisher` ya devuelve un
`LifecyclePublisher`: no hay una función aparte como en Python.

**Verifica**: pasan `RangeDriverTest.ConfigureCreaElPublisher` y
`RangeDriverTest.ConfigureFallaConRateInvalido`.

## Paso 2: `on_activate` y `on_deactivate`

**Descomenta los dos bloques del Paso 2** y borra las cuatro líneas marcadas con
`// elimina esta línea al completar el Paso 2` (dos `(void)previous;` y dos
`return CallbackReturn::SUCCESS;`).

**Verifica**: pasa `RangeDriverTest.PublicaSoloEnActive`.

Experimento: cambia `return LifecycleNode::on_activate(previous);` por
`return CallbackReturn::SUCCESS;`, recompila y repite el test. Falla: el nodo
está en `active`, pero el publisher no. Deja la línea como estaba.

## Paso 3: `on_cleanup`

**Descomenta el bloque del Paso 3**.

**Verifica**: pasa `RangeDriverTest.CleanupLiberaElPublisher`. Los cuatro tests
pasan.

## Paso 4: Mismos comandos, otro lenguaje

Repite el Paso 4 del Ejercicio 03 con `ros2 run ejercicio04_lifecycle_cpp
range_driver`. Las salidas de `ros2 lifecycle` son idénticas; en la terminal 1:

```text
[INFO] [...] [range_driver]: Configurado a 5.0 Hz
[INFO] [...] [range_driver]: Activo
[INFO] [...] [range_driver]: Inactivo
[INFO] [...] [range_driver]: Recursos liberados
[INFO] [...] [range_driver]: Recursos liberados
```

✅ Verificación: quien controla el nodo no sabe en qué lenguaje está escrito.

## Paso 5: Un nodo lifecycle dentro de un container

```bash
# Terminal 1
ros2 run rclcpp_components component_container
```

```bash
# Terminal 2
ros2 component load /ComponentManager ejercicio04_lifecycle_cpp ejercicio04_lifecycle_cpp::RangeDriver
# Loaded component 1 into '/ComponentManager' container node as '/range_driver'
ros2 lifecycle set /range_driver configure
# Transitioning successful
ros2 lifecycle set /range_driver activate
# Transitioning successful
ros2 topic echo /robot/range_m --once
# data: 1.979425538604203   (el valor cambia con cada lectura)
# ---
```

✅ Verificación: cargar no es arrancar. El container crea el nodo en
`unconfigured`, y solo publica después de `configure` y `activate`. Así arranca
Nav2: un container con sus componentes y un lifecycle manager que los activa en
orden.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué aquí `component_container` (un hilo) es suficiente y en el
   Ejercicio 02 no?
2. En Python el publisher descartado en `inactive` no avisa; en C++ escribe un
   warning. ¿Cuál prefieres para depurar y por qué?

## Checklist

- [ ] Los cuatro tests de `test/test_range_driver.cpp` pasan
- [ ] Hice el experimento sin `LifecycleNode::on_activate` y lo deshice
- [ ] Controlé la versión C++ con los mismos comandos que la de Python
- [ ] Cargué el driver en un container y lo activé con `ros2 lifecycle`

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03](../ejercicio-03-lifecycle_py/README.md) | **Ejercicio 04** | [Proyecto](../../3-proyecto/README.md) |

← [Volver a la Semana 04](../../README.md)
