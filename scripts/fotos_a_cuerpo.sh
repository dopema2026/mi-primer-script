#!/usr/bin/env bash
# Convierte fotos del producto + locución en el "cuerpo" del vídeo (9:16, 1080x1920, 30 fps).
# Cada foto lleva un zoom lento alterno (entrada/salida) y el reparto de tiempo
# se ajusta a la duración exacta de la locución. Coste en créditos: 0.
#
# Uso: scripts/fotos_a_cuerpo.sh <carpeta_fotos> <voz.mp3> <salida.mp4>
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "Uso: $0 <carpeta_fotos> <voz.mp3> <salida.mp4>" >&2
  exit 1
fi

FOTOS_DIR="$1"
VOZ="$2"
SALIDA="$3"
FPS=30

mapfile -t FOTOS < <(find "$FOTOS_DIR" -maxdepth 1 -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) | sort)
if [[ ${#FOTOS[@]} -eq 0 ]]; then
  echo "No hay fotos en $FOTOS_DIR" >&2
  exit 1
fi

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOZ")
N=${#FOTOS[@]}
# Frames por foto (redondeo hacia arriba para no quedarnos cortos de imagen).
FRAMES=$(python3 -c "import math; print(math.ceil($DUR * $FPS / $N))")

INPUTS=()
FILTER=""
for i in "${!FOTOS[@]}"; do
  INPUTS+=(-loop 1 -framerate "$FPS" -t "$(python3 -c "print($FRAMES / $FPS)")" -i "${FOTOS[$i]}")
  if (( i % 2 == 0 )); then
    ZOOM="min(1+0.0015*on,1.15)"        # acercamiento
  else
    ZOOM="max(1.15-0.0015*on,1)"        # alejamiento
  fi
  # Se reescala grande antes del zoompan para que el zoom no pixele.
  FILTER+="[$i:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
  FILTER+="zoompan=z='$ZOOM':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$FRAMES:s=1080x1920:fps=$FPS,"
  FILTER+="setsar=1,format=yuv420p[v$i];"
done
for i in "${!FOTOS[@]}"; do FILTER+="[v$i]"; done
FILTER+="concat=n=$N:v=1:a=0[v]"

ffmpeg -y -hide_banner -loglevel error "${INPUTS[@]}" -i "$VOZ" \
  -filter_complex "$FILTER" -map "[v]" -map "$N:a" \
  -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 192k -ar 44100 -ac 2 \
  -t "$DUR" "$SALIDA"

echo "Cuerpo creado: $SALIDA (${DUR}s, $N fotos)"
