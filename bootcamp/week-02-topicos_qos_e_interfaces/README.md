# Semana 02 — Tópicos, QoS e interfaces

> Un topic no es solo un nombre: es un tipo de mensaje que funciona como contrato y un perfil QoS que dice qué garantías tiene cada dato. Esta semana aprendes a elegir ambos, y a escribir tus propios tipos para Python y C++ a la vez.

## 🎯 Objetivos de la Semana

- Usar tipos de mensaje estándar (`sensor_msgs`, `geometry_msgs`) con su `Header`
- Entender las políticas QoS (history, reliability, durability) y su compatibilidad
- Declarar perfiles QoS explícitos en `rclpy` y en `rclcpp`, incluido el patrón latched
- Crear un paquete `_interfaces` con un `.msg` propio y usarlo desde Python y C++
- Diagnosticar desde la CLI por qué un subscriber no recibe

## 📋 Prerrequisitos

- [Semana 01](../week-01-fundamentos_ros2_y_workspace/README.md) completada: workspace,
  publisher/subscriber en ambos lenguajes y CLI `ros2`
- Tu misión/dominio elegida (el proyecto de esta semana la usa)

## 🗂️ Estructura de la Semana

```
week-02-topicos_qos_e_interfaces/
├── README.md                       (este archivo)
├── rubrica-evaluacion.md
├── 0-assets/
│   ├── 01-qos-reliability-durability.svg
│   ├── 02-compatibilidad-qos.svg
│   └── 03-rosidl-generacion.svg
├── 1-teoria/
│   ├── 01-tipos-de-mensaje-e-interfaces-estandar.md
│   ├── 02-qos-politicas-y-compatibilidad.md
│   ├── 03-qos-en-codigo-y-diagnostico.md
│   ├── 04-interfaces-custom-con-rosidl.md
│   └── 05-usar-interfaces-custom-en-python-y-cpp.md
├── 2-practicas/
│   ├── ejercicio-01-qos_py/
│   ├── ejercicio-02-qos_cpp/
│   ├── ejercicio-03-interfaz_compartida/
│   └── ejercicio-04-diagnosticar_qos_cli/
├── 3-proyecto/
│   └── starter/ (proyecto_dominio_interfaces/, proyecto_dominio_py/, proyecto_dominio_cpp/)
├── 4-recursos/
└── 5-glosario/
```

## 📝 Contenidos

### Teoría (4 h)

| Archivo | Tema |
|---|---|
| [`01-tipos-de-mensaje-e-interfaces-estandar.md`](1-teoria/01-tipos-de-mensaje-e-interfaces-estandar.md) | Tipos primitivos, paquetes estándar, `Header` y unidades SI |
| [`02-qos-politicas-y-compatibilidad.md`](1-teoria/02-qos-politicas-y-compatibilidad.md) | Políticas QoS, presets y compatibilidad pedido-ofrecido |
| [`03-qos-en-codigo-y-diagnostico.md`](1-teoria/03-qos-en-codigo-y-diagnostico.md) | QoS en `rclpy`/`rclcpp`, patrón latched, eventos y CLI |
| [`04-interfaces-custom-con-rosidl.md`](1-teoria/04-interfaces-custom-con-rosidl.md) | Paquete `_interfaces`, sintaxis `.msg`, `rosidl_generate_interfaces` |
| [`05-usar-interfaces-custom-en-python-y-cpp.md`](1-teoria/05-usar-interfaces-custom-en-python-y-cpp.md) | Dependencias, import/include y comunicación entre lenguajes |

### Prácticas (6 h)

| Ejercicio | Lenguaje | Qué construye |
|---|---|---|
| 01 | `rclpy` | Sensor `sensor_data`, estado latched y listener con el QoS de cada uno |
| 02 | `rclcpp` | Los mismos tres nodos en C++, mezclables con los de Python |
| 03 | Python + C++ | Interfaz `SensorReading` compartida: publisher Python, listener C++ |
| 04 | — (CLI) | Ver QoS real, reproducir incompatibilidades, publicar un tipo propio |

### Proyecto (1.5 h)

Tercer paquete `proyecto_dominio_interfaces` con el mensaje propio de tu dominio; los
dos `sensor_stub` lo publican con `Header` y el mismo QoS explícito. Ver
[3-proyecto/README.md](3-proyecto/README.md).

## ⏱️ Distribución del Tiempo (12 horas)

| Actividad | Horas |
|---|---|
| Teoría (01-05) | 4.0 |
| Ejercicios 01 y 02 (QoS en `rclpy` y `rclcpp`) | 3.0 |
| Ejercicio 03 (interfaz compartida) | 2.0 |
| Ejercicio 04 (diagnóstico por CLI) | 1.0 |
| Proyecto | 1.5 |
| Autoevaluación (rúbrica) | 0.5 |
| **Total** | **12.0** |

## 🎩 Trucos y atajos

- "No recibo nada": revisa nombre, tipo y QoS, en ese orden. `ros2 topic info -v`
  responde las tres preguntas a la vez
- `ros2 interface proto <tipo>` — YAML listo para `ros2 topic pub`
- `colcon build --packages-up-to <paquete>` — compila un paquete y sus interfaces
- Tras compilar un paquete **nuevo**, `source install/setup.bash` otra vez en cada
  terminal abierta

## 📌 Entregables

- Los cuatro ejercicios de `2-practicas/`: 01, 02 y 03 con sus tests pasando, 04 con
  su checklist completo
- `3-proyecto/` con los tres paquetes compilando y el tipo renombrado a tu misión
- Justificación del QoS y respuestas de los Ejercicios 03 y 04 en el README de tu
  proyecto

## ✅ Verificación

Desde la raíz de tu workspace (la carpeta que contiene `src/`):

```bash
colcon build --symlink-install
source install/setup.bash
colcon test
colcon test-result --verbose
```

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 01](../week-01-fundamentos_ros2_y_workspace/README.md) | **Semana 02** | Semana 03 (pendiente de publicar) |

← [Volver al inicio del bootcamp](../../README.md)
