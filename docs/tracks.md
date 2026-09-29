# 🔀 Política de Tracks y Dominios

El bootcamp usa **dos niveles** de elección para evitar plagio en cohorte y para que
cada estudiante construya **su** sistema durante 19 semanas.

## Nivel 1 — Track (obligatorio, semanas 13-19)

Se fija en la **Semana 12** (checkpoint de integración), no cambia después.

| Track | Nombre | Stack | Capstone |
|---|---|---|---|
| **A** | Móvil Autónomo | SLAM (`slam_toolbox`) + AMCL + Nav2 | Robot que mapea, se localiza y navega de forma autónoma evitando obstáculos |
| **B** | Manipulador | MoveIt2 + visión (OpenCV/YOLO) | Brazo que detecta un objeto por visión y ejecuta pick&place |

Las semanas 01-12 son **100% comunes** a ambos tracks. La bifurcación ocurre justo
al cerrar la Fase 3 (cinemática), que es el punto donde ambos tracks ya tienen la base
que necesitan (TF2, sensores, percepción, cinemática).

## Nivel 2 — Misión/dominio dentro del track (semana 01)

El estudiante elige (o el instructor asigna) una misión en la **Semana 01** y la
mantiene las 19 semanas — se escribe en el README de su repositorio. Reduce el plagio
entre dos estudiantes del mismo track: distinto mundo Gazebo, distintas reglas de
negocio.

### Catálogo — Track A (Móvil)

| # | Misión | Mundo Gazebo | Detalle que obliga a pensar, no copiar |
|---|---|---|---|
| 1 | 📦 Robot de almacén | Estantes y pasillos | Debe evitar zonas restringidas |
| 2 | 🚚 Robot de reparto en campus | Exterior con curvas | Debe esperar en "zonas de cruce" |
| 3 | 🔦 Rover de inspección industrial | Túnel/planta industrial | Debe reportar waypoints de interés (con foto) |
| 4 | 🧹 Robot de limpieza de oficina | Oficina con habitaciones | Cobertura completa, no solo punto-a-punto |
| 5 | 🌾 Rover agrícola | Filas de cultivo simuladas | Debe seguir surcos, no rutas libres |

### Catálogo — Track B (Manipulador)

| # | Misión | Mundo Gazebo | Detalle que obliga a pensar, no copiar |
|---|---|---|---|
| 1 | 🎨 Clasificador por color | Mesa con piezas de colores | Reglas de clasificación distintas por color |
| 2 | 🧩 Ensamblador simple | Mesa con 2 piezas a combinar | El orden de ensamblado importa |
| 3 | 📚 Bibliotecario de mesa | Mesa con marcadores ArUco | Ordenar por código, no por color |
| 4 | ☕ Servicio de café (juguete) | Mesa con vasos | Secuencia con estado (vaso lleno/vacío) |
| 5 | 🔬 Clasificador de muestras | Mesa con tubos etiquetados | Debe verificar etiqueta antes de mover |

## Reglas

- **La misión se define en la Semana 01** y el track en la Semana 12; ninguno cambia
  después: el sistema se acumula durante toda la Fase 4 y el capstone
- **Con instructor**: se asigna una misión distinta a cada estudiante del grupo por
  track. Con más de 5 estudiantes en el mismo track, se combinan misión + variante
  (ej. "almacén de repuestos" y "almacén de alimentos")
- **Copiar el proyecto de otra misión o del otro track** es 0 en Producto esa semana.
  Ver [`CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md)
- Las semanas 18-19 (capstone) comparten la misma estructura de secciones para ambos
  tracks, pero el contenido es del sistema propio de cada estudiante
