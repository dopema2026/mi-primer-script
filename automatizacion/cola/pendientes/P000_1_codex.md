# P000_1 — prueba: 1 imagen y 1 mosaico

- Agente: codex
- Aprobado_gasto: no
- Coste estimado: 0 créditos de ElevenLabs
- Depende de: ninguna

## Objetivo
Comprobar que `codex exec` genera una imagen con la cuota del plan ChatGPT y que sabe montar un mosaico de revisión.

## Entradas
- Ninguna.

## Pasos
1. Con **tu generador de imágenes incluido en el plan**, genera **una sola** imagen vertical 9:16 con este prompt literal:
   "Photorealistic vertical photograph, 9:16. First-person point of view at standing eye height, about 1.6 metres, 24 mm lens: a quiet cobbled street in a Spanish port town at sunset, one fisherman about fifty in a blue wool sweater stands still beside a stack of wooden crates, both hands resting on the top crate, three metres from the viewer. Whitewashed houses with plain walls, warm orange light, long shadows falling to the left. Natural documentary realism."
2. Guárdala como `entregables/P000_1/prueba.png`.
3. Si no tienes generador de imágenes en este modo, o solo podrías hacerlo con una clave de API de pago, **no lo hagas**: marca FALLO y explica qué opción tienes.
4. Con Python (Pillow) o FFmpeg, monta `entregables/P000_1/mosaico_3x4.jpg`: la misma imagen 12 veces en una cuadrícula de 3 columnas por 4 filas, con el número 1–12 visible en cada casilla.
5. En tu resumen, apunta:
   - qué herramienta usaste para la imagen;
   - si te pidió o usó alguna clave de API;
   - la salida de `/status` o el dato de uso del plan, si lo tienes.

## Terminado cuando
Existen `entregables/P000_1/prueba.png` y `entregables/P000_1/mosaico_3x4.jpg`, o hay un FALLO explicado.

## Revisión
- QA nivel 1 (Antigravity): la hace P000_2.
- QA nivel 2 (Claude): mosaico legible y numerado, imagen 9:16, se cumple `CALIDAD_VISUAL.md`.
- Domingo: comprobar en su cuenta de OpenAI que no hay cargos de API nuevos.

## Al acabar
Sigue los puntos 13 y 14 de `REGLAS.md`.
