# ANIMACIÓN — reglas comunes a todos los canales

**Versión 1 · 26 oct 2026.** Escrito por Claude (nube) reuniendo lo que ya estaba en los pipelines de Dopema Web, El Porqué y Time Runners, y añadiendo lo que faltaba. Vale para Dopema Web (largos, shorts y serie de dormir), El Porqué, Time Runners y, si vuelve, Rough Ages. Si un pipeline de canal dice algo más concreto, manda el del canal.

## 0. Reglas que ya existían (no cambian)
- Nada se anima sin el «sí» de Domingo. Siempre **estimación de créditos antes** y el gasto en euros/créditos dicho en voz alta.
- **La animación mueve solo lo que ya está en la imagen.** No aparecen personas, objetos ni luces nuevas.
- **Una imagen mala se rehace antes de animarla.** Animar una imagen floja es tirar créditos.
- **El clip cubre toda su escena**: nunca se corta a imagen fija a mitad de escena («nunca más», 13 oct).
- **Máximo dos intentos de pago por escena con la misma imagen.** Si falla dos veces, nueva imagen de Codex, no otro modelo sobre la misma.
- Prompts de vídeo **en inglés y en positivo** (sin «no», «never», «nobody»): se describe lo que sí se mueve.
- Vehículos, barcas y animales **quietos o amarrados** cuando el plano lo permita; el movimiento lo pone la cámara.
- Se guardan **dos másters**: con animación y sin animación.
- Cada llamada de pago se apunta en `gasto.csv` del proyecto (fecha, escena, modelo, segundos, estimado, real, usado sí/no).

## 1. Quién hace qué
| Paso | Quién |
|---|---|
| Elegir qué escenas se animan y escribir el prompt de movimiento | Claude (en la escaleta / orden del vídeo) |
| Revisar la imagen antes de animar | Claude PC (hoja de contacto) |
| Subir la imagen a ElevenLabs, estimar, generar y descargar | **Codex, si la prueba de acceso a ElevenLabs sale bien**; si no, Claude PC |
| Revisar el clip (§6) y montarlo | Claude PC |
| Aprobar gasto y máster | Domingo |

## 2. Modelos y coste (re-estimar antes de cada tanda; los precios cambian)
| Uso | Modelo | Coste orientativo |
|---|---|---|
| **Las 2 primeras escenas animadas de cada vídeo** (la apertura decide la retención) | `kling-3-pro` | estimar siempre (más caro que Turbo) |
| Resto de escenas | `kling-2.5-turbo` | ~2.100 créditos por 5 s (~420 por segundo) |
| Diálogo con labios (Time Runners) | Kling con audio nativo | estimar |
Si un modelo no admite la duración exacta, se genera la siguiente más larga y se recorta. No se estira más de un 25 % a cámara lenta (se nota).

## 3. Cuándo se anima, por canal
| Canal / formato | Qué se anima |
|---|---|
| Dopema Web, largos normales | La escena 1 siempre que Domingo lo pida; otras, solo las que él nombre |
| Dopema Web, serie de dormir | **3 clips**: escena 1 (duración fija que diga la orden, p. ej. 8 s) y dos más en los primeros 10 min, separadas entre sí. **Sin caras ni manos** |
| El Porqué, shorts | Solo la escena 1 (decisión del 15 oct) |
| Time Runners | Todo el vídeo son clips; reglas propias de continuidad en su pipeline (§P4) |

## 4. Plantilla del prompt de vídeo
Tres frases, siempre en este orden:
1. **Qué se mueve** (lo mínimo): «The candle flame flickers gently», «faint clouds drift very slowly».
2. **Cámara**: por defecto **«Camera still.»** Si se mueve: «Camera pushes in slowly», «Camera pans slowly to the right». Una sola dirección.
3. **Luz**: «The lighting stays the same» o el cambio exacto («the pale line of dawn brightens slightly»).

## 5. Ritmo y dirección (lo que faltaba)
- **Qué es «lento», con números:** la cámara recorre como mucho un **5–10 % del encuadre en 5 s**. Los elementos (nubes, humo, agua) se mueven a velocidad natural o más lenta.
- **Movimientos rápidos solo en momentos marcados en la escaleta** (catástrofe, sorpresa), como mucho uno cada pocos minutos y nunca en vídeos de dormir.
- **Misma dirección dentro de una secuencia:** dentro de un capítulo o época, todos los clips avanzan hacia el mismo lado (todo hacia delante, o todo de izquierda a derecha). Se cambia de dirección solo al cambiar de capítulo/época. En Time Runners manda su regla de primera persona hacia delante.
- **Consistencia:** la ropa, la cara, la luz y la hora del día del primer fotograma se mantienen hasta el último. Si el modelo las cambia, el clip no vale.

## 6. Lo que falla casi siempre → solo movimiento de cámara o «Camera still»
Manos, caras que giran, piernas caminando de cerca, texto y letreros, multitudes en movimiento, agua y fuego rápidos, animales corriendo, puertas y objetos que se abren. En esas escenas se anima solo el ambiente (luz, humo, nubes) o se deja la cámara moverse sobre la escena quieta.

## 7. Revisión de cada clip antes de aceptarlo
1. Primer fotograma = imagen aprobada (sin cambios de encuadre ni de color).
2. Último fotograma: misma ropa, misma cara, misma luz; nada nuevo en el cuadro.
3. Sin deformaciones (manos, extremidades, caras que se funden), sin texto inventado, sin parpadeos.
4. Velocidad dentro de §5.
5. En vídeos de dormir: nada que sobresalte.
Si falla: segundo intento con el prompt corregido (más quieto). Si vuelve a fallar: imagen nueva o se queda la imagen fija con zoom lento (y se avisa a Domingo).

## 8. Entrega
- Nombre: `clip_escena_NNN.mp4` (NNN = número de escena de la orden), en la carpeta `clips\` del proyecto.
- Aspecto igual que la imagen (16:9 largos, 9:16 shorts), resolución la mayor disponible del modelo; el montaje lo adapta a 1920×1080 o 1080×1920.
- Audio del clip desactivado salvo diálogo en Time Runners.
- Una línea por clip en `gasto.csv`.
