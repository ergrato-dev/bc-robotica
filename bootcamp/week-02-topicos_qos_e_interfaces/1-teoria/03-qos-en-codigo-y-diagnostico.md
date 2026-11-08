# QoS en código y diagnóstico

> Saber qué QoS quieres es la mitad; la otra mitad es escribirlo igual en Python y en C++ y saber comprobar desde la terminal qué QoS tiene de verdad cada extremo.

## 🎯 Objetivos

- Declarar perfiles QoS en `rclpy` y en `rclcpp`, con preset o política a política
- Implementar el patrón latched (`TRANSIENT_LOCAL`) en ambos lenguajes
- Detectar un QoS incompatible desde el código con un callback de evento
- Inspeccionar y forzar QoS desde la CLI (`ros2 topic info -v`, `--qos-*`)

## 1. Qué problema resuelve

En la teoría 02 viste que un desajuste de QoS no da error: el callback simplemente no
se ejecuta. Necesitas dos cosas: escribir el QoS **explícito** (nunca un `10` que
nadie sabe qué significa) y tener herramientas para ver el QoS real del grafo cuando
algo no llega.

## 2. Cómo funciona: el tercer argumento

El argumento que en la Semana 01 era `10` acepta en realidad un **perfil QoS**
completo. Pasar un número es un atajo: "perfil por defecto con este `depth`".

```python
self.create_publisher(String, "sensor/state", 10)
# equivale a
self.create_publisher(String, "sensor/state", QoSProfile(depth=10))
```

```cpp
create_publisher<std_msgs::msg::String>("sensor/state", 10);
// equivale a
create_publisher<std_msgs::msg::String>("sensor/state", rclcpp::QoS(10));
```

## 3. Cómo se escribe en Python (`rclpy`)

```python
from rclpy.qos import (
    DurabilityPolicy,
    HistoryPolicy,
    QoSProfile,
    ReliabilityPolicy,
    qos_profile_sensor_data,
)

# 1. Preset para sensores: KEEP_LAST 5, BEST_EFFORT, VOLATILE
self._range_pub = self.create_publisher(Range, "sensor/range", qos_profile_sensor_data)

# 2. Latched: el último mensaje queda guardado para quien llegue tarde
latched_qos = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
)
self._status_pub = self.create_publisher(String, "robot/status", latched_qos)
self._status_pub.publish(String(data="ready"))  # una sola vez, en el constructor
```

`qos_profile_sensor_data` es un objeto `QoSProfile` ya construido: lo pasas tal cual.
Si quieres el preset pero con otro `depth`, cópialo y cambia solo ese campo:

```python
from copy import copy

deep_sensor_qos = copy(qos_profile_sensor_data)
deep_sensor_qos.depth = 20
```

El subscriber del topic latched **también** tiene que pedir `TRANSIENT_LOCAL`; si pide
`VOLATILE` conecta, pero no recibe el mensaje guardado (tabla de la teoría 02):

```python
self._status_sub = self.create_subscription(
    String, "robot/status", self._on_status, latched_qos
)
```

## 4. Cómo se escribe en C++ (`rclcpp`)

`rclcpp::QoS` se construye con el `depth` y se ajusta encadenando métodos. Cada
método devuelve el propio objeto, así que se lee como una frase:

```cpp
// 1. Preset para sensores (mismo perfil que qos_profile_sensor_data)
range_pub_ = create_publisher<sensor_msgs::msg::Range>("sensor/range", rclcpp::SensorDataQoS());

// 2. Latched
auto latched_qos = rclcpp::QoS(1).reliable().transient_local();
status_pub_ = create_publisher<std_msgs::msg::String>("robot/status", latched_qos);

std_msgs::msg::String msg;
msg.data = "ready";
status_pub_->publish(msg);
```

| Python | C++ |
|---|---|
| `qos_profile_sensor_data` | `rclcpp::SensorDataQoS()` |
| `QoSProfile(depth=1)` | `rclcpp::QoS(1)` |
| `reliability=ReliabilityPolicy.BEST_EFFORT` | `.best_effort()` |
| `reliability=ReliabilityPolicy.RELIABLE` | `.reliable()` |
| `durability=DurabilityPolicy.TRANSIENT_LOCAL` | `.transient_local()` |
| `durability=DurabilityPolicy.VOLATILE` | `.durability_volatile()` |
| `history=HistoryPolicy.KEEP_ALL` | `.keep_all()` |
| `copy(...)` + `.depth = 20` | `rclcpp::SensorDataQoS().keep_last(20)` |

## 5. Detectar un QoS incompatible desde el código

Por defecto ROS2 deja el `[WARN]` que viste en la teoría 02. Si quieres reaccionar
(contar fallos, publicar un diagnóstico), registras un **callback de evento** al crear
el subscriber.

En Python:

```python
from rclpy.event_handler import (
    QoSRequestedIncompatibleQoSInfo,
    SubscriptionEventCallbacks,
)
from rclpy.qos import qos_policy_name_from_kind

callbacks = SubscriptionEventCallbacks(incompatible_qos=self._on_incompatible_qos)
self._sub = self.create_subscription(
    Range, "sensor/range", self._on_range, QoSProfile(depth=10),
    event_callbacks=callbacks,
)

def _on_incompatible_qos(self, info: QoSRequestedIncompatibleQoSInfo) -> None:
    # last_policy_kind dice qué política falló; qos_policy_name_from_kind la
    # convierte en texto legible ("RELIABILITY", "DURABILITY"...).
    policy = qos_policy_name_from_kind(info.last_policy_kind)
    self.get_logger().error(
        f"QoS incompatible en sensor/range: {policy} "
        f"({info.total_count} publishers)"
    )
```

En C++, el callback va en las opciones del subscriber:

```cpp
rclcpp::SubscriptionOptions options;
options.event_callbacks.incompatible_qos_callback =
    [this](rclcpp::QOSRequestedIncompatibleQoSInfo& info) {
      RCLCPP_ERROR(get_logger(), "QoS incompatible en sensor/range: %s (%d publishers)",
                   rclcpp::qos_policy_name_from_kind(info.last_policy_kind).c_str(),
                   info.total_count);
    };
sub_ = create_subscription<sensor_msgs::msg::Range>(
    "sensor/range", rclcpp::QoS(10), std::bind(&MyNode::on_range, this, std::placeholders::_1),
    options);
```

En ambos lenguajes la política llega como un número (`enum` de la capa `rmw`);
`qos_policy_name_from_kind` lo traduce al mismo nombre que ves en el `[WARN]`.

## 6. Diagnóstico desde la CLI

### 6.1 Ver el QoS real de cada extremo

```bash
ros2 topic info /sensor/range --verbose
```

Salida (recortada a lo importante):

```text
Type: sensor_msgs/msg/Range

Publisher count: 1

Node name: range_publisher
Node namespace: /
Topic type: sensor_msgs/msg/Range
Endpoint type: PUBLISHER
QoS profile:
  Reliability: BEST_EFFORT
  History (Depth): UNKNOWN
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  ...

Subscription count: 0
```

`History (Depth): UNKNOWN` es normal: DDS no anuncia el `history` ni el `depth` a los
demás procesos, porque no afectan a la compatibilidad. Lo que sí ves es lo que decide
si dos extremos conectan.

Con un subscriber conectado aparece también su bloque. Compara `Reliability` y
`Durability` de ambos contra la tabla de la teoría 02.

### 6.2 Forzar el QoS del `echo` y del `pub`

Por defecto, `ros2 topic echo` adapta su QoS a los publishers que encuentra, así que
casi siempre recibe. Para reproducir lo que vería un subscriber concreto, fuerza las
políticas:

```bash
# Simula un subscriber RELIABLE contra un publisher BEST_EFFORT: no recibe nada
ros2 topic echo /sensor/range --qos-reliability reliable

# Igual que un subscriber con el preset de sensores: recibe
ros2 topic echo /sensor/range --qos-profile sensor_data

# Publicar un valor latched desde la terminal
ros2 topic pub --once --qos-durability transient_local --qos-reliability reliable \
  /robot/status std_msgs/msg/String "{data: 'ready'}"
```

Opciones de ambos comandos: `--qos-profile`, `--qos-depth`, `--qos-history`,
`--qos-reliability`, `--qos-durability`.

## 7. Antipatrones

- ❌ **Un `10` mágico en un nodo de producción.** Escribe el perfil o el preset: quien
  lea el código sabe qué garantías esperas
- ❌ **Latched solo en el publisher.** Si el subscriber pide `VOLATILE`, conecta pero
  no recibe el valor guardado
- ❌ **Copiar `qos_profile_sensor_data` y modificarlo sin `copy()`.** Cambiarías el
  preset global para todo el proceso
- ❌ **Diagnosticar con `ros2 topic echo` sin `--qos-*`.** Como se adapta solo, "el
  echo recibe" no prueba que tu nodo vaya a recibir

## 8. Trucos

- `ros2 topic info -v` es el primer comando cuando "el echo recibe y mi nodo no"
- `ros2 topic echo /x --qos-profile sensor_data --field range` — solo el campo útil
- `ros2 doctor --report` incluye una sección de QoS por topic si el grafo está vivo

## 📚 Recursos Adicionales

- [QoS settings — ROS2 Jazzy](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
- [QoS events — design.ros2.org](https://design.ros2.org/articles/qos_deadline_liveliness_lifespan.html)
- [rclpy.qos — API](https://docs.ros.org/en/jazzy/p/rclpy/api/qos.html)

## ✅ Checklist de Verificación

- [ ] Escribí un publisher con `sensor_data` y otro latched, en Python y en C++
- [ ] Sé traducir cada política entre `QoSProfile` y `rclcpp::QoS`
- [ ] Vi el QoS de un topic con `ros2 topic info --verbose`
- [ ] Reproduje un QoS incompatible con `ros2 topic echo --qos-reliability reliable`

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Políticas QoS](02-qos-politicas-y-compatibilidad.md) | **03 · QoS en código** | [04 · Interfaces custom](04-interfaces-custom-con-rosidl.md) |

← [Volver a la Semana 02](../README.md)
