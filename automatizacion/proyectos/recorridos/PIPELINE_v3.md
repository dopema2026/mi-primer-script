# Pipeline v3 — canal de recorridos en el tiempo (largos y cortos)

Sustituye al reparto de trabajo de `F:\ProyectoYoutube\RECORRIDOS\PIPELINE_RECORRIDOS.md`.
Obligatorio: `F:\automatizacion\CALIDAD_VISUAL.md` (6 leyes físicas) y los candados de `REGLAS.md`.
Siguen vigentes `TRAMPAS_IMAGEN.md`, `VOCES_E_IDIOMAS.md` y `ERRORES_APRENDIDOS.md` en todo lo que no contradiga lo anterior.

## 1. Estrategia
- **Canal único en inglés:** nombre, `@handle` y metadatos base en inglés, para captar el RPM alto anglosajón.
- **El dinero está en YouTube.** TikTok, Instagram y Facebook sirven solo de embudo y prueba viral.
- **Texto quemado en el vídeo: solo el año** (`320 BC`, `1521`). La única excepción es la pregunta final de comunidad.
- **Traducciones en cada subida** (Codex): título, descripción y `.srt` (incluidas las frases históricas habladas) en 6 idiomas: inglés (base), español, portugués, francés, alemán y japonés.

## 2. Fase 0: validación (obligatoria; prohibido empezar por largos)
- Con 0 vídeos publicados está **prohibido** producir un largo.
- Primero, **3–5 cortos de validación**: 45–55 s, 9–11 escenas de 5 s, **techo de 15.000–18.000 créditos por corto**.
- **Un largo de una ciudad solo se desbloquea** si su corto supera **una** de estas métricas:
  - 70 % en "Viewed vs. Swiped Away";
  - 65 % de retención media;
  - 15.000 vistas orgánicas.

## 3. Paso 0: elegir ciudad por datos (vidIQ)
Ninguna ciudad entra sin comprobar:
1. Volumen de búsqueda en inglés: `[City] evolution`, `ancient [City]`, `[City] through time`.
2. Un **ancla visual reconocible en todo el mundo**.
3. Vídeos atípicos (outliers) sobre esa ciudad: más de 3 veces las vistas que corresponden a los suscriptores del canal, en canales pequeños.

## 4. Parámetros
| | Corto de validación | Largo (desbloqueado) | Corto derivado |
|---|---|---|---|
| Aspecto | 9:16 | 16:9, 1080p | 9:16 |
| Duración | 45–55 s | 8–10 min | 45–55 s |
| Segundos por escena | 5 | **5–7** | 5 |
| Escenas | 9–11 | ~70–110 | 9–11 |
| Año en pantalla | arriba a la izquierda, bajo el 14 % superior | abajo a la derecha | como el corto |
| Animación de pago | solo escenas que cumplan las 6 leyes | hitos clave | reutiliza el largo |
| Resto | falso vídeo vivo FFmpeg (0 créditos) | falso vídeo vivo FFmpeg | — |
| Techo de gasto | 15.000–18.000 | por fijar (Domingo) | por fijar |

## 5. Gancho, viralidad y comunidad
- **Segundos 0–2: impacto inmediato** a 1–3 m de cámara. Puede ser un rebobinado relámpago de 1,5 s desde 2026 hacia el pasado, o una acción potente en primer plano. **Prohibido abrir con bosque o descampado vacío.**
- **Ritmo:** 5–7 s por escena, también en los largos.
- **Miniaturas de largos:** siempre 3 radicalmente distintas para "Test & Compare" de YouTube:
  - A: pantalla partida, pasado frente a hoy;
  - B: la época cumbre, épica, con máximo 2 palabras;
  - C: 3 franjas de años.
- **Motor de comunidad:** en los últimos 3 s de la escena final (año actual), la pregunta "Where do we walk next? Vote below". Y un comentario listo para que Domingo lo fije, con 3 ciudades concretas a votar.

## 6. Blindaje de monetización (YPP)
- Cero símbolos de odio, cero heridos o sangre, **prohibido recrear tragedias o atentados reales modernos (siglos XX y XXI)**, y sin logos de marcas reales en escenas de 1950 a hoy.
- **La publicación no se automatiza.** Se sube como Privado o Borrador; **Domingo marca a mano "Contenido alterado o sintético"** y publica.
- **Prueba de autoría humana:** cada entregable guarda fuentes históricas, escaleta y capas de mezcla, por si YouTube pide un vídeo de apelación al solicitar el YPP.
- Contenido repetitivo: cada ciudad cambia ruta, ancla, sonido y gancho. Fuentes en la descripción y capítulos por época en los largos.

## 7. Pasos y quién los hace
| # | Paso | Quién | Sale | Puerta de Domingo |
|---|---|---|---|---|
| 0 | Elegir ciudad con datos de vidIQ | Claude | `CIUDAD.md` | ✔ |
| 1 | Riesgo de monetización, inventario de hitos con fuentes, fichas por parada | Claude | `INVENTARIO_HITOS.md` | ✔ |
| 2 | Escaleta (gancho 0–2 s, hasta el año actual), lista de escenas animables (6 leyes) y presupuesto | Claude | `escaleta.json`, `PRESUPUESTO.md` | ✔ |
| 3 | Prompts de imagen (6 partes) y de vídeo (3V, ≤30 palabras) | Claude | órdenes en `cola/pendientes/` | — |
| 4 | Generar imágenes y mosaicos numerados 3×4 | Codex | `imagenes/`, `mosaicos/` | — |
| 5 | QA nivel 1, imagen por imagen | Antigravity | informe QA | — |
| 6 | QA nivel 2 sobre los mosaicos | Claude | aprobadas o devueltas al paso 4 | ✔ |
| 7 | `--dry-run` de animación con el coste exacto | Codex | estimación | ✔ `Aprobado_gasto: sí` |
| 8 | Animar: **un solo intento por escena** (API si existe; si es web, bajo control directo y sin reintentos) | Codex o Antigravity | `clips/` | — |
| 9 | Tiras de fotogramas cada 0,5 s → QA 1 (Antigravity) → QA 2 (Claude). Fallo: opción A o B, sin volver a pagar | Codex, Antigravity, Claude | clips válidos | — |
| 10 | Voces (ElevenLabs por API con `--dry-run`); ambientes y efectos desde `biblioteca_audio/` | Codex | `audio/` | ✔ Domingo escucha |
| 11 | Montaje, falso vídeo vivo, año, pregunta final, mezcla −16 LUFS, dos másters | Codex | `render/` | — |
| 12 | `auditar_video.py` + mosaico del máster → QA 1 → QA 2 | Codex, Antigravity, Claude | informe | ✔ Domingo ve y escucha |
| 13 | 3 miniaturas (largos), título, descripción con fuentes, capítulos, comentario fijado, traducciones a 6 idiomas | Claude escribe; Codex compone y traduce | `entrega/` | — |
| 14 | Subir como Privado o Borrador | Antigravity o Domingo | borrador | ✔ Domingo marca IA y publica |

## 8. Después de publicar
- A los 7 días, Claude mide con vidIQ: Viewed vs. Swiped Away, retención, vistas y CTR.
- Lo apunta en `APRENDIZAJES.md` y decide si se desbloquea el largo de esa ciudad (Fase 0).
