# Proyecto — Semana 03

## Qué capa se añade esta semana

Hasta ahora, `sensor_stub` solo hablaba: publicaba su estado y nadie podía pedirle
nada. Esta semana aprende a **escuchar órdenes** y a **configurarse sin
recompilar**:

- Un servicio propio, `SetMode.srv` (que renombras), en
  `proyecto_dominio_interfaces`: cambia el modo del robot y responde si lo aceptó
- Un parámetro `publish_period_s` con descripción y rango, que se puede cambiar
  con el nodo en marcha

Las dos capas (Python y C++) ofrecen **el mismo servicio y el mismo parámetro**,
con el mismo nombre de nodo: siguen siendo intercambiables.

```
src/
├── proyecto_dominio_interfaces/   # + srv/SetMode.srv
├── proyecto_dominio_py/           # sensor_stub: + servicio + parámetro
└── proyecto_dominio_cpp/          # el mismo nodo en C++
```

## Por qué va aquí

Los nodos de las semanas siguientes ya no son islas: el orquestador de la misión
(Semana 18) pondrá el robot en modo carga llamando a este servicio, y los launch
files (Semana 06) pasarán el periodo con un YAML. Las acciones de tu misión llegan
con Nav2 (Semana 16), que ya trae las suyas; esta semana las practicas en el
Ejercicio 03.

## Requisitos verificables

1. `colcon build --symlink-install` compila los tres paquetes sin errores ni warnings
2. `ros2 interface show proyecto_dominio_interfaces/srv/<TuServicio>` muestra una
   request con el modo y una response con `accepted` y `message` (o los nombres
   equivalentes de tu misión)
3. `sensor_stub` (Python y C++) ofrece `<tu_dominio>/set_mode` (relativo):
   acepta los `MODE_*` de tu tipo y rechaza cualquier otro valor con un `message`
   que explique por qué
4. El modo aceptado aparece en el siguiente estado publicado
5. `publish_period_s` tiene `description` y rango, y cambiarlo en marcha cambia el
   ritmo de publicación
6. `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
7. El README de tu repositorio justifica el rango del periodo y responde las
   preguntas de los Ejercicios 03 y 04

## Cómo verificarlo, paso a paso

Copia los tres paquetes del `starter/` a `src/`, reemplazando los de la Semana 02
(este starter es su evolución; vuelve a aplicar tus renombrados):

```bash
cp -r <ruta-al-repo>/bootcamp/week-03-servicios_acciones_y_parametros/3-proyecto/starter/* src/
colcon build --symlink-install
# Summary: 3 packages finished [...]
source install/setup.bash
colcon test --packages-select proyecto_dominio_py proyecto_dominio_cpp
colcon test-result --verbose
# Summary: 8 tests, 0 errors, 0 failures, 0 skipped
```

Prueba manual (en cada terminal, antes, `source install/setup.bash`):

```bash
# Terminal 1
ros2 run proyecto_dominio_py sensor_stub
```

```bash
# Terminal 2
ros2 service call /dominio/set_mode proyecto_dominio_interfaces/srv/SetMode "{mode: 2}"
# ...
# response:
# proyecto_dominio_interfaces.srv.SetMode_Response(accepted=True, message='modo 2')

ros2 service call /dominio/set_mode proyecto_dominio_interfaces/srv/SetMode "{mode: 7}"
# ...
# proyecto_dominio_interfaces.srv.SetMode_Response(accepted=False, message='modo desconocido: 7')

ros2 topic echo /dominio/state --field mode --once
# 2
# ---

ros2 param set /sensor_stub publish_period_s 0.5
# Set parameter successful
ros2 topic hz /dominio/state
# average rate: 2.000
# ...
```

Cierra la terminal 1, arranca `ros2 run proyecto_dominio_cpp sensor_stub` y
repite: las respuestas deben ser las mismas.

## Criterios de calidad

- Nombre del servicio en inglés y con significado (`SetAisleMode`), no `Srv1`
- El `message` de un rechazo explica el motivo; no basta con `accepted=False`
- Los modos válidos salen de las constantes de tu tipo, nunca de números sueltos
- El rango del periodo está justificado: qué pasa por debajo del mínimo y por
  encima del máximo en tu misión

## Adaptación al dominio

Renombra `SetMode` junto con tu tipo de estado. Recuerda actualizar el
`CMakeLists.txt` de las interfaces, los `import`/`#include` (snake_case en C++),
la lista de modos válidos de los dos nodos y los dos tests.

| Misión | Servicio sugerido | Modos que debería aceptar |
|---|---|---|
| 📦 Almacén | `SetAisleMode` | `MODE_IDLE`, `MODE_PICKING`, `MODE_CHARGING` |
| 🔬 Laboratorio | `SetBenchMode` | `MODE_IDLE`, `MODE_TRANSFERRING`, `MODE_CLEANING` |
| 🔦 Inspección industrial | `SetInspectionMode` | `MODE_PATROL`, `MODE_INSPECTING`, `MODE_RETURNING` |
| 🧹 Oficina | `SetCleaningMode` | `MODE_IDLE`, `MODE_CLEANING`, `MODE_CHARGING` |
| 🌾 Agrícola | `SetRowMode` | `MODE_IDLE`, `MODE_SCANNING`, `MODE_RETURNING` |
| 📚 Biblioteca | `SetShelfMode` | `MODE_IDLE`, `MODE_RETURNING_BOOKS`, `MODE_CHARGING` |

Sobre el periodo: un estado que alimenta una interfaz gráfica puede ir a 1 Hz; uno
que vigila la batería de un robot que trabaja cerca de personas, quizá más rápido.
Elige el rango pensando en tu misión, no en el ejemplo.

## Checklist

- [ ] Renombré el servicio y adapté los modos válidos a mi dominio
- [ ] Python y C++ ofrecen el mismo servicio y el mismo parámetro
- [ ] `colcon test` pasa en los dos paquetes de nodos
- [ ] Justifiqué el rango del periodo y respondí las preguntas de los Ejercicios 03 y 04

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04](../2-practicas/ejercicio-04-parametros/README.md) | **Proyecto** | [Recursos](../4-recursos/README.md) |

← [Volver a la Semana 03](../README.md)
