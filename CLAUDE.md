# CLAUDE.md

Instrucciones para agentes que trabajan sobre este repositorio.

## Qué es esto

Bootcamp de **Robótica con ROS2 (Jazzy)**, 33 semanas × 12 h = 396 horas, autoestudio.
De cero absoluto en robótica (con programación previa en Python y/o C++) a nivel
avanzado, en una **ruta única**: robot móvil (SLAM+Nav2), brazo (MoveIt2), manipulación
móvil y bloque avanzado. Malla e índice con estado: `bootcamp/README.md`. Por qué 33
semanas: `docs/decision-semanas.md`.

## Fuente de verdad de las convenciones

**[`.github/copilot-instructions.md`](.github/copilot-instructions.md)** contiene el
molde completo: malla curricular, estructura de cada semana, política de
dominios, stack pinneado, reglas de código Python/C++ y el checklist de publicación de
una semana.

Léelo **antes** de generar contenido. No deduzcas el patrón mirando archivos sueltos.

## Reglas duras (resumen — la fuente completa manda)

1. **Python (`rclpy`) y C++ (`rclcpp`) son de primera clase**, no uno opcional. Semanas
   01-06: cada concepto de comunicación se implementa en ambos. A partir de la semana
   07: Python por defecto, C++ obligatorio y justificado por escrito donde hay
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
7. **Anticopia por dominio/misión** (fijo en semana 01, sin tracks) — ver
   `docs/dominios.md`.
8. **Cero absoluto de robótica de verdad.** Cada término técnico (QoS, TF, costmap,
   IK...) se define la primera vez que aparece.
9. **Sin `solution/`.** El código comentado de los ejercicios es la solución.
10. **Tuteo, nunca voseo.** Nunca `pip` (siempre `uv`), nunca `npm` (siempre `pnpm`),
    nunca MySQL (siempre PostgreSQL).
11. **Paso a paso, nunca asumir**: cada comando completo con su salida esperada.
    Comentarios qué/para qué/impacto donde hacen falta, sin repetir.
12. **Tabla de tiempos de cada semana = 12 h exactas.** SVG dark, sin degradados,
    sans-serif, tantos como pida la teoría.
13. **Navegación al pie de todo documento**: tabla `Anterior | Actual | Siguiente`.

## Antes de dar por terminada una tanda

```bash
./scripts/verificar-enlaces.sh
./scripts/verificar-simulaciones.sh week-NN
```

Luego actualizar la fila de la semana en `bootcamp/README.md` y hacer **commit + push
directo a `main`** (proyecto de una sola persona: sin ramas ni PR).

## Estructura

```
bootcamp/README.md            índice de semanas con estado
bootcamp/week-NN-slug/        semanas 01-33, ruta única
docs/                         setup, stack-versions, dominios, decision-semanas, hardware-opcional
scripts/                      verificar-enlaces.sh, verificar-simulaciones.sh
assets/                       header del README
```

## Idioma

Español para la prosa y los comentarios educativos. Inglés para el código, los
identificadores, los nombres de paquetes/API de ROS2 y los mensajes de commit
(Conventional Commits: `feat(week-01): ...`).
