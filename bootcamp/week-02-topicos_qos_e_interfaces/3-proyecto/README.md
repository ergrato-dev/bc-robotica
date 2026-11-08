# Proyecto — Semana 02

## Qué capa se añade esta semana

El `sensor_stub` de la Semana 01 deja de publicar texto libre. Añades un tercer
paquete, `proyecto_dominio_interfaces`, con un **mensaje propio de tu dominio**
(`DomainState.msg`, que renombras), y los dos `sensor_stub` (Python y C++) lo publican
con `Header` y un **perfil QoS explícito y justificado**.

```
src/
├── proyecto_dominio_interfaces/   # nuevo: ament_cmake, solo el .msg
├── proyecto_dominio_py/           # sensor_stub publica el tipo propio
└── proyecto_dominio_cpp/          # el mismo nodo en C++, ahora con test
```

## Por qué va aquí

Todas las semanas siguientes añaden interfaces a este paquete: el servicio y la acción
de la Semana 03, y los mensajes de tu misión hasta el capstone. Crearlo ahora, aparte
de los nodos, evita mover tipos de paquete cuando ya hay diez nodos que los usan.

## Requisitos verificables

1. `colcon build --symlink-install` compila los tres paquetes sin errores ni warnings
2. `ros2 interface show proyecto_dominio_interfaces/msg/<TuTipo>` muestra un `Header`,
   al menos tres campos de tu dominio con unidad SI (en el nombre o en un comentario) y
   al menos un grupo de constantes
3. `sensor_stub` (Python y C++) publica `<TuTipo>` en `<tu_dominio>/state` (relativo)
   con `stamp` del reloj del nodo y `frame_id` no vacío
4. Ambos usan **el mismo** perfil QoS, escrito explícitamente (nunca un `10` suelto)
5. `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
6. El README de tu repositorio justifica el QoS elegido (reliability, durability y
   depth) y responde las preguntas de los Ejercicios 03 y 04

## Cómo verificarlo, paso a paso

Copia los tres paquetes del `starter/` a `src/` (si ya tenías los de la Semana 01,
reemplázalos: este starter es su evolución):

```bash
cp -r <ruta-al-repo>/bootcamp/week-02-topicos_qos_e_interfaces/3-proyecto/starter/* src/
colcon build --symlink-install
# Summary: 3 packages finished [...]
source install/setup.bash
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result --verbose
# Summary: 4 tests, 0 errors, 0 failures, 0 skipped
```

Prueba de intercambiabilidad (en cada terminal, antes, `source install/setup.bash`):

```bash
# Terminal 1
ros2 run proyecto_dominio_py sensor_stub

# Terminal 2
ros2 topic info /<tu_dominio>/state --verbose   # QoS ofrecido
ros2 topic echo /<tu_dominio>/state --once
# header:
#   stamp:
#     sec: 1762600000
#   ...
#   frame_id: base_link
# location: pasillo_A
# ...
```

Cierra la terminal 1 y arranca `ros2 run proyecto_dominio_cpp sensor_stub`: el
`echo` y el `info` deben mostrar lo mismo.

## Criterios de calidad

- Nombres del tipo y de los campos en inglés y con significado (`AisleState`,
  `pending_orders`), no `Data1`, `value2`
- Unidades SI; si un campo es un porcentaje, el nombre lo dice (`battery_percent`)
- Constantes para los estados, nunca números mágicos en el código
- Justificación del QoS en dos o tres frases: qué pasa si se pierde un mensaje y qué
  necesita un nodo que arranque tarde

## Adaptación al dominio

Renombra `DomainState` y adapta los campos. Recuerda actualizar el `CMakeLists.txt`
de las interfaces, los `import`/`#include` (snake_case en C++) y los dos tests.

| Misión | Tipo sugerido | Campos sugeridos (además de `header`) |
|---|---|---|
| 📦 Almacén | `AisleState` | `aisle_id`, `pending_orders`, `battery_percent`, `MODE_*` |
| 🔬 Laboratorio | `BenchState` | `bench_id`, `tubes_waiting`, `gripper_closed`, `MODE_*` |
| 🔦 Inspección industrial | `InspectionState` | `nearest_valve_id`, `valves_pending`, `distance_to_valve_m` |
| 🧹 Oficina | `RoomState` | `room_name`, `rooms_pending`, `battery_percent`, `MODE_*` |
| 🌾 Agrícola | `RowState` | `row_index`, `plants_inspected`, `soil_moisture_percent` |
| 📚 Biblioteca | `ShelfState` | `shelf_id`, `books_to_return`, `battery_percent`, `MODE_*` |

Sobre el QoS: si tu estado se publica periódicamente, `RELIABLE` + `VOLATILE` es un
buen punto de partida. Si además quieres que un nodo que arranque tarde vea el último
estado sin esperar al siguiente ciclo, plantéate `TRANSIENT_LOCAL` con `depth=1` y
justifícalo.

## Checklist

- [ ] Renombré el tipo y sus campos a mi dominio, con unidades y constantes
- [ ] Ambos `sensor_stub` publican mi tipo con el mismo QoS explícito
- [ ] `colcon test` pasa en los dos paquetes de nodos
- [ ] Justifiqué el QoS y respondí las preguntas de los Ejercicios 03 y 04 en mi README

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04](../2-practicas/ejercicio-04-diagnosticar_qos_cli/README.md) | **Proyecto** | [Recursos](../4-recursos/README.md) |

← [Volver a la Semana 02](../README.md)
