# Rúbrica de Evaluación — Semana 01

Evaluación en tres componentes. Mínimo **70%** en cada uno para aprobar la semana.

## 🧠 Conocimiento (30%)

Cuestionario de autoevaluación. Responde primero sin ver las respuestas.

1. ¿Por qué ROS2 no tiene un "nodo maestro" como ROS1?
2. ¿Cuál es la diferencia entre un topic y un servicio?
3. ¿Qué hace `ROS_DOMAIN_ID` y por qué importa en un aula compartida?
4. ¿Qué contiene `build/`, `install/` y `log/` de un workspace, y por qué no se
   versionan?
5. ¿Qué diferencia hay entre un paquete `ament_python` y uno `ament_cmake`?
6. En `rclcpp`, ¿por qué `spin()` necesita un `shared_ptr<Node>` y no un `Node` por
   valor?
7. ¿Qué le pasaría a tu nodo si llamas dos veces a `rclpy.init()` sin un `shutdown()`
   entre medio?

<details>
<summary>Ver respuestas</summary>

1. Porque usa DDS como transporte, que tiene descubrimiento automático entre nodos sin
   un proceso central que los coordine — si un nodo se cae, el resto sigue funcionando.
2. Un topic es asíncrono (publish/subscribe, sin respuesta esperada); un servicio es
   síncrono (petición → una respuesta concreta).
3. Aísla grupos de nodos DDS en la misma red local — dos procesos con distinto
   `ROS_DOMAIN_ID` no se ven entre sí, aunque estén en la misma WiFi.
4. Son artefactos generados por `colcon build` (compilación, instalación, logs); se
   regeneran siempre desde `src/`, así que versionarlos es ruido y puede causar
   conflictos de merge sin sentido.
5. `ament_python` compila/instala un paquete Python (usa `setup.py`/`setuptools`);
   `ament_cmake` compila un paquete C++ con CMake. `colcon` sabe manejar ambos en el
   mismo workspace.
6. Porque el nodo puede ser referenciado internamente por varios callbacks/threads a la
   vez; un `shared_ptr` gestiona ese ciclo de vida compartido sin que tengas que
   preocuparte de cuándo se destruye.
7. Lanza una excepción — el contexto de ROS2 para ese proceso ya está inicializado y no
   se puede inicializar dos veces sin cerrarlo primero.

</details>

## 💪 Desempeño (40%)

Verificado automáticamente por `colcon test` en cada `starter/`:

| Ejercicio | Verificación |
|---|---|
| 01 (`rclpy`) | `test_publisher_existe`, `test_publica_mensajes`, `test_listener_recibe_mensajes_del_publisher` |
| 02 (`rclcpp`) | `PublisherTest.PublisherExiste`, `PublisherTest.PublicaMensajes`, `ListenerTest.RecibeMensajesDelPublisher` |
| 03 | Sin test automatizado — verificación manual con `ros2 topic hz` (ver checklist del ejercicio) |

```bash
colcon test --packages-select ejercicio01_pubsub_py ejercicio02_pubsub_cpp
colcon test-result --verbose
```

## 📦 Producto (30%)

La capa del proyecto del dominio (`3-proyecto/`):

- [ ] Misión/dominio elegido y documentado en el README del repositorio del estudiante
- [ ] `proyecto_dominio_py` y `proyecto_dominio_cpp` compilan y publican en el mismo
      topic (renombrado a la misión elegida)
- [ ] `colcon test` pasa en ambos paquetes
- [ ] Respuestas del Ejercicio 03 (comparación Python/C++) documentadas en el README
      del proyecto

### Penalizaciones (ver también `.github/copilot-instructions.md`)

| Situación | Penalización |
|---|---|
| No compila/lintea limpio | 0 en Producto |
| `rclpy.init()`/`rclcpp::init()` sin su `shutdown()` correspondiente | -10 |
| Topic sin renombrar a la misión elegida | -10 |
| Sin las respuestas del Ejercicio 03 en el README | -10 |
| Código copiado de otra misión/dominio | 0 en Producto |
