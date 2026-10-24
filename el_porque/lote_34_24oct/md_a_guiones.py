# Rehace los 34 guion.json a partir de GUIONES_01-17.md y GUIONES_18-34.md.
# Uso (en la carpeta donde estén los dos .md):
#   python md_a_guiones.py F:\ProyectoYoutube\porque\LOTE_34_24oct
# Crea <destino>\NN_slug\guion.json para cada short.
import json, os, re, sys

VOZ_NOMBRE = {
    "eleven_carmelo": "Carmelo - Mysterious & Deep", "eleven_aitana": "Aitana",
    "eleven_bosco": "Bosco - Deep & Calm with gentle pauses", "eleven_marina": "Marina",
    "eleven_gonzalo": "Gonzalo - Narrador documental de España", "eleven_eva": "Eva Dorado",
    "eleven_david": "David Martin - Confident and Balanced", "eleven_elena": "Elena - cuentos y narraciones",
    "eleven_gabo": "Gabo - Vibrant & Deep Documentaries", "eleven_sara": "Sara Martin 1",
    "eleven_mario": "Mario Pro - Warm Narrations", "eleven_gustavo": "Gustavo - Spanish calm narrator",
    "eleven_salva": "Salva - The Spanish Voice", "eleven_juancarlos": "Juan Carlos - Documentary",
    "eleven_emanuel": "Emanuel - Deep, Warm", "eleven_baldo": "Baldo - voz grave peninsular",
    "eleven_rafael": "Rafael - Tales and Legends", "eleven_arconte": "Arconte - Evocative & Magnetic",
}


def leer(ruta):
    shorts = []
    for trozo in open(ruta, encoding="utf-8").read().split("\n## ")[1:]:
        lineas = trozo.strip().split("\n")
        carpeta = lineas[0].strip()
        c = {}
        for l in lineas:
            m = re.match(r"- \*\*(\w+)\*\*: (.*)", l)
            if m:
                c[m.group(1)] = m.group(2)
        voz, voice_id, genero, modelo = [x.strip() for x in c["voz"].split("·")]
        fecha, palabras, dur = [x.strip() for x in c["publicacion_propuesta"].split("·")]
        bloques = []
        for l in lineas:
            m = re.match(r"(\d+)\. \((\w+)\) (.*)", l)
            if m:
                bloques.append({"n": int(m.group(1)), "texto": m.group(3), "tono": m.group(2)})
        shorts.append({
            "carpeta": carpeta,
            "titulo": c["titulo"], "titulo_base": c["titulo"], "titulo_alternativa": c["titulo_alternativa"],
            "tesis": c["tesis"], "formato": "short", "canal": "El Porqué de las Cosas", "serie": "",
            "estructura": "explicativo", "arranque": "contradiccion",
            "voz": voz, "voice_id": voice_id.replace("voice_id ", ""), "voz_nombre": VOZ_NOMBRE[voz],
            "voz_genero": genero, "voz_acento": "españa", "modelo_voz": modelo,
            "estilo_clave": "D", "estilo_nombre": c["estilo_nombre"], "estilo": c["estilo"],
            "gancho": c["gancho"], "riesgo_monetizacion": c["riesgo_monetizacion"],
            "cultura_visual": c["cultura_visual"],
            "fuentes": [{"dato": f.strip(), "fuente": f.strip()} for f in c["fuentes"].split(" | ")],
            "personajes": [], "bloques": bloques,
            "aprobacion_guion": True, "estado": "GUION_ESCRITO_24OCT_ORDEN_DOMINGO", "lote": "LOTE_34_24oct",
            "orden_publicacion": int(carpeta[:2]), "publicacion_propuesta": fecha,
            "palabras": int(palabras.split()[0]), "duracion_estimada_s": int(dur.strip("~ s")),
        })
    return shorts


if __name__ == "__main__":
    destino = sys.argv[1]
    todos = leer("GUIONES_01-17.md") + leer("GUIONES_18-34.md")
    assert len(todos) == 34, len(todos)
    for g in todos:
        d = os.path.join(destino, g["carpeta"])
        os.makedirs(d, exist_ok=True)
        sin = {k: v for k, v in g.items() if k != "carpeta"}
        json.dump(sin, open(os.path.join(d, "guion.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{len(todos)} guion.json creados en {destino}")
