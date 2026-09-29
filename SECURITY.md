# 🔒 Política de Seguridad

## Versiones Soportadas

| Versión | Soportada |
| ------- | --------- |
| main    | ✅        |

## Reportar una Vulnerabilidad

La seguridad de este proyecto es importante para nosotros. Si descubres una vulnerabilidad de seguridad, te pedimos que la reportes de manera responsable.

### ⚠️ NO hacer público el reporte

Por favor, **NO** abras un issue público para reportar vulnerabilidades de seguridad.

### 📧 Cómo Reportar

1. **Abre un Security Advisory privado** en GitHub:
   - Ve a la pestaña "Security" del repositorio
   - Haz clic en "Report a vulnerability"
   - Completa el formulario con los detalles

2. **Incluye en tu reporte**:
   - Descripción detallada de la vulnerabilidad
   - Pasos para reproducir el problema
   - Impacto potencial
   - Sugerencias de solución (si las tienes)

### ⏱️ Tiempo de Respuesta

- **Confirmación inicial**: 48 horas
- **Evaluación**: 7 días
- **Resolución**: Dependiendo de la severidad

### 🎁 Reconocimiento

Agradecemos a todos los investigadores de seguridad que reportan vulnerabilidades de manera responsable. Tu nombre será incluido en nuestros agradecimientos (si lo deseas).

## Mejores Prácticas de Seguridad

Este bootcamp enseña las siguientes prácticas de seguridad aplicadas a robótica con ROS2:

### Aislamiento de red (DDS)

```bash
# ✅ Cada estudiante/simulación en su propio ROS_DOMAIN_ID
# evita que el tráfico DDS de un contenedor interfiera con el de otro en la misma red
export ROS_DOMAIN_ID=42
```

Por defecto DDS multicast se ve en toda la red local. En clase, cada estudiante fija
un `ROS_DOMAIN_ID` distinto; en producción se usa `ROS_LOCALHOST_ONLY=1` o un perfil
DDS con seguridad (SROS2) si el robot sale del laboratorio.

### Nunca hardcodear credenciales de hardware

```python
# ✅ Variables de entorno / parámetros ROS2 para tokens, IPs de cámaras, claves de API de mapas
class CameraDriverNode(Node):
    def __init__(self) -> None:
        super().__init__("camera_driver")
        self.declare_parameter("camera_url", "")
        camera_url = self.get_parameter("camera_url").value

# ❌ NUNCA hacer esto
# camera_url = "rtsp://admin:admin123@192.168.1.50/stream"
```

### Límites físicos como código, no como buena intención

```cpp
// ✅ Todo nodo que mueve un actuador clamea a límites declarados,
// nunca confía en que el valor de entrada ya viene sano
double clamp_velocity(double v, double v_max) {
  return std::max(-v_max, std::min(v, v_max));
}
```

Un mensaje `Twist`/`JointTrajectory` mal formado o malicioso nunca debe poder mover un
actuador físico fuera de sus límites mecánicos. Esto se valida en el nodo de control,
no se asume del publisher.

### Simulación antes que hardware

```
✅ Todo comportamiento nuevo se valida primero en Gazebo headless (`gz sim -s`)
❌ Nunca se prueba lógica de control sin probar por primera vez directamente en el robot físico
```

### Contenedores con versión pinneada

```dockerfile
# ✅ Imagen con tag de fecha, reproducible
FROM osrf/ros:jazzy-desktop-full-20260901

# ❌ NUNCA
# FROM osrf/ros:jazzy-desktop-full
# FROM osrf/ros:latest
```

## Dependencias

Mantenemos las dependencias actualizadas para evitar vulnerabilidades conocidas. Usamos:

- `rosdep` + `apt` con paquetes `ros-jazzy-*` pinneados por release
- `uv`/`pip` con versión exacta para dependencias Python (OpenCV, ultralytics)
- Dependabot para alertas automáticas
- Auditorías regulares de seguridad

---

Gracias por ayudar a mantener este proyecto seguro. 🛡️
