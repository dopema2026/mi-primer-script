# mi-primer-script

Fábrica de vídeos para TikTok Shop: hooks con IA (ElevenLabs / Seedance) + cuerpo con
fotos reales del producto, montados con FFmpeg. Reglas y flujo completos en `CLAUDE.md`.

```bash
cp -r productos/_plantilla productos/mi-producto
# fotos/, voz.mp3, hooks/*.mp4 y subtitulos.srt dentro de productos/mi-producto
scripts/lote.sh productos/mi-producto   # → productos/mi-producto/finales/
```
