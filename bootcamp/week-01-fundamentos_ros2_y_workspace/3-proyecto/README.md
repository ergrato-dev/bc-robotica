# Proyecto — Semana 01

## Qué capa se añade esta semana

El arranque del workspace del sistema que vas a construir las próximas 19 semanas: un
paquete `ament_python` y un paquete `ament_cmake`, cada uno con un nodo `sensor_stub`
que **publica el estado simulado de tu dominio** (ver `docs/tracks.md` para el catálogo
de misiones). Es la Semana 01 de ambos: aún no eliges track (eso es la Semana 12), pero
sí declaras tu **misión/dominio** aquí y lo mantienes las 19 semanas.

## Por qué va aquí

Cada semana de las Fases 1-3 añade una capa nueva a este mismo sistema. Empezar con dos
paquetes vacíos (uno por lenguaje) desde la Semana 01 es lo que te permite, en la
Semana 04, tener ya el esqueleto donde añadir el nodo CORE en C++ sin reestructurar
nada.

## Requisitos verificables

1. `colcon build --symlink-install` compila ambos paquetes sin errores
2. `proyecto_dominio_py` expone un nodo `sensor_stub` que publica en
   `<tu_dominio>/state` (ej. `almacen/state`, `mesa_trabajo/state`) con un mensaje
   `std_msgs/String`
3. `proyecto_dominio_cpp` expone el mismo nodo, mismo topic, mismo tipo de mensaje
4. `colcon test` pasa para ambos paquetes (test mínimo: el publisher existe)
5. El README de tu propio fork del proyecto (no este) documenta qué dominio elegiste y
   por qué

## Cómo verificarlo

```bash
colcon build --symlink-install
source install/setup.bash
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result --verbose

# Prueba cruzada: publisher Python, listener CLI genérico
ros2 run proyecto_dominio_py sensor_stub &
ros2 topic echo /<tu_dominio>/state
```

## Adaptación al dominio

Renombra `proyecto_dominio_py`/`proyecto_dominio_cpp` y el topic `<tu_dominio>/state`
según tu misión (ver catálogo completo en [`docs/tracks.md`](../../../docs/tracks.md)):

| Misión (ejemplo) | Topic sugerido | Qué publica el `sensor_stub` |
|---|---|---|
| 📦 Robot de almacén (Track A) | `almacen/state` | Posición simulada del robot en la estantería |
| 🎨 Clasificador por color (Track B) | `mesa_clasificacion/state` | Color/posición simulada de la pieza en la mesa |
| 🚚 Robot de reparto (Track A) | `campus/state` | Punto de ruta simulado actual |
| 🧩 Ensamblador (Track B) | `mesa_ensamblado/state` | Pieza simulada actualmente en manipulación |

El campo `data` del mensaje es un `str`/`std::string` libre por ahora — desde la
Semana 02 vas a reemplazarlo por un mensaje custom propio de tu dominio.

## Checklist

- [ ] Elegí mi misión/dominio y lo escribí en el README de mi propio repositorio
- [ ] Ambos paquetes compilan y el nodo `sensor_stub` corre en los dos lenguajes
- [ ] `colcon test` pasa en ambos paquetes
