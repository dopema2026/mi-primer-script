# Encargo de revisión

Eres un revisor experto en canales de YouTube y TikTok monetizados, producción de vídeo con IA y automatización con agentes. Revisa con calma y sin complacencia el sistema y el pipeline de abajo.

**Objetivo del dueño (Domingo):** ganar dinero con el canal (monetización de YouTube), conseguir vídeos virales y que la gente se suscriba y siga el canal. Sirve para **largos y cortos**.

**Responde en español, fácil y por apartados:**
1. **Errores graves:** lo que impide monetizar, crecer o que el sistema funcione. Ordénalos por gravedad.
2. **Monetización:** riesgos con las políticas de YouTube y TikTok (contenido repetitivo, IA, violencia, derechos) y cómo evitarlos.
3. **Viralidad y seguidores:** qué falta para que los vídeos se compartan y la gente se suscriba (gancho, títulos, miniaturas, series, frecuencia, comunidad, idiomas, otras redes).
4. **Costes:** si los números tienen sentido y cómo bajar el gasto sin perder calidad.
5. **Reparto entre IAs:** si cada tarea está en la IA adecuada según lo que tenemos.
6. **Cambios concretos:** lista numerada de cambios, cada uno con el texto nuevo listo para pegar.
7. **Lo que está bien** y no hay que tocar.

No inventes datos. Si algo no lo sabes seguro (cuotas, precios o políticas), dilo.

---

## A. Lo que tenemos

**Personas e IAs**
- **Domingo:** aprueba, escucha el audio y publica. Español. Usa Windows, con disco `F:`.
- **Claude** (plan Pro de pago; el límite semanal se gasta rápido): cerebro y revisor. Investiga, escribe escaletas y órdenes, y revisa imágenes y resultados. Puede ver imágenes; no puede oír audio.
- **Codex CLI** (plan ChatGPT Plus): código, Python, FFmpeg, archivos e **imágenes**. Domingo considera su calidad de imagen superior y no gasta créditos de pago. Se lanza con `codex exec`.
- **Antigravity CLI `agy` 1.4.6** (plan Google AI Pro, Gemini 3.8 Flash): cuota cada 5 h con tope semanal, compartida con el Antigravity de escritorio. Se lanza con `agy -p` y está probado que responde sin colgarse. Parece tener `chrome-devtools-mcp` para manejar Chrome, pero no está comprobado.

**Servicios conectados:** ElevenLabs (imagen, vídeo, voces, música y efectos, por créditos), Fish Audio, Canva, vidIQ (análisis de YouTube), Metricool (programar publicaciones), Google Drive, Gmail, Calendar y Supermetrics. En local: CapCut, FFmpeg y Python.

**Herramientas propias ya hechas:** `mezclar_eleven.py`, `auditar_video.py`, `componer_portada.py`, `montaje_provisional.py` y `musica_por_bloques.py`.

**Canal:** "Caminando por el tiempo" (provisional). Recorre una ciudad en primera persona desde la prehistoria hasta hoy, una época por escena, con el año en pantalla. Sin narrador: frases cortas de la gente en la lengua de su época. Referencia: I Caught Time (inglés, 5.000–112.000 vistas por vídeo). Aún no se ha publicado nada.

---

## B. Sistema de trabajo entre IAs (carpeta `F:\automatizacion`)

```
F:\automatizacion\
  CLAUDE.md               instrucciones de Claude (jefe y revisor)
  REGLAS.md               reglas de los obreros
  AGENTS.md / GEMINI.md   presentación de Codex y de Antigravity
  PLANTILLA_TAREA.md
  lanzar_codex.bat / lanzar_antigravity.bat
  pedidos\                peticiones de Domingo
  cola\pendientes\ → revision\ → hechas\ o fallidas\
  entregables\<ID>\       archivos generados
  resultados\codex.md, antigravity.md, revisiones.md
  proyectos\recorridos\PIPELINE_v2.md
```

**Ciclo:** Domingo pide → Claude divide en tareas (`T001_codex.md`…) → Claude lanza a Codex o a Antigravity por consola → el obrero trabaja, deja la tarea en `revision\` y escribe un resumen → Claude revisa y la aprueba (`hechas\`) o la devuelve con una `## Corrección` → Claude informa a Domingo.

**REGLAS.md (obreros), resumen:** solo hacen sus tareas, en orden y respetando dependencias; arreglan las correcciones; **no gastan, publican, suben ni borran sin `Aprobado: sí`**; trabajan solo en la carpeta; reintentan como mucho 2 veces; nunca se aprueban a sí mismos; no inventan.

**Plantilla de tarea:** agente, aprobado, dependencias, objetivo, entradas, pasos, "terminado cuando" (comprobable), "revisión de Claude" (qué mirará) y cierre.

**Lanzamiento:**
- `codex exec --full-auto "Eres Codex. Lee REGLAS.md y haz todas las tareas de cola/pendientes que terminan en _codex."`
- `agy -p "Eres Antigravity. Lee REGLAS.md y haz todas las tareas de cola/pendientes que terminan en _antigravity."`

**Estado:** instalado. Las 3 tareas de prueba (texto, navegador e imagen) **todavía no se han ejecutado**. Para lanzar a los obreros, Claude tiene que abrirse en local en esa carpeta.

---

## C. Pipeline v2 del canal (largos y cortos)

Las reglas detalladas de imagen, voces y errores siguen en `TRAMPAS_IMAGEN.md`, `VOCES_E_IDIOMAS.md` y `ERRORES_APRENDIDOS.md`. Si las tienes, se adjuntan aparte. Resumen: banderas y monumentos del año exacto, sin anacronismos, violencia solo indirecta, famosos sin cara, sin símbolos de odio, sin texto inventado, prompts sin negaciones, primera persona a 1,6 m y 24 mm, y revisión de todas las imágenes.

### 1. Cómo se gana dinero
| Pieza | Para qué | Meta |
|---|---|---|
| **Largo** 8–12 min, 16:9 | Horas de visualización y anuncios dentro del vídeo. Es lo que paga. | 4.000 h públicas en 12 meses + 1.000 suscriptores |
| **Cortos** 45–90 s, 9:16 | Atraer gente al largo y sumar suscriptores | 3–5 cortos por largo, enlazados al largo |

Orden: largo primero y después sus cortos, reutilizando investigación, escaleta, imágenes y audio. Un corto suelto solo sirve para probar una ciudad nueva.

### 2. Riesgos de monetización
- Contenido repetitivo: cada ciudad cambia ruta, paradas, ancla, sonido y gancho. Fuentes en la descripción y capítulos por época.
- Etiqueta de contenido sintético siempre marcada.
- Violencia solo indirecta; sin heridos ni muertos en primer plano; sin símbolos de odio.
- Música generada o con licencia comercial.
- Los cortos no se recortan del largo: se regeneran en vertical, con gancho propio.

### 3. Parámetros
| | Largo | Corto del largo | Corto de prueba |
|---|---|---|---|
| Aspecto | 16:9, 1080p | 9:16 | 9:16 |
| Duración | 8–12 min | 45–90 s | 60–90 s |
| Escenas | 45–65 | 8–15 | 12–15 |
| Segundos por escena | 8–12 | 5–6 | 5–6 |
| Fecha en pantalla | abajo a la derecha | arriba a la izquierda, bajo el 14 % superior | igual |
| Clips animados con IA | 50 % (los hitos) | 100 % | 100 % |
| Resto | Imagen fija con zoom o paneo lento (FFmpeg, gratis) | — | — |
| Tope de gasto (créditos ElevenLabs) | 120.000 | 15.000 | 30.000 |

### 4. Pasos
| # | Paso | Quién | Puerta de Domingo |
|---|---|---|---|
| 1 | Riesgo de monetización, inventario de hitos con fuentes, fichas por parada | Claude | ✔ |
| 2 | Escaleta hasta el año actual, gancho fuerte en la escena 1, presupuesto | Claude | ✔ |
| 3 | Prompts de imagen (estructura de 6 partes) como órdenes | Claude | — |
| 4 | Generar imágenes y hoja de contacto | Codex | — |
| 5 | Revisar **todas** las imágenes con `CALIDAD_VISUAL.md` antes de animar; las malas vuelven al paso 4 | Claude | ✔ |
| 6 | Animar clips en ElevenLabs (estimar antes de lanzar) | Antigravity | solo si supera el presupuesto |
| 6b | Hoja de contacto de cada clip (fotograma cada 0,5 s) | Codex | — |
| 6c | Revisar las hojas (dirección, brazos, patas, flotar, cantidades); máx. 2 intentos de pago por escena | Claude | — |
| 7 | Voces, ambientes, efectos, música | Antigravity | ✔ (escucha) |
| 8 | Montaje, movimiento en fijas, fechas, mezcla −16 LUFS, auditoría, dos másters | Codex | — |
| 9 | Revisión técnica del máster | Claude | ✔ (ve el vídeo) |
| 10 | Portada, título, descripción con fuentes, capítulos, `.srt` | Claude escribe; Codex compone la portada | — |
| 11 | Cortos derivados: 3–5 tramos, repetir pasos 3–10 en vertical | Todos | ✔ |
| 12 | Subir y programar el largo y los cortos enlazados | Antigravity | ✔ (siempre con "sí") |

### 5. Después de publicar
A los 7 días, Claude lee retención, CTR y vistas con vidIQ y apunta en `APRENDIZAJES.md` qué cambiar en el siguiente vídeo.

---

## C2. Calidad visual (CALIDAD_VISUAL.md, resumen)
Problema real: en el corto de México hubo que rehacer muchísimas escenas de vídeo. Fallos: hombres mitad caballo, caballos con dos cuerpos o al revés, carruajes marcha atrás o que van y vuelven, canoa cruzando una pasarela, mujer sin brazo, lanza y persona levitando, gente que cae, dos antorchas en lugar de una, tranvías demasiado rápidos, cosas que flotan, bandera de otro año, letrero posterior a la fecha.
Reglas: cuerpos completos (2 brazos, 2 piernas; animales con 4 patas y 1 cuerpo); todo lo que avanza va hacia delante y el prompt dice hacia dónde; animales de tiro con la cabeza delante; barcas con la proa delante; columnas en una sola dirección; velocidad de época; gravedad (nada flota); cantidades exactas ("only one…"); sombras coherentes; prompts sin negaciones; vehículos y animales parados cuando se pueda y que se mueva la cámara.
Proceso: revisar la imagen antes de pagar el clip, hoja de contacto de cada clip, máximo 2 intentos de pago por escena, prueba del segundo y registrar cada fallo nuevo.
**Pide al revisor:** ¿qué más se puede hacer para que los clips salgan bien a la primera (modelo de vídeo, tipo de plano, duración del clip, prompts, fotograma final)?
Falta por incorporar: las reglas de calidad del canal Dopema Web (`_contrato\ERRORES_APRENDIDOS.md`), que no se han copiado aún.

## D. Dudas y puntos débiles que ya vemos (atácalos)
1. **Viralidad y seguidores casi no están en el pipeline:** no hay estrategia de miniaturas y títulos con pruebas A/B, de series o listas, de frecuencia de publicación ni de comunidad (por ejemplo, que el público vote la siguiente ciudad en los comentarios).
2. **Idioma:** no hay narrador, así que el mismo vídeo podría servir en varios idiomas solo cambiando subtítulos, título y descripción. ¿Canal en español, en inglés o en ambos?
3. **Elegir ciudad por datos:** qué ciudades buscar con vidIQ antes de invertir en un largo.
4. **Antigravity manejando ElevenLabs por navegador** puede ser frágil. ¿Sería mejor que Codex use la API de ElevenLabs con un script?
5. **Coste por largo:** unos 120.000 créditos es una estimación sin probar. ¿Cuántos largos por mes son realistas?
6. **Revisión de Claude:** mirar 65 imágenes por largo gasta mucha cuota. ¿Hojas de contacto, o un primer filtro hecho por otra IA?
7. **TikTok e Instagram:** ¿cortos en las tres redes, con Metricool?
8. **Sin publicar nada aún:** ¿qué mínimo hay que publicar para validar antes de invertir más?
9. **Riesgos técnicos:** el sistema no está probado de punta a punta, las cuotas de Codex y Antigravity tienen límites, y no se ha comprobado si Codex puede generar imágenes desde `codex exec`.
