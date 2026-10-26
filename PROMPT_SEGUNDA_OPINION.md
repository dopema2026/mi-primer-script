# Prompt para pedir segunda opinión (ChatGPT / Codex)

Copia todo lo que hay debajo de la línea y pégalo tal cual.

---

Quiero tu opinión crítica e independiente sobre mi proyecto de YouTube. Ya he consultado a dos IA (Claude y Gemini) y te resumo abajo lo que dice cada una. No quiero que me des la razón ni que des la razón a ninguna de las dos: quiero que me digas qué está mal, qué sobra y qué harías tú en mi lugar. Si das una cifra, di de dónde sale o márcala como estimación.

## Quién soy y qué busco

- Soy Domingo, de España. Creador en solitario, canales «faceless» (sin cara), no soy programador.
- **Objetivo número uno: monetizar** (Programa de Socios de YouTube con anuncios: 1.000 suscriptores + 4.000 horas de visualización pública en 12 meses, o 10 millones de vistas de Shorts en 90 días). Ningún canal está monetizado todavía.
- Trabajo con varias IA: Claude (guiones, investigación, scripts, montaje), Codex (genera todas las imágenes, gratis con su generador), ElevenLabs, Fish Audio y Amazon Polly (voces), Lyria y ElevenLabs (música), vidIQ (investigación), Metricool (programación de publicaciones), CapCut (subtítulos, los pongo yo a mano).

## Mis canales (datos a 26 oct 2026)

| Canal | Idioma | Subs | Qué publica | Estado |
|---|---|---|---|---|
| **Dopema Web** | Español | 532 | Historia, ciencia y misterio. ~21 largos de 9–15 min y ~164 shorts. CTR de largos 2,7 % (28 sep). Hasta ahora 3 shorts/día + 1–2 largos/semana. También TikTok, Instagram, Facebook | Activo, el más cercano a monetizar |
| **El Porqué de las Cosas** | Español | 100 | Shorts de 90–150 s (2/día) de ciencia, historia, misterio y psicología; 20 largos de 8–11 min (~2.050 vistas en total, el 59 % en un solo vídeo) | Activo. Comparte «fábrica», tono, estilos y temas con Dopema Web |
| **Rough Ages** | Inglés | 1 | Largos de ~9–15 min de historia de la vida cotidiana (barberos cirujanos, baños medievales, vikingos). Unos 20 vídeos hechos | Parado desde el 12 oct |
| **Time Runners** | Multilingüe (sin narrador) | 5 | Una ciudad recorrida en primera persona desde la prehistoria hasta hoy; clips de vídeo IA animados, ambientes, música de época y frases breves en la lengua de cada época. Primer vídeo (Ciudad de México) en revisión, con errores históricos detectados. Competidores del nicho: canales de 1–6 K subs con 50 K–500 K vistas por vídeo; ninguno en español | Sin publicar. Coste ~200.000 créditos de ElevenLabs por largo. La cuenta de ElevenLabs usada es de un tercero (con su autorización escrita) |
| **El engranaje oculto** | Español | 0 | 18 vídeos de geopolítica y cadenas de suministro, 9–31 vistas cada uno | Prácticamente abandonado |

## Cómo produzco (Dopema Web y El Porqué, misma «fábrica»)

Tema (vidIQ + intuición; fórmula «sujeto famoso + creencia extendida + dato que la tumba») → investigación con fuentes → guion en JSON (una frase = una escena = una imagen) → narración con voz IA → plan de escenas con tiempos reales → prompts de imagen → Codex genera las imágenes (yo pego la orden) → revisión de todas las imágenes → montaje automático con scripts Python/FFmpeg → yo lo veo y apruebo → yo pongo subtítulos en CapCut → portadas → programación en Metricool.

Reglas propias que aplico:
- Etiqueta de contenido IA siempre.
- **Voz distinta a la del vídeo anterior** y **estilo de arte distinto en cada short** (para que no parezca contenido repetitivo).
- Nunca pedir like ni suscripción; títulos sensacionalistas que no desvelan el vídeo.
- Nada se publica sin mi aprobación; todo dato con fuente.
- Muchos documentos de reglas (pipeline, estado, aprendido, decisiones) que las IA leen antes de trabajar.

Gastos fijos: Claude Pro, ElevenLabs (plan alto), Fish Audio, vidIQ, Metricool, créditos en la nube. Ingresos: 0.

## Lo nuevo: 12 guiones de «historia para dormir»

He encargado 12 guiones de ~2 h de narración cada uno (Edad Media, Roma, Egipto, primera vuelta al mundo, estoicismo, siete maravillas, ruta de la seda…), escritos en tono tranquilo, con datos rigurosos y estructura distinta en cada uno. Idea: subirlos a Dopema Web para sumar horas de visualización rápido (la gente los deja puestos toda la noche). Narración prevista con Amazon Polly (voz Raúl) o Fish Audio; coste estimado ~25 $ los 12 con Polly generativa, ~84 $ con Polly long-form.

## Lo que yo pienso hacer ahora

- **Dopema Web:** dejar de publicar shorts (solo salen los ya programados). Solo largos de 10–15 min + vídeos de dormir de 2 h.
- **El Porqué de las Cosas:** solo shorts (y algún largo).
- **Time Runners:** largos y algún corto.
- Rough Ages y El engranaje oculto, parados.

## Lo que dice Claude

1. Foco total en Dopema Web hasta 1.000 subs y 4.000 horas. Los shorts no suman horas.
2. Vídeos de dormir en Dopema Web como serie aparte, uno por semana, con lista de reproducción propia.
3. **No dejar Dopema Web en 0 shorts**: en un canal pequeño los shorts son la principal fuente de suscriptores (faltan 468). Mantener **1 short diario de embudo** enlazado a un largo con «Vídeo relacionado» hasta llegar a 1.000.
4. El Porqué canibaliza a Dopema Web (mismo idioma, misma fábrica, mismos temas). Solo tiene sentido si se diferencia de verdad (voz, estilo y temas propios); si no, pausarlo.
5. Time Runners es el canal de más potencial pero el de más riesgo: no publicar hasta tener licencia comercial propia de voz, corregir errores históricos de México y bajar el coste por vídeo.
6. Voz para dormir: prueba de 2 minutos con Polly Raúl generativa, Polly Raúl long-form y Fish; decidir de oído.
7. Crítica a mi forma de producir (ver abajo).

## Lo que dice Gemini

1. Coincide en el foco 80/20 en Dopema Web y en el CTR de 2,7 % como problema principal.
2. Vídeos de dormir: **desmarcar «Publicar en el feed de suscripciones y notificar»** para no hundir el CTR con la audiencia de shorts.
3. Vídeos de dormir con **40–60 imágenes** (Codex + mapas/grabados de dominio público), movimiento Ken Burns, partículas/lluvia/viñeteo que oscurece la pantalla desde el minuto 40 y ambiente sonoro continuo; 15–25 imágenes en 2 h sería riesgo de rechazo por «contenido repetitivo».
4. Pausar El Porqué (en otra respuesta dijo que valía si se diferencia).
5. Rough Ages: no producir más, pero rescatar a coste 0 los vídeos ya subidos (títulos, miniaturas y descripciones con vidIQ).
6. Pausar El engranaje oculto y Time Runners hasta resolver licencia, errores y coste.
7. Shorts en Dopema Web: primero recomendó 1 al día; cuando dije 0, lo llamó «acierto total».
8. Usar Fish o ElevenLabs en vez de Polly para que la voz suene menos robótica.
9. Pruebas A/B de miniaturas en YouTube Studio para subir el CTR.
10. Ahorrar: trabajar en sesiones cortas, guardar todo en el repositorio y usar modelos más baratos para tareas mecánicas.

## Crítica de Claude a mi forma de producir

- **Demasiados canales para una persona:** 5 canales, ~640 suscriptores en total, ninguno monetizado. La dispersión es el mayor freno.
- **Se optimiza la producción, no el empaquetado:** hay una fábrica muy elaborada, pero el cuello de botella es el clic (CTR 2,7 %). Miniatura y título deberían llevarse más tiempo que el resto.
- **Rotar voz y estilo de arte en cada vídeo destruye la identidad del canal.** La política de YouTube castiga el contenido producido en masa sin aportación, no la coherencia. Una voz fija y un estilo reconocible son marca; cambiarlos siempre hace que el canal parezca precisamente una granja.
- **Cambios de rumbo constantes:** cadencias, voces, herramientas y canales cambian cada pocos días, antes de tener datos suficientes para juzgar. Hace falta mantener un formato 8–10 vídeos antes de decidir.
- **Exceso de proceso y de documentación:** muchas reglas, puertas de aprobación y documentos que las IA tienen que leer (gastando créditos). Yo mismo soy el cuello de botella al aprobarlo todo.
- **Gastos fijos sin ingresos:** varias suscripciones de pago con 0 € de ingresos. Falta un presupuesto mensual con tope.
- **Riesgo legal:** usar una cuenta de ElevenLabs de un tercero para contenido comercial.
- Lo bueno: rigor con las fuentes, etiqueta IA siempre, monetización como criterio, temas con buena arquitectura («lo que te contaron era falso») y un sistema para apuntar datos de cada vídeo.

## Lo que te pido

1. **Tu diagnóstico sincero** de mi situación y de mi forma de producir. ¿Qué está mal de raíz?
2. **En qué tienen razón y en qué se equivocan Claude y Gemini**, punto por punto donde discrepen (sobre todo: shorts en Dopema Web 0 o 1 al día; El Porqué pausado o diferenciado; Polly frente a Fish/ElevenLabs; número de imágenes en los vídeos de dormir).
3. **¿Es buena idea subir vídeos de dormir de 2 h a Dopema Web**, un canal de historia con audiencia de shorts? ¿O mejor un canal aparte? Piensa en monetización, no en estética.
4. **Riesgos de rechazo en la revisión del Programa de Socios** que nadie ha mencionado.
5. **Un plan de 8 semanas** concreto (qué publicar, cuántos, en qué canal) para llegar a monetizar Dopema Web, con lo que se puede medir cada semana.
6. **Qué dejarías de hacer o de pagar** desde mañana.

Responde en español de España, directo, sin rodeos y sin darme la razón por defecto.
