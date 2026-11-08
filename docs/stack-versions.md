# 📦 Versiones del Stack - BC Robótica Bootcamp

Este documento define las versiones oficiales de todas las tecnologías usadas en el bootcamp.

> ⚠️ **IMPORTANTE**: la imagen Docker se referencia siempre con **tag de fecha**, nunca
> `:latest`. Las dependencias Python se pinean con versión exacta (`==`) y se instalan
> con `uv`, nunca con `pip`. Ver
> [dependency-security-policy.md](dependency-security-policy.md).
> `scripts/verificar-enlaces.sh` falla si encuentra un rango (`>=`, `~=`, `^`) o `:latest`.

## 🐧 Sistema Base y Runtime

| Tecnología | Versión | Notas |
|------------|---------|-------|
| Ubuntu | **24.04 LTS (Noble)** | Única combinación oficialmente soportada por `ros-jazzy-*` |
| ROS2 | **Jazzy Jalisco** | LTS, soporte hasta mayo 2029 |
| Imagen Docker base | `osrf/ros:jazzy-desktop-full-YYYYMMDD` | Tag de fecha fijo, nunca `:latest`. Actualizar en cada revisión trimestral |
| Docker | **27.5.1** | Container runtime |
| Docker Compose | **2.32.4** | Plugin v2 (sin clave `version:`) |
| Python | **3.12.3** | Versión de Ubuntu 24.04, la que trae `ros-jazzy-desktop-full` |
| CMake | **3.28.3** | Build de paquetes `ament_cmake` |
| GCC | **13.3.0** | Compilador por defecto de Ubuntu 24.04 |
| uv | **0.13.7** (`ghcr.io/astral-sh/uv:0.13.7`) | Instala tooling y dependencias no-ROS. Nunca `pip` |

## 🤖 Simulación y Navegación

| Paquete/Repo | Versión | Propósito |
|---|---|---|
| Gazebo | **Harmonic (`gz-sim` 8.7.0)** | Simulador — reemplaza Gazebo Classic (EOL) |
| `ros_gz` | rama `jazzy` | Puente ROS2 ↔ Gazebo |
| `slam_toolbox` | `ros-jazzy-slam-toolbox` (apt) | SLAM 2D |
| `nav2_bringup` y paquetes `nav2_*` | `ros-jazzy-navigation2` (apt), rama `jazzy` | Stack de navegación autónoma |
| `robot_localization` | `ros-jazzy-robot-localization` (apt) | Fusión sensorial EKF/UKF |
| `ros2_control` + `ros2_controllers` | `ros-jazzy-ros2-control`, `ros-jazzy-ros2-controllers` (apt) | Control de actuadores (semana 10 en adelante) |
| `gz_ros2_control` | `ros-jazzy-gz-ros2-control` (apt) | `ros2_control` dentro de Gazebo Harmonic |

## 🦾 Manipulación

| Paquete/Repo | Versión | Propósito |
|---|---|---|
| MoveIt2 | `ros-jazzy-moveit` (apt), rama `jazzy` | Framework de manipulación |
| `moveit_py` | incluido en MoveIt2 Jazzy | API Python oficial (reemplaza `moveit_commander`) |
| OMPL | incluido en MoveIt2 | Planners de movimiento |
| MoveIt Task Constructor | `ros-jazzy-moveit-task-constructor-core` (apt) | Secuencias de grasping (semana 23) |

## 👁️ Percepción

| Paquete | Versión | Propósito |
|---|---|---|
| `cv_bridge` / `image_transport` | `ros-jazzy-cv-bridge`, `ros-jazzy-image-transport` (apt) | Puente ROS↔OpenCV |
| OpenCV | `python3-opencv` (apt, el que usa `cv_bridge`) | Visión clásica |
| PCL | `ros-jazzy-pcl-ros` (apt) | Point clouds (semana 22) |
| `ultralytics` | `8.3.40`, en `uv venv --system-site-packages` | Detección deep learning (semana 25) |

## 🛠️ Build, Test y Lint

| Herramienta | Versión | Propósito |
|---|---|---|
| `colcon` | `ros-dev-tools` (apt) | Orquestador de build/test del workspace |
| `rosdep` | `ros-dev-tools` (apt) | Resolución de dependencias del sistema |
| `ruff` | `0.8.6` | Lint + format Python |
| `mypy` | `1.13.0` | Tipado estático Python |
| `pytest` + `launch_testing` | `ros-jazzy-launch-testing-ament-cmake` (apt) | Tests de nodos/launch Python |
| `clang-format` | `18.1.3` (apt `clang-format`) | Formato C++, `.clang-format` de la raíz es la única verdad |
| `clang-tidy` | `18.1.3` (apt `clang-tidy`) | Análisis estático C++ (semana 05) |
| `gtest` / `ament_cmake_gtest` | `ros-dev-tools` (apt) | Tests de nodos C++ |
| `ros2_tracing` | `ros-jazzy-ros2trace`, `ros-jazzy-tracetools-launch` (apt) | Perfilado de latencia (semana 28) |
| SROS2 | `ros-jazzy-sros2` (apt) | Seguridad DDS (semana 29) |

## 🐳 Dockerfile Base

```dockerfile
FROM osrf/ros:jazzy-desktop-full-20260901

ENV DEBIAN_FRONTEND=noninteractive \
    ROS_DISTRO=jazzy

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions ros-dev-tools python3-opencv clang-format clang-tidy \
    ros-jazzy-navigation2 ros-jazzy-slam-toolbox ros-jazzy-robot-localization \
    ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-gz-ros2-control \
    ros-jazzy-moveit ros-jazzy-moveit-task-constructor-core \
    ros-jazzy-cv-bridge ros-jazzy-image-transport ros-jazzy-pcl-ros \
    ros-jazzy-ros-gz ros-jazzy-ros2trace ros-jazzy-tracetools-launch ros-jazzy-sros2 \
    && rm -rf /var/lib/apt/lists/*

# Qué: uv como único instalador de Python. Para qué: tooling aislado del Python del
# sistema (contra el que está compilado rclpy). Impacto: cero pip en la imagen.
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/
ENV UV_TOOL_BIN_DIR=/usr/local/bin
RUN uv tool install ruff==0.8.6 && uv tool install mypy==1.13.0

WORKDIR /workspace
COPY . .

RUN . /opt/ros/jazzy/setup.sh && rosdep update && \
    rosdep install --from-paths src --ignore-src -y

RUN echo "source /opt/ros/jazzy/setup.bash" >> /etc/bash.bashrc

CMD ["bash"]
```

> El devcontainer de VS Code añade `--gpus all` y las variables `DISPLAY`/`XDG_RUNTIME_DIR`
> para el passthrough GUI de RViz2/Gazebo vía WSLg. Ver [setup/con-docker.md](setup/con-docker.md).

## 📦 docker-compose.yml Base

```yaml
services:
  ros2:
    build: .
    environment:
      - DISPLAY=${DISPLAY}
      - ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-42}
      - LIBGL_ALWAYS_SOFTWARE=0
    volumes:
      - ./bootcamp:/workspace/src
      - /tmp/.X11-unix:/tmp/.X11-unix
    network_mode: host
    command: bash
```

## 🔄 Actualización de Versiones

- **Trimestral**: revisión de versiones y CVEs ([procedimiento](dependency-security-policy.md#-procedimiento-para-actualizar-versiones))
- **Por release**: al saltar de tag de imagen Docker (`jazzy-desktop-full-YYYYMMDD`), re-verificar
  `scripts/verificar-simulaciones.sh` en todas las semanas antes de publicar
- **Última actualización**: 08/11/2026

## ✅ Verificación de Versiones

```bash
# ROS2 y distro
docker compose exec ros2 printenv ROS_DISTRO
docker compose exec ros2 lsb_release -a

# Gazebo
docker compose exec ros2 gz sim --version

# Nav2 / MoveIt2 (versión del paquete apt instalado)
docker compose exec ros2 apt list --installed 2>/dev/null | grep -E "navigation2|moveit"

# Python
docker compose exec ros2 python3 -c "import cv2, rclpy; print(cv2.__version__)"
docker compose exec ros2 uv --version
docker compose exec ros2 ruff --version
```

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Setup sin Docker](setup/sin-docker.md) | **Versiones del stack** | [Seguridad de dependencias](dependency-security-policy.md) |

← [Volver al inicio del bootcamp](../README.md)
