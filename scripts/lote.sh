#!/usr/bin/env bash
# Regla "1 cuerpo + N hooks": monta un vídeo final por cada hook de un producto.
#
# Estructura esperada en productos/<producto>/:
#   cuerpo.mp4            (o fotos/ + voz.mp3, y se genera solo)
#   hooks/*.mp4           un vídeo por gancho
#   musica.mp3            opcional (si no, se usa la primera de biblioteca/musica/)
#   subtitulos.srt        opcional, subtítulos del cuerpo (tiempos desde 0)
#
# Uso: scripts/lote.sh productos/<producto>
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Uso: $0 productos/<producto>" >&2
  exit 1
fi

DIR="${1%/}"
SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
RAIZ="$(dirname "$SCRIPTS")"
SALIDA_DIR="$DIR/finales"
mkdir -p "$SALIDA_DIR"

if [[ ! -f "$DIR/cuerpo.mp4" ]]; then
  if [[ -d "$DIR/fotos" && -f "$DIR/voz.mp3" ]]; then
    "$SCRIPTS/fotos_a_cuerpo.sh" "$DIR/fotos" "$DIR/voz.mp3" "$DIR/cuerpo.mp4"
  else
    echo "Falta $DIR/cuerpo.mp4 (o $DIR/fotos/ + $DIR/voz.mp3)" >&2
    exit 1
  fi
fi

MUSICA=""
if [[ -f "$DIR/musica.mp3" ]]; then
  MUSICA="$DIR/musica.mp3"
else
  MUSICA="$(find "$RAIZ/biblioteca/musica" -maxdepth 1 -type f \( -iname '*.mp3' -o -iname '*.wav' \) | sort | head -1 || true)"
fi

SRT=""
if [[ -f "$DIR/subtitulos.srt" ]]; then
  # Los subtítulos del cuerpo se desplazan por la duración de cada hook.
  SRT_BASE="$DIR/subtitulos.srt"
fi

shopt -s nullglob
HOOKS=("$DIR"/hooks/*.mp4)
if [[ ${#HOOKS[@]} -eq 0 ]]; then
  echo "No hay hooks en $DIR/hooks/" >&2
  exit 1
fi

for HOOK in "${HOOKS[@]}"; do
  NOMBRE="$(basename "$HOOK" .mp4)"
  if [[ -n "${SRT_BASE:-}" ]]; then
    D_HOOK=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$HOOK")
    SRT="$SALIDA_DIR/.$NOMBRE.srt"
    python3 "$SCRIPTS/desplazar_srt.py" "$SRT_BASE" "$D_HOOK" "$SRT"
  fi
  "$SCRIPTS/montar.sh" "$HOOK" "$DIR/cuerpo.mp4" "$SALIDA_DIR/$NOMBRE.mp4" "$MUSICA" "$SRT"
done

echo "Listo: ${#HOOKS[@]} vídeos en $SALIDA_DIR"
