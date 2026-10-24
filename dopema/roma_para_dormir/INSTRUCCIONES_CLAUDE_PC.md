# Roma para dormir — Instrucciones para Claude en el PC (Dopema Web)

**Escrito por Claude en la nube el 24 oct 2026, a petición de Domingo.** Vídeo largo de unas 2 horas para el canal Dopema Web. Objetivo: sumar horas de visualización (el vídeo de 8 h de 2018 dio 137 h en un año).

## Orden de Domingo
> «Prepara guion de toda la historia de Roma desde el inicio, hazla interesante; le pondré voz pausada; pocas imágenes; mi música relajante; voz con Amazon Polly (Raúl).»

El guion está aprobado para producir. **No se publica ni se programa sin orden expresa de Domingo.**

## Archivos (esta carpeta de Drive)
- `GUION_ROMA_1_intro_cap01-04.md`, `GUION_ROMA_2_cap05-08.md`, `GUION_ROMA_3_cap09-12.md`, `GUION_ROMA_4_cap13-16.md`: guion completo en 4 partes, en orden.
- Total: unas 13.500 palabras narradas (unos 80.000 caracteres), 17 bloques (introducción y 16 capítulos), **114 imágenes**.
- Formato: `## CAPÍTULO…` es el título del capítulo y no se narra. `[IMAGEN NN · descripción]` es el cambio de imagen y tampoco se narra. Todo lo demás es narración.

## Paso 0 · Prueba de voz (antes de gastar nada)
1. **Decisión de Domingo: voz Amazon Polly, Raúl.** Con el primer párrafo de la introducción (de «Buenas noches» a «apagando»), genera 2 pruebas:
   - Raúl, motor **neural**
   - Raúl, motor **generative** (si la cuenta lo permite)

   Hazlas a velocidad 90 % y 95 %.
2. Déjalas en `Escritorio\PENDIENTE_PUBLICAR\1_DOPEMA_WEB\ROMA_PARA_DORMIR\pruebas_voz\` y **espera a que Domingo elija.**
3. Coste aproximado del vídeo entero: Polly neural unos 1,30 $; Polly generative unos 2,40 $; ElevenLabs Multilingual unos 80.000 créditos. Confírmalo con los precios actuales.
4. **Claves de AWS:** solo en la configuración local del PC (AWS CLI o variables de entorno). **Nunca en Drive, en documentos ni en el chat.**

## Paso 1 · Narración (con la voz elegida)
- Ritmo lento: en Polly, SSML con `<prosody rate="90%">`. Si suena arrastrado, súbelo a 95 %.
- Pausas:
  - 0,8 s entre frases (las pone el propio motor);
  - **1,5 s entre párrafos**;
  - **4 s entre capítulos**.
- Polly admite unos 3.000 caracteres por llamada. Parte por párrafos, nunca a mitad de frase, y une los audios con ffmpeg.
- Pronunciaciones a vigilar: Tíber, Numitor, Amulio, Rea Silvia, Fáustulo, Tulo Hostilio, Anco Marcio, Tarquinio, Cincinato, Menenio Agripa, Breno, Vae victis, Horcas Caudinas, Apio Claudio, Pirro, Milas, Égadas, Amílcar, Cunctator, Áufido, Cannas, Zama, Viriato, Numancia, Graco, Cimbrios, Espartaco, Alea iacta est, Farsalia, Vercingétorix, Alesia, Carras, Veni vidi vici, Actium, Teutoburgo, Arminio, Sejano, Incitato, Agripina, Antium, Herculano, Itálica, Apolodoro, Antonino Pío, cuados, marcomanos, Pertinax, Didio Juliano, Leptis Magna, Eboracum, Geta, sasánidas, Sapor, Zenobia, Palmira, Aureliano, Restitutor Orbis, tetrarquía, Majencio, Milvio, Bósforo, Adrianópolis, Estilicón, Alarico, Rávena, Aecio, Cataláunicos, Odoacro, Augústulo. **Si una sale mal, usa `<phoneme>` o escríbela como suena solo en el texto de la locución, nunca en el guion.**
- Verifica con whisper que no falte ni sobre ninguna frase.
- Duración esperada: entre 1 h 50 y 2 h 10.

## Paso 2 · Imágenes (Codex)
- 114 imágenes, una por cada `[IMAGEN NN]`. Cada una dura en pantalla lo que dura la narración hasta la siguiente marca, entre 40 s y 1 min 30 s.
- **Estilo único para todo el vídeo**, adecuado para dormir: pintura al óleo clásica, oscura y cálida, como un cuadro de museo a la luz de las velas, con tonos ámbar, ocre y azul noche, mucha sombra y sin colores chillones. Bloque de estilo (en inglés, al principio de cada prompt):
  `Rendered entirely as a classical oil painting in a dark, warm museum style, candlelit amber and deep blue tones, soft shadows, calm atmosphere, 16:9 horizontal composition.`
- Formato **16:9 horizontal** (es un largo, no un Short).
- Prompts en inglés, en positivo, **sin texto en la imagen**. Nadie mira a cámara. Escenas tranquilas.
- **Batallas y muertes:** paisaje, siluetas lejanas o el momento anterior o posterior. **Nunca sangre, heridas, cadáveres ni violencia explícita.** Ya está así en las descripciones; respétalo. Los vídeos para dormir no pueden tener sobresaltos.
- **Caras distintas:** ningún personaje genérico repite cara. Los personajes históricos que salen varias veces (Aníbal, César, Augusto, Marco Aurelio, Constantino) mantienen su aspecto entre sus imágenes.
- Tandas de unos 20 prompts, con tanda de prueba: las 5 primeras se revisan antes de seguir. Domingo pega cada tanda en un chat nuevo de Codex.

## Paso 3 · Montaje
- Cada imagen con **movimiento muy lento**: zoom del 100 % al 108 % durante toda su duración, o un desplazamiento lateral suave. Alterna entre los dos. Sin movimientos bruscos.
- Transición entre imágenes: **fundido cruzado de 2 s**. Nada de cortes secos.
- Entre capítulos: fundido a negro de 1 s y vuelta.
- **Música:** la de Domingo (relajante). Pídele los archivos.
  - Volumen entre −22 y −25 dB respecto a la voz, constante, sin subidas.
  - Fundido de entrada de 5 s y fundido de salida de 10 s.
  - Antes de usarla, pregunta a Domingo si esa música está en algún distribuidor con Content ID (DistroKid, etc.). Si lo está, que ponga el canal en la lista blanca del distribuidor o desactive el Content ID para esas pistas.
- Al final de la narración: **5 minutos más de música con la última imagen** (Roma de noche), con fundido lento a negro.
- Sin subtítulos quemados.
- Resolución 1920×1080. Audio normalizado a −16 LUFS para la voz.

## Paso 4 · Capítulos, título, descripción y portada
- Genera los tiempos de capítulo reales a partir del audio montado: `00:00 Introducción`, `CAPÍTULO 1 · Una colina junto al río`, etc. (los 16 títulos están en el guion).
- **Título (Domingo elige):**
  1. «La historia de Roma para dormir: de Rómulo a la caída del Imperio (2 horas)»
  2. «Toda la historia de Roma para dormir | Historia relajante con voz pausada»
  3. «Roma, de la loba al último emperador | Historia para dormir (2 h)»
- **Descripción:**
  - 2–3 líneas tranquilas sobre el viaje;
  - la lista de capítulos con sus tiempos;
  - la línea «Imágenes, voz y música creadas con IA», o la que corresponda según la voz y la música reales;
  - las etiquetas #HistoriaParaDormir #HistoriaDeRoma #ImperioRomano.
- **Uso de IA en YouTube Studio: marcar «Sí».**
- **Portada 16:9:**
  - la imagen 01 (Roma de noche) o la 08 (la loba);
  - texto grande en 2–3 palabras: «ROMA» y debajo «para dormir»;
  - una luna o una vela como acento cálido.
- Entrega en `Escritorio\PENDIENTE_PUBLICAR\1_DOPEMA_WEB\ROMA_PARA_DORMIR\`:
  - `roma_para_dormir.mp4`;
  - `portada.jpg`;
  - `LEEME.txt` con los 3 títulos, la descripción con los capítulos y los créditos de voz y música.

## Paso 5 · Después
- Anota en `ESTADO.md` de Dopema Web en Drive cada paso hecho, el mismo día.
- No publiques ni programes nada. Domingo da la orden con fecha y hora.
- Al terminar, informa a Domingo de la duración final, la voz usada, el coste real y qué ha fallado.
