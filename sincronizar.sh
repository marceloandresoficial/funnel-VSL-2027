#!/bin/zsh
# ── Sincronización automática con GitHub ─────────────────────────────
# Si no hay cambios, no hace absolutamente nada.
# Si los hay: commit y push. Si no hay red, el commit se queda local
# y el siguiente intento lo sube. Nunca se pierde trabajo.
#
#   ./sincronizar.sh          → una pasada
#   Se ejecuta solo cada 15 min vía com.marcelo.funnel.sync (launchd)

cd "${0:A:h}" || exit 1
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin"

REGISTRO=".sync.log"
di() { echo "$(date '+%Y-%m-%d %H:%M:%S')  $1" >> "$REGISTRO"; }

# Nada que hacer
if [ -z "$(git status --porcelain)" ] && \
   [ -z "$(git log origin/main..HEAD --oneline 2>/dev/null)" ]; then
  exit 0
fi

# Nunca subir a un repositorio público: las fotos y cifras de los
# clientes no salen de aquí si alguien cambia la visibilidad.
URL=$(git remote get-url origin 2>/dev/null)
NOMBRE=${URL##*/}; NOMBRE=${NOMBRE%.git}; DUENO=${URL#*:}; DUENO=${DUENO%%/*}
if curl -s -o /dev/null -w '%{http_code}' --max-time 10 \
     "https://api.github.com/repos/$DUENO/$NOMBRE" | grep -q '^200$'; then
  di "DETENIDO · el repositorio es PÚBLICO. Nada subido."
  exit 2
fi

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  N=$(git diff --cached --numstat | wc -l | tr -d ' ')
  git commit -q -m "Sincronización automática · $(date '+%d %b %Y, %H:%M')

$N archivo/s.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" || { di "commit falló"; exit 1; }
  di "commit de $N archivo/s"
fi

if git push -q origin main 2>>"$REGISTRO"; then
  di "subido a $NOMBRE"
else
  di "sin red o rechazado — se reintenta en 15 min"
  exit 1
fi
