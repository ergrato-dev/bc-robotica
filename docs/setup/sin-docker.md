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
  ros-jazzy-moveit \
  ros-jazzy-cv-bridge ros-jazzy-image-transport
```

## 4. Instalar herramientas Python

```bash
python3 -m pip install --user --break-system-packages \
  ruff==0.8.6 mypy==1.13.0 opencv-python==4.10.0.84
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
cd bootcamp/week-01-fundamentos_ros2_y_workspace/2-practicas/01-ejercicio-publisher-py/starter
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
Considera un `venv` para las dependencias Python puras (`ruff`, `mypy`, `opencv-python`)
si esto te afecta — los paquetes `ros-jazzy-*` en sí no se pueden aislar sin Docker.

---

→ Volver a [setup/README.md](README.md)
