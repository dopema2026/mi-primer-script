#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
montar_dormir.py — Montador limpio y parametrizable para los vídeos «Historia para dormir».

No tiene rutas fijas: todo sale de la carpeta del proyecto (--proyecto) y de su
archivo plan_dormir.json. Solo LEE la voz, el ambiente y las imágenes; escribe
únicamente dentro de <proyecto>/_tmp_dormir y <proyecto>/render, y nunca
sobrescribe un máster existente.

Tres órdenes:

  plantilla  Crea plan_dormir.json con los huecos de escena según la duración real
             de la voz (rellena con las imágenes de <proyecto>/imagenes si existen).
  validar    Comprueba el plan sin renderizar nada.
  montar     Mezcla el audio (−16 LUFS, ambiente ~22 dB bajo la voz) y monta el vídeo
             por partes, con fundidos, movimiento suave y oscurecimiento gradual.

Ejemplos (Windows):
  python montar_dormir.py plantilla --proyecto "F:\\ProyectoYoutube\\barco_dormir"
  python montar_dormir.py validar   --proyecto "F:\\ProyectoYoutube\\barco_dormir"
  python montar_dormir.py montar    --proyecto "F:\\ProyectoYoutube\\barco_dormir" --hasta 600

Estos criterios son decisiones de producción de Dopema Web, no reglas de YouTube,
y no garantizan la aprobación del canal.
"""

import argparse
import datetime
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys

VERSION = "1.0"

# ---------------------------------------------------------------------------
# Criterios aprobados por Domingo (perfil dormir)
# ---------------------------------------------------------------------------
FASE_INICIO_SEG = 7 * 60          # primeros siete minutos
INICIO_MIN, INICIO_MAX = 8.0, 14.0
CUERPO_MIN, CUERPO_MAX = 25.0, 40.0
FUNDIDO_MIN, FUNDIDO_MAX = 2.0, 3.0
OSCURECER_TOPE = 0.30             # nunca más de un 30 % de oscurecimiento
NEGRO_MAX_SEG = 1.5               # cualquier tramo negro más largo es un fallo

PLAN_POR_DEFECTO = {
    "voz": "audio/voz.wav",
    "ambiente": {"archivo": "audio/ambiente.wav", "licencia": ""},
    "cola_segundos": 30,
    "fundido_segundos": 2.5,
    "ambiente_db_bajo_voz": 22,
    "lufs_objetivo": -16.0,
    "true_peak": -1.5,
    "zoom_inicio": 1.08,
    "zoom_cuerpo": 1.06,
    "oscurecer": {"maximo": 0.25, "desde": 0.5, "hasta": 0.9},
    "escenas": [],
}

MOVIMIENTOS = ("acercar", "paneo_derecha", "alejar", "paneo_izquierda", "quieto")
EXTENSIONES_IMAGEN = (".png", ".jpg", ".jpeg", ".webp")


class ErrorPlan(Exception):
    pass


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def decir(texto=""):
    print(texto, flush=True)


def herramienta(nombre):
    ruta = shutil.which(nombre)
    if not ruta:
        raise ErrorPlan("No encuentro «%s». Instala FFmpeg y añádelo al PATH." % nombre)
    return ruta


def ejecutar(cmd, capturar=False):
    """Ejecuta un comando; si falla, muestra el final del error de FFmpeg."""
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        cola = "\n".join(res.stderr.strip().splitlines()[-15:])
        raise ErrorPlan("Falló el comando:\n  %s\n%s" % (" ".join(cmd[:6]) + " ...", cola))
    return res.stderr if capturar else None


def duracion(ruta):
    salida = subprocess.run(
        [herramienta("ffprobe"), "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", ruta],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    try:
        return float(salida.stdout.strip())
    except ValueError:
        raise ErrorPlan("No puedo leer la duración de: %s" % ruta)


def a_segundos(valor):
    """Acepta 75, 75.5, "1:15" o "0:01:15"."""
    if isinstance(valor, (int, float)):
        return float(valor)
    partes = str(valor).strip().split(":")
    try:
        total = 0.0
        for p in partes:
            total = total * 60 + float(p)
        return total
    except ValueError:
        raise ErrorPlan("Tiempo no válido: %r" % valor)


def hms(seg):
    seg = int(round(seg))
    return "%d:%02d:%02d" % (seg // 3600, (seg % 3600) // 60, seg % 60)


def huella_archivo(ruta):
    h = hashlib.sha1()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def medir_loudnorm(ruta, filtro_previo=""):
    """Primera pasada de loudnorm: devuelve el JSON con input_i, input_tp, etc."""
    af = (filtro_previo + "," if filtro_previo else "") + \
        "loudnorm=I=-16:TP=-1.5:LRA=20:print_format=json"
    err = ejecutar([herramienta("ffmpeg"), "-hide_banner", "-nostats", "-i", ruta,
                    "-af", af, "-f", "null", "-"], capturar=True)
    bloque = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S)
    if not bloque:
        raise ErrorPlan("No pude medir la sonoridad de %s" % ruta)
    return json.loads(bloque.group(0))


def medir_ebur128(ruta):
    err = ejecutar([herramienta("ffmpeg"), "-hide_banner", "-nostats", "-i", ruta,
                    "-map", "0:a:0", "-af", "ebur128=peak=true:framelog=quiet",
                    "-f", "null", "-"], capturar=True)
    resumen = err[err.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", resumen)
    tp = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", resumen)
    return (float(i.group(1)) if i else None, float(tp.group(1)) if tp else None)


def detectar_negro(ruta):
    err = ejecutar([herramienta("ffmpeg"), "-hide_banner", "-nostats", "-i", ruta,
                    "-map", "0:v:0", "-vf",
                    "blackdetect=d=%s:pix_th=0.10" % NEGRO_MAX_SEG, "-an", "-f", "null", "-"],
                   capturar=True)
    tramos = re.findall(r"black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)", err)
    return [(float(a), float(b), float(c)) for a, b, c in tramos]


# ---------------------------------------------------------------------------
# Plan
# ---------------------------------------------------------------------------
def ruta_plan(proyecto):
    return os.path.join(proyecto, "plan_dormir.json")


def cargar_plan(proyecto):
    ruta = ruta_plan(proyecto)
    if not os.path.isfile(ruta):
        raise ErrorPlan("No existe %s. Créalo con: python montar_dormir.py plantilla --proyecto ..." % ruta)
    with open(ruta, encoding="utf-8") as f:
        try:
            datos = json.load(f)
        except json.JSONDecodeError as e:
            raise ErrorPlan("plan_dormir.json tiene un error de formato (línea %d): %s" % (e.lineno, e.msg))
    plan = json.loads(json.dumps(PLAN_POR_DEFECTO))
    plan.update(datos)
    for clave in ("ambiente", "oscurecer"):
        base = dict(PLAN_POR_DEFECTO[clave])
        base.update(datos.get(clave, {}))
        plan[clave] = base
    return plan


def absoluta(proyecto, ruta):
    return ruta if os.path.isabs(ruta) else os.path.join(proyecto, ruta)


def factor_brillo(t, total, osc):
    """1.0 = brillo original. Baja en línea recta entre «desde» y «hasta» (fracciones del total)."""
    ini, fin, maximo = osc["desde"] * total, osc["hasta"] * total, osc["maximo"]
    if t <= ini:
        return 1.0
    if t >= fin:
        return 1.0 - maximo
    return 1.0 - maximo * (t - ini) / (fin - ini)


def preparar_escenas(proyecto, plan, total):
    """Convierte el plan en una lista de escenas con inicio, duración, movimiento y brillo."""
    crudas = plan["escenas"]
    if not crudas:
        raise ErrorPlan("El plan no tiene escenas.")
    escenas = []
    ciclo = ("acercar", "paneo_derecha", "alejar", "paneo_izquierda")
    for n, e in enumerate(crudas):
        if "inicio" not in e or not e.get("imagen"):
            raise ErrorPlan("La escena %d no tiene «inicio» o «imagen»." % (n + 1))
        mov = e.get("movimiento") or ciclo[n % len(ciclo)]
        if mov not in MOVIMIENTOS:
            raise ErrorPlan("Escena %d: movimiento «%s» no válido (usa: %s)." % (n + 1, mov, ", ".join(MOVIMIENTOS)))
        escenas.append({"n": n + 1, "inicio": a_segundos(e["inicio"]),
                        "imagen": absoluta(proyecto, e["imagen"]), "movimiento": mov})
    for a, b in zip(escenas, escenas[1:] + [None]):
        fin = b["inicio"] if b else total
        a["duracion"] = fin - a["inicio"]
        a["brillo"] = round(factor_brillo(a["inicio"] + a["duracion"] / 2, total, plan["oscurecer"]), 4)
    return escenas


def validar(proyecto, plan, total, escenas):
    """Devuelve (errores, avisos). Los errores bloquean el montaje."""
    errores, avisos = [], []
    F = float(plan["fundido_segundos"])
    if not (FUNDIDO_MIN <= F <= FUNDIDO_MAX):
        errores.append("El fundido debe durar entre %g y %g s (ahora %g)." % (FUNDIDO_MIN, FUNDIDO_MAX, F))
    osc = plan["oscurecer"]
    if not (0 <= osc["maximo"] <= OSCURECER_TOPE):
        errores.append("El oscurecimiento máximo debe estar entre 0 y %d %% (ahora %g %%)."
                       % (OSCURECER_TOPE * 100, osc["maximo"] * 100))
    if not (0 <= osc["desde"] < osc["hasta"] <= 1):
        errores.append("En «oscurecer», «desde» debe ser menor que «hasta» (fracciones entre 0 y 1).")
    if osc["desde"] < 0.5:
        avisos.append("El oscurecimiento empieza antes de la mitad del vídeo (desde=%g)." % osc["desde"])

    amb = plan["ambiente"]
    if not str(amb.get("licencia", "")).strip():
        errores.append("Falta «licencia» del ambiente: indica procedencia y licencia comprobada.")
    for etiqueta, ruta in (("voz", absoluta(proyecto, plan["voz"])),
                           ("ambiente", absoluta(proyecto, amb["archivo"]))):
        if not os.path.isfile(ruta):
            errores.append("No existe el archivo de %s: %s" % (etiqueta, ruta))

    if escenas[0]["inicio"] != 0:
        errores.append("La primera escena debe empezar en 0 (empieza en %g)." % escenas[0]["inicio"])
    huellas = {}
    for i, e in enumerate(escenas):
        ultima = i == len(escenas) - 1
        etiqueta = "Escena %d (%s)" % (e["n"], hms(e["inicio"]))
        if e["duracion"] <= 0:
            errores.append("%s: los tiempos no van en orden creciente." % etiqueta)
            continue
        if not os.path.isfile(e["imagen"]):
            errores.append("%s: no existe la imagen %s" % (etiqueta, e["imagen"]))
        else:
            h = huella_archivo(e["imagen"])
            if h in huellas:
                errores.append("%s: repite la imagen de la escena %d. Sin bucles: cada escena, una imagen distinta."
                               % (etiqueta, huellas[h]))
            huellas.setdefault(h, e["n"])
        if e["duracion"] < 2 * F + 1:
            errores.append("%s: dura %.1f s, demasiado poco para dos fundidos de %g s." % (etiqueta, e["duracion"], F))
        if ultima:
            continue  # la última escena incluye la cola final y puede ser más larga
        if e["inicio"] < FASE_INICIO_SEG:
            lo, hi, fase = INICIO_MIN, INICIO_MAX, "primeros 7 min"
        else:
            lo, hi, fase = CUERPO_MIN, CUERPO_MAX, "cuerpo"
        if not (lo <= e["duracion"] <= hi):
            errores.append("%s: dura %.1f s; en %s debe durar entre %g y %g s." % (etiqueta, e["duracion"], fase, lo, hi))
    if escenas[-1]["inicio"] >= total:
        errores.append("La última escena empieza después del final del audio (%s)." % hms(total))
    return errores, avisos


# ---------------------------------------------------------------------------
# Orden: plantilla
# ---------------------------------------------------------------------------
def huecos(total, ritmo_inicio, ritmo_cuerpo):
    inicios, t = [], 0.0
    while t < total:
        inicios.append(round(t, 2))
        t += ritmo_inicio if t < FASE_INICIO_SEG else ritmo_cuerpo
    # si el último hueco queda demasiado corto, lo absorbe el anterior
    minimo = INICIO_MIN if inicios[-1] < FASE_INICIO_SEG else CUERPO_MIN
    if len(inicios) > 1 and total - inicios[-1] < minimo:
        inicios.pop()
    return inicios


def orden_plantilla(args):
    proyecto = args.proyecto
    destino = ruta_plan(proyecto)
    if os.path.exists(destino):
        raise ErrorPlan("Ya existe %s. No lo sobrescribo: renómbralo o bórralo tú si quieres otra plantilla." % destino)
    voz = absoluta(proyecto, PLAN_POR_DEFECTO["voz"] if not args.voz else args.voz)
    if not os.path.isfile(voz):
        raise ErrorPlan("No encuentro la voz en %s (usa --voz para indicar otra ruta)." % voz)
    total = duracion(voz) + args.cola
    inicios = huecos(total, args.ritmo_inicio, args.ritmo_cuerpo)

    carpeta = os.path.join(proyecto, "imagenes")
    imagenes = []
    if os.path.isdir(carpeta):
        imagenes = sorted(f for f in os.listdir(carpeta) if f.lower().endswith(EXTENSIONES_IMAGEN))
    plan = json.loads(json.dumps(PLAN_POR_DEFECTO))
    plan["voz"] = os.path.relpath(voz, proyecto)
    plan["cola_segundos"] = args.cola
    plan["escenas"] = [{"inicio": hms(t) if t == int(t) else t,
                        "imagen": ("imagenes/" + imagenes[i]) if i < len(imagenes) else "",
                        "descripcion": ""} for i, t in enumerate(inicios)]
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    inicio = sum(1 for t in inicios if t < FASE_INICIO_SEG)
    decir("Plantilla creada: %s" % destino)
    decir("Duración total con cola: %s" % hms(total))
    decir("Huecos de escena: %d (%d en los primeros 7 min, %d en el cuerpo)" % (len(inicios), inicio, len(inicios) - inicio))
    if len(imagenes) < len(inicios):
        decir("AVISO: hay %d imágenes en %s y hacen falta %d. Completa las vacías en el plan."
              % (len(imagenes), carpeta, len(inicios)))
    decir("Ajusta cada «inicio» a la narración real y rellena «licencia» del ambiente antes de montar.")


# ---------------------------------------------------------------------------
# Orden: validar
# ---------------------------------------------------------------------------
def cargar_y_validar(proyecto):
    plan = cargar_plan(proyecto)
    voz = absoluta(proyecto, plan["voz"])
    if not os.path.isfile(voz):
        raise ErrorPlan("No existe la voz: %s" % voz)
    total = duracion(voz) + float(plan["cola_segundos"])
    escenas = preparar_escenas(proyecto, plan, total)
    errores, avisos = validar(proyecto, plan, total, escenas)
    return plan, total, escenas, errores, avisos


def informar_validacion(total, escenas, errores, avisos):
    inicio = [e for e in escenas if e["inicio"] < FASE_INICIO_SEG]
    cuerpo = [e for e in escenas if e["inicio"] >= FASE_INICIO_SEG]
    decir("Duración total (voz + cola): %s" % hms(total))
    decir("Escenas: %d  (primeros 7 min: %d · cuerpo: %d)" % (len(escenas), len(inicio), len(cuerpo)))
    if cuerpo:
        d = [e["duracion"] for e in cuerpo[:-1]] or [cuerpo[-1]["duracion"]]
        decir("Cuerpo: escenas de %.0f a %.0f s" % (min(d), max(d)))
    decir("Brillo final: %d %%" % round(escenas[-1]["brillo"] * 100))
    for a in avisos:
        decir("AVISO: " + a)
    for e in errores:
        decir("ERROR: " + e)
    decir("Plan correcto." if not errores else "Plan con %d error(es): no se puede montar." % len(errores))


def orden_validar(args):
    _, total, escenas, errores, avisos = cargar_y_validar(args.proyecto)
    informar_validacion(total, escenas, errores, avisos)
    return 1 if errores else 0


# ---------------------------------------------------------------------------
# Orden: montar — audio
# ---------------------------------------------------------------------------
def bucle_ambiente(origen, destino, cruce=5.0):
    """Crea un bucle sin costura: el final del ambiente se funde con su principio."""
    A = duracion(origen)
    if A < 3 * cruce:
        raise ErrorPlan("El ambiente dura %.1f s; necesito al menos %.0f s para un bucle sin cortes." % (A, 3 * cruce))
    fc = ("[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=3[c][f][p];"
          "[c]atrim=%(c)s:%(f)s,asetpts=PTS-STARTPTS[cuerpo];"
          "[f]atrim=%(f)s:%(A)s,asetpts=PTS-STARTPTS[final];"
          "[p]atrim=0:%(c)s,asetpts=PTS-STARTPTS[principio];"
          "[final][principio]acrossfade=d=%(c)s:c1=qsin:c2=qsin[union];"
          "[cuerpo][union]concat=n=2:v=0:a=1[out]") % {"c": cruce, "f": A - cruce, "A": A}
    ejecutar([herramienta("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error", "-i", origen,
              "-filter_complex", fc, "-map", "[out]", "-c:a", "pcm_s16le", destino])


def mezclar_audio(proyecto, plan, total, hasta, tmp, eq_voz):
    ff = herramienta("ffmpeg")
    voz = absoluta(proyecto, plan["voz"])
    amb = absoluta(proyecto, plan["ambiente"]["archivo"])
    cola = float(plan["cola_segundos"])
    largo = min(total, hasta) if hasta else total
    filtro_voz = "highpass=f=80,deesser" if eq_voz else ""

    decir("Audio 1/4 · midiendo la voz…")
    voz_i = float(medir_loudnorm(voz, filtro_voz)["input_i"])

    decir("Audio 2/4 · preparando el ambiente en bucle sin cortes…")
    bucle = os.path.join(tmp, "ambiente_bucle.wav")
    bucle_ambiente(amb, bucle)
    amb_i = float(medir_loudnorm(bucle)["input_i"])
    ganancia = (voz_i - float(plan["ambiente_db_bajo_voz"])) - amb_i
    decir("        voz %.1f LUFS · ambiente %.1f LUFS → ganancia del ambiente %+.1f dB" % (voz_i, amb_i, ganancia))

    voz_lista = os.path.join(tmp, "voz_preparada.wav")
    cadena = "aformat=sample_rates=48000:channel_layouts=stereo"
    if filtro_voz:
        cadena += "," + filtro_voz
    cadena += ",apad=whole_dur=%.3f,atrim=0:%.3f" % (total, largo)
    ejecutar([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", voz, "-af", cadena,
              "-c:a", "pcm_s16le", voz_lista])

    amb_listo = os.path.join(tmp, "ambiente_ajustado.wav")
    cadena = "volume=%.2fdB,afade=t=in:d=2" % ganancia
    if cola > 0 and largo >= total:
        cadena += ",afade=t=out:st=%.3f:d=%.3f" % (total - cola, cola)
    ejecutar([ff, "-y", "-hide_banner", "-loglevel", "error", "-stream_loop", "-1", "-i", bucle,
              "-af", cadena, "-t", "%.3f" % largo, "-c:a", "pcm_s16le", amb_listo])

    decir("Audio 3/4 · mezclando…")
    previa = os.path.join(tmp, "mezcla_previa.wav")
    # amix divide entre el número de entradas; volume=2 lo compensa y la relación voz/ambiente no cambia
    ejecutar([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", voz_lista, "-i", amb_listo,
              "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=0,volume=2[m]",
              "-map", "[m]", "-c:a", "pcm_s24le", previa])

    decir("Audio 4/4 · normalizando a %g LUFS (dos pasadas)…" % plan["lufs_objetivo"])
    I, TP = float(plan["lufs_objetivo"]), float(plan["true_peak"])
    m = medir_loudnorm(previa)
    final = os.path.join(tmp, "mezcla_final.wav")
    err = ejecutar([ff, "-y", "-hide_banner", "-nostats", "-i", previa, "-af",
                    ("loudnorm=I=%g:TP=%g:LRA=20:measured_I=%s:measured_TP=%s:measured_LRA=%s:"
                     "measured_thresh=%s:offset=%s:linear=true:print_format=json")
                    % (I, TP, m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"]),
                    "-ar", "48000", "-c:a", "pcm_s24le", final], capturar=True)
    tipo = re.search(r'"normalization_type"\s*:\s*"(\w+)"', err)
    return final, largo, ganancia, (tipo.group(1) if tipo else "desconocido")


# ---------------------------------------------------------------------------
# Orden: montar — vídeo
# ---------------------------------------------------------------------------
def expresiones_movimiento(mov, frames, zoom):
    """Expresiones de zoompan con aceleración suave (sin tirones al principio ni al final)."""
    p = "(1-cos(PI*on/%d))/2" % max(frames - 1, 1)
    centro_x, centro_y = "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"
    extra = zoom - 1
    if mov == "acercar":
        return "1+%g*%s" % (extra, p), centro_x, centro_y
    if mov == "alejar":
        return "%g-%g*%s" % (zoom, extra, p), centro_x, centro_y
    if mov == "paneo_derecha":
        return "%g" % zoom, "(iw-iw/zoom)*%s" % p, centro_y
    if mov == "paneo_izquierda":
        return "%g" % zoom, "(iw-iw/zoom)*(1-%s)" % p, centro_y
    return "1", "0", "0"


def renderizar_parte(escenas, ultima_global, cfg, destino):
    ff = herramienta("ffmpeg")
    W, H, fps, k, Ff = cfg["ancho"], cfg["alto"], cfg["fps"], cfg["sobremuestreo"], cfg["fundido_frames"]
    cmd = [ff, "-y", "-hide_banner", "-loglevel", "error"]
    for e in escenas:
        cmd += ["-i", e["imagen"]]
    trozos, offset = [], 0
    for i, e in enumerate(escenas):
        frames = e["frames"] + (0 if e is ultima_global else Ff)
        zoom = cfg["zoom_inicio"] if e["inicio"] < FASE_INICIO_SEG else cfg["zoom_cuerpo"]
        z, x, y = expresiones_movimiento(e["movimiento"], frames, zoom)
        b = e["brillo"]
        trozos.append(
            "[%d:v]scale=%d:%d:force_original_aspect_ratio=increase:flags=lanczos,crop=%d:%d,"
            "format=rgb24,colorchannelmixer=rr=%g:gg=%g:bb=%g,format=yuv420p,"
            "zoompan=z='%s':x='%s':y='%s':d=%d:s=%dx%d:fps=%d,setsar=1,settb=AVTB[v%d]"
            % (i, W * k, H * k, W * k, H * k, b, b, b, z, x, y, frames, W, H, fps, i))
    previo = "v0"
    for i in range(1, len(escenas)):
        offset += escenas[i - 1]["frames"]
        trozos.append("[%s][v%d]xfade=transition=fade:duration=%.4f:offset=%.4f[x%d]"
                      % (previo, i, Ff / fps, offset / fps, i))
        previo = "x%d" % i
    cmd += ["-filter_complex", ";".join(trozos), "-map", "[%s]" % previo,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", str(cfg["crf_partes"]),
            "-pix_fmt", "yuv420p", "-r", str(fps), destino + ".tmp.mp4"]
    ejecutar(cmd)
    os.replace(destino + ".tmp.mp4", destino)


def unir_partes(partes, audio, largo, cfg, destino):
    ff = herramienta("ffmpeg")
    fps, Ff = cfg["fps"], cfg["fundido_frames"]
    cmd = [ff, "-y", "-hide_banner", "-loglevel", "error", "-stats"]
    for p in partes:
        cmd += ["-i", p["archivo"]]
    cmd += ["-i", audio]
    if len(partes) == 1:
        filtro, salida = "[0:v]null[v]", "v"
    else:
        trozos, previo, offset = [], "0:v", 0
        for j in range(1, len(partes)):
            offset += partes[j - 1]["frames"]
            trozos.append("[%s][%d:v]xfade=transition=fade:duration=%.4f:offset=%.4f[u%d]"
                          % (previo, j, Ff / fps, offset / fps, j))
            previo = "u%d" % j
        filtro, salida = ";".join(trozos), previo
    cmd += ["-filter_complex", filtro, "-map", "[%s]" % salida, "-map", "%d:a" % len(partes),
            "-c:v", "libx264", "-preset", cfg["preset"], "-crf", str(cfg["crf"]),
            "-pix_fmt", "yuv420p", "-r", str(fps),
            "-c:a", "aac", "-b:a", "192k", "-t", "%.3f" % largo,
            "-movflags", "+faststart", destino]
    ejecutar(cmd)


def orden_montar(args):
    proyecto = args.proyecto
    plan, total, escenas, errores, avisos = cargar_y_validar(proyecto)
    informar_validacion(total, escenas, errores, avisos)
    if errores:
        return 1

    largo_objetivo = min(total, args.hasta) if args.hasta else total
    tmp = os.path.join(proyecto, "_tmp_dormir")
    carpeta_partes = os.path.join(tmp, "partes")
    render = os.path.join(proyecto, "render")
    for c in (tmp, carpeta_partes, render):
        os.makedirs(c, exist_ok=True)
    marca = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = ("prueba_dormir_%s.mp4" if args.hasta else "dormir_master_%s.mp4") % marca
    destino = os.path.join(render, nombre)
    if os.path.exists(destino):
        raise ErrorPlan("Ya existe %s; no lo sobrescribo." % destino)

    final_audio, largo, ganancia, tipo_norm = mezclar_audio(
        proyecto, plan, total, args.hasta, tmp, args.eq_voz)

    cfg = {"ancho": args.ancho, "alto": args.alto, "fps": args.fps, "sobremuestreo": args.sobremuestreo,
           "crf": args.crf, "crf_partes": args.crf_partes, "preset": args.preset,
           "zoom_inicio": float(plan["zoom_inicio"]), "zoom_cuerpo": float(plan["zoom_cuerpo"])}
    cfg["fundido_frames"] = int(round(float(plan["fundido_segundos"]) * cfg["fps"]))

    # tiempos en fotogramas exactos para que no se acumulen desfases en dos horas
    usadas = [e for e in escenas if e["inicio"] < largo]
    limite = int(round(largo * cfg["fps"]))
    for i, e in enumerate(usadas):
        ini = int(round(e["inicio"] * cfg["fps"]))
        fin = int(round(usadas[i + 1]["inicio"] * cfg["fps"])) if i + 1 < len(usadas) else limite
        e["frames"] = fin - ini
    if usadas[-1]["frames"] < cfg["fundido_frames"] + 1:
        usadas.pop()
        usadas[-1]["frames"] = limite - int(round(usadas[-1]["inicio"] * cfg["fps"]))
    ultima = usadas[-1]

    grupos = [usadas[i:i + args.por_parte] for i in range(0, len(usadas), args.por_parte)]
    partes = []
    decir("Vídeo · %d escenas en %d partes (%dx%d, %d fps)" % (len(usadas), len(grupos), cfg["ancho"], cfg["alto"], cfg["fps"]))
    for n, grupo in enumerate(grupos, 1):
        firma = json.dumps({"v": VERSION, "cfg": cfg, "ultima": grupo[-1] is ultima,
                            "esc": [(huella_archivo(e["imagen"]), e["frames"], e["movimiento"], e["brillo"],
                                     e["inicio"] < FASE_INICIO_SEG) for e in grupo]}, sort_keys=True)
        archivo = os.path.join(carpeta_partes, "parte_%03d_%s.mp4" % (n, hashlib.sha1(firma.encode()).hexdigest()[:10]))
        frames = sum(e["frames"] for e in grupo)
        partes.append({"archivo": archivo, "frames": frames})
        if os.path.exists(archivo):
            decir("  parte %d/%d · ya renderizada con estos mismos datos, la reutilizo" % (n, len(grupos)))
            continue
        decir("  parte %d/%d · escenas %d–%d (%s–%s)…" % (n, len(grupos), grupo[0]["n"], grupo[-1]["n"],
                                                         hms(grupo[0]["inicio"]), hms(grupo[0]["inicio"] + frames / cfg["fps"])))
        renderizar_parte(grupo, ultima, cfg, archivo)

    decir("Uniendo partes y audio en %s…" % destino)
    unir_partes(partes, final_audio, largo, cfg, destino)

    decir("Comprobaciones del resultado…")
    lufs, pico = medir_ebur128(destino)
    negros = detectar_negro(destino)
    dur = duracion(destino)
    decir("  Duración: %s (objetivo %s)" % (hms(dur), hms(largo)))
    decir("  Sonoridad: %s LUFS integrados · pico real %s dBTP · normalización %s"
          % ("?" if lufs is None else "%.1f" % lufs, "?" if pico is None else "%.1f" % pico, tipo_norm))
    decir("  Ambiente: %+.1f dB aplicados para quedar %g dB bajo la voz" % (ganancia, plan["ambiente_db_bajo_voz"]))
    if negros:
        for a, b, c in negros:
            decir("  FALLO: pantalla negra de %.1f s entre %s y %s" % (c, hms(a), hms(b)))
    else:
        decir("  Sin tramos negros de más de %g s." % NEGRO_MAX_SEG)
    decir("Listo: %s" % destino)
    decir("Revísalo entero antes de aprobarlo: estas comprobaciones no sustituyen tu revisión.")
    return 1 if negros else 0


# ---------------------------------------------------------------------------
def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="Montador limpio para «Historia para dormir» (Dopema Web).")
    sub = p.add_subparsers(dest="orden")

    a = sub.add_parser("plantilla", help="crear plan_dormir.json a partir de la voz")
    a.add_argument("--proyecto", required=True)
    a.add_argument("--voz", help="ruta de la voz, si no es audio/voz.wav")
    a.add_argument("--cola", type=float, default=30, help="segundos de ambiente tras la voz (30)")
    a.add_argument("--ritmo-inicio", type=float, default=11, help="segundos por escena en los 7 primeros minutos (11)")
    a.add_argument("--ritmo-cuerpo", type=float, default=33, help="segundos por escena en el cuerpo (33)")

    v = sub.add_parser("validar", help="comprobar el plan sin renderizar")
    v.add_argument("--proyecto", required=True)

    m = sub.add_parser("montar", help="mezclar el audio y montar el vídeo")
    m.add_argument("--proyecto", required=True)
    m.add_argument("--hasta", type=float, help="montar solo los primeros N segundos (prueba)")
    m.add_argument("--ancho", type=int, default=1920)
    m.add_argument("--alto", type=int, default=1080)
    m.add_argument("--fps", type=int, default=24)
    m.add_argument("--crf", type=int, default=20)
    m.add_argument("--crf-partes", type=int, default=14)
    m.add_argument("--preset", default="medium")
    m.add_argument("--sobremuestreo", type=int, default=3, help="ampliación previa para que el zoom no tiemble (3)")
    m.add_argument("--por-parte", type=int, default=10, help="escenas por parte; menos = menos memoria (10)")
    m.add_argument("--eq-voz", action="store_true", help="aplicar paso alto a 80 Hz y quitar sibilancias a la voz")

    args = p.parse_args(argv)
    if not args.orden:
        p.print_help()
        return 2
    try:
        args.proyecto = os.path.abspath(args.proyecto)
        if not os.path.isdir(args.proyecto):
            raise ErrorPlan("No existe la carpeta del proyecto: %s" % args.proyecto)
        if args.orden == "plantilla":
            orden_plantilla(args)
            return 0
        if args.orden == "validar":
            return orden_validar(args)
        return orden_montar(args)
    except ErrorPlan as e:
        decir("ERROR: %s" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
