# Acciones en Python y C++

> Un action server es un bucle que trabaja, informa y mira si le piden parar. Un action client son tres callbacks: aceptado, progreso, terminado. Esta teoría escribe el server en Python y el cliente en C++.

## 🎯 Objetivos

- Crear un action server en `rclpy` con validación del goal, feedback y cancelación
- Saber por qué ese server necesita un `MultiThreadedExecutor`
- Crear un action client en `rclcpp` con sus tres callbacks
- Declarar las dependencias de `rclcpp_action`

## 1. Qué problema resuelve

La CLI envía goals, pero un robot real los envía desde nodos: el orquestador de
la misión pide "navega a la estantería 3" y decide qué hacer según el result.
Para eso necesitas escribir tanto el server (quien trabaja) como el cliente
(quien pide).

## 2. Action server en Python, paso a paso

```python
import time

from ejercicio03_interfaces.action import MoveDistance
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node

SPEED_MPS = 0.5
PERIOD_S = 0.1


class MoveServer(Node):
    def __init__(self) -> None:
        super().__init__("move_server")
        self._server = ActionServer(
            self,
            MoveDistance,
            "robot/move_distance",
            execute_callback=self._execute,
            goal_callback=self._on_goal,
            cancel_callback=self._on_cancel,
            callback_group=ReentrantCallbackGroup(),
        )

    def _on_goal(self, goal_request: MoveDistance.Goal) -> GoalResponse:
        # Decide antes de empezar: rechazar aquí no cuesta nada.
        if 0.0 < goal_request.distance_m <= 10.0:
            return GoalResponse.ACCEPT
        return GoalResponse.REJECT

    def _on_cancel(self, goal_handle: ServerGoalHandle) -> CancelResponse:
        # Aceptar solo marca el goal; _execute decide cuándo para.
        return CancelResponse.ACCEPT

    def _execute(self, goal_handle: ServerGoalHandle) -> MoveDistance.Result:
        result = MoveDistance.Result()
        distance_m = goal_handle.request.distance_m
        feedback = MoveDistance.Feedback()
        while result.traveled_m < distance_m:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()  # estado final CANCELED
                return result
            time.sleep(PERIOD_S)  # simula el tiempo que tarda moverse
            step_m = SPEED_MPS * PERIOD_S
            result.traveled_m = min(distance_m, result.traveled_m + step_m)
            feedback.remaining_m = distance_m - result.traveled_m
            goal_handle.publish_feedback(feedback)
        goal_handle.succeed()  # estado final SUCCEEDED
        return result
```

Qué hace cada callback:

| Callback | Cuándo se llama | Qué devuelve |
|---|---|---|
| `goal_callback` | Al llegar un goal | `GoalResponse.ACCEPT` o `REJECT` |
| `execute_callback` | Tras aceptar el goal | El `Result`, después de marcar el estado final |
| `cancel_callback` | Al llegar una petición de cancelar | `CancelResponse.ACCEPT` o `REJECT` |

Dentro de `_execute`, antes de devolver el result marca **siempre** un estado
final: `succeed()`, `canceled()` o `abort()`. Si no lo haces, rclpy avisa en el
log y lo da por abortado.

### 2.1 Por qué hace falta un `MultiThreadedExecutor`

`_execute` pasa varios segundos dentro de su bucle. Con el executor de un solo
hilo de la Semana 01 (`rclpy.spin(node)`), mientras el bucle corre **nadie**
atiende la petición de cancelar: `is_cancel_requested` nunca cambia y el goal
llega al final aunque pulses `Ctrl+C`.

La solución tiene dos piezas que van juntas:

```python
from rclpy.executors import MultiThreadedExecutor

executor = MultiThreadedExecutor()  # varios hilos para callbacks
executor.add_node(node)
executor.spin()
```

- **`MultiThreadedExecutor`**: ejecuta callbacks en varios hilos a la vez
- **`ReentrantCallbackGroup`** (en el `ActionServer`): permite que dos callbacks
  del mismo grupo, aquí `_execute` y `_on_cancel`, corran a la vez. Sin él, el
  grupo por defecto solo deja correr uno cada vez y el problema sigue

La Semana 04 explica executors y grupos de callbacks a fondo. Por ahora basta
con la regla: **un action server con un bucle largo usa los dos**.

## 3. Action client en C++, paso a paso

`rclcpp_action` es una librería aparte de `rclcpp`. Va en `package.xml`:

```xml
<depend>rclcpp_action</depend>
<depend>ejercicio03_interfaces</depend>
```

Y en `CMakeLists.txt`:

```cmake
find_package(rclcpp_action REQUIRED)
find_package(ejercicio03_interfaces REQUIRED)
ament_target_dependencies(move_client rclcpp rclcpp_action ejercicio03_interfaces)
```

El cliente:

```cpp
#include "ejercicio03_interfaces/action/move_distance.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"

#include <chrono>
#include <memory>
#include <stdexcept>

class MoveClient : public rclcpp::Node {
 public:
  using MoveDistance = ejercicio03_interfaces::action::MoveDistance;
  using GoalHandle = rclcpp_action::ClientGoalHandle<MoveDistance>;

  MoveClient() : Node("move_client") {
    client_ = rclcpp_action::create_client<MoveDistance>(this, "robot/move_distance");
  }

  void send(double distance_m) {
    if (!client_->wait_for_action_server(std::chrono::seconds(2))) {
      throw std::runtime_error("el action server robot/move_distance no está disponible");
    }
    MoveDistance::Goal goal;
    goal.distance_m = distance_m;
    rclcpp_action::Client<MoveDistance>::SendGoalOptions options;
    // 1. Aceptado o rechazado: un handle nulo significa rechazado.
    options.goal_response_callback = [this](const GoalHandle::SharedPtr& handle) {
      if (!handle) {
        RCLCPP_WARN(get_logger(), "Goal rechazado");
        done_ = true;
      }
    };
    // 2. Progreso: una llamada por cada publish_feedback del server.
    options.feedback_callback = [this](GoalHandle::SharedPtr,
                                       const std::shared_ptr<const MoveDistance::Feedback> fb) {
      RCLCPP_INFO(get_logger(), "Faltan %.2f m", fb->remaining_m);
    };
    // 3. Final: una sola vez, con el código (SUCCEEDED, CANCELED, ABORTED).
    options.result_callback = [this](const GoalHandle::WrappedResult& result) {
      RCLCPP_INFO(get_logger(), "Terminado: %.2f m recorridos", result.result->traveled_m);
      done_ = true;
    };
    client_->async_send_goal(goal, options);
  }

  bool done() const { return done_; }

 private:
  rclcpp_action::Client<MoveDistance>::SharedPtr client_;
  bool done_{false};
};
```

`async_send_goal` devuelve enseguida, como `call_async`. Las tres callbacks
llegan durante el spin. Por eso `main` gira hasta que `done()` es `true`:

```cpp
rclcpp::executors::SingleThreadedExecutor executor;
executor.add_node(node);
while (rclcpp::ok() && !node->done()) {
  executor.spin_once(std::chrono::milliseconds(100));
}
```

Aquí basta un hilo: ninguna callback del cliente se queda esperando a otra.

`result.code` es un `rclcpp_action::ResultCode` (`SUCCEEDED`, `CANCELED`,
`ABORTED`); compruébalo antes de fiarte del result.

## 4. Probar entre lenguajes

```bash
# Terminal 1
ros2 run ejercicio03_accion_py move_server

# Terminal 2
ros2 run ejercicio03_accion_cpp move_client 0.15
# [INFO] [...] [move_client]: Faltan 0.10 m
# [INFO] [...] [move_client]: Faltan 0.05 m
# [INFO] [...] [move_client]: Faltan 0.00 m
# [INFO] [...] [move_client]: Terminado: 0.15 m recorridos
```

## 5. Errores típicos y su causa

| Síntoma | Causa | Arreglo |
|---|---|---|
| `Ctrl+C` en el cliente no para el goal | Executor de un hilo o grupo por defecto en el server | `MultiThreadedExecutor` + `ReentrantCallbackGroup` |
| Log `Goal state not set, assuming aborted` | `_execute` devolvió el result sin `succeed()`/`canceled()`/`abort()` | Marca el estado final antes del `return` |
| C++: `undefined reference to rclcpp_action::...` | Falta `rclcpp_action` en `ament_target_dependencies` | Añádelo |
| El cliente no recibe feedback | El nodo cliente no hace spin mientras espera | Gira hasta `done()` |

## 6. Antipatrones

- ❌ **`time.sleep` largo sin mirar `is_cancel_requested`.** El robot tarda en
  parar todo lo que dure el `sleep`
- ❌ **Validar el goal dentro de `_execute`.** El cliente ya recibió "aceptado";
  rechazar en `goal_callback` es más claro
- ❌ **Bloquear el hilo de `main` con `std::this_thread::sleep_for` en vez de
  hacer spin.** Las callbacks no llegan

## 📚 Recursos Adicionales

- [Writing an action server and client (Python) — ROS2 Jazzy](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html)
- [Writing an action server and client (C++) — ROS2 Jazzy](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Cpp.html)

## ✅ Checklist de Verificación

- [ ] Mi action server valida el goal, publica feedback y marca un estado final
- [ ] Sé por qué el server necesita `MultiThreadedExecutor` y `ReentrantCallbackGroup`
- [ ] Mi action client C++ usa las tres callbacks
- [ ] Un cliente C++ completó un goal contra un server Python

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Acciones](03-acciones-goal-feedback-result.md) | **04 · Acciones en código** | [05 · Parámetros](05-parametros.md) |

← [Volver a la Semana 03](../README.md)
