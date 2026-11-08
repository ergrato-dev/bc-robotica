# Rúbrica de Evaluación — Semana 02

Evaluación en tres componentes. Mínimo **70%** en cada uno para aprobar la semana.

## 🧠 Conocimiento (30%)

Cuestionario de autoevaluación. Responde primero sin ver las respuestas.

1. ¿Qué dos campos tiene `std_msgs/Header` y qué significa cada uno?
2. ¿Por qué `header.stamp` se rellena con el reloj del nodo y no con `time.time()`?
3. Un publisher ofrece `BEST_EFFORT` y un subscriber pide `RELIABLE`. ¿Conectan? ¿Qué
   ves en el log?
4. Un publisher ofrece `TRANSIENT_LOCAL` y un subscriber pide `VOLATILE`. ¿Conectan?
   ¿Recibe el subscriber los mensajes anteriores?
5. ¿Qué QoS usarías para un láser a 10 Hz por WiFi, y cuál para un mapa que se
   publica una sola vez?
6. ¿Afecta el `depth` a la compatibilidad entre publisher y subscriber?
7. ¿Por qué un paquete de interfaces tiene que ser `ament_cmake` aunque todos tus
   nodos sean Python?
8. ¿Qué línea de `package.xml` registra un paquete como paquete de interfaces?
9. Tu tipo se llama `BatteryReport`. ¿Qué escribes en el `#include` de C++ y en el
   `import` de Python si el paquete es `robot_interfaces`?
10. ¿Por qué `ros2 topic echo` sin opciones no sirve para descartar un problema de QoS
    en tu nodo?

<details>
<summary>Ver respuestas</summary>

1. `stamp`, el instante en que se tomó el dato, y `frame_id`, el nombre del sistema de
   coordenadas (sensor) desde el que se midió.
2. Porque en simulación el reloj de ROS lo marca el simulador y no coincide con el del
   sistema; el reloj del nodo funciona igual en real y en simulación.
3. No conectan: el subscriber pide reintentos que el publisher no da. El log muestra
   `offering incompatible QoS ... Last incompatible policy: RELIABILITY` y el callback
   nunca se ejecuta.
4. Sí conectan, porque lo ofrecido cubre lo pedido, pero el subscriber volátil no
   recibe el historial: solo lo que se publique después.
5. Láser: `sensor_data` (`BEST_EFFORT`, `VOLATILE`, depth 5). Mapa: `RELIABLE` +
   `TRANSIENT_LOCAL` con `depth=1`, para que lo reciba quien arranque tarde.
6. No. `history`, `depth` y `lifespan` no intervienen en la compatibilidad; cada
   extremo usa los suyos.
7. Porque la generación de código la hace CMake (`rosidl_generate_interfaces`); un
   paquete `ament_python` no puede ejecutarla.
8. `<member_of_group>rosidl_interface_packages</member_of_group>`.
9. `#include "robot_interfaces/msg/battery_report.hpp"` y
   `from robot_interfaces.msg import BatteryReport`.
10. Porque por defecto adapta su QoS al de los publishers que encuentra: recibe aunque
    tu nodo, con otro QoS, no reciba. Hay que forzar el QoS con `--qos-*` o mirar
    `ros2 topic info --verbose`.

</details>

## 💪 Desempeño (40%)

Verificado automáticamente por `colcon test` en cada `starter/`:

| Ejercicio | Verificación |
|---|---|
| 01 (`rclpy`) | `test_range_publisher_es_best_effort`, `test_range_lleva_header`, `test_status_llega_a_suscriptor_tardio`, `test_listener_recibe_ambos_topics` |
| 02 (`rclcpp`) | `RangePublisherTest.EsBestEffort`, `RangePublisherTest.LlevaHeader`, `StatusPublisherTest.LlegaASuscriptorTardio`, `QosListenerTest.RecibeAmbosTopics` |
| 03 (Python + C++) | `test_interfaz_tiene_campos_y_constantes`, `test_publisher_publica_sensor_reading`, `ReadingListenerTest.RecibeYClasificaLecturas` |
| 04 | Sin test automatizado: cada paso tiene su ✅ de verificación por CLI (ver checklist del ejercicio) |

```bash
colcon test --packages-select ejercicio01_qos_py ejercicio02_qos_cpp \
  ejercicio03_reading_py ejercicio03_reading_cpp
colcon test-result --verbose
```

## 📦 Producto (30%)

La capa del proyecto del dominio (`3-proyecto/`):

- [ ] `proyecto_dominio_interfaces` con un tipo propio renombrado a la misión, con
      `Header`, campos con unidad y constantes
- [ ] `sensor_stub` Python y C++ publican ese tipo con el mismo QoS explícito
- [ ] `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
- [ ] Justificación del QoS y respuestas de los Ejercicios 03 y 04 en el README del
      proyecto

### Penalizaciones (ver también `.github/copilot-instructions.md`)

| Situación | Penalización |
|---|---|
| No compila/lintea limpio | 0 en Producto |
| QoS como número suelto (`10`) en vez de perfil explícito | -10 |
| `stamp` o `frame_id` vacíos | -10 |
| Tipo `DomainState` sin renombrar o con campos genéricos (`value1`...) | -10 |
| `.msg` dentro de un paquete de nodos | -10 |
| Código copiado de otra misión/dominio | 0 en Producto |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica** | [Semana 03](../week-03-servicios_acciones_y_parametros/README.md) |

← [Volver a la Semana 02](README.md)
