# Semana 04 — Executors, composición y lifecycle

> Ya sabes hablar con topics, servicios, acciones y parámetros. Ahora toca decidir **cómo se ejecuta** todo eso: qué callbacks pueden correr a la vez, cuántos nodos caben en un proceso y en qué orden arranca un robot. Son las piezas sobre las que están construidos Nav2 y MoveIt2.

## 🎯 Objetivos de la Semana

- Explicar qué hace un executor y elegir entre uno de un hilo y uno multihilo
- Separar callbacks en callback groups para que uno lento no bloquee a los demás
- Convertir un nodo `rclcpp` en componente y cargarlo en un container
- Justificar por escrito el executor de un nodo o container
- Escribir nodos lifecycle en `rclpy` y `rclcpp` y controlarlos con `ros2 lifecycle`

## 📋 Prerrequisitos

- [Semana 03](../week-03-servicios_acciones_y_parametros/README.md) completada:
  servicios, acciones y parámetros en los dos lenguajes
- Tu proyecto del dominio de la Semana 03 compilando (esta semana lo amplías)

## 🗂️ Estructura de la Semana

```
week-04-executors_composicion_y_lifecycle/
├── README.md                       (este archivo)
├── rubrica-evaluacion.md
├── 0-assets/
│   ├── 01-bucle-del-executor.svg
│   ├── 02-un-hilo-frente-a-varios.svg
│   ├── 03-procesos-frente-a-container.svg
│   └── 04-maquina-de-estados-lifecycle.svg
├── 1-teoria/
│   ├── 01-executors-y-spin.md
│   ├── 02-callback-groups.md
│   ├── 03-composicion-y-componentes.md
│   └── 04-nodos-lifecycle.md
├── 2-practicas/
│   ├── ejercicio-01-callback_groups_py/
│   ├── ejercicio-02-componente_cpp/
│   ├── ejercicio-03-lifecycle_py/
│   └── ejercicio-04-lifecycle_cpp/
├── 3-proyecto/
│   └── starter/ (proyecto_dominio_interfaces/, proyecto_dominio_py/, proyecto_dominio_cpp/)
├── 4-recursos/
└── 5-glosario/
```

## 📝 Contenidos

### Teoría (3.5 h)

| Archivo | Tema |
|---|---|
| [`01-executors-y-spin.md`](1-teoria/01-executors-y-spin.md) | Qué hace `spin()`, executors de uno y varios hilos, variantes de `spin` |
| [`02-callback-groups.md`](1-teoria/02-callback-groups.md) | `MutuallyExclusive` y `Reentrant`, grupo por defecto, `call()` con grupo propio, datos compartidos |
| [`03-composicion-y-componentes.md`](1-teoria/03-composicion-y-componentes.md) | Componentes `rclcpp`, containers, `ros2 component`, intra-process y qué hay en Python |
| [`04-nodos-lifecycle.md`](1-teoria/04-nodos-lifecycle.md) | Estados, transiciones, publisher lifecycle, `ros2 lifecycle` |

### Prácticas (6.5 h)

| Ejercicio | Lenguaje | Qué construye |
|---|---|---|
| 01 | `rclpy` | Nodo `monitor`: callback groups y executor multihilo |
| 02 | `rclcpp` | El mismo `monitor` como componente, en dos containers |
| 03 | `rclpy` | Driver simulado `range_driver` como nodo lifecycle |
| 04 | `rclcpp` | El mismo driver lifecycle en C++, también como componente |

### Proyecto (1.5 h)

`sensor_stub` pasa a ser un nodo lifecycle en Python y en C++, y la capa C++ se
registra como componente. Ver [3-proyecto/README.md](3-proyecto/README.md).

## ⏱️ Distribución del Tiempo (12 horas)

| Actividad | Horas |
|---|---|
| Teoría (01-04) | 3.5 |
| Ejercicio 01 (callback groups en `rclpy`) | 1.5 |
| Ejercicio 02 (componente en `rclcpp` y justificación del executor) | 2.0 |
| Ejercicio 03 (lifecycle en `rclpy`) | 1.5 |
| Ejercicio 04 (lifecycle en `rclcpp`) | 1.5 |
| Proyecto | 1.5 |
| Autoevaluación (rúbrica) | 0.5 |
| **Total** | **12.0** |

## 🎩 Trucos y atajos

- `ros2 component types` — todos los componentes registrados en tu workspace
- `ros2 lifecycle nodes` — qué nodos del grafo son lifecycle
- `ros2 lifecycle list /<nodo>` — qué transiciones admite ahora mismo
- ¿Un timer que "se para" a ratos? Busca un callback lento en su mismo grupo
- ¿Un nodo lifecycle activo y mudo? Busca la llamada a la base en `on_activate`

## 📌 Entregables

- Los cuatro ejercicios de `2-practicas/` con sus tests pasando y sus checklists
  completos
- `3-proyecto/` con los tres paquetes compilando y las dos capas como nodos
  lifecycle
- Justificación del executor y respuestas de los Ejercicios 01, 03 y 04 en el
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
| [Semana 03](../week-03-servicios_acciones_y_parametros/README.md) | **Semana 04** | Semana 05 (pendiente de publicar) |

← [Volver al inicio del bootcamp](../../README.md)
