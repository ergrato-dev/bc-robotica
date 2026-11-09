# Rúbrica de Evaluación — Semana 06

Evaluación en tres componentes. Mínimo **70%** en cada uno para aprobar la semana.

## 🧠 Conocimiento (30%)

Cuestionario de autoevaluación. Responde primero sin ver las respuestas.

1. ¿Qué devuelve `generate_launch_description()` y qué hace `ros2 launch` con ello?
2. Un launch file declara `radius_m` y lo pasa a un nodo que lo declara como
   `double`. ¿Con qué valor en la terminal falla, y cómo se evita?
3. ¿Por qué en un launch file no puedes hacer `float(LaunchConfiguration("radius_m"))`?
4. ¿Por qué el manejador `OnStateTransition` se registra antes de emitir el
   evento `configure`? ¿Qué pasa con el nodo si `on_configure` falla?
5. ¿Qué es un árbol TF y por qué un marco no puede tener dos padres?
6. ¿Qué va en `/tf` y qué en `/tf_static`? ¿Por qué `/tf_static` es transient local?
7. Escribe el cuaternión `(x, y, z, w)` de un robot que mira hacia +y. ¿Qué pasa
   si escribes `z` y olvidas `w`?
8. `lookupTransform("base_link", "dock", ...)` devuelve una traslación `(0, -2, 0)`.
   ¿Dónde está el dock respecto al robot?
9. ¿Qué tipo de joint lleva una rueda, un sensor atornillado y la articulación de
   un brazo? ¿Cuál de ellos publica `robot_state_publisher` en `/tf_static`?
10. ¿Para qué sirve `joint_state_publisher` en un robot sin motores?

<details>
<summary>Ver respuestas</summary>

1. Una `LaunchDescription`: la lista de acciones de launch. `ros2 launch` las
   ejecuta en orden; cada `Node` se convierte en un proceso, y con `Ctrl+C` los
   para todos con SIGINT.
2. Con un entero, `radius_m:=2`: launch lee el texto como YAML y el parámetro
   llega como `INTEGER`. Se evita con
   `ParameterValue(LaunchConfiguration("radius_m"), value_type=float)`.
3. Porque `LaunchConfiguration` es una sustitución: un valor que launch resuelve
   al ejecutar la acción que la usa. Mientras se construye la descripción, aún no
   tiene valor.
4. Para no perderse la llegada a `inactive`: si se registrara después, la
   transición podría ocurrir antes. Si `on_configure` falla, el nodo se queda en
   `unconfigured`, nunca llega a `inactive` y nunca se activa.
5. El conjunto de transformaciones entre marcos, donde cada marco cuelga de un
   padre. Con dos padres habría dos caminos entre algunos marcos, con resultados
   distintos, y las consultas fallarían según qué mensaje llegó último.
6. En `/tf`, lo que cambia (el robot respecto a `odom`, una rueda); en
   `/tf_static`, lo fijo (un sensor en el chasis). Transient local hace que un nodo
   que arranca tarde reciba las estáticas publicadas una sola vez al principio.
7. Yaw = π/2: `(0, 0, 0.707, 0.707)`. Si olvidas `w`, queda `w = 1`, el
   cuaternión no mide 1 y TF2 descarta la transformación con
   `TF_DENORMALIZED_QUATERNION`.
8. A 2 m a su derecha: `x` es delante, `y` positivo es la izquierda (REP 103),
   así que `y = -2` es la derecha.
9. Rueda: `continuous`. Sensor: `fixed`. Brazo: `revolute` (con límites). Solo
   los `fixed` van a `/tf_static`; los móviles, a `/tf` con cada `/joint_states`.
10. `robot_state_publisher` solo publica un joint móvil cuando sabe su ángulo, y
    ese ángulo llega por `/joint_states`. Sin motores, `joint_state_publisher`
    publica 0 para cada joint móvil y el árbol queda completo.

</details>

## 💪 Desempeño (40%)

Verificado automáticamente por `colcon test` en cada `starter/`:

| Ejercicio | Verificación |
|---|---|
| 01 (`rclpy`) | `test_geometry` (10), `test_patrol_launch` |
| 02 (`rclcpp`) | `DockReading.*` (4), `TfBuffer.*` (3) |
| 03 (URDF/xacro) | `test_urdf` (5), `test_display_launch` |

Además, haber roto el código a propósito y visto fallar el test correspondiente
(checklist de cada ejercicio), y el checklist de paridad del Ejercicio 02 relleno.

```bash
colcon test --packages-select ejercicio01_tf_broadcaster_py ejercicio02_tf_listener_cpp \
  ejercicio03_urdf_xacro
colcon test-result --verbose
```

## 📦 Producto (30%)

La capa del proyecto del dominio (`3-proyecto/`):

- [ ] `robot.urdf.xacro` describe tu robot: nombre, medidas, sensor propio y
      ruedas con macro; `test_description.py` pasa
- [ ] La capa C++ publica `odom → base_link` con el mismo `stamp` que el estado
- [ ] `test_bringup_launch.py` pasa con `impl:=py` y con `impl:=cpp`
- [ ] `colcon test` pasa en `proyecto_dominio_py` y `proyecto_dominio_cpp`
- [ ] Respuestas de los tres ejercicios y checklist de paridad en el README del proyecto

Criterios observables más allá de los tests:

| Criterio | Bien | Mal |
|---|---|---|
| Modelo | Medidas en propiedades xacro; inercias calculadas con fórmula | Números repetidos; inercias inventadas |
| Sensor | Posición justificada en el README con la tarea de la misión | El `sensor_link` del starter sin mover |
| Launch | Argumentos con `description` y `choices` donde aplica | Valores fijos que alguien querrá cambiar |

### Penalizaciones (ver también `.github/copilot-instructions.md`)

| Situación | Penalización |
|---|---|
| No compila/lintea limpio | 0 en Producto |
| `check_urdf` rechaza el modelo | 0 en Producto |
| Algo fijo publicado en `/tf` en vez de `/tf_static` | -10 |
| Capa C++ sin `odom → base_link` (las capas dejan de ser intercambiables) | -15 |
| Transiciones de lifecycle tecleadas a mano en vez de en el bringup | -10 |
| Código copiado de otra misión/dominio | 0 en Producto |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica** | Semana 07 (pendiente de publicar) |

← [Volver a la Semana 06](README.md)
