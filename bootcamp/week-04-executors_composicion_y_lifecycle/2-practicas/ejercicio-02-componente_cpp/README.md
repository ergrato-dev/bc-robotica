# Ejercicio 02 — El mismo monitor como componente (`rclcpp`)

Mismo nodo `monitor`, mismo servicio `robot/slow_check` y misma respuesta que en
el Ejercicio 01, ahora en C++ y como **componente**. Al final lo cargas en dos
containers distintos y la diferencia te sirve para justificar un executor.

**Antes de empezar**: Ejercicio 01 completado y teoría
[03](../../1-teoria/03-composicion-y-componentes.md) leída.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-04-executors_composicion_y_lifecycle/2-practicas/ejercicio-02-componente_cpp/starter \
  src/ejercicio02_componente_cpp
```

Estructura:

```
src/ejercicio02_componente_cpp/
├── package.xml                          # depende de rclcpp, rclcpp_components, std_srvs
├── CMakeLists.txt                       # PASO 2
├── include/ejercicio02_componente_cpp/
│   └── monitor.hpp                      # PASO 1
├── src/
│   └── monitor_component.cpp            # PASO 2 (registro)
└── test/
    └── test_monitor.cpp                 # gtest ya escrito
```

No hay `main.cpp`: un componente no lo necesita, y el ejecutable lo genera CMake
en el Paso 2. Verificación de cada paso:

```bash
colcon build --packages-select ejercicio02_componente_cpp
source install/setup.bash
colcon test --packages-select ejercicio02_componente_cpp
colcon test-result --verbose
```

Antes del primer paso, los tres tests fallan.

## Paso 1: Un grupo para cada callback

**Abre `include/ejercicio02_componente_cpp/monitor.hpp`** y descomenta el bloque
del Paso 1. `create_wall_timer` y `create_service` ya reciben `timer_group_` y
`service_group_` como último argumento; hasta ahora eran `nullptr` (grupo por
defecto).

Fíjate en `std::atomic<int> ticks_`: con varios hilos, el timer escribe el
contador y el servicio lo lee a la vez (teoría 02, sección 5).

**Verifica**: pasan `MonitorTest.UsaGruposPropios` y
`MonitorTest.TimerSigueDuranteLaComprobacion`.

## Paso 2: Compilar y registrar el componente

Dos partes:

1. **En `CMakeLists.txt`**, descomenta el bloque del Paso 2:
   `add_library(... SHARED ...)`, `rclcpp_components_register_node` y su
   `install`
2. **En `src/monitor_component.cpp`**, descomenta la línea
   `RCLCPP_COMPONENTS_REGISTER_NODE(ejercicio02_componente_cpp::Monitor)`

**Por qué**: la macro crea la "fábrica" que instancia `Monitor` a partir de su
nombre; CMake la compila en `libmonitor_component.so` y la anuncia en el índice
de ament. `EXECUTABLE monitor` genera además un ejecutable normal, y
`EXECUTOR MultiThreadedExecutor` elige el executor de ese ejecutable.

**Verifica**: pasa `MonitorTest.SeRegistraComoComponente`. Los tres tests pasan.

```bash
ros2 component types | grep -A1 ejercicio02
# ejercicio02_componente_cpp
#   ejercicio02_componente_cpp::Monitor
```

## Paso 3: Dos containers, dos resultados

En cada terminal, primero `source install/setup.bash`.

```bash
# Terminal 1: container con executor de un hilo
ros2 run rclcpp_components component_container
```

```bash
# Terminal 2
ros2 component load /ComponentManager ejercicio02_componente_cpp ejercicio02_componente_cpp::Monitor
# Loaded component 1 into '/ComponentManager' container node as '/monitor'
ros2 component list
# /ComponentManager
#   1  /monitor
ros2 service call /robot/slow_check std_srvs/srv/Trigger
# ...
# std_srvs.srv.Trigger_Response(success=True, message='ticks durante la comprobación: 0')
```

En la terminal 1 verás cómo el container carga la biblioteca:

```text
[INFO] [...] [ComponentManager]: Load Library: .../lib/libmonitor_component.so
[INFO] [...] [ComponentManager]: Found class: rclcpp_components::NodeFactoryTemplate<ejercicio02_componente_cpp::Monitor>
[INFO] [...] [ComponentManager]: Instantiate class: rclcpp_components::NodeFactoryTemplate<ejercicio02_componente_cpp::Monitor>
```

Cierra el container (`Ctrl+C`) y repite con el multihilo:

```bash
# Terminal 1
ros2 run rclcpp_components component_container_mt
```

```bash
# Terminal 2
ros2 component load /ComponentManager ejercicio02_componente_cpp ejercicio02_componente_cpp::Monitor
ros2 service call /robot/slow_check std_srvs/srv/Trigger
# std_srvs.srv.Trigger_Response(success=True, message='ticks durante la comprobación: 5')
```

✅ Verificación: mismo `.so`, distinto resultado. Los grupos del Paso 1 solo
sirven si el proceso que carga el componente tiene varios hilos.

## Paso 4: Cruzar lenguajes

El ejecutable generado usa `MultiThreadedExecutor` (lo pediste en CMake):

```bash
# Terminal 1
ros2 run ejercicio02_componente_cpp monitor
```

```bash
# Terminal 2
ros2 service call /robot/slow_check std_srvs/srv/Trigger
# std_srvs.srv.Trigger_Response(success=True, message='ticks durante la comprobación: 5')
```

Cierra el nodo C++, arranca el de Python del Ejercicio 01 y repite la llamada:
misma respuesta. Para quien llama, los dos nodos son intercambiables.

## Justificación del executor (para tu informe)

Escribe en el README de tu `3-proyecto/` un párrafo con este esquema, aplicado al
`monitor`:

1. Qué callbacks tiene el nodo y cuánto tarda cada uno
2. Cuál no puede esperar a cuál
3. Qué executor y qué grupos elegiste, y qué container o `EXECUTOR` lo aplica

## Checklist

- [ ] Los tres tests de `test/test_monitor.cpp` pasan
- [ ] `ros2 component types` muestra `ejercicio02_componente_cpp::Monitor`
- [ ] Vi 0 ticks en `component_container` y unos 5 en `component_container_mt`
- [ ] Escribí la justificación del executor

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01](../ejercicio-01-callback_groups_py/README.md) | **Ejercicio 02** | [Ejercicio 03](../ejercicio-03-lifecycle_py/README.md) |

← [Volver a la Semana 04](../../README.md)
