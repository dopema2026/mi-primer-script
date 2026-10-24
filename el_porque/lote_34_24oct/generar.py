# Genera los guion.json del lote, el fichero combinado y comprueba las reglas del pipeline.
import json, datetime, pathlib, sys
from datos import SHORTS, VOCES, ESTILOS
from ajustes import aplicar
SHORTS = aplicar(SHORTS)
# Regla del pipeline: tonos distintos entre bloques seguidos.
for _s in SHORTS:
    bl = _s["bloques"]
    for k in range(1, len(bl)):
        if bl[k][0] == bl[k - 1][0] and bl[k][0] != "cierre":
            nxt = bl[k + 1][0] if k + 1 < len(bl) else None
            for t in ("neutro", "cercano", "intriga", "contundente"):
                if t not in (bl[k - 1][0], nxt):
                    bl[k] = (t, bl[k][1]); break

OUT = pathlib.Path(__file__).parent
PPM = 146  # palabras por minuto de referencia (eleven_david); Bosco varía
inicio = datetime.datetime(2026, 10, 29, 15, 0)
errores = []

def fecha(i):
    d = inicio + datetime.timedelta(days=i // 2)
    return d.replace(hour=15 if i % 2 == 0 else 20)

prev = None
lote = []
for i, s in enumerate(SHORTS):
    voice_id, voz_nombre, genero, modelo = VOCES[s["voz"]]
    est_nombre, est_bloque = ESTILOS[s["estilo"]]
    textos = [t for _, t in s["bloques"]]
    palabras = sum(len(t.split()) for t in textos)
    seg = palabras / PPM * 60
    if len(textos[0].split()) > 14: errores.append(f'{s["slug"]}: arranque de {len(textos[0].split())} palabras')
    for t in textos[:3]:
        if len(t.split()) > 13: errores.append(f'{s["slug"]}: bloque inicial largo: {t}')
    if not 230 <= palabras <= 320: errores.append(f'{s["slug"]}: {palabras} palabras')
    if prev:
        if prev["estilo"] == s["estilo"]: errores.append(f'{s["slug"]}: mismo estilo que el anterior')
        if VOCES[prev["voz"]][2] == genero: errores.append(f'{s["slug"]}: mismo género de voz que el anterior')
        if prev["riesgo"].startswith("MEDIO") and s["riesgo"].startswith("MEDIO"): errores.append(f'{s["slug"]}: dos de riesgo medio seguidos')
    prev = s
    f = fecha(i)
    g = {
        "titulo": s["titulo"], "titulo_base": s["titulo"], "titulo_alternativa": s["titulo_b"],
        "tesis": s["tesis"], "formato": "short", "canal": "El Porqué de las Cosas", "serie": "",
        "estructura": "explicativo", "arranque": "contradiccion",
        "voz": s["voz"], "voice_id": voice_id, "voz_nombre": voz_nombre, "voz_genero": genero,
        "voz_acento": "españa", "modelo_voz": modelo,
        "estilo_clave": "D", "estilo_nombre": est_nombre, "estilo": est_bloque,
        "gancho": s["gancho"], "riesgo_monetizacion": s["riesgo"], "cultura_visual": s["cultura"],
        "fuentes": [{"dato": x, "fuente": x} for x in s["fuentes"]], "personajes": [],
        "bloques": [{"n": k + 1, "texto": t, "tono": tono} for k, (tono, t) in enumerate(s["bloques"])],
        "aprobacion_guion": True, "estado": "GUION_ESCRITO_24OCT_ORDEN_DOMINGO",
        "lote": "LOTE_34_24oct", "orden_publicacion": s["n"],
        "publicacion_propuesta": f.strftime("%Y-%m-%d %H:%M"),
        "palabras": palabras, "duracion_estimada_s": round(seg),
    }
    nombre = f'{s["n"]:02d}_{s["slug"]}'
    (OUT / "guiones" / nombre).mkdir(parents=True, exist_ok=True)
    (OUT / "guiones" / nombre / "guion.json").write_text(json.dumps(g, ensure_ascii=False, indent=2))
    lote.append({"carpeta": nombre, **g})
    print(f'{s["n"]:02d} {f:%d/%m %H:%M} {est_nombre[:22]:22} {s["voz"][7:]:10} {genero} {palabras:3}p ~{round(seg)}s  {s["titulo"]}')

(OUT / "LOTE_34_24oct_GUIONES.json").write_text(json.dumps(lote, ensure_ascii=False, indent=2))
print("\nERRORES:" if errores else "\nSin errores de reglas.")
for e in errores: print(" -", e)
sys.exit(1 if errores else 0)
