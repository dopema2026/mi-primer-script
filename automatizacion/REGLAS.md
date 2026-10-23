# Reglas para los obreros (Codex y Antigravity)

Lee esto antes de cada tarea. Claude revisa todo lo que entregas.

1. Tus tareas están en `cola/pendientes/`. Haz solo las que llevan tu nombre en el archivo (`_codex` o `_antigravity`).
2. Hazlas en orden por número. Si una depende de otra sin terminar, sáltala.
3. Si la tarea tiene una sección `## Corrección`, es una devolución de Claude: arregla exactamente lo que pide.
4. Trabaja solo dentro de `F:\automatizacion`. Lo que generes va en `entregables/<ID>/`.
5. Si generas imágenes o vídeo, o escribes sus prompts, cumple `CALIDAD_VISUAL.md`.
6. No inventes. Si falta información, marca FALLO y explica qué falta.

## Candados (no se saltan nunca)
7. **Gasto:** nada que gaste créditos (ElevenLabs, APIs de pago) si la tarea no dice `Aprobado_gasto: sí`. Ese "sí" solo lo escribe Domingo.
8. **Simulación primero:** todo script que gaste créditos se ejecuta antes en modo `--dry-run`. Calcula el coste exacto, lo apunta y se para si falta `Aprobado_gasto: sí`.
9. **Cero reintentos en pasos de pago.** Si un paso de pago falla, la tarea va directa a `cola/fallidas/` con el motivo. En pasos gratis, como mucho 2 reintentos.
10. **Un solo intento de animación de pago por escena** (`CALIDAD_VISUAL.md`, apartado C).
11. **Prohibido borrar en `entregables/`.** Nunca `del` ni `rm` sobre entregables. Las versiones nuevas llevan sufijo `_v2`, `_v3`…
12. **Prohibido publicar.** Como mucho se sube como **Privado o Borrador**. Domingo marca la casilla de contenido sintético y publica a mano.

## Al terminar cada tarea, salga bien o mal
13. Mueve su archivo a `cola/revision/` (o a `cola/fallidas/` si falló un paso de pago). Nunca a `hechas`: eso lo decide Claude.
14. Añade al final de `resultados/<tu_nombre>.md` un resumen corto:
    ```
    ## <ID> — OK / FALLO — <fecha y hora>
    - Qué hice:
    - Archivos creados (rutas):
    - Créditos gastados (o 0):
    - Cómo comprobé que está bien:
    - Problemas o dudas:
    ```
