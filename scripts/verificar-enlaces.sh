#!/usr/bin/env bash
# Verifica integridad estructural del bootcamp:
#   1. Nombres de carpeta week-NN-slug bien formados (planas en bootcamp/ y
#      anidadas en bootcamp/track-{a,b}/).
#   2. Enlaces relativos en markdown que resuelven a una ruta real.
#   3. Sección "Navegación" en el README de cada semana.
#   4. SVG de 0-assets/ y assets/ con XML válido y enlazados desde algún .md.
#   5. Ninguna carpeta solution/ dentro de bootcamp/.
#   6. Dependencias Python con versión exacta (==) en pyproject.toml y requirements.txt.
#   7. Ninguna imagen Docker referenciada con tag :latest o sin tag.
#
# Uso: scripts/verificar-enlaces.sh
# Salida: lista de problemas encontrados; exit code 1 si hay al menos uno.

set -u
cd "$(dirname "$0")/.." || exit 1

fail=0

echo "== 1. Nombres de carpeta =="
while IFS= read -r d; do
  name=$(basename "$d")
  if ! [[ "$name" =~ ^week-[0-9]{2}-[a-z0-9_]+$ ]]; then
    echo "NOMBRE INVALIDO (week): $d"
    fail=1
  fi
done < <(find bootcamp -mindepth 1 -maxdepth 3 -type d -iname "week-*" 2>/dev/null)

while IFS= read -r d; do
  name=$(basename "$d")
  if ! [[ "$name" =~ ^track-[ab]$ ]]; then
    echo "NOMBRE INVALIDO (track): $d"
    fail=1
  fi
done < <(find bootcamp -mindepth 1 -maxdepth 1 -type d -iname "track-*" 2>/dev/null)

echo "== 2. Enlaces relativos en markdown =="
# ponytail: no parsea markdown de verdad, solo strip de fences ``` y luego
# quita `código inline` y hace grep de enlaces "](...)" y src="...". Falsos positivos: URLs con
# paréntesis anidados. Si el script reporta algo distinto a eso, es un enlace roto real.
while IFS= read -r f; do
  content=$(awk '/^[[:space:]]*```/{c=!c; next} !c' "$f" | sed -E 's/`[^`]*`//g')
  while IFS= read -r link; do
    [ -z "$link" ] && continue
    clean="${link%%#*}"
    [ -z "$clean" ] && continue
    case "$clean" in http*|\<http*|mailto:*|\#*|/*) continue ;; esac
    dir=$(dirname "$f")
    resolved=$(realpath -m "$dir/$clean")
    if [ ! -e "$resolved" ]; then
      echo "ENLACE ROTO: $f -> $link"
      fail=1
    fi
  done < <(printf '%s\n' "$content" \
             | grep -oE '\]\([^)]+\)|src="[^"]+"' \
             | sed -E 's/^\]\(//;s/\)$//;s/^src="//;s/"$//' \
             | sed -E 's/ +"[^"]*"$//')
done < <(find . -iname "*.md" -not -path "./.git/*" -not -path "*/.venv/*" \
           -not -path "*/build/*" -not -path "*/install/*" -not -path "*/log/*")

echo "== 3. Navegación anterior/siguiente en README de cada semana =="
# Solo el README.md en la raíz de una carpeta week-NN-* (no los de sus subcarpetas
# 1-teoria/, 2-practicas/, etc., que no llevan navegación propia).
while IFS= read -r rm; do
  parent=$(basename "$(dirname "$rm")")
  [[ "$parent" =~ ^week-[0-9]{2}-[a-z0-9_]+$ ]] || continue
  if ! grep -q "Navegación" "$rm"; then
    echo "SIN NAVEGACION: $rm"
    fail=1
  fi
done < <(find bootcamp -mindepth 2 -maxdepth 3 -iname "README.md" 2>/dev/null)

echo "== 4. SVG huérfanos y XML válido =="
while IFS= read -r svg; do
  base=$(basename "$svg")
  if ! python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" "$svg" 2>/dev/null; then
    echo "SVG MAL FORMADO (XML inválido; GitHub no lo renderiza): $svg"
    fail=1
  fi
  if ! grep -rqF "$base" --include="*.md" .; then
    echo "SVG HUERFANO (no enlazado desde ningún .md): $svg"
    fail=1
  fi
done < <(find bootcamp assets -iname "*.svg" 2>/dev/null)

echo "== 5. Carpetas prohibidas =="
while IFS= read -r d; do
  echo "CARPETA PROHIBIDA: $d"
  fail=1
done < <(find bootcamp -type d -name solution 2>/dev/null)

echo "== 6. Versiones exactas en dependencias Python =="
while IFS= read -r hit; do
  echo "VERSION NO EXACTA: $hit"
  fail=1
done < <(
  find . -name pyproject.toml -not -path "./.git/*" -not -path "*/.venv/*" -print0 \
    | xargs -0 grep -HnE '^\s*"[A-Za-z0-9_.\[\],-]+\s*(>=|~=|>|<|\^)' 2>/dev/null
  find . -name "requirements*.txt" -not -path "./.git/*" -not -path "*/.venv/*" -print0 \
    | xargs -0 grep -HnE '^[A-Za-z0-9_.\[\],-]+\s*(>=|~=|>|<)' 2>/dev/null
)

echo "== 7. Imagenes Docker sin tag exacto (:latest o sin tag) =="
while IFS= read -r hit; do
  echo "TAG NO PINNEADO: $hit"
  fail=1
done < <(
  find . -iname "Dockerfile*" -not -path "./.git/*" -print0 \
    | xargs -0 grep -HnE '^FROM\s+\S+(:latest)?\s*$' 2>/dev/null \
    | grep -vE ':[0-9]{8}|@sha256:'
)

if [ "$fail" -eq 0 ]; then
  echo "OK: sin problemas detectados."
fi
exit "$fail"
