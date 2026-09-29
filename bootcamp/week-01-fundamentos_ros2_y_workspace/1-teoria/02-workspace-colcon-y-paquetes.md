# Workspace, `colcon` y paquetes

> Todo lo que vas a construir en ROS2 vive dentro de un paquete, y todos los paquetes se compilan juntos con una sola herramienta: `colcon`.

## 🎯 Objetivos

- Entender la estructura de un workspace ROS2 (`src/`, `build/`, `install/`, `log/`)
- Diferenciar un paquete `ament_python` de uno `ament_cmake`
- Compilar un workspace con `colcon build` y activarlo con `source install/setup.bash`

## 1. Qué problema resuelve

Un sistema robótico real tiene decenas de paquetes: unos en Python, otros en C++, cada
uno con sus propias dependencias. Necesitas una forma de:

1. Declarar qué depende de qué
2. Compilar todo en el orden correcto (C++ necesita compilación; Python no, pero
   igual necesita "instalarse" para que sus mensajes/launch files se vean)
3. Activar todo eso en tu shell sin tener que hacerlo a mano paquete por paquete

`colcon` (COLlective CONstruction) es la herramienta que hace esto. No es específica de
un lenguaje: sabe compilar paquetes `ament_cmake` (C++) y `ament_python` a la vez, en
el orden que dicten sus dependencias declaradas.

## 2. Cómo funciona: la estructura del workspace

```
mi_workspace/
├── src/                    # tú escribes aquí: un paquete por subcarpeta
│   ├── paquete_python/
│   └── paquete_cpp/
├── build/                  # artefactos intermedios de compilación (generado)
├── install/                # lo que queda "instalado" y listo para usar (generado)
│   └── setup.bash          # lo activas con: source install/setup.bash
└── log/                    # logs de cada build (generado)
```

`build/`, `install/` y `log/` **nunca se versionan** (van en `.gitignore`): se
regeneran con `colcon build`. Solo `src/` es tuyo.

```bash
# Desde la raíz del workspace
colcon build --symlink-install
source install/setup.bash
```

`--symlink-install` crea enlaces simbólicos en vez de copiar archivos — así, si editas
un archivo Python de tu paquete, el cambio se ve sin recompilar. Para C++ sí hace falta
recompilar siempre: los enlaces solo ayudan con los ficheros no compilados
(`package.xml`, launch files, recursos).

## 3. Cómo se escribe: anatomía de un paquete

Todo paquete ROS2 tiene un `package.xml` en su raíz — es su tarjeta de identidad:
nombre, versión, dependencias, mantenedor. `colcon` lo lee para saber el orden de
compilación.

### Paquete `ament_python`

```
paquete_python/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
│   └── paquete_python        # archivo vacío, marca el paquete como "recurso" ROS2
└── paquete_python/            # el módulo Python de verdad
    ├── __init__.py
    └── mi_nodo.py
```

```xml
<!-- package.xml -->
<?xml version="1.0"?>
<package format="3">
  <name>paquete_python</name>
  <version>0.1.0</version>
  <description>Ejemplo de paquete ament_python</description>
  <maintainer email="tu@email.com">Tu Nombre</maintainer>
  <license>CC-BY-NC-SA-4.0</license>

  <exec_depend>rclpy</exec_depend>
  <exec_depend>std_msgs</exec_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

```python
# setup.py
from setuptools import find_packages, setup

package_name = "paquete_python"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages",
            [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    entry_points={
        "console_scripts": [
            "mi_nodo = paquete_python.mi_nodo:main",
        ],
    },
)
```

El `entry_points` es lo que permite correr `ros2 run paquete_python mi_nodo` — `colcon`
lo registra como ejecutable durante la instalación.

### Paquete `ament_cmake` (C++)

```
paquete_cpp/
├── package.xml
├── CMakeLists.txt
├── include/paquete_cpp/
└── src/
    └── mi_nodo.cpp
```

```cmake
# CMakeLists.txt mínimo
cmake_minimum_required(VERSION 3.28)
project(paquete_cpp)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(mi_nodo src/mi_nodo.cpp)
target_include_directories(mi_nodo PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_compile_features(mi_nodo PUBLIC cxx_std_17)
ament_target_dependencies(mi_nodo rclcpp std_msgs)

install(TARGETS mi_nodo DESTINATION lib/${PROJECT_NAME})

ament_package()
```

`ament_target_dependencies` es el pegamento que conecta CMake con el sistema de
paquetes de ROS2 — sin él, el compilador no encontraría los headers de `rclcpp`.

## 4. Antipatrones

- ❌ **Editar archivos dentro de `build/` o `install/`.** Se sobrescriben en el
  siguiente `colcon build`; el único lugar donde editas código es `src/`
- ❌ **Versionar `build/`, `install/`, `log/`.** Van en `.gitignore` desde el primer
  commit del workspace
- ❌ **Un paquete que mezcla nodos Python y C++ en el mismo `ament_python`.** Si
  necesitas ambos lenguajes en el mismo proyecto (como en este bootcamp), son dos
  paquetes separados — uno `ament_python`, otro `ament_cmake` — que pueden vivir en el
  mismo repositorio

## 5. Trucos

- `colcon build --packages-select mi_paquete` — compila solo un paquete, no todo el
  workspace (mucho más rápido en workspaces grandes)
- `colcon build --symlink-install` — úsalo siempre en desarrollo con Python
- `colcon test --packages-select mi_paquete && colcon test-result --verbose` — corre y
  muestra el detalle de los tests de un paquete
- `ros2 pkg list | grep mi_paquete` — confirma que tu paquete quedó registrado tras el
  build

## 📚 Recursos Adicionales

- [Creating a workspace — ROS2 Jazzy docs](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)
- [Colcon documentation](https://colcon.readthedocs.io/)

## ✅ Checklist de Verificación

- [ ] Puedo explicar la diferencia entre `src/`, `build/`, `install/` y `log/`
- [ ] Sé cuándo un paquete es `ament_python` y cuándo `ament_cmake`
- [ ] Compilé un workspace con `colcon build --symlink-install` y lo activé con
      `source install/setup.bash`
