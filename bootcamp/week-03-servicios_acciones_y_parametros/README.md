# Semana 03 — Servicios, acciones y parámetros

> Los topics solo emiten. Un robot también necesita recibir órdenes y responder ("¿has habilitado los motores?"), ejecutar tareas largas que se pueden seguir y cancelar ("avanza 5 metros") y ajustarse sin recompilar ("publica cada medio segundo"). Esta semana completas las formas de comunicación de ROS2, en Python y en C++.

## 🎯 Objetivos de la Semana

- Escribir servers y clientes de servicios en `rclpy` y `rclcpp`, siempre asíncronos
- Escribir un action server con validación, feedback y cancelación, y un action client
- Declarar parámetros con descriptor, cambiarlos en marcha y cargarlos desde YAML
- Hacer hablar nodos de lenguajes distintos a través del mismo `.srv` y `.action`
- Elegir entre topic, servicio, acción y parámetro para cada necesidad

## 📋 Prerrequisitos

- [Semana 02](../week-02-topicos_qos_e_interfaces/README.md) completada: QoS,
  paquete `_interfaces` y tipos propios en ambos lenguajes
- Tu proyecto del dominio de la Semana 02 compilando (esta semana lo amplías)

## 🗂️ Estructura de la Semana

```
week-03-servicios_acciones_y_parametros/
├── README.md                       (este archivo)
├── rubrica-evaluacion.md
├── 0-assets/
│   ├── 01-servicio-request-response.svg
│   ├── 02-deadlock-servicio-sincrono.svg
│   ├── 03-ciclo-de-una-accion.svg
│   └── 04-elegir-mecanismo.svg
├── 1-teoria/
│   ├── 01-servicios-request-response.md
│   ├── 02-servicios-en-python-y-cpp.md
│   ├── 03-acciones-goal-feedback-result.md
│   ├── 04-acciones-en-python-y-cpp.md
│   └── 05-parametros.md
├── 2-practicas/
│   ├── ejercicio-01-servicio_py/
│   ├── ejercicio-02-servicio_cpp/
│   ├── ejercicio-03-accion_compartida/
│   └── ejercicio-04-parametros/
├── 3-proyecto/
│   └── starter/ (proyecto_dominio_interfaces/, proyecto_dominio_py/, proyecto_dominio_cpp/)
├── 4-recursos/
└── 5-glosario/
```

## 📝 Contenidos

### Teoría (3.5 h)

| Archivo | Tema |
|---|---|
| [`01-servicios-request-response.md`](1-teoria/01-servicios-request-response.md) | Servicio frente a topic, anatomía de un `.srv`, `ros2 service` |
| [`02-servicios-en-python-y-cpp.md`](1-teoria/02-servicios-en-python-y-cpp.md) | Server y cliente en ambos lenguajes, `call_async` y el bloqueo de `call()` |
| [`03-acciones-goal-feedback-result.md`](1-teoria/03-acciones-goal-feedback-result.md) | Goal, feedback, result, estados, `.action` y `ros2 action` |
| [`04-acciones-en-python-y-cpp.md`](1-teoria/04-acciones-en-python-y-cpp.md) | Action server en `rclpy`, executor multihilo, action client en `rclcpp` |
| [`05-parametros.md`](1-teoria/05-parametros.md) | Declarar con descriptor, callbacks, YAML, `ros2 param` y cuándo usar cada mecanismo |

### Prácticas (6.5 h)

| Ejercicio | Lenguaje | Qué construye |
|---|---|---|
| 01 | `rclpy` | Server y cliente del servicio `robot/enable` |
| 02 | `rclcpp` | El mismo servicio en C++, cruzado con el cliente y el server de Python |
| 03 | Python + C++ | Acción `MoveDistance`: server Python, cliente C++ |
| 04 | Python + C++ | Nodo `heartbeat` con parámetros y un YAML para los dos lenguajes |

### Proyecto (1.5 h)

`sensor_stub` ofrece un servicio propio para cambiar de modo y un parámetro para su
periodo de publicación, igual en Python y en C++. Ver
[3-proyecto/README.md](3-proyecto/README.md).

## ⏱️ Distribución del Tiempo (12 horas)

| Actividad | Horas |
|---|---|
| Teoría (01-05) | 3.5 |
| Ejercicio 01 (servicio en `rclpy`) | 1.5 |
| Ejercicio 02 (servicio en `rclcpp` y cruce de lenguajes) | 1.5 |
| Ejercicio 03 (acción compartida) | 2.0 |
| Ejercicio 04 (parámetros) | 1.5 |
| Proyecto | 1.5 |
| Autoevaluación (rúbrica) | 0.5 |
| **Total** | **12.0** |

## 🎩 Trucos y atajos

- `ros2 service list -t` y `ros2 action list -t` — nombre y tipo a la vez
- `ros2 interface proto <tipo>` — YAML listo para `ros2 service call` o
  `ros2 action send_goal`
- `ros2 param dump /<nodo> > mi_config.yaml` — guarda la configuración actual
  para reutilizarla con `--params-file`
- Un cliente que "no hace nada": ¿hace spin mientras espera la response?

## 📌 Entregables

- Los cuatro ejercicios de `2-practicas/` con sus tests pasando y sus checklists
  completos
- `3-proyecto/` con los tres paquetes compilando y el servicio renombrado a tu misión
- Respuestas de los Ejercicios 03 y 04 y justificación del rango del periodo en el
  README de tu proyecto

## ✅ Verificación

Desde la raíz de tu workspace (la carpeta que contiene `src/`):

```bash
colcon build --symlink-install
source install/setup.bash
colcon test
colcon test-result --verbose
```

Cada test usa su propio dominio DDS (`ROS_DOMAIN_ID`), así que `colcon test` puede
correr paquetes en paralelo sin que sus nodos se mezclen.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 02](../week-02-topicos_qos_e_interfaces/README.md) | **Semana 03** | Semana 04 (pendiente de publicar) |

← [Volver al inicio del bootcamp](../../README.md)
