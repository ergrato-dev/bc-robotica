# 🔒 Política de Seguridad en Dependencias

> **Audiencia**: Instructores, contributors y mantenedores del bootcamp.

---

## 🥇 Regla de Oro: SIEMPRE versiones exactas, nunca `:latest`

```dockerfile
# ✅ CORRECTO — tag de fecha, reproducible y auditable
FROM osrf/ros:jazzy-desktop-full-20260901

# ❌ PROHIBIDO — se mueve solo, puede traer un cambio que rompe todo el bootcamp
FROM osrf/ros:jazzy-desktop-full
FROM osrf/ros:latest
```

```toml
# ✅ CORRECTO — dependencias Python con versión exacta
ruff==0.8.6
mypy==1.13.0
opencv-python==4.10.0.84

# ❌ PROHIBIDO
ruff>=0.8
opencv-python
```

Los paquetes `apt` (`ros-jazzy-*`) se resuelven por distro (Jazzy) y no llevan `==`,
pero se fijan indirectamente pinneando el **tag de fecha de la imagen Docker base**:
esa fecha determina exactamente qué versión de cada paquete `apt ros-jazzy-*` se
instaló. Cambiar el tag de fecha es la única forma soportada de "actualizar" el stack
apt completo, nunca `apt upgrade` suelto dentro del contenedor.

### ¿Por qué no rangos abiertos?

| Especificador | Problema |
|---|---|
| `:latest` / imagen sin tag | Cambia sin aviso; puede romper compatibilidad Nav2/MoveIt2/Gazebo entre sí |
| `>=X.Y.Z` (Python) | Instala la última disponible; puede traer una versión con CVE o breaking changes |
| Sin versión | No reproducible. Cada build puede dar un resultado diferente |

### ¿Por qué sí versiones exactas?

- **Reproducibilidad**: todos los estudiantes corren exactamente el mismo stack
- **Compatibilidad cruzada**: ROS2/Gazebo/Nav2/MoveIt2 son varios proyectos
  independientes que solo garantizan compatibilidad entre versiones específicas — un
  `apt upgrade` parcial puede desalinearlos
- **Auditabilidad**: se puede revisar CVEs para una versión específica
- **Estabilidad**: el código del bootcamp siempre funciona igual

---

## 📋 Versiones pineadas — Mapa de referencia

La tabla de referencia vive en [stack-versions.md](stack-versions.md) para no
duplicarla.

---

## 🔄 Procedimiento para actualizar versiones

Cuando se quiera actualizar el stack (por CVE nuevo, funcionalidad necesaria, o nueva
release de imagen `osrf/ros`):

### 1. Verificar el nuevo tag de imagen y sus paquetes

```bash
# Listar tags disponibles de la imagen base
docker run --rm quay.io/skopeo/stable list-tags docker://docker.io/osrf/ros | grep jazzy-desktop-full

# Confirmar versiones de Nav2/MoveIt2/Gazebo que trae el nuevo tag
docker run --rm osrf/ros:jazzy-desktop-full-NUEVA_FECHA bash -c \
  "apt list --installed 2>/dev/null | grep -E 'navigation2|moveit|gz-sim'"
```

### 2. Auditar dependencias Python con `pip-audit`

```bash
echo "opencv-python==NUEVA_VERSION" > /tmp/check.txt
uvx pip-audit -r /tmp/check.txt -s osv
```

### 3. Actualizar el tag en todos los archivos

```bash
# Script de reemplazo masivo (desde la raíz del repo)
grep -rl "osrf/ros:jazzy-desktop-full-" --include="Dockerfile*" . \
  | xargs sed -i 's/jazzy-desktop-full-[0-9]\{8\}/jazzy-desktop-full-NUEVA_FECHA/g'
```

### 4. Verificar que no quedaron `:latest` ni rangos abiertos

```bash
# Falla si queda algún :latest o rango (>=, ~=, ^) en Dockerfile/pyproject/requirements
scripts/verificar-enlaces.sh
```

### 5. Re-verificar simulaciones

```bash
# El nuevo tag puede cambiar comportamiento de Gazebo/Nav2 — re-correr en todas las semanas
for w in bootcamp/week-*/ bootcamp/track-*/week-*/; do
  scripts/verificar-simulaciones.sh "$(basename "$w")"
done
```

### 6. Actualizar este documento y `stack-versions.md`

---

## 🛡️ Próxima auditoría recomendada

- **Frecuencia**: cada 3 meses, o ante cualquier aviso de seguridad de ROS2/Gazebo
- **Herramienta**: `pip-audit` para Python + revisión de release notes de
  `osrf/ros`, Nav2 y MoveIt2
- **Responsable**: Mantenedor del bootcamp

---

_Documento creado: 29/09/2026_
