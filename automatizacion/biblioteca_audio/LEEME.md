# Biblioteca de audio reutilizable (coste 0)

Sonidos de ambiente y efectos que se usan en muchos vídeos. Se generan o consiguen **una sola vez** y se reutilizan.

## Regla
- Antes de pedir un ambiente o efecto a ElevenLabs, busca aquí. Si existe, se usa este (0 créditos).
- Solo se gastan créditos en **voces históricas nuevas** y en **efectos únicos** de una escena.
- Cada sonido nuevo que se pague y sirva para más vídeos se guarda aquí después.

## Carpetas
viento · lluvia · agua · fuego · pasos (tierra, adoquín, asfalto, madera) · caballos_carros · multitud_mercado · tráfico · campanas · aves_naturaleza

## Nombres de archivo
`<categoria>_<descripcion>_<segundos>s_<origen>.wav`
Ejemplo: `pasos_adoquin_lento_30s_eleven.wav`

`origen`: `eleven` (generado con licencia comercial), `propio` (grabado por Domingo) o el nombre de una librería con licencia comercial. Nunca audio sin licencia.

## Índice
`INDICE.csv`: archivo, categoría, segundos, loop (sí/no), origen, licencia y fecha. Lo mantiene Codex.
El script de mezcla busca en este índice antes de pedir nada nuevo.
