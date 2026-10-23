# P000_3 — prueba: biblioteca de audio

- Agente: codex
- Aprobado_gasto: no
- Coste estimado: 0 créditos
- Depende de: ninguna

## Objetivo
Dejar `biblioteca_audio/` lista y conectada al pipeline.

## Entradas
- `biblioteca_audio/LEEME.md`

## Pasos
1. Comprueba que existen las 10 categorías de `biblioteca_audio/LEEME.md`, con las 4 subcarpetas de `pasos`. Si falta alguna, créala.
2. Crea `biblioteca_audio/INDICE.csv` solo con la cabecera:
   `archivo,categoria,segundos,loop,origen,licencia,fecha`
3. Crea `biblioteca_audio/buscar_audio.py`:
   - recibe una categoría y una duración mínima;
   - lee `INDICE.csv` y devuelve las rutas que encajan;
   - si no hay ninguna, devuelve vacío y un código de salida 1.
4. Pruébalo con `python biblioteca_audio/buscar_audio.py viento 10`. Debe devolver vacío y código 1, porque aún no hay audios.
5. No toques `F:\ProyectoYoutube\`. Adaptar `mezclar_eleven.py` será otra tarea, con permiso de Domingo.

## Terminado cuando
Existen las carpetas, `INDICE.csv` y `buscar_audio.py`, y la prueba del paso 4 da el resultado esperado.

## Revisión
- QA nivel 2 (Claude): lee el script y la salida de la prueba.

## Al acabar
Sigue los puntos 13 y 14 de `REGLAS.md`.
