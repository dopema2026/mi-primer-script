#!/usr/bin/env bash
# Une un hook + el cuerpo en un vídeo final listo para TikTok (1080x1920, 30 fps).
# - Si el hook no trae audio, se le añade silencio.
# - La música (opcional) entra después del hook, a -18 dB, con fundido de salida.
# - Los subtítulos (opcional, .srt) se queman en la imagen.
#
# Uso: scripts/montar.sh <hook.mp4> <cuerpo.mp4> <salida.mp4> [musica.mp3] [subtitulos.srt]
set -euo pipefail

if [[ $# -lt 3 || $# -gt 5 ]]; then
  echo "Uso: $0 <hook.mp4> <cuerpo.mp4> <salida.mp4> [musica.mp3] [subtitulos.srt]" >&2
  exit 1
fi

HOOK="$1"
CUERPO="$2"
SALIDA="$3"
MUSICA="${4:-}"
SRT="${5:-}"

duracion() { ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }
tiene_audio() { [[ -n "$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$1")" ]]; }

D_HOOK=$(duracion "$HOOK")
D_CUERPO=$(duracion "$CUERPO")
D_TOTAL=$(python3 -c "print($D_HOOK + $D_CUERPO)")

NORM="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p"
ANORM="aresample=44100,aformat=channel_layouts=stereo"

INPUTS=(-i "$HOOK" -i "$CUERPO")
if tiene_audio "$HOOK"; then
  A_HOOK="[0:a]$ANORM,atrim=0:$D_HOOK,apad=whole_dur=$D_HOOK[ah]"
else
  A_HOOK="anullsrc=r=44100:cl=stereo,atrim=0:$D_HOOK[ah]"
fi

FILTER="[0:v]$NORM[vh];[1:v]$NORM[vc];$A_HOOK;[1:a]$ANORM[ac];"
FILTER+="[vh][ah][vc][ac]concat=n=2:v=1:a=1[vcat][acat];"

if [[ -n "$MUSICA" ]]; then
  INPUTS+=(-stream_loop -1 -i "$MUSICA")
  FADE_INI=$(python3 -c "print(max($D_CUERPO - 1.5, 0))")
  DELAY_MS=$(python3 -c "print(int($D_HOOK * 1000))")
  FILTER+="[2:a]$ANORM,atrim=0:$D_CUERPO,volume=-18dB,afade=t=out:st=$FADE_INI:d=1.5,"
  FILTER+="adelay=$DELAY_MS|$DELAY_MS[am];"
  FILTER+="[acat][am]amix=inputs=2:duration=first:normalize=0[aout];"
else
  FILTER+="[acat]anull[aout];"
fi

if [[ -n "$SRT" ]]; then
  # Estilo TikTok: letra gruesa blanca con borde negro, en el tercio inferior.
  ESTILO="FontName=DejaVu Sans,Bold=1,FontSize=13,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,Alignment=2,MarginV=110"
  SRT_ESC=$(printf '%s' "$SRT" | sed "s/[\\\\:']/\\\\&/g")
  FILTER+="[vcat]subtitles='$SRT_ESC':force_style='$ESTILO'[vout]"
else
  FILTER+="[vcat]null[vout]"
fi

ffmpeg -y -hide_banner -loglevel error "${INPUTS[@]}" \
  -filter_complex "$FILTER" -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 192k \
  -movflags +faststart -t "$D_TOTAL" "$SALIDA"

echo "Vídeo final: $SALIDA (${D_TOTAL}s)"
