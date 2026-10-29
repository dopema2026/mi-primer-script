#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crea un proyecto SINTÉTICO para probar montar_dormir.py sin tocar proyectos reales
ni gastar créditos: imágenes de patrón, una «voz» de tonos con pausas y un ambiente
de ruido marrón. Uso:

  python crear_proyecto_prueba.py <carpeta_vacia> [--minutos 9] [--imagenes 50]
"""
import argparse
import os
import shutil
import subprocess
import sys


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + list(args), check=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("carpeta")
    p.add_argument("--minutos", type=float, default=9)
    p.add_argument("--imagenes", type=int, default=50)
    a = p.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("Falta ffmpeg en el PATH.")
    if os.path.exists(a.carpeta) and os.listdir(a.carpeta):
        sys.exit("La carpeta no está vacía: %s" % a.carpeta)
    os.makedirs(os.path.join(a.carpeta, "imagenes"), exist_ok=True)
    os.makedirs(os.path.join(a.carpeta, "audio"), exist_ok=True)

    for i in range(a.imagenes):
        # algunas en 4:3 para comprobar el recorte a 16:9
        tam = "1600x1200" if i % 5 == 0 else "1920x1080"
        ff("-f", "lavfi", "-i", "testsrc2=s=%s:d=1" % tam, "-vf", "hue=h=%d,drawbox=x=40:y=40:w=200:h=200:color=white@0.8:t=fill" % (i * 37 % 360),
           "-frames:v", "1", os.path.join(a.carpeta, "imagenes", "%03d.png" % (i + 1)))

    seg = a.minutos * 60
    # «voz»: tono que suena 3 s y calla 1 s, con el volumen de una locución normal
    ff("-f", "lavfi", "-i",
       "aevalsrc='0.25*sin(2*PI*180*t)*sin(2*PI*3*t)*lt(mod(t\\,4)\\,3)':s=48000:d=%g" % seg,
       "-c:a", "pcm_s16le", os.path.join(a.carpeta, "audio", "voz.wav"))
    ff("-f", "lavfi", "-i", "anoisesrc=color=brown:amplitude=0.4:d=40:seed=7",
       "-c:a", "pcm_s16le", os.path.join(a.carpeta, "audio", "ambiente.wav"))
    print("Proyecto de prueba creado en", a.carpeta)


if __name__ == "__main__":
    main()
