# Rúbrica de Evaluación — Semana 03

Evaluación en tres componentes. Mínimo **70%** en cada uno para aprobar la semana.

## 🧠 Conocimiento (30%)

Cuestionario de autoevaluación. Responde primero sin ver las respuestas.

1. ¿Qué dos diferencias principales hay entre un topic y un servicio?
2. ¿Por qué no debes llamar a `client.call()` dentro del callback de un timer?
3. ¿Qué devuelve `call_async` y cuándo se completa?
4. En C++, ¿qué pasa si el `rclcpp::Service` se guarda en una variable local del
   constructor en vez de en un miembro?
5. ¿Qué añade una acción sobre un servicio? Nombra sus tres partes en el orden en
   que van en el `.action`.
6. ¿Cuál es la diferencia entre `CANCELED` y `ABORTED`?
7. ¿Por qué el action server de Python necesita un `MultiThreadedExecutor` y un
   `ReentrantCallbackGroup` para poder cancelar?
8. ¿Qué tres rechazos puede dar `ros2 param set` y qué los provoca?
9. Si pasas `--params-file f.yaml -p period_s:=0.3`, ¿qué valor toma `period_s`?
   ¿Y con el orden al revés?
10. Elige topic, servicio, acción o parámetro: lectura de batería, "empieza a
    cargar", "ve a la estantería 3", velocidad máxima del robot.

<details>
<summary>Ver respuestas</summary>

1. El servicio tiene respuesta y es uno a uno (la response vuelve solo a quien
   pidió); el topic no tiene respuesta y es uno a muchos.
2. Porque `call()` espera la response, y la response solo la puede procesar el
   executor, que está ocupado ejecutando ese mismo callback: el nodo se bloquea
   para siempre.
3. Un `Future`. Se completa cuando llega la response, durante el spin del nodo
   cliente.
4. El `SharedPtr` se destruye al salir del constructor y el servicio desaparece
   del grafo.
5. Feedback (progreso) y cancelación. Partes: goal, result y feedback.
6. `CANCELED`: paró porque el cliente lo pidió. `ABORTED`: paró por un fallo
   propio del server.
7. Porque `_execute` ocupa un hilo durante todo el bucle. Hace falta otro hilo
   (`MultiThreadedExecutor`) y que el grupo permita correr `_on_cancel` a la vez
   (`ReentrantCallbackGroup`).
8. Fuera de rango (`floating_point_range`/`integer_range`), solo lectura
   (`read_only`) y tipo equivocado (por ejemplo `1` para un `double`).
9. `0.3`: gana el último de la línea de comandos. Al revés, el valor del YAML.
10. Topic, servicio, acción y parámetro.

</details>

## 💪 Desempeño (40%)

Verificado automáticamente por `colcon test` en cada `starter/`:

| Ejercicio | Verificación |
|---|---|
| 01 (`rclpy`) | `test_server_anuncia_el_servicio`, `test_server_cambia_estado_una_vez`, `test_cliente_recibe_respuesta` |
| 02 (`rclcpp`) | `EnableServerTest.AnunciaElServicio`, `EnableServerTest.CambiaEstadoUnaVez`, `EnableClientTest.RecibeRespuesta` |
| 03 (Python + C++) | `test_server_anuncia_la_accion`, `test_rechaza_distancia_invalida`, `test_completa_con_feedback`, `test_se_puede_cancelar`, `MoveClientTest.RecibeFeedbackYResultado`, `MoveClientTest.RechazoTerminaSinResultado` |
| 04 (Python + C++) | `test_declara_parametros_con_descriptor`, `test_rechaza_valores_invalidos`, `test_publica_latido_con_nombre`, `test_cambio_de_periodo_en_marcha` y sus cuatro equivalentes `HeartbeatTest.*` |

```bash
colcon test --packages-select ejercicio01_servicio_py ejercicio02_servicio_cpp \
  ejercicio03_accion_py ejercicio03_accion_cpp \
  ejercicio04_parametros_py ejercicio04_parametros_cpp
colcon test-result --verbose
```

## 📦 Producto (30%)

La capa del proyecto del dominio (`3-proyecto/`):

- [ ] Servicio propio renombrado a la misión en `proyecto_dominio_interfaces`
- [ ] `sensor_stub` Python y C++ ofrecen el mismo servicio: aceptan los modos de tu
      tipo y rechazan el resto con un `message`
- [ ] Parámetro `publish_period_s` con descripción y rango, aplicado en marcha
- [ ] `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
- [ ] Justificación del rango y respuestas de los Ejercicios 03 y 04 en el README
      del proyecto

### Penalizaciones (ver también `.github/copilot-instructions.md`)

| Situación | Penalización |
|---|---|
| No compila/lintea limpio | 0 en Producto |
| `client.call()` síncrono dentro de un callback | -10 |
| Rechazo sin `message` o modos como números sueltos | -10 |
| Parámetro sin `description` o sin rango cuando tiene límites físicos | -10 |
| `SetMode` sin renombrar | -10 |
| Código copiado de otra misión/dominio | 0 en Producto |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica** | Semana 04 (pendiente de publicar) |

← [Volver a la Semana 03](README.md)
