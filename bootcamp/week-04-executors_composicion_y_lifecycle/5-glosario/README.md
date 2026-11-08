# 📖 Glosario — Semana 04

Términos A-Z. El término/API en inglés va entre paréntesis cuando existe en la
documentación oficial.

- **Callback group (callback group)**: etiqueta que decide qué callbacks pueden
  ejecutarse a la vez. Cada nodo tiene uno por defecto, `MutuallyExclusive`.
- **Componente (component)**: nodo `rclcpp` compilado como biblioteca compartida
  y registrado con `RCLCPP_COMPONENTS_REGISTER_NODE` para que un container lo
  cargue en marcha.
- **Composición (composition)**: ejecutar varios nodos en un mismo proceso.
- **Container (component container)**: proceso que carga componentes y los
  ejecuta con su executor. `component_container` usa un hilo;
  `component_container_mt`, varios.
- **Executor (executor)**: pieza que espera eventos y ejecuta los callbacks de
  uno o varios nodos. `spin()` es su bucle.
- **Intra-process (intra-process communication)**: comunicación entre nodos del
  mismo proceso sin serializar ni pasar por DDS.
- **Lifecycle manager (lifecycle manager)**: nodo que pide las transiciones de
  otros nodos lifecycle en orden. Nav2 trae `nav2_lifecycle_manager`.
- **Lifecycle publisher (lifecycle publisher)**: publisher de un nodo lifecycle;
  solo entrega mensajes en `active`.
- **`MultiThreadedExecutor`**: executor con varios hilos; por defecto, uno por
  núcleo de CPU.
- **`MutuallyExclusiveCallbackGroup`**: grupo en el que como mucho corre un
  callback a la vez.
- **Nodo lifecycle (managed node / lifecycle node)**: nodo con la máquina de
  estados estándar `unconfigured`, `inactive`, `active`, `finalized`.
- **`NodeOptions`**: opciones con las que se construye un nodo (parámetros,
  intra-process...). Un componente las recibe del container.
- **`ReentrantCallbackGroup`**: grupo sin límite: sus callbacks, incluso el mismo
  dos veces, pueden correr a la vez.
- **Serializar (serialize)**: convertir un mensaje en bytes para enviarlo por la
  red o entre procesos.
- **`SingleThreadedExecutor`**: executor de un hilo; el que usa `rclpy.spin`.
- **Transición (transition)**: paso entre estados de un nodo lifecycle
  (`configure`, `activate`, `deactivate`, `cleanup`, `shutdown`). Su callback
  devuelve `SUCCESS`, `FAILURE` o `ERROR`.
- **Wait set (wait set)**: conjunto de timers, subscriptions, servicios y
  clientes sobre el que el executor espera a que haya trabajo.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Webgrafía](../4-recursos/webgrafia/README.md) | **Glosario** | [Rúbrica](../rubrica-evaluacion.md) |

← [Volver a la Semana 04](../README.md)
