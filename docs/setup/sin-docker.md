# 🐧 Configuración sin Docker (Ubuntu 24.04 nativo)

Alternativa válida si ya tienes **Ubuntu 24.04 LTS nativo** (no WSL2, no macOS). Pierdes
la reproducibilidad de versiones exactas que da la imagen Docker oficial: instala
siempre las versiones de `docs/stack-versions.md`, no `ros-jazzy-desktop-full` a secas
sin revisar el tag.

> ⚠️ **Advertencia**: `scripts/verificar-simulaciones.sh` y la verificación tipo CI del
> bootcamp asumen la imagen Docker oficial. Con instalación nativa eres responsable de
> mantener las versiones alineadas manualmente.

## 1. Prerrequisitos

```bash
lsb_release -a
# Distributor ID: Ubuntu
# Release: 24.04
```

Si no tienes exactamente Ubuntu 24.04, usa la [opción Docker](con-docker.md) en su
lugar — ROS2 Jazzy no está soportado oficialmente en otras versiones.

## 2. Instalar ROS2 Jazzy

Sigue la [guía oficial de instalación](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)
resumida aquí:

```bash
sudo apt update && sudo apt install -y curl gnupg lsb-release

sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt install -y ros-jazzy-desktop-full ros-dev-tools

echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## 3. Instalar Gazebo Harmonic y paquetes del bootcamp

```bash
sudo apt install -y \
  ros-jazzy-ros-gz \
  ros-jazzy-navigation2 ros-jazzy-slam-toolbox ros-jazzy-robot-localization \
  ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-gz-ros2-control \
  ros-jazzy-moveit ros-jazzy-moveit-task-constructor-core \
  ros-jazzy-cv-bridge ros-jazzy-image-transport ros-jazzy-pcl-ros python3-opencv \
  ros-jazzy-ros2trace ros-jazzy-tracetools-launch ros-jazzy-sros2
```

## 4. Instalar herramientas Python con `uv`

En este bootcamp nunca se usa `pip`. `rclpy` y OpenCV ya vienen por `apt` (paso 3);
`uv` solo instala el tooling, aislado del Python del sistema:

```bash
# Qué: instala uv 0.13.7 en ~/.local/bin. Para qué: gestionar herramientas Python sin
# tocar el Python del sistema, contra el que está compilado rclpy.
curl -LsSf https://astral.sh/uv/0.13.7/install.sh | sh
source ~/.bashrc

uv tool install ruff==0.8.6
uv tool install mypy==1.13.0
```

Salida esperada de la verificación:

```bash
uv --version     # uv 0.13.7
ruff --version   # ruff 0.8.6
mypy --version   # mypy 1.13.0 (compiled: yes)
```

## 5. Verificar

```bash
ros2 doctor
gz sim --version
ros2 pkg list | grep -E "nav2|moveit"
```

## 6. Clonar el repositorio

```bash
git clone https://github.com/ergrato-dev/bc-robotica.git
cd bc-robotica
```

## 7. Compilar un ejercicio

```bash
cd bootcamp/week-01-fundamentos_ros2_y_workspace/2-practicas/ejercicio-01-publisher_subscriber_py/starter
colcon build --symlink-install
source install/setup.bash
ros2 run <paquete> <nodo>
```

---

## ❓ Resolución de Problemas

### `rosdep init` falla ("already initialized")

Normal si otro bootcamp ya lo inicializó en esta máquina — puedes ignorarlo y correr
directamente `rosdep update`.

### Conflictos de versión con otro proyecto ROS2/Python en la misma máquina

Es la razón principal por la que el bootcamp recomienda Docker: una instalación nativa
comparte el `PATH`/site-packages de Python con cualquier otro proyecto ROS2 que tengas.
`uv tool` ya aísla `ruff` y `mypy`; las dependencias no-ROS de semanas avanzadas van en
un `uv venv --system-site-packages` — los paquetes `ros-jazzy-*` en sí no se pueden aislar sin Docker.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Setup con Docker](con-docker.md) | **Setup sin Docker** | [Versiones del stack](../stack-versions.md) |

← [Volver al inicio del bootcamp](../../README.md)
