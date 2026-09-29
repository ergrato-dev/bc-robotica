# Ejercicio 01 — Publisher/Subscriber en Python (`rclpy`)

Vas a completar un nodo publisher y un nodo subscriber descomentando código paso a
paso. Cada paso tiene un test que falla hasta que lo completas.

## Abrir el starter

```bash
cd bootcamp/week-01-fundamentos_ros2_y_workspace/2-practicas/ejercicio-01-publisher_subscriber_py/starter
```

Estructura:

```
starter/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/ejercicio01_pubsub_py
├── ejercicio01_pubsub_py/
│   ├── __init__.py
│   ├── sensor_publisher.py    # PASO 1 y 2
│   └── sensor_listener.py     # PASO 3
└── test/
    └── test_pubsub.py          # tests ya escritos, fallan hasta completar los pasos
```

## Paso 1: El publisher crea su canal

**Por qué**: sin declarar el publisher en el constructor, el nodo no aparece en el
grafo como publicador de nada — `ros2 topic list` no mostraría `/sensor/state`.

**Abre `ejercicio01_pubsub_py/sensor_publisher.py`** y descomenta la sección del Paso 1.

**Verifica**:

```bash
colcon build --packages-select ejercicio01_pubsub_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio01_pubsub_py
colcon test-result --verbose
```

Debe pasar `test_publisher_existe`. Los demás tests siguen fallando: son de pasos
posteriores.

## Paso 2: El timer publica periódicamente

**Por qué**: un publisher sin nada que lo dispare nunca envía mensajes. El timer es lo
que convierte "puedo publicar" en "publico cada 0.5 segundos".

**Descomenta la sección del Paso 2** en el mismo archivo.

**Verifica**: debe pasar `test_publica_mensajes`.

## Paso 3: El listener se suscribe y cuenta mensajes

**Por qué**: un subscriber sin callback registrado no recibe nada, aunque esté
"suscrito" — el callback es lo que ROS2 invoca cuando llega un mensaje nuevo.

**Abre `ejercicio01_pubsub_py/sensor_listener.py`** y descomenta la sección del Paso 3.

**Verifica**: debe pasar `test_listener_recibe_mensajes_del_publisher`. Con esto, los
tres tests del starter pasan.

## Correr los nodos de verdad (no solo los tests)

```bash
# Terminal 1
ros2 run ejercicio01_pubsub_py sensor_publisher

# Terminal 2
ros2 run ejercicio01_pubsub_py sensor_listener

# Terminal 3 — inspección
ros2 topic echo /sensor/state
ros2 topic hz /sensor/state
```

## Checklist

- [ ] Los tres tests de `test/test_pubsub.py` pasan
- [ ] `ros2 topic hz /sensor/state` reporta ~2 Hz (el timer es de 0.5 s)
- [ ] `ros2 node info /sensor_listener` muestra la subscripción a `/sensor/state`
