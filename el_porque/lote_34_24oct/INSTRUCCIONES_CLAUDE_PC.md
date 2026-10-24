# LOTE_34_24oct — Instrucciones para Claude en el PC (El Porqué de las Cosas)

**Escrito por Claude en la nube el 24 oct 2026, por orden de Domingo.** Antes de empezar, lee en Drive `EL_PORQUE_DE_LAS_COSAS/00_PIPELINE/` (PIPELINE, APRENDIDO, ESTADO, TEMAS_USADOS). Este encargo sigue ese pipeline. Donde no diga nada, manda el pipeline.

## Orden de Domingo (24 oct 2026)
> «Crea todos los guiones (estilo de arte y narrador) e instrucciones de todos los shorts. Claude PC preparará la narración de todo, luego hará la petición masiva a Codex, luego creará una animación de 6 segundos para cada uno con un modelo medio en ElevenLabs, luego montará todo y lo dejará en El Porqué de las Cosas.»

Cuenta como **aprobación de los 34 guiones** y como **«adelante»** para narrar, pedir imágenes a Codex, animar la escena 1 y montar. **NO** cuenta para música ni efectos, para programar en Metricool ni para publicar: eso necesita orden aparte.

**Riesgo de monetización:** medio en 3 shorts (10 Atapuerca, 20 pollo Mike, 31 monjes momificados). Están separados en el orden de publicación y llevan reglas visuales en su campo `riesgo_monetizacion`: se narra, no se dibuja. Los otros 31 no tienen riesgo. Todos van con la etiqueta de IA de siempre.

## Qué hay en esta carpeta de Drive
- `LOTE_34_24oct_GUIONES.json`: los 34 `guion.json` en una lista. Cada elemento lleva `carpeta` (p. ej. `01_apolo10_musica`) y el resto de campos que exige la fábrica: títulos A/B, tesis, voz con su `voice_id`, estilo y bloque de estilo, gancho, riesgo, cultura visual, fuentes y bloques con tono.
- `CALENDARIO.md`: el orden, las fechas propuestas y el reparto de estilos y voces.
- Este fichero.

## Pasos

### 0 · Comprobaciones antes de gastar nada
1. Cruza los 34 temas con `TEMAS_USADOS.md`, `EXCLUIDOS.md` y la cola de Metricool (brandId 7423688). Ya están cruzados con TEMAS_USADOS; si alguno choca, apártalo y avisa.
2. **Saldo de ElevenLabs.** Estimación: narración unos 1.700 créditos por short (≈58.000 en total) y animación unos 2.100 por short (≈71.400). **Total aproximado: 130.000 créditos.** Haz `estimate` en la primera tanda. Si el saldo no llega para todo, haz los que se puedan **en orden de publicación** y avisa a Domingo con la cifra exacta.
3. **Verifica los datos dudosos antes de narrar** (regla de APRENDIDO del 13 oct). Los he puesto con fuente, pero revisa sobre todo:
   - 01: que el audio salió en 2016.
   - 18: los unos 40 minutos del túnel.
   - 29: el tesoro según las crónicas.
   - 34: que la ascensorista cayó 75 pisos.
   - 13: que se crían cientos de miles de parejas.

   Si una cifra no se sostiene, corrige la frase y apúntalo.

### 1 · Carpetas y guion
Crea `F:\ProyectoYoutube\porque\LOTE_34_24oct\NN_slug\` para cada short, con el `guion.json` sacado del JSON combinado (cada elemento sin el campo `carpeta`). Mantén `aprobacion_guion: true` (orden de Domingo).

### 2 · Narración (ElevenLabs por MCP, nunca por API)
- Un texto por short **en una sola línea**, con `<break time="1.2s" />` entre bloques. Usa la voz y el modelo de cada `guion.json`.
- Parte y valida como siempre: `partir_audio.py`, `narrar_mcp.py ingerir … --voz <voz>` y `verificar_voz.py` con whisper.
- Duración prevista: 95–105 s por short (230–255 palabras). Bosco varía de ritmo: mídelo en el primer bloque.
- Reparto de voces: alterna hombre/mujer y nunca repite la del anterior. No hay voces retiradas.
- Pronunciaciones a vigilar: Horyu-ji, Draupner, Natron, Areni, Ereván, Albuquerque, sokushinbutsu, Yamagata, Fruita, Olsen, Elisha Otis, déjà vu.

### 3 · Escenas y prompts (los escribes tú, como dice el pipeline)
- `planificar_escenas.py` con los tiempos reales: una frase, una escena, una imagen.
- En los primeros 8 s ningún plano pasa de 3 s.
- La escena 1 es el **gancho**. Usa el campo `gancho` de cada guion: sujeto reconocible en un segundo, lo más potente del vídeo. **Si la gente no engancha en el primer segundo, se va.**
- Prompts en inglés, en positivo, sin texto en las imágenes, nadie mirando a cámara salvo el gancho, y el resto de reglas de PIPELINE y APRENDIDO.
- **Estilo:** usa el bloque literal del campo `estilo` de cada guion.
  - Va **al principio** del prompt («Rendered entirely as a …»), salvo en el **Fotorrealista**, donde va al final.
  - Los 5 estilos nuevos de prueba (acuarela, plano técnico azul, cómic de línea clara, cuento de los años cuarenta, tinta sumi-e) son de libre elección según la regla del 14 oct. Ninguno es de los prohibidos.
- **Avisos visuales por short:**
  - 26 palabras desordenadas, 27 regla y 30 metro: **sin letras ni números legibles**. Escalas solo como rayas y palabras como formas.
  - 19 hipertimesia: persona real. **No reproducir su cara**, figura de collage genérica.
  - 10, 20 y 31 (riesgo medio): las reglas de su campo `riesgo_monetizacion`.
  - 13 Natron: las aves conservadas como figuras blancas de sal, sin descomposición.
  - 17 ciervos: el terciopelo seco, sin sangre.
  - 34 ascensor: nada del avión estrellado ni de víctimas.
- `verificar_guion.py` a cero bloqueos → `encargo_codex.py` → `listo_para_codex.py --orden`.

### 4 · Imágenes: petición masiva a Codex
- Agrupa los 34 encargos en **tandas grandes** (unos 7 shorts por orden), con la tanda de prueba obligatoria: las 5 primeras imágenes de cada orden se miran antes de dejarla correr.
- Domingo pega cada orden en un chat **nuevo** de Codex.
- Recoge emparejando por el texto del prompt si hubo rechazos; no por orden de llegada.
- Pre-revisión completa con `prerevisar_imagenes.py` y hojas de contacto de **todas** las escenas.

### 5 · Animación de la escena 1 (ElevenLabs, modelo medio)
- Modelo `kling-2.5-turbo`, 9:16, calidad media, partiendo de la imagen de la escena 1, como en la receta del pipeline.
- El clip **cubre toda la escena 1 (unos 6 s) sin cortarse a imagen fija**: se estira con `setpts` si hace falta. Es regla de «nunca más».
- Solo se mueve lo que ya está en la imagen.
- Si la imagen de la escena 1 es mala, se rehace **antes** de animar.

### 6 · Montaje y entrega
- `fabrica.py "<proyecto>" --voz <voz>` → `render\master.mp4` (máster limpio, sin texto).
- Comprueba los primeros 6 s de cada máster: la animación entera y el gancho claro.
- **Sin música ni efectos** salvo nueva orden de Domingo.
- **Subtítulos:** los pone Domingo en CapCut, como siempre. No los quemes salvo que él lo pida.
- Portada 9:16 de cada short a partir de la escena del gancho.
- **Entrega en `Escritorio\PENDIENTE_PUBLICAR\Porque de las cosas\`.** Un short por subcarpeta (`NN_slug`), con el mp4, la portada y un `LEEME.txt` que lleve el título A, el título B, la fecha propuesta y las 3 etiquetas.
- Nombres de archivo: `porque_<slug>_<díames><hora>.mp4` y `.jpg`, con la fecha de `CALENDARIO.md`. Ejemplo: `porque_apolo10_musica_29oct1500.mp4`.

### 7 · Después
- Actualiza **el mismo día** `ESTADO.md` y `TEMAS_USADOS.md` en Drive con cada short que avance de paso (narrado, imágenes, animado, montado).
- Las lecciones nuevas van a `APRENDIDO.md`.
- No programes nada en Metricool hasta que Domingo dé la orden con fecha y hora.
- Al terminar, dile a Domingo cuántos están montados, cuántos créditos se han gastado y qué ha fallado.
