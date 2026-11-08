# Rúbrica de Evaluación — Semana 04

Evaluación en tres componentes. Mínimo **70%** en cada uno para aprobar la semana.

## 🧠 Conocimiento (30%)

Cuestionario de autoevaluación. Responde primero sin ver las respuestas.

1. ¿Qué hace `spin()` en cada vuelta de su bucle?
2. Un nodo tiene un timer y un servicio lento. Cambias a `MultiThreadedExecutor`
   y el timer sigue bloqueado. ¿Por qué?
3. ¿Qué diferencia hay entre `MutuallyExclusiveCallbackGroup` y
   `ReentrantCallbackGroup`? Da un caso para cada uno.
4. ¿Cómo se puede usar `client.call()` dentro de un callback sin bloquear el nodo?
5. ¿Qué tres cambios convierten un nodo `rclcpp` en componente?
6. ¿Qué gana un componente cargado en un container frente a un `ros2 run`? ¿Y
   qué ofrece Python en su lugar?
7. ¿Cuándo elegirías `component_container_mt` en lugar de `component_container`?
8. Nombra los cuatro estados primarios de un nodo lifecycle y la transición que
   lleva de cada uno al siguiente.
9. Un nodo lifecycle está en `active` pero no publica nada. ¿Cuál es la causa más
   probable?
10. ¿Qué pasa si `on_configure` devuelve `FAILURE`? ¿Por qué es mejor que lanzar
    una excepción?

<details>
<summary>Ver respuestas</summary>

1. Espera en el wait set a que algo esté listo (timer, mensaje, request...),
   ejecuta los callbacks listos y vuelve a esperar.
2. Porque los dos están en el grupo por defecto del nodo, que es
   `MutuallyExclusive`: aunque haya hilos libres, solo corre uno de los dos a la vez.
3. `MutuallyExclusive`: como mucho un callback del grupo a la vez (callbacks que
   comparten datos sin protección). `Reentrant`: cualquier número, incluso el
   mismo callback dos veces (`execute` y `cancel` de un action server).
4. Poniendo el cliente en su propio callback group y usando un executor
   multihilo: otro hilo atiende la response.
5. Constructor con `const rclcpp::NodeOptions&`, la macro
   `RCLCPP_COMPONENTS_REGISTER_NODE` y compilar como biblioteca con
   `rclcpp_components_register_node` en CMake.
6. Un solo proceso y executor para varios nodos, y comunicación intra-process
   sin serializar ni pasar por DDS. Python no tiene componentes: solo puede meter
   varios nodos en el mismo executor dentro de un `main`.
7. Cuando algún componente tiene callbacks lentos que no deben bloquear a otros
   y los ha separado en grupos.
8. `unconfigured` → `configure` → `inactive` → `activate` → `active`; `shutdown`
   lleva a `finalized` desde cualquiera de los tres.
9. `on_activate` no llama a la implementación base (`super().on_activate` /
   `LifecycleNode::on_activate`), así que el publisher lifecycle sigue inactivo.
10. El nodo se queda en `unconfigured` y quien pidió la transición recibe el
    fallo. Una excepción no le dice a quien la pidió por qué falló.

</details>

## 💪 Desempeño (40%)

Verificado automáticamente por `colcon test` en cada `starter/`:

| Ejercicio | Verificación |
|---|---|
| 01 (`rclpy`) | `test_usa_grupos_propios`, `test_timer_sigue_durante_la_comprobacion` |
| 02 (`rclcpp`) | `MonitorTest.UsaGruposPropios`, `MonitorTest.TimerSigueDuranteLaComprobacion`, `MonitorTest.SeRegistraComoComponente` |
| 03 (`rclpy`) | `test_configure_crea_el_publisher`, `test_configure_falla_con_rate_invalido`, `test_publica_solo_en_active`, `test_cleanup_libera_el_publisher` |
| 04 (`rclcpp`) | Los mismos cuatro como `RangeDriverTest.*` |

```bash
colcon test --packages-select ejercicio01_callback_groups_py ejercicio02_componente_cpp \
  ejercicio03_lifecycle_py ejercicio04_lifecycle_cpp
colcon test-result --verbose
```

## 📦 Producto (30%)

La capa del proyecto del dominio (`3-proyecto/`):

- [ ] `sensor_stub` Python y C++ son nodos lifecycle: arrancan en `unconfigured`
      y solo publican en `active`
- [ ] Cada recurso se crea y se destruye en transiciones opuestas
- [ ] La capa C++ se registra como componente y funciona cargada en un container
- [ ] `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
- [ ] Justificación del executor de cada capa, fila de tu misión y respuestas de
      los Ejercicios 01, 03 y 04 en el README del proyecto

### Penalizaciones (ver también `.github/copilot-instructions.md`)

| Situación | Penalización |
|---|---|
| No compila/lintea limpio | 0 en Producto |
| `client.call()` dentro de un callback sin grupo propio | -10 |
| Publicar o crear timers en el constructor de un nodo lifecycle | -10 |
| `on_activate` sin llamar a la implementación base | -10 |
| Justificación del executor sin callbacks concretos | -10 |
| Código copiado de otra misión/dominio | 0 en Producto |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica** | Semana 05 (pendiente de publicar) |

← [Volver a la Semana 04](README.md)
