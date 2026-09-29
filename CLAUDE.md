# CLAUDE.md

Instrucciones para agentes que trabajan sobre este repositorio.

## Qué es esto

Bootcamp de **Robótica con ROS2 (Jazzy)**, 19 semanas, 190 horas, autoestudio. De cero
absoluto en robótica (con programación previa en Python y/o C++) a un robot móvil
autónomo con SLAM+Nav2 (Track A) o un brazo manipulador con visión (Track B).

## Fuente de verdad de las convenciones

**[`.github/copilot-instructions.md`](.github/copilot-instructions.md)** contiene el
molde completo: malla curricular, estructura de cada semana, política de tracks y
dominios, stack pinneado, reglas de código Python/C++ y el checklist de publicación de
una semana.

Léelo **antes** de generar contenido. No deduzcas el patrón mirando archivos sueltos.

## Reglas duras (resumen — la fuente completa manda)

1. **Python (`rclpy`) y C++ (`rclcpp`) son de primera clase**, no uno opcional. Semanas
   01-05: cada concepto de comunicación se implementa en ambos. A partir de la semana
   06: Python por defecto, C++ obligatorio y justificado por escrito donde hay
   restricción de latencia/frecuencia fija o el framework solo expone el punto de
   extensión en C++ (`pluginlib` de Nav2/MoveIt2).
2. **Todo corre primero en simulación** (Gazebo Harmonic, headless para verificación).
   El hardware físico siempre es una sección opcional al final del README de la
   semana, nunca bloqueante para evaluar.
3. **Stack fijo**: ROS2 Jazzy / Ubuntu 24.04 / Gazebo Harmonic / Nav2 jazzy / MoveIt2
   jazzy — versiones exactas en `docs/stack-versions.md`.
4. **Entorno Docker obligatorio** (`osrf/ros:jazzy-desktop-full`, tag de fecha, nunca
   `:latest`).
5. **Todo código compila/lintea limpio**: Python con `ruff`+`mypy`; C++ con
   `-Wall -Wextra -Wpedantic -Werror` + `clang-format`.
6. **Ningún plugin `pluginlib` se escribe en Python** — no está soportado.
7. **Política de dos niveles anticopia**: track (A/B, fijo en semana 12) + dominio/misión
   (fijo en semana 01) — ver `docs/tracks.md`.
8. **Cero absoluto de robótica de verdad.** Cada término técnico (QoS, TF, costmap,
   IK...) se define la primera vez que aparece.
9. **Sin `solution/`.** El código comentado de los ejercicios es la solución.

## Antes de dar por terminada una tanda

```bash
./scripts/verificar-enlaces.sh
./scripts/verificar-simulaciones.sh week-NN
```

## Estructura

```
bootcamp/week-NN-slug/        semanas 01-12, comunes a ambos tracks
bootcamp/track-a/week-NN-*/   semanas 13-19, Track A (SLAM+Nav2)
bootcamp/track-b/week-NN-*/   semanas 13-19, Track B (MoveIt2+visión)
docs/                         setup, stack-versions, tracks, hardware-opcional
scripts/                      verificar-enlaces.sh, verificar-simulaciones.sh
assets/                       header del README
```

## Idioma

Español para la prosa y los comentarios educativos. Inglés para el código, los
identificadores, los nombres de paquetes/API de ROS2 y los mensajes de commit
(Conventional Commits: `feat(week-01): ...`).
