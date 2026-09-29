# 🐳 Configuración con Docker

Esta es la opción **oficial y obligatoria** del bootcamp. Docker garantiza un entorno
ROS2 idéntico para todos los estudiantes, con la complicación extra de que RViz2 y
Gazebo son aplicaciones GUI con aceleración gráfica: esta guía cubre ese passthrough
paso a paso.

## 📋 Requisitos Previos

| Herramienta | Versión | Verificar |
|-------------|---------|-----------|
| Docker | 27.5.1 | `docker --version` |
| Docker Compose | 2.32.4 | `docker compose version` |
| Git | 2.43.0 | `git --version` |
| VS Code | 1.95.3 con extensión Dev Containers | (recomendado) |

---

## 1. Instalar Docker

### Windows (WSL2 + WSLg) — camino recomendado del bootcamp

1. Instalar/actualizar WSL2: `wsl --install` (PowerShell como administrador)
2. Instalar **Docker Desktop** desde [docker.com](https://docker.com/products/docker-desktop)
   con el backend WSL2 habilitado (por defecto en instalaciones recientes)
3. **WSLg** (GUI de Linux en Windows sin servidor X externo) viene incluido en WSL2
   desde 2021 — no instalar VcXsrv ni ningún servidor X aparte

```powershell
wsl --update
wsl --version
# WSLg version debe aparecer en la salida
```

### Ubuntu / Debian (nativo o dentro de WSL2)

```bash
sudo apt update
sudo apt install docker.io docker-compose-v2
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# Cierra sesión y vuelve a entrar para que el grupo tenga efecto
```

### macOS

```bash
# Docker Desktop (interfaz gráfica)
# Descargar desde https://docker.com/products/docker-desktop
```

> macOS no tiene X11/WSLg nativo: RViz2/Gazebo se ven vía XQuartz. Ver sección
> "Problemas específicos de macOS" al final.

---

## 2. Verificar la Instalación

```bash
docker --version
docker compose version
docker run --rm hello-world
```

Si el último comando muestra `Hello from Docker!`, todo está bien.

---

## 3. Clonar el Repositorio

```bash
git clone https://github.com/ergrato-dev/bc-robotica.git
cd bc-robotica
```

---

## 4. Levantar el Contenedor Base

```bash
# Desde la raíz del repo (usa docs/stack-versions.md como referencia del Dockerfile)
docker compose build
docker compose up -d
docker compose exec ros2 bash
```

Dentro del contenedor, ROS2 ya está en el `PATH` (source automático vía
`/etc/bash.bashrc`):

```bash
ros2 doctor
# No debe reportar errores críticos
```

---

## 5. Verificar GUI (RViz2 / Gazebo)

### Windows (WSLg)

No requiere configuración extra: `DISPLAY` se propaga automáticamente desde WSLg al
contenedor gracias a `network_mode: host` en `docker-compose.yml`.

```bash
docker compose exec ros2 rviz2
# Debe abrir una ventana en el escritorio de Windows
```

### Linux nativo (X11)

```bash
xhost +local:docker
export DISPLAY=:0
docker compose exec ros2 rviz2
```

> `xhost +local:docker` se ejecuta en el **host**, no dentro del contenedor. Revertir
> con `xhost -local:docker` al terminar por higiene, aunque no es estrictamente
> necesario en una máquina de un solo usuario.

### macOS (XQuartz)

```bash
brew install --cask xquartz
# Abrir XQuartz → Preferencias → Seguridad → habilitar "Allow connections from network clients"
open -a XQuartz
export DISPLAY=host.docker.internal:0
docker compose exec ros2 rviz2
```

Si la ventana no abre, revisa la sección de problemas al final.

---

## 6. Ejecutar una Semana

```bash
# Cada ejercicio/proyecto trae su propio paquete ROS2 dentro de starter/
cd bootcamp/week-01-fundamentos_ros2_y_workspace/2-practicas/01-ejercicio-publisher-py/starter
colcon build --symlink-install
source install/setup.bash
ros2 run <paquete> <nodo>
```

Para simulación headless (verificación tipo CI, sin GUI):

```bash
gz sim -s -r <mundo>.sdf --headless-rendering
```

---

## 7. Comandos del Día a Día

```bash
docker compose up -d           # Levantar en segundo plano
docker compose exec ros2 bash  # Shell interactiva
docker compose logs -f ros2    # Ver logs
docker compose down            # Detener
docker compose build --no-cache && docker compose up -d   # Rebuild forzado
```

---

## 8. VS Code con Dev Containers (Recomendado)

1. Instalar extensión [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Abrir la paleta de comandos (`Ctrl+Shift+P`)
3. `Dev Containers: Reopen in Container`

Esto habilita autocompletado de ROS2 (extensión `ms-iot.vscode-ros`), linting y
debugging directamente en el entorno del contenedor.

---

## ❓ Resolución de Problemas

### `permission denied` al ejecutar docker

```bash
sudo usermod -aG docker $USER
# Cierra sesión y vuelve a entrar (o ejecuta: newgrp docker)
```

### RViz2/Gazebo no abren ventana (Linux)

```bash
echo $DISPLAY          # debe tener un valor, ej. :0 o :1
xhost +local:docker     # en el host, no en el contenedor
```

### RViz2/Gazebo no abren ventana (WSL2)

```powershell
wsl --update
wsl --shutdown
# Reabrir WSL2 y reintentar — WSLg necesita estar en su versión más reciente
```

### Gazebo va muy lento / sin aceleración

```bash
# Dentro del contenedor, forzar renderizado por software si no hay GPU pass-through
export LIBGL_ALWAYS_SOFTWARE=1
gz sim <mundo>.sdf
```

### Problemas específicos de macOS

Si XQuartz no conecta: revisa que "Allow connections from network clients" esté
habilitado y reinicia XQuartz. El rendimiento de Gazebo en macOS vía XQuartz es
notablemente peor que en Linux/WSLg — para las semanas de simulación pesada (06 en
adelante) se recomienda usar `--headless-rendering` y verificar el resultado con
`ros2 topic echo`/`ros2 bag` en vez de la ventana GUI cuando sea posible.

### Imagen desactualizada

```bash
docker compose pull
docker compose build --no-cache && docker compose up -d
```

---

→ Volver a [setup/README.md](README.md)
