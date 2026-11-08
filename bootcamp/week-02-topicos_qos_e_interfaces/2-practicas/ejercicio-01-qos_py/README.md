# Ejercicio 01 — Perfiles QoS en Python (`rclpy`)

Vas a construir tres nodos: un sensor de distancia con QoS `sensor_data`, un publisher
de estado latched (`TRANSIENT_LOCAL`) y un listener que pide el QoS correcto a cada
uno. Cada paso tiene un test que falla hasta que lo completas.

**Antes de empezar**: teorías [01](../../1-teoria/01-tipos-de-mensaje-e-interfaces-estandar.md),
[02](../../1-teoria/02-qos-politicas-y-compatibilidad.md) y
[03](../../1-teoria/03-qos-en-codigo-y-diagnostico.md) leídas.

## Preparar el workspace

Copia el starter dentro de `src/` de tu workspace (la carpeta que contiene `src/`):

```bash
cp -r <ruta-al-repo>/bootcamp/week-02-topicos_qos_e_interfaces/2-practicas/ejercicio-01-qos_py/starter \
  src/ejercicio01_qos_py
```

Estructura:

```
src/ejercicio01_qos_py/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/ejercicio01_qos_py
├── ejercicio01_qos_py/
│   ├── __init__.py
│   ├── range_publisher.py     # PASO 1 y 2
│   ├── status_publisher.py    # PASO 3
│   └── qos_listener.py        # PASO 4
└── test/
    └── test_qos.py            # tests ya escritos, fallan hasta completar los pasos
```

Todos los pasos se verifican igual, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio01_qos_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio01_qos_py
colcon test-result --verbose
```

Antes del primer paso, los cuatro tests fallan. Es lo esperado.

## Paso 1: Publisher con el preset de sensores

**Por qué**: un sensor a 10 Hz no necesita reintentos; si se pierde una lectura, la
siguiente llega en 100 ms. `qos_profile_sensor_data` da `BEST_EFFORT` con `depth` 5.

**Abre `ejercicio01_qos_py/range_publisher.py`** y descomenta el bloque del Paso 1.

**Verifica**: pasa `test_range_publisher_es_best_effort`. El test pregunta al grafo
con `get_publishers_info_by_topic` qué QoS ofrece tu publisher, lo mismo que hace
`ros2 topic info -v`.

## Paso 2: Rellenar el `Header`

**Por qué**: sin `stamp` ni `frame_id`, nadie puede saber cuándo ni desde dónde se
midió la distancia (teoría 01, sección 3.1).

**Descomenta el bloque del Paso 2** en el mismo archivo, dentro de `_on_timer`.

**Verifica**: pasa `test_range_lleva_header`.

## Paso 3: Estado latched

**Por qué**: el nodo publica `"ready"` **una sola vez** al arrancar. Con `VOLATILE`,
cualquier nodo que arranque un segundo después nunca lo sabría. Con `TRANSIENT_LOCAL`,
el publisher lo guarda y se lo entrega a cada subscriber que llegue tarde.

**Abre `ejercicio01_qos_py/status_publisher.py`**. El perfil `LATCHED_QOS` ya está
definido arriba del archivo; descomenta el bloque del Paso 3, que lo usa.

**Verifica**: pasa `test_status_llega_a_suscriptor_tardio`. El test espera medio
segundo **después** de publicar y solo entonces crea el subscriber: si recibe
`"ready"`, la durabilidad funciona.

## Paso 4: Listener con el QoS de cada publisher

**Por qué**: el subscriber decide la otra mitad de la compatibilidad (teoría 02,
sección 4). Para `sensor/range` pide `sensor_data`; para `robot/status`, `LATCHED_QOS`.

**Abre `ejercicio01_qos_py/qos_listener.py`** y descomenta el bloque del Paso 4.

**Verifica**: pasa `test_listener_recibe_ambos_topics`. Con esto, los cuatro tests
pasan.

## Paso 5: Romperlo a propósito

Aprender a reconocer el fallo vale tanto como el código correcto. En
`qos_listener.py`, cambia temporalmente `qos_profile_sensor_data` por `10` en la
subscripción de `sensor/range` y vuelve a compilar y testear.

**Verifica**: `colcon test-result --verbose` muestra
`AssertionError: range_count=0, status='ready'`. El estado latched llega; el sensor no.
El motivo está en el log completo del test:

```bash
grep -o "Last incompatible policy: [A-Z]*" log/latest_test/ejercicio01_qos_py/stdout_stderr.log
# Last incompatible policy: RELIABILITY
```

La línea entera del aviso es:

```text
New publisher discovered on topic 'sensor/range', offering incompatible QoS.
No messages will be received from it. Last incompatible policy: RELIABILITY
```

Deja el código como estaba y comprueba que los cuatro tests vuelven a pasar.

## Correr los nodos de verdad

En cada terminal nueva, primero `source install/setup.bash` desde la raíz del
workspace.

```bash
# Terminal 1
ros2 run ejercicio01_qos_py range_publisher

# Terminal 2
ros2 run ejercicio01_qos_py status_publisher
# [INFO] [...] [status_publisher]: Estado publicado una vez: ready

# Terminal 3: arranca DESPUÉS de las otras dos
ros2 run ejercicio01_qos_py qos_listener
# [INFO] [...] [qos_listener]: Estado del robot: ready
# [INFO] [...] [qos_listener]: range_sensor: 1.40 m
```

El listener recibe `ready` aunque se publicó antes de que existiera.

## Checklist

- [ ] Los cuatro tests de `test/test_qos.py` pasan
- [ ] Vi fallar el Paso 5 con el aviso `incompatible QoS` y lo dejé arreglado
- [ ] El listener recibe `ready` aunque arranque el último

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Prácticas](../README.md) | **Ejercicio 01** | [Ejercicio 02](../ejercicio-02-qos_cpp/README.md) |

← [Volver a la Semana 02](../../README.md)
