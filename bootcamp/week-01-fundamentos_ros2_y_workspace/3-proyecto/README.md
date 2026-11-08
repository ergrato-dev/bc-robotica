# Proyecto — Semana 01

## Qué capa se añade esta semana

El arranque del workspace del sistema que vas a construir durante las 33 semanas: un
paquete `ament_python` y un paquete `ament_cmake`, cada uno con un nodo `sensor_stub`
que **publica el estado simulado de tu dominio**. Aquí declaras tu **misión/dominio**
(catálogo en [`docs/dominios.md`](../../../docs/dominios.md)) y la mantienes hasta el
capstone.

## Por qué va aquí

Cada semana añade una capa nueva a este mismo sistema. Empezar con dos paquetes (uno
por lenguaje) desde la Semana 01 es lo que te permite, en las semanas siguientes, añadir
interfaces propias (02), servicios (03) y nodos CORE en C++ sin reestructurar nada.

## Requisitos verificables

1. `colcon build --symlink-install` compila ambos paquetes sin errores
2. `proyecto_dominio_py` expone un nodo `sensor_stub` que publica en
   `<tu_dominio>/state` (topic **relativo**, sin `/` inicial: ver teoría 05) con un
   mensaje `std_msgs/String`
3. `proyecto_dominio_cpp` expone el mismo nodo, mismo topic, mismo tipo de mensaje
4. `colcon test` pasa para ambos paquetes (test mínimo: el publisher existe)
5. El README de tu propio repositorio (no este) documenta qué dominio elegiste y por qué,
   y responde las preguntas de los Ejercicios 03 y 04

## Cómo verificarlo, paso a paso

Desde la raíz de tu workspace (la carpeta que contiene `src/`):

```bash
colcon build --symlink-install
# Summary: 2 packages finished [...]

source install/setup.bash
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result --verbose
# Summary: N tests, 0 errors, 0 failures, 0 skipped
```

Prueba cruzada, con el publisher en un lenguaje y la CLI como subscriber:

```bash
# Terminal 1
ros2 run proyecto_dominio_py sensor_stub

# Terminal 2
ros2 topic echo /<tu_dominio>/state
# data: '...'
```

Repite con `ros2 run proyecto_dominio_cpp sensor_stub` en la terminal 1: la terminal 2
debe seguir recibiendo sin cambiar nada.

## Criterios de calidad

- Mismo nombre de nodo, de topic y de tipo en ambos lenguajes: son intercambiables
- Logs con `get_logger()`/`RCLCPP_INFO`, nunca `print`/`std::cout`
- El contenido de `data` dice algo con sentido en tu dominio, no `"hola"`

## Adaptación al dominio

Renombra `proyecto_dominio_py`/`proyecto_dominio_cpp` y el topic `<tu_dominio>/state`
según tu misión:

| Misión | Topic sugerido | Qué publica el `sensor_stub` |
|---|---|---|
| 📦 Almacén | `almacen/state` | Pasillo simulado en el que está el robot |
| 🔬 Laboratorio | `laboratorio/state` | Mesa actual y tubo simulado en espera |
| 🔦 Inspección industrial | `planta/state` | Válvula simulada más cercana |
| 🧹 Oficina | `oficina/state` | Habitación simulada actual |
| 🌾 Agrícola | `cultivo/state` | Surco simulado actual |
| 📚 Biblioteca | `biblioteca/state` | Estantería simulada actual |

El campo `data` es un `str`/`std::string` libre por ahora; en la Semana 02 lo
reemplazas por un mensaje custom propio de tu dominio.

## Checklist

- [ ] Elegí mi misión/dominio y lo escribí en el README de mi propio repositorio
- [ ] Ambos paquetes compilan y el nodo `sensor_stub` corre en los dos lenguajes
- [ ] `colcon test` pasa en ambos paquetes
- [ ] Respondí las preguntas de los Ejercicios 03 y 04

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04](../2-practicas/ejercicio-04-explorar_grafo_cli/README.md) | **Proyecto** | [Recursos](../4-recursos/README.md) |

← [Volver a la Semana 01](../README.md)
