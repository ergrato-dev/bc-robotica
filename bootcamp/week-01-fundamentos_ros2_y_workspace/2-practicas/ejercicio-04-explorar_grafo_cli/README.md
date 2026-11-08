# Ejercicio 04 — Explorar y reconectar el grafo con la CLI

Sin código nuevo. Usas la CLI `ros2` para inspeccionar el grafo, publicar a mano,
aislar dos grafos con `ROS_DOMAIN_ID` y reconectar tus propios nodos (Python y C++) con
remapping. Es la base de toda depuración que harás en el bootcamp.

**Antes de empezar**: teoría [05 · Introspección CLI y remapping](../../1-teoria/05-introspeccion-cli-nombres-y-remapping.md)
leída, y los Ejercicios 01 y 02 compilados.

En **cada terminal nueva** que abras, ejecuta primero esto desde la raíz del workspace
(la carpeta que contiene `src/`, `build/` e `install/`):

```bash
source install/setup.bash
```

Sin ese paso, `ros2 run` no encuentra `ejercicio01_pubsub_py` ni `ejercicio02_pubsub_cpp`
y responde `Package 'ejercicio01_pubsub_py' not found`.

## Paso 1: Inspeccionar un nodo que no escribiste

```bash
# Terminal 1
ros2 run demo_nodes_cpp talker
```

```bash
# Terminal 2
ros2 node list
ros2 topic list -t
ros2 topic info /chatter
ros2 interface show std_msgs/msg/String
```

Salida esperada (las líneas importantes):

```text
/talker
/chatter [std_msgs/msg/String]
Type: std_msgs/msg/String
Publisher count: 1
Subscription count: 0
string data
```

✅ Verificación: `Publisher count: 1` y `Subscription count: 0`.

## Paso 2: Contar subscribers

Deja el talker corriendo. En la terminal 2:

```bash
ros2 topic echo /chatter
```

Abre una **terminal 3**:

```bash
ros2 topic info /chatter
```

✅ Verificación: ahora `Subscription count: 1`. El `echo` de la terminal 2 cuenta como
subscriber. Cierra el `echo` con `Ctrl+C` y repite `ros2 topic info /chatter`: vuelve a
`0`.

## Paso 3: Probar un listener aislado

Cierra el talker (`Ctrl+C` en la terminal 1) y arranca tu listener Python:

```bash
# Terminal 1
ros2 run ejercicio01_pubsub_py sensor_listener
```

```bash
# Terminal 2
ros2 topic pub --once /sensor/state std_msgs/msg/String "{data: 'lectura manual'}"
```

✅ Verificación: en la terminal 1 aparece
`[INFO] [...] [sensor_listener]: Recibido: lectura manual`.

Acabas de probar el subscriber sin el publisher real.

## Paso 4: Aislar dos grafos con `ROS_DOMAIN_ID`

Deja el listener de la terminal 1 corriendo (está en el `ROS_DOMAIN_ID` por defecto de
tu entorno). En la terminal 2:

```bash
ROS_DOMAIN_ID=7 ros2 topic pub --once /sensor/state std_msgs/msg/String "{data: 'otro dominio'}"
```

✅ Verificación: el listener **no** imprime nada y `ros2 topic pub` se queda esperando
un subscriber que nunca aparece (ciérralo con `Ctrl+C`). El prefijo `ROS_DOMAIN_ID=7`
solo afecta a ese comando: es otro grafo, invisible para el tuyo.

```bash
echo $ROS_DOMAIN_ID
# 42   (el valor que fija el docker-compose del bootcamp; si sale vacío, es 0)
```

## Paso 5: Namespace que rompe, remapping que repara (entre lenguajes)

Cierra todo. Arranca tu publisher **C++** dentro del namespace `/robot1`:

```bash
# Terminal 1
ros2 run ejercicio02_pubsub_cpp sensor_publisher --ros-args -r __ns:=/robot1
```

```bash
# Terminal 2
ros2 topic list
# /parameter_events
# /robot1/sensor/state
# /rosout

ros2 run ejercicio01_pubsub_py sensor_listener
```

✅ Verificación: el listener Python **no** recibe nada. Escucha `/sensor/state`, pero el
publisher, al tener el topic relativo `sensor/state`, publica en `/robot1/sensor/state`.

Cierra el listener (`Ctrl+C`) y arráncalo remapeado:

```bash
# Terminal 2
ros2 run ejercicio01_pubsub_py sensor_listener --ros-args -r sensor/state:=/robot1/sensor/state
```

✅ Verificación: aparece `Recibido: lectura #N`. Publisher C++ y listener Python
conectados por un nombre que ninguno de los dos tiene en su código.

## Paso 6: Renombrar el nodo

```bash
# Terminal 3
ros2 run ejercicio01_pubsub_py sensor_listener --ros-args -r __node:=monitor \
  -r sensor/state:=/robot1/sensor/state
ros2 node list
```

✅ Verificación: `ros2 node list` muestra `/monitor` además de `/robot1/sensor_publisher`
y `/sensor_listener`. Dos copias del mismo ejecutable conviven porque tienen nombres
distintos.

> Si ves el mismo nodo listado dos veces o un nodo que ya cerraste, es el daemon con
> información vieja: `ros2 daemon stop` y repite el comando.

## Paso 7: Verlo dibujado

Con los nodos del paso 6 corriendo:

```bash
rqt_graph
```

✅ Verificación: ves `/robot1/sensor_publisher` unido por `/robot1/sensor/state` a
`/sensor_listener` y a `/monitor`. Si no aparecen, pulsa el botón de recarga (flechas
circulares, arriba a la izquierda).

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué `/rosout` y `/parameter_events` aparecen en `ros2 topic list` aunque ningún
   nodo tuyo los cree?
2. Si tu publisher usara el topic absoluto `"/sensor/state"`, ¿qué habría pasado en el
   paso 5 sin remapping? ¿Por qué eso es un problema con dos robots?
3. ¿Qué comando usarías para comprobar, sin arrancar el publisher real, que tu listener
   procesa bien un mensaje concreto?

## Checklist

- [ ] Inspeccioné nodos, topics, tipos y contadores con la CLI
- [ ] Probé un listener aislado con `ros2 topic pub --once`
- [ ] Comprobé que `ROS_DOMAIN_ID` distinto aísla los grafos
- [ ] Reconecté un publisher C++ en `/robot1` con un listener Python usando solo `-r`
- [ ] Vi el grafo resultante en `rqt_graph`
- [ ] Respondí las tres preguntas en `3-proyecto/README.md`

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03](../ejercicio-03-comparar_latencia/README.md) | **Ejercicio 04** | [Proyecto](../../3-proyecto/README.md) |

← [Volver a la Semana 01](../../README.md)
