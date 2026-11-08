# 🔧 Hardware Opcional (BOM de referencia)

El bootcamp es **100% verificable en simulación**. Todo lo de este documento es una
**extensión opcional**: nunca es requisito para aprobar una semana ni el capstone.
Cada README de semana que tenga una sección de hardware la marca en un bloque
`> [!NOTE]` al final, separada de los pasos de simulación.

## Robot móvil (fases 2, 3 y 5)

| Opción | Componentes | Costo aprox. | Nota |
|---|---|---|---|
| **Kit oficial** | TurtleBot3 Burger/Waffle (ROBOTIS) | ~550-1000 USD | Paquetes ROS2 oficiales mantenidos, cero fricción de integración con Nav2 |
| **DIY económico** | Raspberry Pi 4/5 · 2× motor DC con encoder · driver TB6612FNG · RPLiDAR A1/C1 · IMU (BNO055) · cámara USB · chasis + batería | ~150-250 USD | Requiere driver propio (hardware interface de `ros2_control`, ver Semana 10); soporte comunitario, no oficial |

**Semanas donde aplica** (siempre opcional):

| Semana | Qué se prueba en hardware real |
|---|---|
| 08 | Teleop del chasis real en vez de simulado |
| 10 | Hardware interface propio de `ros2_control` sobre los motores reales |
| 12 | Calibrar odometría (radio de rueda, separación entre ruedas) y la covarianza del EKF |
| 14 | SLAM (`slam_toolbox`) sobre sensores reales |
| 15 | AMCL con el mapa generado en la semana 14 |
| 16-18 | Nav2 completo (planners, controllers, BT, misión) en el robot físico |
| 30 | ESP32 como cliente micro-ROS que publica encoders e IMU |

## Brazo manipulador (fases 4 y 5)

| Opción | Componentes | Costo aprox. | Nota |
|---|---|---|---|
| **Kit oficial** | ROBOTIS OpenManipulator-X | ~700-1000 USD | Paquetes MoveIt2 oficiales, config lista |
| **DIY económico** | Brazo de 4-6 servos · PCA9685 · ESP32/Arduino (micro-ROS o bridge serie) · cámara USB fija o eye-in-hand | ~100-200 USD | Requiere driver de gripper propio (nodo de acción); soporte comunitario, no oficial |

**Semanas donde aplica** (siempre opcional):

| Semana | Qué se prueba en hardware real |
|---|---|
| 20 | Mover el brazo real con `moveit_py`/`MoveGroupInterface` |
| 22 | Percepción con cámara real y calibración hand-eye real |
| 23-24 | Grasping y pipeline pick&place completo en el brazo físico |
| 26 | Manipulador móvil: TurtleBot3 Waffle + OpenManipulator-X (combinación oficial de ROBOTIS) |

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
- **Deja el ajuste de calibración expuesto como parámetro.** El hardware real nunca es el
  ideal: un PCA9685 corre unos puntos por ciento rápido, un encoder pierde pulsos, una
  IMU tiene sesgo. Offsets, escalas y límites van en el YAML de parámetros, no en el código

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Decisión de ritmo](decision-semanas.md) | **Hardware opcional** | [Índice de semanas](../bootcamp/README.md) |

← [Volver al inicio del bootcamp](../README.md)
