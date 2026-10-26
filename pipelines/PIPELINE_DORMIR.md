# DOPEMA WEB — SERIE «HISTORIA PARA DORMIR» (vídeos de ~2 h)

**Versión 1 · 26 oct 2026.** Formato nuevo de Dopema Web. Lo que no diga este fichero sigue el `PIPELINE.md` de Dopema Web. Animación: `ANIMACION.md`.

## 0. Por qué existe
Dopema Web tiene 532 suscriptores y 249 horas válidas (datos al 21 oct): para anuncios faltan **3.751 horas**. Un vídeo de 2 h que se deja puesto de noche es la palanca más directa para esas horas. Riesgo de monetización: bajo si cada vídeo es distinto (tema, estructura, imágenes) y no parece hecho en serie sin aportación.

## 1. Guion
- Fichero `guiones-dormir/NN-tema.md` (GitHub `dopema2026/mi-primer-script`) con tres secciones: **FICHA** (no se narra), **GUION**, **FUENTES**. Los títulos `###` de capítulo no se narran.
- **Texto limpio**: sin etiquetas SSML ni `<break>`. Las pausas las pone el script (1,5 s entre párrafos, 4 s entre capítulos).
- Longitud: **~14.000–15.000 palabras** (con Raúl: ~126 palabras/min ≈ 1 h 50 min – 2 h) más el cierre de ambiente.
- **Estructura distinta en cada vídeo** (un reloj, un viaje, una biografía, una vuelta hacia atrás…).
- **Apertura**: frase-gancho de 14 palabras como mucho con la contradicción dentro, en tono suave; después el saludo de la casa («Buenas noches…», «no hace falta que prestes atención a cada palabra… puede esperar una noche más»); invitación a comentar desde dónde escuchan y qué hora es. **«Para dormir» se dice una sola vez.**
- Segundo gancho hacia los 20 s: los hilos que el vídeo va a pagar. Re-enganches suaves (pequeños hilos de curiosidad) cada 1,5–2 min en la primera hora; se espacian y desaparecen hacia el final.
- Tono: compañía cálida, de tú; plural de viaje compartido («vamos a recorrer»); avisos de tramo («Cuenta la leyenda…»). Sin exclamaciones, sin sobresaltos, sin muletillas de IA. Más lento y sensorial en el último tercio. Cierre que se disuelve.
- Reglas de Dopema que se mantienen: cifras en letra, sin siglas, eñes y tildes, dato real con fuente, lo discutido con matiz, nunca pedir like/suscripción, nunca «YouTube» en el audio. Nombres difíciles escritos como se pronuncian y listados en la FICHA para comprobarlos de oído.
- Temas religiosos o míticos: tono de museo; las figuras sagradas nunca con rostro (ver §3).

## 2. Voz
- **Raúl, Polly long-form, al 90 %, la misma en toda la serie.** (Raúl solo existe en long-form; Sergio y Lucía son las generativas.)
- `python narrar_dormir.py --prueba-2min --voz Raul --motor long-form guiones-dormir/NN-*.md` → escuchar nombres → `python narrar_dormir.py --voz Raul --motor long-form guiones-dormir/NN-*.md`.
- Sale el MP3 y `NN-…_capitulos.json` (segundo de inicio de cada capítulo). Coste: ~7–8 $ por vídeo.

## 3. Imágenes (Codex)
- **~100 imágenes** por vídeo (una cada ~1 min de media), repartidas por la duración real de los capítulos; más densas al principio, nunca menos de 3 por capítulo.
- Estilo de la serie: **maqueta en miniatura tilt-shift**, con dos variantes según el tema:
  - **Cálida** (vida cotidiana: Edad Media, Roma, aldeas): bloque de estilo de `ORDEN_CODEX_DORMIR_01_EXTRA.md`.
  - **Oscura de museo** (mitos, religión, temas solemnes): bloque de estilo de `ORDEN_CODEX_DORMIR_13.md`.
- Cada escena con **tipo de plano** (primer plano, plano medio, general) y **su propia luz** al principio; interiores como habitación de maqueta abierta. Así no salen todas iguales.
- Reglas de la casa: inglés, en positivo, siglo y lugar en cada escena, caras de perfil sin mirar a cámara, cada persona distinta, nada de texto legible, ~1 de cada 4 escenas sin personas.
- **Lo sagrado es luz**: Dios y el trono, resplandor desde lo alto; Jesucristo, luz suave o silueta lejana de espaldas; la espada de san Miguel, haz vertical de luz dorada. Ningún diablo grotesco: si aparece, como obra de arte de su época o como caballero.
- Tandas: prueba de 10 (se miran las 5 primeras) y después tandas de ~45, cada una en un chat nuevo.

## 4. Animación
Tres clips por vídeo según `ANIMACION.md` §3: escena 1 con la duración fija de la orden (8 s en el vídeo 13) y dos más en los primeros 10 min; sin caras ni manos; las 2 primeras con `kling-3-pro`, la tercera con `kling-2.5-turbo`.

## 5. Montaje
- 16:9, 1920×1080. Cada capítulo empieza en su segundo de `_capitulos.json`; sus imágenes se reparten a partes iguales (salvo las animadas, que duran lo que su clip).
- Zoom o desplazamiento muy lento, variando la dirección entre capítulos; fundidos de 2–3 s.
- Desde la mitad del vídeo, el brillo baja poco a poco hasta un 60–70 %.
- Sonido: ambiente continuo suave según el capítulo y música Lyria tranquila, todo a −20/−24 dB respecto a la voz; nada brusco.
- **Cierre de 10–15 min** de ambiente y música que se apagan sobre las últimas imágenes, hasta ~2 h.
- **−16 LUFS**, pico ≤ −1 dBFS. Sin subtítulos quemados, sin texto en pantalla. `auditar_video.py` antes de enseñarlo.

## 6. Publicación
- Título: «[Tema]: [promesa] | Historia para dormir» o con «para dormir» dentro del título.
- Descripción: 3–4 líneas tranquilas, capítulos con tiempos sacados de `_capitulos.json`, «Imágenes, voz y música creadas con IA.», «Suscríbete a @dopemaweb para más historia contada con fuentes.», 3 hashtags. Fuentes en fichero aparte.
- Contenido sintético: sí. No es para niños. Categoría Educación. Lista de reproducción «Historia para dormir».
- La casilla «Publicar en el feed de suscripciones y notificar» la decide Domingo en cada subida.
- **Cuando el canal esté monetizado:** anuncios intermedios colocados a mano en las pausas entre capítulos, sobre todo en la primera hora; pocos o ninguno en la última media hora.
- Cadencia de partida: uno por semana.

## 7. Datos
A los 7 y 28 días: horas, duración media vista, retención inicial, espectadores recurrentes. Comparar los vídeos a la misma edad antes de cambiar nada.
