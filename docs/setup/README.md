# ⚙️ Configuración del Entorno

Antes de empezar el bootcamp necesitas un entorno con ROS2 Jazzy, Gazebo Harmonic y las
herramientas GUI (RViz2, Gazebo) funcionando. Tienes dos opciones:

## 🔀 Elige tu Opción

| | 🐳 Con Docker | 🐧 Sin Docker |
|---|---|---|
| **Dificultad inicial** | Baja | Alta (ROS2 nativo es sensible a la versión de Ubuntu) |
| **Consistencia** | ✅ Idéntico en todas las máquinas | ⚠️ Depende de tu sistema |
| **Requisitos** | Docker 27.5.1, GPU/X11 configurado | Ubuntu 24.04 exacto |
| **GUI (RViz2/Gazebo)** | ✅ Vía WSLg/X11 passthrough documentado | ✅ Nativo |
| **Recomendado para** | Todos los estudiantes | Quien ya tenga Ubuntu 24.04 nativo |

## ✅ Opción Recomendada: Docker

Docker es el entorno **oficial y obligatorio** del bootcamp (ver `.github/copilot-instructions.md`).
Garantiza que todos los estudiantes trabajen con exactamente la misma versión de ROS2,
Gazebo, Nav2 y MoveIt2, independientemente del sistema operativo — y evita instalar ROS2
directamente sobre el sistema operativo de tu máquina.

→ [Guía: Configuración con Docker](con-docker.md)

## 🔧 Opción Alternativa: Nativo (Ubuntu 24.04)

Si ya tienes Ubuntu 24.04 nativo (no WSL2) y prefieres instalar ROS2 directamente sobre
el sistema, es una alternativa válida — pero pierdes la reproducibilidad de versiones
que da Docker, y algunas prácticas del bootcamp (headless CI, `docs/stack-versions.md`)
asumen la imagen Docker oficial.

→ [Guía: Configuración sin Docker](sin-docker.md)

---

## 📋 ¿Cuál Elegir?

```
¿Windows o macOS?
        │
        ├── SÍ ──► Docker + WSLg (Windows) / Docker Desktop (macOS) — única opción viable
        │
        └── NO, Linux ──► ¿Ubuntu 24.04 exacto?
                        │
                        ├── SÍ ──► Cualquiera de las dos; Docker sigue siendo la recomendada
                        │
                        └── NO (otra distro/versión) ──► Docker (evita conflictos con ROS2 del sistema)
```

---

→ Volver a [docs/README.md](../README.md)
