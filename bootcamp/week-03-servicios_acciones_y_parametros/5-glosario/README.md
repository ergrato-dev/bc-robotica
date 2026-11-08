# 📖 Glosario — Semana 03

Términos A-Z. El término/API en inglés va entre paréntesis cuando existe en la
documentación oficial.

- **Acción (action)**: comunicación para tareas largas con objetivo, progreso,
  resultado y cancelación. Por dentro son tres servicios y dos topics.
- **Action client (action client)**: nodo que envía goals a una acción y recibe su
  feedback y su result.
- **Action server (action server)**: nodo que acepta o rechaza goals, los ejecuta,
  publica feedback y marca el estado final.
- **Callback group (callback group)**: grupo que decide qué callbacks pueden
  ejecutarse a la vez. `MutuallyExclusive` (por defecto) solo deja una;
  `Reentrant`, varias. Se estudia en la Semana 04.
- **Cancelación (cancel)**: petición del cliente para que el server pare un goal.
  El server decide si la acepta y cuándo para.
- **Cliente (client)**: nodo que envía peticiones a un servicio.
- **Descriptor de parámetro (parameter descriptor)**: metadatos de un parámetro
  (descripción, rango, solo lectura) que ROS2 hace cumplir.
- **Estado final (terminal state)**: cómo acaba un goal: `SUCCEEDED`, `CANCELED` o
  `ABORTED`.
- **Feedback (feedback)**: progreso que un action server publica mientras trabaja.
- **Future (future)**: objeto que se completa más tarde con un resultado, por
  ejemplo la response de un servicio pedida con `call_async`.
- **Goal (goal)**: lo que el cliente pide a una acción.
- **`MultiThreadedExecutor`**: executor que ejecuta callbacks en varios hilos a la vez.
- **Parámetro (parameter)**: valor de configuración de un nodo, con nombre y tipo,
  que se fija al arrancar o se cambia en marcha.
- **Post-set callback (post-set parameters callback)**: función que se llama
  después de aplicar un cambio de parámetros, para usar el valor nuevo.
- **Request (request)**: parte de un servicio que envía el cliente.
- **Response (response)**: parte de un servicio que devuelve el server.
- **Result (result)**: lo que devuelve un action server al terminar un goal.
- **Server (server)**: nodo que atiende las peticiones de un servicio. Debe haber
  uno por nombre de servicio.
- **Servicio (service)**: comunicación petición-respuesta entre un cliente y un
  server.
- **YAML de parámetros (parameters file)**: archivo con los valores de los
  parámetros de uno o más nodos, que se pasa con `--params-file`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Webgrafía](../4-recursos/webgrafia/README.md) | **Glosario** | [Rúbrica](../rubrica-evaluacion.md) |

← [Volver a la Semana 03](../README.md)
