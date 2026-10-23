# P000_2 — prueba: QA visual nivel 1

- Agente: antigravity
- Aprobado_gasto: no
- Coste estimado: 0 créditos
- Depende de: P000_1

## Objetivo
Comprobar que `agy -p` ve imágenes, revisa con `CALIDAD_VISUAL.md` y deja su informe sin colgarse.

## Entradas
- `entregables/P000_1/prueba.png`
- `entregables/P000_1/mosaico_3x4.jpg`
- `CALIDAD_VISUAL.md`

## Pasos
1. Abre y mira `prueba.png`. Revisa: brazos, manos y dedos; pies en el suelo; dirección de las sombras; texto o letreros; personas a menos de 4 m y si se solapan; prueba del segundo.
2. Abre `mosaico_3x4.jpg` y comprueba que se ven los números del 1 al 12.
3. Escribe `entregables/P000_2/qa.md` con:
   - un veredicto por punto (OK o FALLO, con el motivo);
   - un veredicto global: APROBADA o RECHAZADA;
   - si pudiste ver la imagen de verdad o solo leer el archivo.

## Terminado cuando
Existe `entregables/P000_2/qa.md` con todos los puntos y el veredicto global.

## Revisión
- QA nivel 2 (Claude): compara su informe con la imagen y valora si su filtro es fiable.

## Al acabar
Sigue los puntos 13 y 14 de `REGLAS.md`.
