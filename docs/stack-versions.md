# 📦 Versiones del Stack - BC Robótica Bootcamp

Este documento define las versiones oficiales de todas las tecnologías usadas en el bootcamp.

> ⚠️ **IMPORTANTE**: la imagen Docker se referencia siempre con **tag de fecha**, nunca
> `:latest`. Las dependencias Python se pinean con versión exacta (`==`). Ver
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

## 🤖 Simulación y Navegación

| Paquete/Repo | Versión | Propósito |
|---|---|---|
| Gazebo | **Harmonic (`gz-sim` 8.7.0)** | Simulador — reemplaza Gazebo Classic (EOL) |
| `ros_gz` | rama `jazzy` | Puente ROS2 ↔ Gazebo |
| `slam_toolbox` | `ros-jazzy-slam-toolbox` (apt) | SLAM 2D |
| `nav2_bringup` y paquetes `nav2_*` | `ros-jazzy-navigation2` (apt), rama `jazzy` | Stack de navegación autónoma |
| `robot_localization` | `ros-jazzy-robot-localization` (apt) | Fusión sensorial EKF/UKF |

## 🦾 Manipulación

| Paquete/Repo | Versión | Propósito |
|---|---|---|
| MoveIt2 | `ros-jazzy-moveit` (apt), rama `jazzy` | Framework de manipulación |
| `moveit_py` | incluido en MoveIt2 Jazzy | API Python oficial (reemplaza `moveit_commander`) |
| OMPL | incluido en MoveIt2 | Planners de movimiento |

## 👁️ Percepción

| Paquete | Versión | Propósito |
|---|---|---|
| `cv_bridge` / `image_transport` | `ros-jazzy-cv-bridge`, `ros-jazzy-image-transport` (apt) | Puente ROS↔OpenCV |
| `opencv-python` | `4.10.0.84` | Visión clásica |
| `ultralytics` | `8.3.40` | YOLOv8 preentrenado — extensión opcional (semana 10, 15-B) |

## 🛠️ Build, Test y Lint

| Herramienta | Versión | Propósito |
|---|---|---|
| `colcon` | `ros-dev-tools` (apt) | Orquestador de build/test del workspace |
| `rosdep` | `ros-dev-tools` (apt) | Resolución de dependencias del sistema |
| `ruff` | `0.8.6` | Lint + format Python |
| `mypy` | `1.13.0` | Tipado estático Python |
| `pytest` + `launch_testing` | `ros-jazzy-launch-testing-ament-cmake` (apt) | Tests de nodos/launch Python |
| `clang-format` | `18.1.3` | Formato C++, `.clang-format` de la raíz es la única verdad |
| `gtest` / `ament_cmake_gtest` | `ros-dev-tools` (apt) | Tests de nodos C++ |

## 🐳 Dockerfile Base

```dockerfile
FROM osrf/ros:jazzy-desktop-full-20260901

ENV DEBIAN_FRONTEND=noninteractive \
    ROS_DISTRO=jazzy

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip python3-colcon-common-extensions ros-dev-tools \
    ros-jazzy-navigation2 ros-jazzy-slam-toolbox ros-jazzy-robot-localization \
    ros-jazzy-moveit ros-jazzy-cv-bridge ros-jazzy-image-transport \
    ros-jazzy-ros-gz \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --break-system-packages \
    ruff==0.8.6 mypy==1.13.0 opencv-python==4.10.0.84

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
- **Última actualización**: 29/09/2026

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
docker compose exec ros2 python3 -c "import cv2, ultralytics; print(cv2.__version__, ultralytics.__version__)"
```
