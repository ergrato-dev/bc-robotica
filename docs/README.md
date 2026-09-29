# 📚 Documentación del Bootcamp

Esta carpeta contiene documentación general que aplica a todo el bootcamp.

## 📋 Índice

| Documento | Descripción |
|-----------|-------------|
| [setup/](setup/README.md) | ⚙️ Configuración del entorno (con y sin Docker) |
| [stack-versions.md](stack-versions.md) | Versiones oficiales de ROS2, Gazebo, Nav2, MoveIt2 y dependencias |
| [dependency-security-policy.md](dependency-security-policy.md) | 🔒 Política de seguridad, regla de oro (versiones exactas, sin `:latest`) |
| [tracks.md](tracks.md) | 🔀 Política de tracks (A/B) y dominios/misiones — anticopia |
| [hardware-opcional.md](hardware-opcional.md) | 🔧 BOM de referencia para quien quiera hardware físico |

## 🐳 Entorno de Desarrollo

Este bootcamp usa **Docker** como entorno oficial para:

- ✅ Evitar el infierno de instalación de ROS2 nativo
- ✅ Garantizar la misma versión de ROS2/Gazebo/Nav2/MoveIt2 para todos los estudiantes
- ✅ Resolver GUI (RViz2, Gazebo) vía WSLg/X11 sin instalación adicional
- ✅ Simplificar la configuración inicial

### Requisitos

- Docker 27.5.1
- Docker Compose 2.32.4
- VS Code (recomendado, con Dev Containers)

### Inicio Rápido

```bash
git clone https://github.com/ergrato-dev/bc-robotica.git
cd bc-robotica

# Levantar el entorno base
docker compose up -d
docker compose exec ros2 bash

# Ir a una semana específica
cd bootcamp/week-01-fundamentos_ros2_y_workspace
```

## 📦 Stack Tecnológico

| Categoría | Tecnologías |
|-----------|-------------|
| **Middleware** | ROS2 Jazzy Jalisco, Ubuntu 24.04 |
| **Lenguajes** | Python 3.12 (`rclpy`), C++17 (`rclcpp`) — ambos de primera clase |
| **Simulación** | Gazebo Harmonic (`gz-sim`), `ros_gz` |
| **Navegación** | Nav2, `slam_toolbox`, AMCL |
| **Manipulación** | MoveIt2, `moveit_py`, OMPL |
| **Percepción** | OpenCV, `cv_bridge`, YOLOv8/`ultralytics` (opcional) |
| **Testing** | `colcon test`, `pytest`/`launch_testing`, `gtest` |
| **Herramientas** | Docker 27.5.1, `ruff`, `mypy`, `clang-format` |

Ver [stack-versions.md](stack-versions.md) para versiones detalladas pinneadas.

## 🔗 Enlaces Útiles

- [ROS2 Jazzy Documentation](https://docs.ros.org/en/jazzy/)
- [Nav2 Documentation](https://docs.nav2.org/)
- [MoveIt2 Documentation](https://moveit.picknik.ai/)
- [Gazebo Harmonic Documentation](https://gazebosim.org/docs/harmonic)
- [Docker Documentation](https://docs.docker.com/)
