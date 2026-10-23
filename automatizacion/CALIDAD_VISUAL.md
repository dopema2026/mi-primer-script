# Calidad visual: realismo y física real

Obligatorio para cualquier imagen o clip de cualquier canal.
Lo leen Codex y Antigravity antes de escribir o lanzar un prompt, y Claude lo usa como lista de revisión.
Cada regla nace de un fallo real del corto de México (entre paréntesis).

## 1. Personas
- Cada persona: **dos brazos, dos piernas, una cabeza, cinco dedos por mano**. (1867: mujer sin brazo)
- Una persona, un cuerpo: nada de cuerpos fundidos con otros, con animales ni con objetos. (1520: hombres mitad caballo)
- Pies en el suelo. Nadie levita, nadie flota. (1519: lanza que levita; 1600: español sobre el agua)
- Nadie cae sin motivo: si corren, siguen de pie. (1968: gente que cae)
- Sin clones: solo una o dos personas nítidas y distintas en edad, complexión y ropa; el resto, lejos o desenfocado.
- Manos: sujetando algo de verdad o fuera del plano. Lo que se sostiene toca la mano o el suelo.
- Un solo gesto llamativo por imagen.
- Famosos sin cara: de espaldas, lejos o tapados por la multitud.

## 2. Animales
- Cada animal: **cuatro patas, un cuerpo, una cabeza**; se cuentan patas y ojos. (1864: caballos con dos cuerpos)
- Animales de tiro: **cabeza delante, en la dirección de la marcha**, bien enganchados al carro. (1867: caballos con el cuerpo al revés)
- Animales quietos y en silencio, salvo que el guion pida otra cosa. (2017: perro aullando)

## 3. Vehículos, barcas y marchas (dirección)
- **Todo lo que avanza va hacia delante**: carros, carruajes, tranvías, coches, barcas, tropas y procesiones.
  El prompt dice **hacia dónde** avanza ("moving away from the viewer toward the cathedral") y añade "always moving forward".
  (1864 y 1867: carruajes que van y vuelven o van marcha atrás)
- Barcas y canoas con **la proa delante**, en el sentido del recorrido, y nunca atravesando puentes ni estructuras. (1325: canoa cruzando la pasarela; canoa al revés)
- **Columnas y marchas:** todos miran y caminan hacia el mismo lado, el que dice el prompt. Escudos en el brazo, de frente. La bandera de la época, a la cabeza.
- **Velocidad de época:** carros al paso; tranvías antiguos despacio. (1910: tranvías a velocidad moderna)
- Si el plano lo permite, vehículos, barcas y animales **parados, atados o amarrados en la foto**, y que el movimiento lo ponga la cámara. Es lo más seguro.

## 4. Física y cantidades
- Gravedad: nada flota. Humo y fuego suben; el agua cae y fluye hacia abajo. (2026: cosas que flotan)
- **Cantidades exactas**: si debe haber una antorcha, el prompt dice "only one torch" y se cuenta en el fotograma. (1968: dos antorchas)
- Luz coherente: las sombras van todas al mismo lado, igual que la fuente de luz (sol, antorcha, farol).
- Escala real: si el hecho fue multitudinario, la multitud llena el fondo hasta el horizonte.

## 5. Época y lugar
- Bandera **del año exacto**, descrita por su dibujo, nunca por su nombre. (1790: salió la cruz de Borgoña cuando ya era la rojigualda)
- El monumento, en el estado de ese día (en obras, sin torres, recién construido).
- Ropa, etnia, oficio y arquitectura de esa década y ese lugar.
- Sin letreros ni nombres posteriores a la fecha. (1969: "Pantitlán", estación de 1984)
- Cada persona habla la lengua de su sitio y de su fecha. (1500: se oyó español antes de que llegaran los españoles)
- Texto en la imagen: solo el que existió de verdad, revisado letra a letra. El resto, sin texto.

## 6. Cómo se escribe el prompt
- **Sin negaciones** ("no", "nobody", "never" plantan lo que niegan). Se describe lo que sí se ve. Excepción: cantidades ("only one…").
- Las restricciones van **dentro de la frase de la escena**, no en una cabecera.
- En el prompt de vídeo:
  - quién se mueve y hacia dónde;
  - qué está quieto ("the carriage stays parked; only the camera walks forward");
  - movimientos pequeños ("everyone keeps small, natural movements").
- Cada escena en su propia llamada, sin imágenes anteriores como referencia (salvo la edición de continuidad).

## 7. Proceso para no tener que retocar
1. **Antes de animar**, Claude revisa la imagen con las secciones 1–5. Si falla algo, se rehace la imagen (Codex, gratis) **antes de gastar** en el clip.
   Se descarta toda foto con pies tapados, manos sin cerrar sobre el objeto o vehículos en posición dudosa.
2. **Escenas de riesgo** (vehículos en marcha, animales, multitudes en movimiento): se prefiere cámara en movimiento con todo lo demás quieto, o una acción a un metro de cámara (herrero, pregonero) en vez de gente corriendo.
3. **Después de animar**, Codex saca **un fotograma cada 0,5 s** de cada clip y monta una **hoja de contacto** por clip. Claude revisa la hoja: dirección de la marcha, brazos, patas, cosas que flotan, cantidades.
4. Como mucho **2 intentos de pago por escena** con la misma foto. Al segundo fallo, nueva foto y otro plano.
5. Antes de regenerar, se añade al prompt la regla concreta que falló y se cuenta el intento.
6. **Prueba del segundo:** si se nota que es IA en menos de un segundo, se rehace.
7. Cada fallo nuevo se apunta aquí, con su ejemplo, para que no se repita.
