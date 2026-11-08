# Ejercicio 01 — Servicio `SetBool` en Python (`rclpy`)

Vas a construir un server que habilita o deshabilita los motores (simulados) del
robot y un cliente que lo llama sin bloquear. Cada paso tiene un test que falla
hasta que lo completas.

**Antes de empezar**: teorías [01](../../1-teoria/01-servicios-request-response.md)
y [02](../../1-teoria/02-servicios-en-python-y-cpp.md) leídas.

## Preparar el workspace

Copia el starter dentro de `src/` de tu workspace (la carpeta que contiene `src/`):

```bash
cp -r <ruta-al-repo>/bootcamp/week-03-servicios_acciones_y_parametros/2-practicas/ejercicio-01-servicio_py/starter \
  src/ejercicio01_servicio_py
```

Estructura:

```
src/ejercicio01_servicio_py/
├── package.xml                # depende de rclpy y std_srvs
├── setup.py
├── setup.cfg
├── resource/ejercicio01_servicio_py
├── ejercicio01_servicio_py/
│   ├── __init__.py
│   ├── enable_server.py       # PASO 1 y 2
│   └── enable_client.py       # PASO 3 y 4
└── test/
    └── test_servicio.py       # tests ya escritos, fallan hasta completar los pasos
```

Todos los pasos se verifican igual, desde la raíz del workspace:

```bash
colcon build --packages-select ejercicio01_servicio_py --symlink-install
source install/setup.bash
colcon test --packages-select ejercicio01_servicio_py
colcon test-result --verbose
```

Antes del primer paso, los tres tests fallan. Es lo esperado.

## Paso 1: Anunciar el servicio

**Por qué**: hasta que el server existe en el grafo, ningún cliente lo encuentra.

**Abre `ejercicio01_servicio_py/enable_server.py`** y descomenta el bloque del
Paso 1.

**Verifica**: pasa `test_server_anuncia_el_servicio`. El test pregunta al grafo
qué servicios hay, lo mismo que `ros2 service list -t`.

## Paso 2: Atender la petición

**Por qué**: el callback es el contrato del server: qué hace con cada `data` y qué
responde. Pedir el estado que ya hay no cambia nada, y el cliente debe saberlo.

**Descomenta el bloque del Paso 2** en `_on_enable`. Fíjate en el `return response`
que ya está al final: sin él, el nodo se cae al recibir la primera petición.

**Verifica**: pasa `test_server_cambia_estado_una_vez`.

Prueba también desde la CLI (terminal 1 con el server, terminal 2 con la llamada;
en cada una, primero `source install/setup.bash`):

```bash
# Terminal 1
ros2 run ejercicio01_servicio_py enable_server

# Terminal 2
ros2 service call /robot/enable std_srvs/srv/SetBool "{data: true}"
# ...
# response:
# std_srvs.srv.SetBool_Response(success=True, message='habilitado')

ros2 service call /robot/enable std_srvs/srv/SetBool "{data: true}"
# ...
# std_srvs.srv.SetBool_Response(success=False, message='ya estaba habilitado')
```

En la terminal 1:

```text
[INFO] [...] [enable_server]: Petición data=True: habilitado
[INFO] [...] [enable_server]: Petición data=True: ya estaba habilitado
```

## Paso 3: Crear el cliente

**Abre `ejercicio01_servicio_py/enable_client.py`** y descomenta el bloque del
Paso 3. Tipo y nombre son los mismos que en el server.

## Paso 4: Llamada asíncrona

**Por qué**: `call_async` envía la petición y devuelve un `Future` sin esperar.
Quien llame a `send()` decide cómo esperar: `main` hace
`spin_until_future_complete`; el test, un executor con los dos nodos.

**Descomenta el bloque del Paso 4** en `send()` y **borra la línea
`raise NotImplementedError`** que queda debajo (lleva el comentario
`# elimina esta línea al completarlo`).

**Verifica**: pasa `test_cliente_recibe_respuesta`. Con esto, los tres tests
pasan.

Con el server de la terminal 1 aún corriendo:

```bash
ros2 run ejercicio01_servicio_py enable_client false
# [INFO] [...] [enable_client]: success=True message='deshabilitado'
```

Y con el server parado (`Ctrl+C` en la terminal 1):

```bash
ros2 run ejercicio01_servicio_py enable_client true
# [ERROR] [...] [enable_client]: el servicio robot/enable no está disponible
```

Tarda unos 2 segundos: es el `timeout_sec` de `wait_for_service`.

## Checklist

- [ ] Los tres tests de `test/test_servicio.py` pasan
- [ ] Llamé al server desde `ros2 service call` y desde `enable_client`
- [ ] Vi el error del cliente cuando el server no existe

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Prácticas](../README.md) | **Ejercicio 01** | [Ejercicio 02](../ejercicio-02-servicio_cpp/README.md) |

← [Volver a la Semana 03](../../README.md)
