# Fábrica de vídeos TikTok Shop (afiliado)

Sistema para producir vídeos verticales de venta para el canal secundario de TikTok,
generados con ElevenLabs (MCP `Eleven_labs`) y montados con FFmpeg en local.
Idioma de los vídeos: español de España, salvo que se indique otra cosa.

## Principio: arquitectura sándwich + "1 cuerpo, N hooks"

- La IA de vídeo (cara) **solo** se usa en el hook (4–5 s).
- El cuerpo (demo, ~15 s) se hace con **fotos reales del producto + locución**,
  animadas con `scripts/fotos_a_cuerpo.sh` (coste 0).
- De cada producto: **1 cuerpo + 3–5 hooks** → `scripts/lote.sh` monta un vídeo por hook.
- Música y SFX se generan **una vez** y se reutilizan desde `biblioteca/`.

## Modelos (IDs verificados en el workspace, oct 2026)

| Uso | Modelo | model_id |
| --- | --- | --- |
| Hook de prueba (barato) | Seedance 2.0 Fast, 720p | `bytedance-seedance-v2-fast` |
| Hook final / producto ganador | Seedance 2.5 | `bytedance-seedance-v2.5` |
| Alargar un clip ganador | Seedance 2.5 Extend | `bytedance-seedance-v2.5-extend` |
| Fotos del producto (cambiar fondo, sin tocar el artículo) | GPT Image 2.5 | `gpt-image-2.5-sunburst` |
| Locución en volumen / pruebas | Flash v2.5 | `eleven_flash_v2_5` |
| Locución de hooks emocionales | Eleven v4 | `eleven_v4` |
| SFX (solo para la biblioteca) | Sound Effects v2 | `eleven_text_to_sound_v2` |
| Música (solo para la biblioteca) | Music v2.5, instrumental | `eleven_music_v2_5` |
| Transcribir vídeos de referencia / subtítulos | Scribe | `eleven_scribe_v1` |
| Voz "de móvil / nota de WhatsApp" | Audio Effects (`cheap_microphone` o `phone` + `small_room`) | `eleven_audio_effects` (gratis) |

Notas:
- La duración mínima de Seedance es **4 s** (no 3). Hooks: 4–5 s.
- Para la voz de móvil **no regenerar audio**: pasar la locución por el nodo Audio Effects.
- No hay nodo de "Text to Dialogue" en Flows: el formato de 2 voces se hace con
  dos nodos TTS (una voz cada uno) unidos en un nodo Composition o con FFmpeg.

## Reglas de ahorro de créditos (obligatorias)

1. Nunca generar vídeo IA de más de 5 s salvo que el producto ya haya vendido
   y el usuario lo pida explícitamente.
2. Primera ronda de hooks siempre en `bytedance-seedance-v2-fast` a 720p.
   Solo el hook que funcione se rehace en Seedance 2.5 / 1080p.
3. Para pruebas, generar 1 variación (`generations_count` = 1). No reintentar una
   generación fallida sin avisar: cada llamada cobra.
4. Nunca generar música o SFX dentro de un vídeo: usar `biblioteca/musica` y `biblioteca/sfx`.
5. Locución por defecto con `eleven_flash_v2_5`; `eleven_v4` solo para hooks.
6. Antes de una tanda grande (más de 5 vídeos IA), decir al usuario cuántas
   generaciones se van a lanzar y esperar confirmación.

## Flujo por producto

Carpeta: `productos/<nombre-producto>/` (copiar de `productos/_plantilla/`).

1. **Ficha** (`guion.md`): producto, enlace, comisión, valoración, 3 objeciones
   sacadas de reseñas negativas, ángulo elegido.
2. **Fotos**: 3–5 fotos limpias de la ficha en `fotos/`. Si hace falta cambiar el
   fondo, GPT Image 2.5 con la foto como referencia y la instrucción
   "no alterar forma, tamaño, color, logotipo ni envase del producto".
3. **Guion del cuerpo** (12–18 s, ~35–50 palabras): demo + resolver una objeción + CTA
   al carrito naranja. Locución → `voz.mp3`.
4. **Subtítulos**: transcribir `voz.mp3` con Scribe y guardar `subtitulos.srt`
   (frases de 2–4 palabras por línea).
5. **Hooks**: 3–5 frases distintas → un vídeo de 4–5 s cada uno en `hooks/` (prompt abajo).
6. **Montaje**: `scripts/lote.sh productos/<nombre-producto>` → `finales/`.

## Prompt maestro de hook (Seedance)

Aspect ratio `9:16`, `duration_secs` 4–5, `generate_audio` true, foto del producto
conectada como imagen de referencia:

> Vídeo vertical 9:16 grabado con la cámara de un móvil sujeto con el brazo, ligero
> movimiento natural de la mano, habitación normal con luz de ventana, compresión
> suave de teléfono. Una persona corriente ya está hablando cuando empieza el clip y
> dice en español de España: "[FRASE HOOK]", mientras sostiene a cámara exactamente
> el producto de la imagen de referencia, sin cambiar su tamaño, forma, envase ni
> color. Sonido ambiente real de habitación, roce de ropa, sin música.

## Tipos de hook

- **Negativo a mitad de frase**: "…no lo compres si te gusta pasarte media hora quitando pelos del sofá."
- **Objeción de reseña**: texto en pantalla con la queja real de 1 estrella y respuesta en la demo.
- **Pique de 2 voces**: dos voces TTS discutiendo sobre el producto encima de las fotos.
- **Resultado primero**: el "después" en el segundo 0, el "antes" justo detrás.

## Límites (no negociables)

- Activar siempre la etiqueta **"AI-generated content"** al publicar.
- Las personas generadas con IA **no** pueden decir que han usado o comprado el
  producto ("yo lo uso cada día", "me cambió la vida"), ni presentarse como
  clientes reales. Usar frases sobre el producto, no testimonios inventados.
- Sin afirmaciones de salud, adelgazamiento o resultados garantizados.
  Nada de suplementos ni cosmética "milagro".
- Los vídeos de la competencia se analizan para sacar la **estructura**; nunca se
  copia su texto literal, su música ni sus imágenes.
- Las prestaciones que se dicen en el guion deben estar en la ficha del producto.

## Scripts

- `scripts/fotos_a_cuerpo.sh <fotos/> <voz.mp3> <cuerpo.mp4>`: fotos + voz → cuerpo 1080x1920.
- `scripts/montar.sh <hook.mp4> <cuerpo.mp4> <salida.mp4> [musica] [srt]`: une hook + cuerpo, música a -18 dB, subtítulos quemados.
- `scripts/lote.sh productos/<nombre-producto>`: todo lo anterior para cada hook.
- `scripts/desplazar_srt.py`: retrasa los subtítulos del cuerpo la duración del hook.

Requisitos: `ffmpeg`, `ffprobe`, `python3`.
