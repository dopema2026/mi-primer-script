# Calidad visual: realismo y física anti-fallos

Obligatorio para cualquier imagen o clip de cualquier canal.
Lo leen Codex y Antigravity antes de escribir o lanzar un prompt; Antigravity (QA nivel 1) y Claude (QA nivel 2) lo usan como lista de revisión.
Los ejemplos entre paréntesis son fallos reales del corto de México.

## A. Las 6 leyes físicas (mandan sobre todo lo demás)

### Ley 1 · Prompt de imagen y prompt de vídeo, separados
- **Prompt de imagen (Codex):** detallado, con la estructura de 6 partes, rigor histórico, cámara a 1,6 m y objetivo de 24 mm.
- **Prompt de vídeo (animación): máximo 30 palabras, fórmula 3V.** Nunca repite historia, ropa ni arquitectura.
  1. **Vector de cámara:** `Steady first-person POV walk forward`
  2. **Vector del sujeto, simple:** `pedestrians walk slowly away down the street`
  3. **Vector ambiental y física:** `smoke drifts right, natural slow pace, consistent shadows`

### Ley 2 · Eje Z: prohibido el cruce lateral
- Prohibido animar marchas, caballería, procesiones o tráfico que **crucen de lado** (eje X) en primer o segundo plano. Al cruzar, los motores funden piernas, quitan brazos e invierten la marcha. (1520: hombres mitad caballo; 1864 y 1867: carruajes que van y vuelven)
- Todo avance va en el **eje Z**: alejándose de espaldas hacia el punto de fuga, o acercándose suave en una diagonal limpia.
- Si no se puede, los sujetos quedan casi quietos y **solo avanza la cámara**.

### Ley 3 · Bloqueo asimétrico contra la marcha atrás
- Todo vehículo o embarcación que se vaya a animar muestra en la imagen fija **pistas de dirección que no se puedan leer al revés**:
  - estela o espuma claramente detrás de la popa;
  - polvo o humo detrás de las ruedas;
  - animales de tiro o conductor visibles delante.
  (1325: canoa al revés y cruzando la pasarela)
- Con tráfico complejo o riesgo de marcha atrás: vehículos aparcados o quietos, y solo avanza la cámara.

### Ley 4 · Zona de exclusión anatómica (0–4 m de cámara)
- Entre 0 y 4 m: **máximo 2 personas o 1 animal**, con siluetas **100 % separadas** (sin ningún solapamiento de cuerpos). (1867: mujer sin brazo)
- Manos en reposo o agarrando un objeto firme (cesta, lanza, herramienta). Nunca dedos abiertos gesticulando en el aire.
- Ningún brazo ni pata medio tapado por una capa, escudo, vasija u otra persona: al animar sale un tercer miembro o desaparece.
- **Multitudes densas, solo a más de 8 m** de profundidad.

### Ley 5 · Prohibidas las acciones físicamente complejas
- **No se anima con IA:** gente corriendo, combates cuerpo a cuerpo, remeros remando rápido, ruedas de radios girando en primer plano ni personas pasándose objetos de mano en mano. (1968: gente que cae)
- **Solo movimientos lentos:** caminar pausado, girar el torso o la cabeza, trabajar quieto en su puesto (martillear), y humo, agua, fuego y viento.

### Ley 6 · Cero texto generado por IA
- Prohibido pedir carteles, letreros o estandartes con palabras. Salen garabatos o anacronismos. (1969: "Pantitlán", estación de 1984)
- Fachadas con **símbolos gremiales dibujados** o con el texto desenfocado por la distancia.
- **El año lo pone solo FFmpeg.** Esta ley sustituye a la antigua regla de dejar el texto real de la época.

## B. Reglas de siempre (se mantienen)

### Personas y animales
- Cada persona: dos brazos, dos piernas, una cabeza y cinco dedos por mano. Cada animal: cuatro patas, un cuerpo y una cabeza. Se cuentan. (1864: caballos con dos cuerpos)
- Pies en el suelo: nada levita ni flota. (1519: lanza que levita; 1600: hombre sobre el agua; 2026: cosas que flotan)
- Animales de tiro con la cabeza delante, en la dirección de la marcha. (1867)
- Animales quietos y en silencio, salvo que el guion pida otra cosa. (2017: perro aullando)
- Sin clones: el resto de la gente, lejos o desenfocada.
- Famosos sin cara: de espaldas, lejos o tapados por la multitud.

### Física y cantidades
- Humo y fuego suben; el agua cae y fluye hacia abajo.
- Cantidades exactas con "only one…", y se cuentan en el fotograma. (1968: dos antorchas)
- Sombras coherentes con una sola fuente de luz.
- Velocidad de época: carros al paso, tranvías antiguos despacio. (1910: tranvías a velocidad moderna)

### Época y lugar
- Bandera del año exacto, descrita por su dibujo, nunca por su nombre. (1790: cruz de Borgoña cuando ya era la rojigualda)
- Monumento en el estado de ese día. Ropa, etnia, oficio y arquitectura de la década y el lugar.
- Cada persona habla la lengua de su sitio y de su fecha. (1500: español antes de que llegaran los españoles)

### Monetización en imagen
- Cero símbolos de odio. En Europa en los años 30 y 40, encuadres limpios o enseñas neutras de la época.
- Cero heridos y cero sangre. **Prohibido recrear tragedias o atentados reales modernos (siglos XX y XXI).**
- Escenas de 1950 a hoy: prohibidos los logos de marcas reales (deformados o no).

### Cómo se escribe el prompt
- Sin negaciones ("no", "nobody", "never" plantan lo que niegan). Excepción: cantidades ("only one…").
- Las restricciones van dentro de la frase de la escena.
- Cada escena en su propia llamada, sin imágenes anteriores como referencia (salvo la edición de continuidad).

## C. Proceso anti-retoques y candado de gasto
1. **Antes de animar**, la imagen pasa el QA nivel 1 (Antigravity) y el nivel 2 (Claude, por mosaico). Si falla algo, Codex la rehace gratis antes de gastar.
2. **Un solo intento de pago por escena.** Si la tira de fotogramas (uno cada 0,5 s) muestra marcha atrás, miembros que desaparecen o deformaciones, **prohibido volver a pagar por animar esa imagen**. Se elige:
   - **Opción A:** nueva imagen base gratis con un plano seguro (sujetos quietos y avance de cámara), o
   - **Opción B:** **falso vídeo vivo con FFmpeg** (imagen fija + vaivén suave de pasos + capa de partículas: polvo, niebla, chispas o lluvia + sonido 3D) = 0 créditos.
3. **Prueba del segundo:** si se nota que es IA en menos de un segundo, se rehace gratis o pasa a la opción B.
4. Cada fallo nuevo se apunta aquí con su ejemplo.
