# 🔧 Hardware Opcional (BOM de referencia)

El bootcamp es **100% verificable en simulación**. Todo lo de este documento es una
**extensión opcional**: nunca es requisito para aprobar una semana ni el capstone.
Cada README de semana que tenga una sección de hardware la marca en un bloque
`> [!NOTE]` al final, separada de los pasos de simulación.

## Track A — Móvil

| Opción | Componentes | Costo aprox. | Nota |
|---|---|---|---|
| **Kit oficial** | TurtleBot3 Burger/Waffle (ROBOTIS) | ~550-1000 USD | Paquetes ROS2 oficiales mantenidos, cero fricción de integración con Nav2 |
| **DIY económico** | Raspberry Pi 4/5 · 2× motor DC con encoder · driver TB6612FNG · RPLiDAR A1/C1 · IMU (BNO055) · cámara USB · chasis + batería | ~150-250 USD | Requiere driver propio (nodo puente de motores, ver Semana 06); soporte comunitario, no oficial |

**Semanas donde aplica** (siempre opcional):

| Semana | Qué se prueba en hardware real |
|---|---|
| 06 | Teleop del chasis real en vez de simulado |
| 13 | SLAM (`slam_toolbox`) sobre sensores reales |
| 14 | AMCL con el mapa generado en la semana 13 |
| 15-17 | Nav2 completo (planners, controllers, BT, misión) en el robot físico |

## Track B — Manipulador

| Opción | Componentes | Costo aprox. | Nota |
|---|---|---|---|
| **Kit oficial** | ROBOTIS OpenManipulator-X | ~700-1000 USD | Paquetes MoveIt2 oficiales, config lista |
| **DIY económico** | Brazo de 4-6 servos · PCA9685 · ESP32/Arduino (micro-ROS o bridge serie) · cámara USB fija o eye-in-hand | ~100-200 USD | Requiere driver de gripper propio (nodo de acción); soporte comunitario, no oficial |

**Semanas donde aplica** (siempre opcional):

| Semana | Qué se prueba en hardware real |
|---|---|
| 13 | Mover el brazo real con `moveit_py`/`MoveGroupInterface` |
| 15 | Percepción con cámara real en vez de simulada |
| 16-17 | Grasping y pipeline pick&place completo en el brazo físico |

## Principios

- **Simulación primero, siempre.** Ningún comportamiento nuevo se prueba por primera
  vez en hardware; se valida en Gazebo headless antes
- **Nunca bloqueante.** La rúbrica de cada semana se cumple 100% en simulación
- **Límites físicos como código.** Todo nodo que mueve un actuador real clampea a
  límites declarados — ver reglas de seguridad en `.github/copilot-instructions.md`
- **DIY es "soporte comunitario"**: el kit oficial (TurtleBot3 / OpenManipulator-X)
  tiene paquetes ROS2 mantenidos por Open Robotics/ROBOTIS; el DIY puede requerir
  ajustes propios de driver que el bootcamp no puede probar en cada combinación de
  hardware posible
