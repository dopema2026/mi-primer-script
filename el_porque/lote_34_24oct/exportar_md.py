import json
L=json.load(open('LOTE_34_24oct_GUIONES.json'))
def md(g):
    o=[f"## {g['carpeta']}",f"- **titulo**: {g['titulo']}",f"- **titulo_alternativa**: {g['titulo_alternativa']}",
       f"- **tesis**: {g['tesis']}",f"- **voz**: {g['voz']} · voice_id {g['voice_id']} · {g['voz_genero']} · {g['modelo_voz']}",
       f"- **estilo_nombre**: {g['estilo_nombre']}",f"- **estilo**: {g['estilo']}",f"- **gancho**: {g['gancho']}",
       f"- **riesgo_monetizacion**: {g['riesgo_monetizacion']}",f"- **cultura_visual**: {g['cultura_visual']}",
       f"- **publicacion_propuesta**: {g['publicacion_propuesta']} · {g['palabras']} palabras · ~{g['duracion_estimada_s']} s",
       "- **fuentes**: "+" | ".join(f['fuente'] for f in g['fuentes']),"","Bloques (n · tono · texto):"]
    o+=[f"{b['n']}. ({b['tono']}) {b['texto']}" for b in g['bloques']]
    return "\n".join(o)+"\n"
cab=("# LOTE_34_24oct — Guiones {r} (El Porqué de las Cosas)\n\n"
"Cada short = un guion.json de la fábrica. Campos fijos para todos: formato short, canal El Porqué de las Cosas, estructura explicativo, "
"arranque contradiccion, voz_acento españa, estilo_clave D, aprobacion_guion true (orden de Domingo 24 oct), estado GUION_ESCRITO_24OCT_ORDEN_DOMINGO, "
"personajes []. Fuentes en el campo fuentes como {{dato, fuente}}. Ver INSTRUCCIONES_CLAUDE_PC.md.\n\n")
for n,p,r in (("GUIONES_01-17.md",L[:17],"01–17"),("GUIONES_18-34.md",L[17:],"18–34")):
    open(n,'w').write(cab.format(r=r)+"\n".join(md(g) for g in p))
