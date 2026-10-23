#!/usr/bin/env python3
"""Posproducción local de «Así hablaban los grandes personajes de la historia».

Uso:
  python scripts/build_master.py audio  <id|all>   # voz + SFX -> mezcla maestra (referencia para Seedance)
  python scripts/build_master.py scene  <id|all>   # clip Seedance -> versiones «limpio» y «letras»
  python scripts/build_master.py master            # concatena los 6 clips -> 2 másteres ~62.5 s
  (--variant limpio|letras|ambas; por defecto ambas)
  python scripts/build_master.py check  <archivo>  # ffprobe: duración, resolución, fps

Archivos esperados (por id de escena, p. ej. 01_cesar):
  03_audio_voices/<id>_voice.(wav|mp3)
  04_audio_sfx/<id>_sfx.(wav|mp3)
  05_video_clips/<id>.mp4
Fuente: --font /ruta/a/fuente.ttf o variable DOPEMA_FONT (si no, se busca una serif del sistema).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "01_manifest" / "scenes.json"
VOICES, SFX = ROOT / "03_audio_voices", ROOT / "04_audio_sfx"
CLIPS, EXPORT = ROOT / "05_video_clips", ROOT / "06_final_export"

SAMPLE_RATE = 48000
TITLE_COLOR = "0xF5EFE0"  # marfil
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "/Library/Fonts/Georgia Bold.ttf",
    "C:/Windows/Fonts/georgiab.ttf",
    "C:/Windows/Fonts/timesbd.ttf",
]


def load_manifest():
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def pick_scenes(manifest, which):
    scenes = sorted(manifest["scenes"], key=lambda s: s["order"])
    if which == "all":
        return scenes
    match = [s for s in scenes if s["id"] == which or s["id"].split("_", 1)[-1] == which]
    if not match:
        sys.exit(f"Escena desconocida: {which}. Opciones: {', '.join(s['id'] for s in scenes)}")
    return match


def find_input(folder, stem):
    for ext in (".wav", ".mp3", ".m4a", ".flac"):
        p = folder / f"{stem}{ext}"
        if p.exists():
            return p
    return None


def run(cmd):
    print("  $", " ".join(str(c) for c in cmd[:6]), "...")
    subprocess.run([str(c) for c in cmd], check=True)


def ff_path(p):
    """Ruta segura para usar dentro de un filtro de ffmpeg (Windows incluido)."""
    return str(p).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


def find_font(cli_font):
    for candidate in [cli_font, os.environ.get("DOPEMA_FONT"), *FONT_CANDIDATES]:
        if candidate and Path(candidate).exists():
            return candidate
    sys.exit("No encuentro una fuente serif. Pasa --font /ruta/fuente.ttf o define DOPEMA_FONT.")


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


# ---------------------------------------------------------------- audio

def build_audio(scene, manifest):
    sid = scene["id"]
    voice, sfx = find_input(VOICES, f"{sid}_voice"), find_input(SFX, f"{sid}_sfx")
    if not voice or not sfx:
        print(f"[{sid}] falta voz o SFX, se omite (voz={voice}, sfx={sfx})")
        return
    # La mezcla dura lo mismo que el clip que se pedirá a Seedance; luego se recorta en 'scene'.
    duration = float(scene.get("seedance_duration", scene["final_duration"]))
    delay_ms = int(manifest["timing_rule"]["voice_start_seconds"] * 1000)
    out = VOICES / f"{sid}_master_audio.wav"
    graph = (
        f"[0:a]aresample={SAMPLE_RATE},aformat=channel_layouts=stereo,"
        f"adelay={delay_ms}|{delay_ms},apad,asplit[v1][v2];"
        f"[1:a]aresample={SAMPLE_RATE},aformat=channel_layouts=stereo,aloop=loop=-1:size=2e9,"
        f"volume=0.8[amb];"
        # Ducking suave: el ambiente baja cuando habla el personaje.
        f"[amb][v1]sidechaincompress=threshold=0.04:ratio=4:attack=30:release=500[duck];"
        f"[duck][v2]amix=inputs=2:normalize=0,atrim=0:{duration},"
        f"afade=t=in:st=0:d=0.3,afade=t=out:st={duration - 0.4}:d=0.4[out]"
    )
    print(f"[{sid}] mezcla de audio {duration:.1f}s -> {out.name}")
    run(["ffmpeg", "-y", "-v", "error", "-i", voice, "-i", sfx,
         "-filter_complex", graph, "-map", "[out]", "-ar", SAMPLE_RATE, out])


# ---------------------------------------------------------------- escena

def title_filters(scene, manifest, font, tmpdir):
    t0, t1 = manifest["timing_rule"]["title_window_seconds"]
    fade = 0.4
    alpha = (f"'if(lt(t,{t0}),0,if(lt(t,{t0 + fade}),(t-{t0})/{fade},"
             f"if(lt(t,{t1 - fade}),1,if(lt(t,{t1}),({t1}-t)/{fade},0))))'")
    filters = []
    # Tercio medio-bajo, a la izquierda: lejos de caras, de la columna de botones y del pie de TikTok.
    # «Lugar · fecha (Idioma)» se parte en dos líneas para no invadir la columna de botones.
    place, _, lang = scene["title"]["line2"].partition(" (")
    lines = [(scene["title"]["line1"], 64, "h*0.62"), (place, 36, "h*0.62+88")]
    if lang:
        lines.append((lang.rstrip(")"), 30, "h*0.62+138"))
    for i, (text, size, y) in enumerate(lines):
        txt = Path(tmpdir) / f"{scene['id']}_l{i}.txt"
        txt.write_text(text, encoding="utf-8")
        filters.append(
            f"drawtext=fontfile='{ff_path(font)}':textfile='{ff_path(txt)}':"
            f"fontsize={size}:fontcolor={TITLE_COLOR}:x=w*0.07:y={y}:"
            f"shadowcolor=black@0.6:shadowx=2:shadowy=2:alpha={alpha}"
        )
    return filters


def watermark_filter(manifest, font, tmpdir):
    txt = Path(tmpdir) / "brand.txt"
    txt.write_text(manifest["brand"], encoding="utf-8")
    # Arriba a la izquierda, por debajo de las pestañas de la app.
    return (f"drawtext=fontfile='{ff_path(font)}':textfile='{ff_path(txt)}':"
            f"fontsize=34:fontcolor=white@0.65:x=w*0.06:y=h*0.085:"
            f"shadowcolor=black@0.4:shadowx=1:shadowy=1")


def subtitle_filter(scene, font, tmpdir):
    # Traducción discreta: entra cuando se va el rótulo y sale al terminar la frase.
    text = scene["voice"].get("translation")
    if not text:
        return None
    txt = Path(tmpdir) / f"{scene['id']}_sub.txt"
    txt.write_text("\n".join(textwrap.wrap(f"«{text}»", 34)), encoding="utf-8")
    t0, t1, fade = 3.6, 8.2, 0.3
    alpha = (f"'if(lt(t,{t0}),0,if(lt(t,{t0 + fade}),(t-{t0})/{fade},"
             f"if(lt(t,{t1 - fade}),1,if(lt(t,{t1}),({t1}-t)/{fade},0))))'")
    return (f"drawtext=fontfile='{ff_path(font)}':textfile='{ff_path(txt)}':"
            f"fontsize=40:line_spacing=10:fontcolor={TITLE_COLOR}:x=(w-text_w)/2:y=h*0.62:"
            f"box=1:boxcolor=black@0.35:boxborderw=18:shadowcolor=black@0.6:shadowx=2:shadowy=2:"
            f"alpha={alpha}")


def build_scene(scene, manifest, font, audio_mode, variant):
    sid = scene["id"]
    clip = CLIPS / f"{sid}.mp4"
    if not clip.exists():
        print(f"[{sid}] falta {clip.relative_to(ROOT)}, se omite")
        return
    fmt = manifest["format"]
    W, H, fps = fmt["width"], fmt["height"], fmt["fps"]
    dur = float(scene["final_duration"])
    clip_dur = probe_duration(clip)
    pad = max(0.0, dur - clip_dur)  # si el clip es más corto, se congela el último fotograma
    master_audio = VOICES / f"{sid}_master_audio.wav"
    if audio_mode in ("master", "mix") and not master_audio.exists():
        print(f"[{sid}] no hay {master_audio.name}; uso el audio del clip")
        audio_mode = "clip"

    with tempfile.TemporaryDirectory() as tmpdir:
        vf = [
            f"scale={W}:{H}:force_original_aspect_ratio=increase",
            f"crop={W}:{H}", "setsar=1", f"fps={fps}",
            f"tpad=stop_mode=clone:stop_duration={pad:.3f}",
            f"trim=0:{dur}", "setpts=PTS-STARTPTS",
        ]
        if variant == "letras":
            vf += title_filters(scene, manifest, font, tmpdir)
            sub = subtitle_filter(scene, font, tmpdir)
            if sub:
                vf.append(sub)
            vf.append(watermark_filter(manifest, font, tmpdir))
        graph = f"[0:v]{','.join(vf)}[v];"
        inputs = ["-i", clip]
        tail = f"aresample={SAMPLE_RATE},aformat=channel_layouts=stereo,apad,atrim=0:{dur}," \
               f"afade=t=out:st={dur - 0.3}:d=0.3[a]"
        if audio_mode == "clip":
            graph += f"[0:a]{tail}"
        elif audio_mode == "master":
            inputs += ["-i", master_audio]
            graph += f"[1:a]{tail}"
        else:  # mix: mezcla maestra + un poco del audio propio de Seedance
            inputs += ["-i", master_audio]
            graph += (f"[0:a]volume=0.25[ca];[1:a][ca]amix=inputs=2:normalize=0,{tail}")

        out = EXPORT / f"{sid}_{variant}.mp4"
        print(f"[{sid}] clip {clip_dur:.2f}s -> {dur:.2f}s (audio: {audio_mode}) -> {out.name}")
        run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph,
             "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
             "-pix_fmt", "yuv420p", "-r", fps, "-c:a", "aac", "-b:a", "256k", "-ar", SAMPLE_RATE,
             "-movflags", "+faststart", out])


# ---------------------------------------------------------------- máster

def build_master(manifest, variant):
    scenes = sorted(manifest["scenes"], key=lambda s: s["order"])
    parts = [EXPORT / f"{s['id']}_{variant}.mp4" for s in scenes]
    missing = [p.name for p in parts if not p.exists()]
    if missing:
        sys.exit(f"Faltan clips finales: {', '.join(missing)}. Ejecuta antes 'scene all'.")
    fmt = manifest["format"]
    inputs, refs = [], ""
    for i, p in enumerate(parts):
        inputs += ["-i", p]
        refs += f"[{i}:v][{i}:a]"
    graph = (f"{refs}concat=n={len(parts)}:v=1:a=1[v][acat];"
             f"[acat]loudnorm=I={fmt['target_loudness_lufs']}:TP=-1.5:LRA=11,"
             f"aresample={SAMPLE_RATE}[a]")
    out = EXPORT / f"master_asi_hablaban_{variant}.mp4"
    print(f"Montando máster con {len(parts)} escenas -> {out.name}")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph,
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
         "-pix_fmt", "yuv420p", "-r", fmt["fps"], "-c:a", "aac", "-b:a", "256k",
         "-movflags", "+faststart", out])
    check(out, manifest)


def check(path, manifest):
    info = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,width,height,r_frame_rate", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout)
    dur = float(info["format"]["duration"])
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    print(f"{Path(path).name}: {dur:.2f}s · {v['width']}x{v['height']} · {v['r_frame_rate']} fps")
    target = manifest["format"]["target_total_seconds"]
    if Path(path).name.startswith("master"):
        ok = 62.0 <= dur <= 63.0
        print(f"  Duración {'OK' if ok else 'FUERA DE RANGO'} (objetivo {target}s, rango 62.0–63.0s)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["audio", "scene", "master", "check"])
    ap.add_argument("target", nargs="?", default="all")
    ap.add_argument("--font", help="Ruta a una fuente .ttf/.otf para rótulos y marca")
    ap.add_argument("--audio", choices=["master", "clip", "mix"], default="master",
                    help="Audio del clip final: mezcla maestra (defecto), el de Seedance o ambos")
    ap.add_argument("--variant", choices=["limpio", "letras", "ambas"], default="ambas",
                    help="limpio: sin ningún texto · letras: rótulo + traducción + marca · ambas (defecto)")
    args = ap.parse_args()
    variants = ["limpio", "letras"] if args.variant == "ambas" else [args.variant]
    manifest = load_manifest()
    EXPORT.mkdir(exist_ok=True)

    if args.command == "audio":
        for s in pick_scenes(manifest, args.target):
            build_audio(s, manifest)
    elif args.command == "scene":
        font = find_font(args.font)
        for s in pick_scenes(manifest, args.target):
            for variant in variants:
                build_scene(s, manifest, font, args.audio, variant)
    elif args.command == "master":
        for variant in variants:
            build_master(manifest, variant)
    else:
        check(args.target, manifest)


if __name__ == "__main__":
    main()
