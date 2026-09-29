#!/usr/bin/env bash
# Levanta headless cada mundo Gazebo de una semana y valida que arranca sin error.
# Equivalente robótico de compilar-starters.sh (bc-cpp): aquí no hay "compilación",
# hay "¿el mundo/los nodos declarados arrancan sin crashear?".
#
# Uso: scripts/verificar-simulaciones.sh week-NN [timeout_segundos]
#   Busca la carpeta bootcamp/week-NN* o bootcamp/track-*/week-NN* y prueba cada
#   mundo .sdf/.world que encuentre bajo ella (típicamente en 2-practicas/ o 3-proyecto/).
#
# Un starter tal cual está en el repo puede no tener aún todos los nodos completos
# (patrón "descomentar"): lo que se exige aquí es que Gazebo headless arranque el
# mundo y no crashee en el timeout, no que la lógica del ejercicio ya funcione.
#
# Exit code 1 si algún mundo no arranca o Gazebo crashea.

set -u
cd "$(dirname "$0")/.." || exit 1

week="${1:-}"
timeout_s="${2:-20}"

if [ -z "$week" ]; then
  echo "Uso: $0 week-NN [timeout_segundos]" >&2
  exit 2
fi

dir=$(find bootcamp -mindepth 1 -maxdepth 3 -type d -name "${week}*" | head -1)
if [ -z "$dir" ]; then
  echo "No existe ninguna carpeta bootcamp/**/${week}*" >&2
  exit 2
fi

worlds=$(find "$dir" \( -iname "*.sdf" -o -iname "*.world" \) 2>/dev/null)
if [ -z "$worlds" ]; then
  echo "$dir: sin mundos Gazebo (.sdf/.world) — nada que verificar en esta semana."
  exit 0
fi

fail=0
while IFS= read -r world; do
  log=$(mktemp)
  # -s: servidor sin GUI. -r: arranca corriendo. --iterations: cierra solo tras N pasos
  # en vez de correr indefinidamente (headless no tiene ventana que cerrar a mano).
  if timeout "${timeout_s}s" gz sim -s -r --headless-rendering \
      --iterations 100 "$world" >"$log" 2>&1; then
    echo "$world: ✅ ARRANCA sin error"
  else
    code=$?
    if [ "$code" -eq 124 ]; then
      echo "$world: 🔴 TIMEOUT (no arrancó/no cerró en ${timeout_s}s): $(tail -1 "$log")"
    else
      echo "$world: 🔴 CRASH (exit $code): $(grep -m1 -iE 'error|segfault|abort' "$log")"
    fi
    fail=1
  fi
  rm -f "$log"
done <<< "$worlds"

exit "$fail"
