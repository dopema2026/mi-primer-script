#!/usr/bin/env python3
"""Narra los guiones de guiones-dormir/ con Amazon Polly y genera un MP3 por guion.

Lee solo la sección GUION (sin títulos de capítulo), mete 1,5 s entre párrafos y
4 s entre capítulos, y une los trozos con ffmpeg.

Uso:
  python3 narrar_dormir.py --dry-run                      # cuenta caracteres y coste, sin llamar a Polly
  python3 narrar_dormir.py --prueba-2min guiones-dormir/01-*.md                         # Sergio generativa
  python3 narrar_dormir.py --prueba-2min --voz Lucia guiones-dormir/01-*.md
  python3 narrar_dormir.py --prueba-2min --voz Raul --motor long-form guiones-dormir/01-*.md
  python3 narrar_dormir.py --voz Sergio guiones-dormir/01-*.md                          # guion completo

Voces de España: Raúl y Alba solo existen en long-form; Sergio y Lucía, en generativa.
Si Polly rechaza la etiqueta de velocidad con algún motor, repetir con --velocidad "".

Credenciales: las normales de AWS (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
AWS_DEFAULT_REGION). Necesita boto3 y ffmpeg.
"""
import argparse
import glob
import html
import os
import re
import subprocess
import sys
import tempfile

PAUSA_PARRAFO = "1.5s"
PAUSA_CAPITULO = "4s"
MAX_CARACTERES = 2800  # Polly factura hasta 3000 caracteres de texto por petición
PRECIO_POR_MILLON = {"standard": 4, "neural": 16, "long-form": 100, "generative": 30}
MOTORES_POR_VOZ = {
    "Raul": {"long-form"},
    "Alba": {"long-form"},
    "Sergio": {"neural", "generative"},
    "Lucia": {"standard", "neural", "generative"},
}
PALABRAS_PRUEBA = 240  # unos 2 minutos a ritmo de dormir


def leer_guion(ruta):
    """Devuelve una lista de capítulos; cada capítulo es una lista de párrafos."""
    texto = open(ruta, encoding="utf-8").read()
    inicio = texto.index("## GUION")
    fin = texto.index("## FUENTES")
    capitulos, actual = [], []
    for bloque in re.split(r"\n\s*\n", texto[inicio + len("## GUION"):fin]):
        bloque = bloque.strip()
        if not bloque or bloque == "---":
            continue
        if bloque.startswith("#"):
            if actual:
                capitulos.append(actual)
            actual = []
            continue
        actual.append(" ".join(bloque.split()))
    if actual:
        capitulos.append(actual)
    return capitulos


def recortar(capitulos, palabras):
    """Primeros párrafos del guion hasta sumar al menos `palabras` palabras."""
    parrafos, total = [], 0
    for parrafo in (p for c in capitulos for p in c):
        parrafos.append(parrafo)
        total += len(parrafo.split())
        if total >= palabras:
            break
    return [parrafos]


def trozos_ssml(capitulos, velocidad):
    """Agrupa párrafos en peticiones SSML de menos de MAX_CARACTERES de texto."""
    trozos, partes, largo = [], [], 0
    for i, capitulo in enumerate(capitulos):
        for j, parrafo in enumerate(capitulo):
            ultimo_del_capitulo = j == len(capitulo) - 1
            pausa = PAUSA_CAPITULO if ultimo_del_capitulo and i < len(capitulos) - 1 else PAUSA_PARRAFO
            if partes and largo + len(parrafo) > MAX_CARACTERES:
                trozos.append(partes)
                partes, largo = [], 0
            partes.append((parrafo, pausa))
            largo += len(parrafo)
    if partes:
        trozos.append(partes)

    ssml = []
    for partes in trozos:
        cuerpo = "".join(f'{html.escape(p, quote=False)}<break time="{b}"/>' for p, b in partes)
        if velocidad:
            cuerpo = f'<prosody rate="{velocidad}">{cuerpo}</prosody>'
        ssml.append(f"<speak>{cuerpo}</speak>")
    return ssml


def capitulos_a_narrar(ruta, args):
    capitulos = leer_guion(ruta)
    return recortar(capitulos, PALABRAS_PRUEBA) if args.prueba_2min else capitulos


def narrar(ruta, args, polly):
    ssml = trozos_ssml(capitulos_a_narrar(ruta, args), args.velocidad)
    sufijo = f"_prueba_{args.voz}_{args.motor}.mp3" if args.prueba_2min else ".mp3"
    salida = os.path.join(args.salida, os.path.basename(ruta).replace(".md", sufijo))
    if os.path.exists(salida):
        print(f"ya existe, lo salto: {salida}")
        return
    with tempfile.TemporaryDirectory() as tmp:
        lista = []
        for n, trozo in enumerate(ssml):
            respuesta = polly.synthesize_speech(
                Text=trozo, TextType="ssml", OutputFormat="mp3",
                VoiceId=args.voz, Engine=args.motor, SampleRate="24000",
            )
            parte = os.path.join(tmp, f"{n:04d}.mp3")
            with open(parte, "wb") as f:
                f.write(respuesta["AudioStream"].read())
            lista.append(parte)
            print(f"\r{os.path.basename(ruta)}: {n + 1}/{len(ssml)}", end="", flush=True)
        indice = os.path.join(tmp, "lista.txt")
        with open(indice, "w") as f:
            f.writelines(f"file '{p}'\n" for p in lista)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", indice, "-c", "copy", salida], check=True)
    print(f"\n-> {salida}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("guiones", nargs="*")
    parser.add_argument("--voz", default="Sergio", choices=sorted(MOTORES_POR_VOZ))
    parser.add_argument("--motor", default="generative", choices=sorted(PRECIO_POR_MILLON))
    parser.add_argument("--velocidad", default="90%", help="prosody rate; vacío para no usarlo")
    parser.add_argument("--region", default=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
                        help="long-form y generativa están en us-east-1")
    parser.add_argument("--salida", default="audios")
    parser.add_argument("--prueba-2min", action="store_true",
                        help="narra solo los primeros ~2 minutos, para comparar voces")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.motor not in MOTORES_POR_VOZ[args.voz]:
        parser.error(f"la voz {args.voz} solo existe con el motor: {', '.join(sorted(MOTORES_POR_VOZ[args.voz]))}")

    rutas = args.guiones or sorted(glob.glob("guiones-dormir/[01][0-9]-*.md"))
    rutas = [r for r in rutas if not os.path.basename(r).startswith("00")]

    total = 0
    for ruta in rutas:
        caracteres = sum(len(p) for c in capitulos_a_narrar(ruta, args) for p in c)
        total += caracteres
        print(f"{os.path.basename(ruta)}: {caracteres:,} caracteres")
    print(f"TOTAL: {total:,} caracteres ≈ {total / 1e6 * PRECIO_POR_MILLON[args.motor]:.0f} USD con el motor {args.motor}")
    if args.dry_run:
        return

    import boto3
    polly = boto3.client("polly", region_name=args.region)
    os.makedirs(args.salida, exist_ok=True)
    for ruta in rutas:
        narrar(ruta, args, polly)


if __name__ == "__main__":
    sys.exit(main())
