# Ejercicio 04 — Diagnosticar QoS e interfaces con la CLI

Sin código nuevo. Usas los nodos de los Ejercicios 01-03 para ver el QoS real de cada
extremo, reproducir las dos incompatibilidades de la teoría 02 y publicar tu tipo
propio desde la terminal. Es la rutina que repetirás cada vez que "un nodo no recibe".

**Antes de empezar**: Ejercicios 01, 02 y 03 compilados en el mismo workspace.

En **cada terminal nueva**, primero, desde la raíz del workspace:

```bash
source install/setup.bash
```

## Paso 1: Ver el QoS ofrecido

```bash
# Terminal 1
ros2 run ejercicio01_qos_py range_publisher
```

```bash
# Terminal 2
ros2 topic info /sensor/range --verbose
```

Salida esperada (las líneas importantes):

```text
Type: sensor_msgs/msg/Range
Publisher count: 1
Node name: range_publisher
Endpoint type: PUBLISHER
  Reliability: BEST_EFFORT
  History (Depth): UNKNOWN
  Durability: VOLATILE
Subscription count: 0
```

✅ Verificación: `Reliability: BEST_EFFORT` y `Durability: VOLATILE`, el preset
`sensor_data`. `History (Depth): UNKNOWN` es normal: el `depth` no se anuncia a otros
procesos porque no afecta a la compatibilidad (teoría 03, sección 6.1).

## Paso 2: Reproducir la incompatibilidad de reliability

Deja el `range_publisher` corriendo. En la terminal 2:

```bash
ros2 topic echo /sensor/range --qos-reliability reliable
```

✅ Verificación: no aparece ningún mensaje y sí un aviso con
`offering incompatible QoS` y `Last incompatible policy: RELIABILITY`. Ciérralo con
`Ctrl+C`.

```bash
ros2 topic echo /sensor/range --qos-profile sensor_data --field range
# 1.2000000476837158
# ---
# 1.300000011920929
# ---
```

✅ Verificación: ahora sí llegan datos. Los decimales raros son normales: `range` es
`float32` y Python lo imprime con la precisión de un `float` de 64 bits.

## Paso 3: Contar subscribers con QoS distinto

Con el `echo` del paso anterior corriendo, abre una **terminal 3**:

```bash
ros2 topic info /sensor/range --verbose
```

✅ Verificación: `Subscription count: 1` y, en el bloque del subscriber,
`Reliability: BEST_EFFORT`. Un `echo` incompatible **también** aparece en el recuento:
contar subscribers no prueba que reciban. Cierra todo con `Ctrl+C`.

## Paso 4: Reproducir la incompatibilidad de durability

```bash
# Terminal 1
ros2 run ejercicio02_qos_cpp status_publisher
# [INFO] [...] [status_publisher]: Estado publicado una vez: ready
```

Espera unos segundos y, en la terminal 2:

```bash
ros2 topic echo /robot/status --qos-durability volatile --qos-reliability reliable
```

✅ Verificación: no aparece nada. No es incompatible (`TRANSIENT_LOCAL` ofrecido
cubre `VOLATILE` pedido), pero un subscriber volátil no recibe el historial y el
publisher no vuelve a publicar. `Ctrl+C` y ahora:

```bash
ros2 topic echo /robot/status --qos-durability transient_local --qos-reliability reliable --once
# data: ready
# ---
```

✅ Verificación: `ready` llega aunque se publicó segundos antes.

## Paso 5: El caso incompatible de durability

Cierra el `status_publisher`. Publica el estado desde la CLI **sin** durabilidad:

```bash
# Terminal 1
ros2 topic pub /robot/status std_msgs/msg/String "{data: 'volatile'}" --qos-durability volatile
```

```bash
# Terminal 2
ros2 run ejercicio01_qos_py qos_listener
```

✅ Verificación: el listener no imprime `Estado del robot` y el log muestra
`offering incompatible QoS` con `Last incompatible policy: DURABILITY`. Su
subscripción pide `TRANSIENT_LOCAL`, el publisher solo ofrece `VOLATILE`. Cierra
ambos.

## Paso 6: Publicar tu tipo propio desde la CLI

```bash
# Terminal 1
ros2 run ejercicio03_reading_cpp reading_listener
```

```bash
# Terminal 2
ros2 interface proto ejercicio03_interfaces/msg/SensorReading
# "header:
#   stamp:
#     sec: 0
#     nanosec: 0
#   frame_id: ''
# sensor_id: ''
# value: 0.0
# unit: m
# is_valid: true
# status: 0
# "

ros2 topic pub --once /sensor/reading ejercicio03_interfaces/msg/SensorReading \
  "{sensor_id: 'cli', value: 9.0, status: 2}"
```

✅ Verificación: en la terminal 1 aparece
`[WARN] [...] [reading_listener]: cli fuera de rango: 9.00 m`. `unit` vale `m` sin
haberlo escrito: es el valor por defecto del `.msg`.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. En el Paso 3, ¿por qué `Subscription count: 1` no basta para saber que el
   subscriber recibe datos? ¿Qué mirarías además?
2. ¿Por qué el Paso 4 (`VOLATILE` contra `TRANSIENT_LOCAL`) no da aviso y el Paso 5
   (al revés) sí?
3. Un compañero dice "con `ros2 topic echo` sí veo los datos, así que mi nodo está
   bien". ¿Qué le contestas?

## Checklist

- [ ] Leí el QoS de un publisher y de un subscriber con `ros2 topic info --verbose`
- [ ] Reproduje la incompatibilidad de reliability y la de durability y leí sus avisos
- [ ] Recibí un mensaje latched con `ros2 topic echo --qos-durability transient_local`
- [ ] Publiqué un `SensorReading` desde la CLI y lo vi en el listener C++
- [ ] Respondí las tres preguntas en `3-proyecto/README.md`

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03](../ejercicio-03-interfaz_compartida/README.md) | **Ejercicio 04** | [Proyecto](../../3-proyecto/README.md) |

← [Volver a la Semana 02](../../README.md)
