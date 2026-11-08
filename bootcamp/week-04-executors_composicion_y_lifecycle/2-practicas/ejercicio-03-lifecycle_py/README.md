# Ejercicio 03 — Driver lifecycle en Python (`rclpy`)

`range_driver` simula el driver de un sensor de distancia: publica la distancia
al obstáculo de delante en `robot/range_m` (`std_msgs/msg/Float64`). Como nodo
lifecycle, no hace nada hasta que lo configuras y lo activas.

**Antes de empezar**: teoría [04](../../1-teoria/04-nodos-lifecycle.md) leída.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-04-executors_composicion_y_lifecycle/2-practicas/ejercicio-03-lifecycle_py/starter \
  src/ejercicio03_lifecycle_py
```

Estructura:

```
src/ejercicio03_lifecycle_py/
├── package.xml                         # depende de rclpy, lifecycle_msgs, std_msgs
├── setup.py
├── setup.cfg
├── resource/ejercicio03_lifecycle_py
├── ejercicio03_lifecycle_py/
│   ├── __init__.py
│   └── range_driver.py                 # PASOS 1, 2 y 3
└── test/
    └── test_range_driver.py            # tests ya escritos
```

Verificación:

```bash
colcon build --packages-select ejercicio03_lifecycle_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio03_lifecycle_py
colcon test-result --verbose
```

Los tests llaman a las transiciones directamente: `node.trigger_configure()`,
`node.trigger_activate()`... Es lo mismo que hace `ros2 lifecycle set`, sin pasar
por un servicio. Antes del primer paso, los cuatro fallan.

## Paso 1: `on_configure`

**Abre `ejercicio03_lifecycle_py/range_driver.py`** y descomenta el bloque del
Paso 1. Valida `rate_hz`: si no es positivo, devuelve `FAILURE` y el nodo se
queda en `unconfigured`. Si sirve, crea el publisher lifecycle.

**Por qué**: un `rate_hz` de 0 provocaría una división por cero en
`on_activate`. Mejor detectarlo al configurar, cuando el nodo aún no ha
reservado nada.

**Verifica**: pasan `test_configure_crea_el_publisher` y
`test_configure_falla_con_rate_invalido`.

## Paso 2: `on_activate` y `on_deactivate`

**Descomenta los dos bloques del Paso 2** y borra las dos líneas
`return TransitionCallbackReturn.SUCCESS` marcadas con
`# elimina en el Paso 2`.

Fíjate en el `return super().on_activate(state)`: es lo que activa el publisher.

**Verifica**: pasa `test_publica_solo_en_active`.

## Paso 3: `on_cleanup`

**Descomenta el bloque del Paso 3**. `on_shutdown` ya llama a `on_cleanup`: el
nodo puede apagarse desde cualquier estado y debe soltar lo mismo.

**Verifica**: pasa `test_cleanup_libera_el_publisher`. Los cuatro tests pasan.

## Paso 4: Recorrer los estados desde la CLI

En cada terminal, primero `source install/setup.bash`.

```bash
# Terminal 1
ros2 run ejercicio03_lifecycle_py range_driver
```

```bash
# Terminal 2
ros2 lifecycle get /range_driver
# unconfigured [1]
ros2 topic list | grep range
# /range_driver/transition_event
```

Todavía no existe `/robot/range_m`: el publisher se crea al configurar.

```bash
ros2 lifecycle set /range_driver configure
# Transitioning successful
timeout 3 ros2 topic echo /robot/range_m --once
# (sin salida: inactive no publica)
ros2 lifecycle set /range_driver activate
# Transitioning successful
ros2 topic hz /robot/range_m
# average rate: 5.000
# ...
```

`Ctrl+C` para cortar `ros2 topic hz`. En la terminal 1:

```text
[INFO] [...] [range_driver]: Configurado a 5.0 Hz
[INFO] [...] [range_driver]: Activo
```

Ahora de vuelta hasta el final:

```bash
ros2 lifecycle set /range_driver deactivate
# Transitioning successful
ros2 lifecycle set /range_driver cleanup
# Transitioning successful
ros2 lifecycle set /range_driver shutdown
# Transitioning successful
ros2 lifecycle get /range_driver
# finalized [4]
```

✅ Verificación: en la terminal 1 aparecen `Inactivo` y dos veces `Recursos
liberados` (una de `cleanup` y otra de `shutdown`). El proceso sigue vivo en
`finalized`; ciérralo con `Ctrl+C`.

## Paso 5: Una configuración que falla

```bash
# Terminal 1
ros2 run ejercicio03_lifecycle_py range_driver --ros-args -p rate_hz:=0.0
```

```bash
# Terminal 2
ros2 lifecycle set /range_driver configure
# Transitioning failed
ros2 lifecycle get /range_driver
# unconfigured [1]
```

En la terminal 1: `[ERROR] [...] [range_driver]: rate_hz debe ser > 0, llegó 0.0`.
El nodo sigue vivo y sin recursos a medias.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué `rate_hz` se declara en `__init__` y no en `on_configure`?
2. ¿Qué pasaría tras dos ciclos `activate` → `deactivate` si `on_deactivate` no
   destruyera el timer?
3. Si el sensor real se desconecta estando `active`, ¿a qué estado llevarías el
   nodo y quién debería pedirlo?

## Checklist

- [ ] Los cuatro tests de `test/test_range_driver.py` pasan
- [ ] Llevé el nodo de `unconfigured` a `finalized` con `ros2 lifecycle`
- [ ] Comprobé que `inactive` no publica y `active` publica a 5 Hz
- [ ] Vi fallar `configure` con `rate_hz:=0.0`

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02](../ejercicio-02-componente_cpp/README.md) | **Ejercicio 03** | [Ejercicio 04](../ejercicio-04-lifecycle_cpp/README.md) |

← [Volver a la Semana 04](../../README.md)
