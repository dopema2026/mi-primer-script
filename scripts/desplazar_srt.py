"""Desplaza todos los tiempos de un .srt N segundos (para colocar los subtítulos del cuerpo tras el hook).

Uso: python3 scripts/desplazar_srt.py <entrada.srt> <segundos> <salida.srt>
"""
import re
import sys

TIEMPO = re.compile(r"(\d+):(\d+):(\d+),(\d+)")


def desplazar(match, offset):
    h, m, s, ms = (int(x) for x in match.groups())
    total = max(0, round((h * 3600 + m * 60 + s) * 1000 + ms + offset * 1000))
    h, resto = divmod(total, 3_600_000)
    m, resto = divmod(resto, 60_000)
    s, ms = divmod(resto, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    entrada, offset, salida = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    with open(entrada, encoding="utf-8-sig") as f:
        texto = f.read()
    texto = TIEMPO.sub(lambda m: desplazar(m, offset), texto)
    with open(salida, "w", encoding="utf-8") as f:
        f.write(texto)


if __name__ == "__main__":
    main()
