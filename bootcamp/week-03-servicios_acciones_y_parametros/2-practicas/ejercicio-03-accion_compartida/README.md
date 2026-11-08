# Ejercicio 03 — Acción compartida: server Python, cliente C++

Una acción `MoveDistance` ("avanza N metros") definida una sola vez en un paquete
de interfaces. El server, en Python, simula el avance con feedback y admite
cancelación. El cliente, en C++, envía el goal y sigue el progreso.

**Antes de empezar**: teorías [03](../../1-teoria/03-acciones-goal-feedback-result.md)
y [04](../../1-teoria/04-acciones-en-python-y-cpp.md) leídas.

## Preparar el workspace

Tres paquetes. El de interfaces ya viene completo: escribir un paquete
`_interfaces` lo practicaste en la Semana 02.

```bash
cp -r <ruta-al-repo>/bootcamp/week-03-servicios_acciones_y_parametros/2-practicas/ejercicio-03-accion_compartida/starter/* \
  src/
```

```
src/
├── ejercicio03_interfaces/          # completo: action/MoveDistance.action
├── ejercicio03_accion_py/
│   ├── ejercicio03_accion_py/move_server.py   # PASOS 1, 2 y 3
│   └── test/test_move_server.py
└── ejercicio03_accion_cpp/
    ├── include/ejercicio03_accion_cpp/move_client.hpp   # PASOS 4 y 5
    ├── src/move_client_main.cpp
    └── test/test_move_client.cpp    # usa un server falso en C++
```

Lee primero la acción:

```bash
colcon build --packages-select ejercicio03_interfaces
source install/setup.bash
ros2 interface show ejercicio03_interfaces/action/MoveDistance
```

Sin comentarios ni líneas vacías, lo importante es:

```text
float64 distance_m
---
float64 traveled_m
---
float64 remaining_m
```

Verificación de los pasos de Python:

```bash
colcon build --packages-up-to ejercicio03_accion_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio03_accion_py
colcon test-result --verbose
```

Y de los de C++, igual con `ejercicio03_accion_cpp`.

## Paso 1: Crear el server y validar el goal

**Abre `ejercicio03_accion_py/move_server.py`**. Descomenta el bloque del
**Paso 1 (parte A)** en `__init__` y el del **Paso 1 (parte B)** en `_on_goal`.

**Por qué**: rechazar un goal imposible (distancia negativa o mayor de 10 m) en
`_on_goal` le avisa al cliente antes de empezar.

**Verifica**: pasan `test_server_anuncia_la_accion` y
`test_rechaza_distancia_invalida`.

## Paso 2: Ejecutar con feedback

**Descomenta el bloque del Paso 2** en `_execute`. Lee el bucle: cada vuelta
mira si piden cancelar, espera `PERIOD_S`, avanza y publica cuánto falta. Al
salir del bucle marca `succeed()`.

**Verifica**: pasa `test_completa_con_feedback`.

```bash
# Terminal 1
ros2 run ejercicio03_accion_py move_server

# Terminal 2
ros2 action send_goal --feedback /robot/move_distance \
  ejercicio03_interfaces/action/MoveDistance "{distance_m: 0.2}"
# ...
# Feedback:
#     remaining_m: 0.15000000000000002
# ...
# Result:
#     traveled_m: 0.2
#
# Goal finished with status: SUCCEEDED
```

## Paso 3: Aceptar la cancelación

**Por qué**: el bucle del Paso 2 ya comprueba `is_cancel_requested`, pero con
`_on_cancel` devolviendo `REJECT` nunca se activa.

**Descomenta el bloque del Paso 3** y borra la línea `return CancelResponse.REJECT`
marcada con `# elimina esta línea al completar el Paso 3`.

**Verifica**: pasa `test_se_puede_cancelar`. Los cuatro tests de Python pasan.

Pruébalo: reinicia el server, envía `{distance_m: 5.0}` sin `--feedback` y pulsa
`Ctrl+C` a los dos segundos.

```text
Goal accepted with ID: ...

^CCanceling goal...
```

En la terminal del server: `[INFO] [...] [move_server]: Cancelado a 1.00 m` (o
la distancia a la que llegó). Si aparece `Executor is already spinning` en la
terminal de la CLI, ignóralo: es un aviso de la herramienta.

## Paso 4: Crear el action client en C++

**Abre `include/ejercicio03_accion_cpp/move_client.hpp`** y descomenta el bloque
del Paso 4.

## Paso 5: Enviar el goal con sus callbacks

**Descomenta el bloque del Paso 5** en `send()` y borra las dos líneas marcadas
con `// elimina esta línea al completar el Paso 5`.

**Verifica**: pasan `MoveClientTest.RecibeFeedbackYResultado` y
`MoveClientTest.RechazoTerminaSinResultado`.

Y entre lenguajes, con el server Python en la terminal 1:

```bash
ros2 run ejercicio03_accion_cpp move_client 0.15
# [INFO] [...] [move_client]: Faltan 0.10 m
# [INFO] [...] [move_client]: Faltan 0.05 m
# [INFO] [...] [move_client]: Faltan 0.00 m
# [INFO] [...] [move_client]: Terminado: 0.15 m recorridos

ros2 run ejercicio03_accion_cpp move_client -1
# [WARN] [...] [move_client]: Goal rechazado
```

## Paso 6: Experimento con el executor

Comprueba con tus propios ojos la teoría 04, sección 2.1. En `main()` de
`move_server.py`, sustituye las cuatro líneas del executor por
`rclpy.spin(node)`, recompila y repite la cancelación del Paso 3.

✅ Verificación: `Canceling goal...` aparece en la CLI, pero el server sigue
hasta `Completado: 5.00 m`. Anota en tu informe por qué, y deja `main()` como
estaba.

## Preguntas para tu informe (respóndelas en el README de tu `3-proyecto/`)

1. ¿Por qué el test de C++ usa un server falso en C++ en vez del server Python?
2. En el Paso 6, ¿qué hilo estaba ocupado cuando llegó la petición de cancelar?
3. Si el robot real tarda 2 s en frenar, ¿en qué callback del server lo
   tendrías en cuenta y qué estado final marcarías?

## Checklist

- [ ] Los cuatro tests de Python y los dos de C++ pasan
- [ ] Envié, seguí y cancelé un goal desde la CLI
- [ ] El cliente C++ completó un goal contra el server Python
- [ ] Hice el experimento del Paso 6 y dejé el server como estaba

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02](../ejercicio-02-servicio_cpp/README.md) | **Ejercicio 03** | [Ejercicio 04](../ejercicio-04-parametros/README.md) |

← [Volver a la Semana 03](../../README.md)
