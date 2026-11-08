# Ejercicio 02 — El mismo servicio en C++ (`rclcpp`)

Mismo servicio, `robot/enable` de tipo `std_srvs/srv/SetBool`, y mismas
respuestas que en el Ejercicio 01, ahora en C++. Al final cruzas los lenguajes:
cliente C++ contra server Python y al revés.

**Antes de empezar**: Ejercicio 01 completado y teoría
[02](../../1-teoria/02-servicios-en-python-y-cpp.md), secciones 4 a 6.

## Preparar el workspace

```bash
cp -r <ruta-al-repo>/bootcamp/week-03-servicios_acciones_y_parametros/2-practicas/ejercicio-02-servicio_cpp/starter \
  src/ejercicio02_servicio_cpp
```

Estructura:

```
src/ejercicio02_servicio_cpp/
├── package.xml
├── CMakeLists.txt                       # un ejecutable por nodo (foreach)
├── include/ejercicio02_servicio_cpp/
│   ├── enable_server.hpp                # PASO 1 y 2
│   └── enable_client.hpp                # PASO 3 y 4
├── src/
│   ├── enable_server_main.cpp           # solo main(); no se toca
│   └── enable_client_main.cpp           # lee true/false de la línea de comandos
└── test/
    └── test_servicio.cpp                # gtest ya escrito
```

Los nodos viven en los headers para que el test los cree sin arrancar
ejecutables. Verificación de cada paso:

```bash
colcon build --packages-select ejercicio02_servicio_cpp
source install/setup.bash
colcon test --packages-select ejercicio02_servicio_cpp
colcon test-result --verbose
```

## Paso 1: Anunciar el servicio

**Abre `include/ejercicio02_servicio_cpp/enable_server.hpp`** y descomenta el
bloque del Paso 1. `std::bind` con `_1` y `_2` conecta los dos argumentos que
pasará rclcpp (request y response) con `on_enable`.

**Verifica**: pasa `EnableServerTest.AnunciaElServicio`.

## Paso 2: Atender la petición

**Descomenta el bloque del Paso 2** en `on_enable` y **borra las dos líneas
`(void)`** de debajo (marcadas con `// elimina esta línea al completar el Paso 2`).
Solo estaban para que el starter compilara con `-Werror` sin usar los
argumentos.

**Verifica**: pasa `EnableServerTest.CambiaEstadoUnaVez`.

## Paso 3: Crear el cliente

**Abre `include/ejercicio02_servicio_cpp/enable_client.hpp`** y descomenta el
bloque del Paso 3.

## Paso 4: Llamada asíncrona

**Descomenta el bloque del Paso 4** en `send()` y borra las dos líneas marcadas
con `// elimina esta línea al completar el Paso 4`.

`async_send_request` devuelve un `FutureAndRequestId`; `.future.share()` lo
convierte en un `SharedFuture`, que se puede copiar y consultar desde `main` y
desde el test.

**Verifica**: pasa `EnableClientTest.RecibeRespuesta`. Los tres tests pasan.

## Paso 5: Cruzar lenguajes

Necesitas el Ejercicio 01 compilado en el mismo workspace. En cada terminal,
primero `source install/setup.bash`.

```bash
# Terminal 1: server C++
ros2 run ejercicio02_servicio_cpp enable_server

# Terminal 2: cliente Python
ros2 run ejercicio01_servicio_py enable_client true
# [INFO] [...] [enable_client]: success=True message='habilitado'
```

En la terminal 1:

```text
[INFO] [...] [enable_server]: Petición data=1: habilitado
```

Cierra el server C++ y arranca el de Python en la terminal 1:

```bash
# Terminal 1: server Python
ros2 run ejercicio01_servicio_py enable_server

# Terminal 2: cliente C++
ros2 run ejercicio02_servicio_cpp enable_client true
# [INFO] [...] [enable_client]: success=1 message='habilitado'
ros2 run ejercicio02_servicio_cpp enable_client true
# [INFO] [...] [enable_client]: success=0 message='ya estaba habilitado'
```

✅ Verificación: cada cliente funciona igual con los dos servers. `1`/`0` en lugar
de `True`/`False` es solo el formato `%d` de C++ para un `bool`.

## Checklist

- [ ] Los tres tests de `test/test_servicio.cpp` pasan
- [ ] Cliente Python contra server C++: funciona
- [ ] Cliente C++ contra server Python: funciona
- [ ] Sé por qué los `(void)` del starter había que borrarlos

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01](../ejercicio-01-servicio_py/README.md) | **Ejercicio 02** | [Ejercicio 03](../ejercicio-03-accion_compartida/README.md) |

← [Volver a la Semana 03](../../README.md)
