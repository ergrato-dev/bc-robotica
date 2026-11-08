# Proyecto — Semana 04

## Qué capa se añade esta semana

Hasta ahora, `sensor_stub` empezaba a publicar en cuanto existía. Esta semana
arranca **en orden**:

- Las dos capas (Python y C++) son **nodos lifecycle**: en `unconfigured` solo
  existe el parámetro; `configure` crea el publisher y el servicio `set_mode`;
  `activate` empieza a publicar
- La capa C++ es además un **componente**: se puede cargar en un container o
  arrancar con `ros2 run` como siempre
- El README de tu repositorio **justifica el executor** de cada capa

Mismo nombre de nodo, topic, servicio, parámetro y transiciones en los dos
lenguajes: siguen siendo intercambiables.

```
src/
├── proyecto_dominio_interfaces/   # sin cambios
├── proyecto_dominio_py/           # sensor_stub: LifecycleNode
└── proyecto_dominio_cpp/          # sensor_stub: LifecycleNode + componente
```

## Por qué va aquí

En la misión, el estado del robot no debe publicarse antes de que sus fuentes
estén listas. En la Semana 06 un launch file arrancará y activará
`sensor_stub` junto al resto de nodos, y desde la Semana 15 el lifecycle manager
de Nav2 hará lo mismo con los suyos. Llegar con tus nodos ya preparados evita
reescribirlos entonces.

## Requisitos verificables

1. `colcon build --symlink-install` compila los tres paquetes sin errores ni warnings
2. Recién arrancado, `ros2 lifecycle get /sensor_stub` da `unconfigured [1]` y
   no existen ni `<tu_dominio>/state` ni `<tu_dominio>/set_mode`
3. Tras `configure`, el servicio responde pero no se publica nada; tras
   `activate`, el estado se publica al periodo de `publish_period_s`
4. `deactivate` para la publicación; `cleanup` elimina publisher y servicio y
   devuelve modo y batería a sus valores iniciales
5. `ros2 component types` muestra `proyecto_dominio_cpp::SensorStub`, y cargado
   en un container se controla con los mismos comandos `ros2 lifecycle`
6. `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
7. El README de tu repositorio justifica el executor de cada capa (esquema del
   Ejercicio 02) y responde las preguntas de los Ejercicios 01, 03 y 04

## Cómo verificarlo, paso a paso

Copia los tres paquetes del `starter/` a `src/`, reemplazando los de la Semana 03
(este starter es su evolución; vuelve a aplicar tus renombrados):

```bash
cp -r <ruta-al-repo>/bootcamp/week-04-executors_composicion_y_lifecycle/3-proyecto/starter/* src/
colcon build --symlink-install
# Summary: 3 packages finished [...]
source install/setup.bash
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result --verbose
# Summary: 11 tests, 0 errors, 0 failures, 0 skipped
```

Son cinco tests por lenguaje; `colcon test-result` cuenta uno más por el
resumen que genera el paquete C++.

Prueba manual (en cada terminal, antes, `source install/setup.bash`):

```bash
# Terminal 1
ros2 run proyecto_dominio_py sensor_stub
```

```bash
# Terminal 2
ros2 lifecycle get /sensor_stub
# unconfigured [1]
ros2 service list | grep set_mode
# (sin salida)

ros2 lifecycle set /sensor_stub configure
# Transitioning successful
ros2 service call /dominio/set_mode proyecto_dominio_interfaces/srv/SetMode "{mode: 2}"
# ...
# proyecto_dominio_interfaces.srv.SetMode_Response(accepted=True, message='modo 2')

ros2 lifecycle set /sensor_stub activate
# Transitioning successful
ros2 topic echo /dominio/state --field mode --once
# 2
# ---

ros2 param set /sensor_stub publish_period_s 0.5
# Set parameter successful
ros2 topic hz /dominio/state
# average rate: 2.000
# ...
```

Cierra la terminal 1 y repite con la capa C++, primero con `ros2 run
proyecto_dominio_cpp sensor_stub` y después como componente:

```bash
# Terminal 1
ros2 run rclcpp_components component_container
```

```bash
# Terminal 2
ros2 component load /ComponentManager proyecto_dominio_cpp proyecto_dominio_cpp::SensorStub
# Loaded component 1 into '/ComponentManager' container node as '/sensor_stub'
ros2 lifecycle set /sensor_stub configure
ros2 lifecycle set /sensor_stub activate
ros2 topic echo /dominio/state --field mode --once
# 1
# ---
```

`1` es `MODE_WORKING`, el modo inicial: el componente es un nodo nuevo.

## Criterios de calidad

- Cada recurso se crea en una transición y se destruye en su opuesta
  (`configure`/`cleanup`, `activate`/`deactivate`)
- `on_activate` y `on_deactivate` llaman a la implementación base
- La justificación del executor nombra callbacks concretos y su duración, no
  "porque es más rápido"
- Python y C++ responden igual a la misma secuencia de `ros2 lifecycle`

## Adaptación al dominio

Además de los renombrados de semanas anteriores (topic, tipo, servicio, modos),
piensa qué significa cada estado en tu misión:

| Misión | Qué reservaría `configure` en un robot real | Qué empezaría `activate` |
|---|---|---|
| 📦 Almacén | Conexión con el sistema de gestión del almacén | Publicar estado y aceptar pedidos |
| 🔬 Laboratorio | Comprobar la pinza y la balanza | Publicar estado de la estación |
| 🔦 Inspección industrial | Abrir cámara térmica y sensor de gas | Publicar lecturas de la ronda |
| 🧹 Oficina | Mapa de zonas y horario de limpieza | Publicar estado de limpieza |
| 🌾 Agrícola | GPS y cámara multiespectral | Publicar estado del surco |
| 📚 Biblioteca | Lector RFID y catálogo | Publicar estado de devoluciones |

Escribe la fila de tu misión en tu README, con lo que haría `cleanup` para
deshacer `configure`.

## Checklist

- [ ] Las dos capas arrancan en `unconfigured` y solo publican en `active`
- [ ] La capa C++ se carga en un container y se controla con `ros2 lifecycle`
- [ ] `colcon test` pasa en los dos paquetes de nodos
- [ ] Justifiqué el executor de cada capa y respondí las preguntas de los ejercicios

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04](../2-practicas/ejercicio-04-lifecycle_cpp/README.md) | **Proyecto** | [Recursos](../4-recursos/README.md) |

← [Volver a la Semana 04](../README.md)
