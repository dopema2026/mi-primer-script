# montar_dormir.py — montador para «Historia para dormir»

Herramienta nueva e independiente. **No modifica** `montar.py`, `montar_por_partes.py`,
`auditar_video.py` ni los scripts de `roma_para_dormir`. Solo lee la voz, el ambiente y las
imágenes del proyecto, y escribe en `<proyecto>\_tmp_dormir` y `<proyecto>\render`.
Nunca sobrescribe un máster: cada montaje lleva fecha y hora en el nombre.

Necesita Python 3.8 o posterior y FFmpeg (con `ffmpeg` y `ffprobe` en el PATH). No usa
servicios de pago.

## Carpeta del proyecto

```
F:\ProyectoYoutube\barco_dormir\
    audio\voz.wav            ← narración aprobada
    audio\ambiente.wav       ← madera y oleaje, con licencia comprobada (mínimo 15 s)
    imagenes\001.png ...     ← una imagen distinta por escena
    plan_dormir.json         ← lo crea la orden «plantilla»
```

## Uso en tres pasos

1. **Plantilla** (lee la duración real de la voz y propone los huecos de escena):

   ```
   python montar_dormir.py plantilla --proyecto "F:\ProyectoYoutube\barco_dormir"
   ```

   Abre `plan_dormir.json`, ajusta cada `"inicio"` a la narración real, pon la imagen de
   cada escena y rellena `"licencia"` del ambiente (procedencia + licencia). Sin licencia
   no monta.

2. **Validar** (no renderiza nada):

   ```
   python montar_dormir.py validar --proyecto "F:\ProyectoYoutube\barco_dormir"
   ```

3. **Montar**. Primero una prueba corta, y después el vídeo completo:

   ```
   python montar_dormir.py montar --proyecto "F:\ProyectoYoutube\barco_dormir" --hasta 600
   python montar_dormir.py montar --proyecto "F:\ProyectoYoutube\barco_dormir"
   ```

   Las partes ya renderizadas con **exactamente** los mismos datos se reutilizan. Si cambias
   una imagen, un tiempo o un ajuste, esa parte se vuelve a renderizar sola, así que nunca
   se cuela una parte antigua.

## Qué aplica (criterios de Domingo, no reglas de YouTube)

| Aspecto | Valor |
| --- | --- |
| Primeros 7 min | escenas de 8–14 s, zoom suave hasta 1,08 |
| Desde el minuto 7 | escenas de 25–40 s, zoom o paneo hasta 1,06 |
| Fundidos | 2–3 s entre todas las escenas, también entre partes |
| Movimiento | acercar, paneo, alejar, paneo… (o el que indiques en cada escena) |
| Brillo | igual hasta la mitad; baja poco a poco hasta un 25 % (tope 30 %) |
| Negro | nunca funde a negro; avisa si hay más de 1,5 s de pantalla negra |
| Repeticiones | da error si dos escenas usan la misma imagen |
| Ambiente | bucle sin costuras, ~22 dB por debajo de la voz, se apaga en la cola final |
| Sonoridad | −16 LUFS integrados, pico real −1,5 dBTP, en dos pasadas |
| Vídeo final | H.264, CRF 20, 24 fps, AAC 192 kb/s |

Opciones útiles de `montar`:

- `--por-parte 6` usa menos memoria si el ordenador va justo (por defecto, 10).
- `--eq-voz` aplica a la voz un paso alto a 80 Hz y un filtro que quita las sibilancias.
- `--ancho 1280 --alto 720` sirve para pruebas rápidas.

## Probar sin material real

```
python pruebas\crear_proyecto_prueba.py C:\temp\prueba_dormir --minutos 9
python montar_dormir.py plantilla --proyecto C:\temp\prueba_dormir
```

Después escribe cualquier texto en `"licencia"` y ejecuta `montar` con `--ancho 640 --alto 360`.

## Límites

- Estas comprobaciones no sustituyen la revisión completa del máster por parte de Domingo.
- Cumplir estos valores no garantiza la aprobación de YouTube.
- Después de montar, pasa también `auditar_video.py --perfil dormir`.
