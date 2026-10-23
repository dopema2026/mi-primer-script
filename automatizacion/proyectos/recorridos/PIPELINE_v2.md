# Pipeline v2 — Caminando por el tiempo (largos y cortos)

Sustituye al reparto de trabajo de `F:\ProyectoYoutube\RECORRIDOS\PIPELINE_RECORRIDOS.md`.
Las reglas de imagen, voz y errores siguen en `TRAMPAS_IMAGEN.md`, `VOCES_E_IDIOMAS.md` y `ERRORES_APRENDIDOS.md`: los obreros las leen antes de cada tarea.

## 1. Cómo se gana dinero
| Pieza | Para qué | Meta |
|---|---|---|
| **Largo** 8–12 min, 16:9 | Horas de visualización y anuncios dentro del vídeo. Es lo que paga. | 4.000 h públicas en 12 meses + 1.000 suscriptores |
| **Cortos** 45–90 s, 9:16 | Atraer gente al largo y sumar suscriptores. Pagan poco. | 3–5 cortos por cada largo, enlazados al largo |

Orden: **largo primero, cortos después**, reutilizando su investigación, escaleta, imágenes y audio.
Un corto suelto solo sirve para probar una ciudad nueva antes de hacer su largo.

## 2. Riesgos de monetización (revisar en cada vídeo)
- **Contenido repetitivo:** cada ciudad cambia la ruta, el número de paradas, el ancla, el sonido y el gancho. Fuentes en la descripción y capítulos por época.
- **IA realista:** etiqueta de contenido sintético siempre marcada.
- **Violencia:** solo indirecta. Sin heridos ni muertos en primer plano. Sin símbolos de odio.
- **Música:** solo generada o con licencia comercial.
- **Cortos copiados del largo:** no se recortan; se regeneran en vertical, con otro montaje y gancho propio.

## 3. Parámetros por formato
| | Largo | Corto del largo | Corto de prueba |
|---|---|---|---|
| Aspecto | 16:9, 1080p | 9:16 | 9:16 |
| Duración | 8–12 min | 45–90 s | 60–90 s |
| Escenas | 45–65 | 8–15 | 12–15 |
| Segundos por escena | 8–12 | 5–6 | 5–6 |
| Fecha en pantalla | abajo derecha | arriba izquierda, bajo el 14 % superior | igual |
| Clips animados | 50 % (los hitos) | 100 % | 100 % |
| Resto de escenas | Imagen fija con movimiento de cámara en local (FFmpeg, gratis) | — | — |
| Tope de gasto | 120.000 créditos | 15.000 | 30.000 |

En los largos, la mitad de las escenas son imágenes fijas con zoom y paneo lentos hechos con FFmpeg. Así el coste baja a la mitad.

## 4. Pasos y quién los hace
| # | Paso | Quién | Sale | Puerta (aprueba Domingo) |
|---|---|---|---|---|
| 1 | Riesgo de monetización, inventario de hitos con fuentes y fichas por parada | Claude | `INVENTARIO_HITOS.md`, `INVESTIGACION.md` | ✔ 1 |
| 2 | Escaleta hasta el año actual, gancho fuerte en la escena 1, presupuesto | Claude | `escaleta.json`, `ESCALETA.md`, `PRESUPUESTO.md` | ✔ 2 |
| 3 | Prompts de imagen, uno por escena, con la estructura de 6 partes | Claude | órdenes en `cola/pendientes/` | — |
| 4 | Generar las imágenes | **Codex** | `imagenes/` + hoja de contacto | — |
| 5 | Revisar **todas** las imágenes (bandera, cuerpos, manos, texto, anacronismos, prueba del segundo) | Claude | `REVISION.md`; las malas vuelven al paso 4 | ✔ 3 |
| 6 | Animar los clips en ElevenLabs (estimar antes de lanzar) | **Antigravity** | `clips/` | Solo si supera el presupuesto |
| 7 | Voces, ambientes, efectos y música | **Antigravity** | `audio/` | ✔ 4 (Domingo escucha) |
| 8 | Montaje, movimiento en imágenes fijas, fechas, mezcla a −16 LUFS, auditoría, dos másters | **Codex** | `render/` | — |
| 9 | Revisión técnica del máster (duración, fechas en su escena, cortes) | Claude | informe | ✔ 5 (Domingo ve el vídeo) |
| 10 | Portada, título, descripción con fuentes, capítulos, `.srt` | Claude escribe, Codex compone la portada | `entrega/` | — |
| 11 | Cortos derivados: Claude elige 3–5 tramos y repite los pasos 3–10 en vertical | Todos | cortos 9:16 | ✔ 6 |
| 12 | Subir y programar (largo y cortos enlazados) | **Antigravity** | publicado | ✔ 7 (siempre con "sí") |

Claude no genera, no monta y no sube: piensa, escribe las órdenes y revisa.

## 5. Después de publicar
- A los 7 días: Claude lee retención, CTR y vistas (vidIQ) y anota en `APRENDIZAJES.md` qué funcionó.
- Esas notas cambian la siguiente escaleta: gancho, duración y tipo de hitos.
