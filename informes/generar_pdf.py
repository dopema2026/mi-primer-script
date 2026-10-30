#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera HOJA_DE_RUTA_MAESTRA_3_CANALES_2026.pdf a partir de los informes .md
y de las tablas de datos (puntuaciones, auditoría de colas, registro de créditos).

Uso:  python3 generar_pdf.py
Necesita: python-markdown y Node.js con Playwright (Chromium).
"""
import csv
import html
import os
import subprocess
import sys

import re

import markdown

BASE = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(BASE, "datos")
SALIDA_HTML = os.path.join(BASE, "HOJA_DE_RUTA_MAESTRA_3_CANALES_2026.html")
SALIDA_PDF = os.path.join(BASE, "HOJA_DE_RUTA_MAESTRA_3_CANALES_2026.pdf")

CANALES = [
    ("dopema", "Dopema Web", "informe_dopema_extremo.md", "Arqueología, vida cotidiana e historia para dormir · público 70 % LatAm"),
    ("elporque", "El Porqué de las Cosas", "informe_elporque_extremo.md", "Preguntas con contradicción sobre el cuerpo, los animales y los objetos"),
    ("timerunners", "Time Runners", "informe_timerunners_extremo.md", "Ciudades a través del tiempo en primera persona · ruta a la monetización"),
]


def md(texto):
    return markdown.markdown(texto, extensions=["tables", "fenced_code", "sane_lists"])


def leer(nombre):
    with open(os.path.join(BASE, nombre), encoding="utf-8") as f:
        return f.read()


def tabla_tsv(ruta, columnas=None, titulos=None):
    with open(ruta, encoding="utf-8") as f:
        filas = list(csv.reader(f, delimiter="\t"))
    cab, cuerpo = filas[0], filas[1:]
    idx = list(range(len(cab))) if columnas is None else [cab.index(c) for c in columnas]
    nombres = titulos or [cab[i] for i in idx]
    out = ["<table><thead><tr>"] + ["<th>%s</th>" % html.escape(n) for n in nombres] + ["</tr></thead><tbody>"]
    for fila in cuerpo:
        if not any(fila):
            continue
        fila = fila + [""] * (len(cab) - len(fila))
        out.append("<tr>" + "".join("<td>%s</td>" % html.escape(fila[i]) for i in idx) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def portada():
    insignias = "".join(
        '<div class="insignia %s"><b>%s</b><span>%s</span></div>' % (cid, nombre, sub)
        for cid, nombre, _, sub in CANALES
    )
    return """
<section class="portada">
  <div class="portada-banda"></div>
  <p class="portada-antetitulo">INFORME MAESTRO · INVESTIGACIÓN Y PRODUCCIÓN</p>
  <h1 class="portada-titulo">Hoja de ruta maestra<br>3 canales · 60 días</h1>
  <p class="portada-sub">Competencia, reglas empíricas de formato, 90 piezas cerradas con título, miniatura,
  gancho y prueba de vidIQ, manual técnico y calendario de 8 semanas.</p>
  <div class="insignias">%s</div>
  <div class="portada-pie">
    <div><b>Para</b> Domingo · Dopema Web</div>
    <div><b>Datos</b> vidIQ (1.880 créditos) y Metricool · extraídos el 30-oct-2026</div>
    <div><b>Periodo</b> 2-nov → 27-dic-2026</div>
    <div class="riesgo">Riesgo de monetización: ninguno (documento de análisis; ningún cambio aplicado)</div>
  </div>
</section>""" % insignias


def indice():
    filas = [
        ("1", "Cómo usar este informe · 12 pautas comunes · primeras 72 horas · metodología · créditos", "comun"),
        ("2", "Dopema Web — pautas, estado, auditoría de lo programado, competencia, 15 largos, 15 Shorts, manual, calendario", "dopema"),
        ("3", "El Porqué de las Cosas — pautas, cambio de régimen, competencia y arbitraje EN→ES, 15 largos, 15 Shorts, manual, calendario", "elporque"),
        ("4", "Time Runners — pautas, CDMX vs Alejandría, ecosistema inglés, monetización con números, 15 largos, 15 Shorts, manual, calendario", "timerunners"),
        ("A", "Anexo A — Puntuaciones vidIQ de las 90 piezas y sus variantes", "anexo"),
        ("B", "Anexo B — Títulos B para la prueba A/B de los 45 largos", "anexo"),
        ("C", "Anexo C — Auditoría de las colas programadas en Metricool", "anexo"),
        ("D", "Anexo D — Registro de créditos de vidIQ llamada a llamada", "anexo"),
    ]
    li = "".join('<li class="%s"><span class="num">%s</span><span>%s</span></li>' % (c, n, html.escape(t)) for n, t, c in filas)
    return '<section class="indice"><h1 class="sin-salto">Índice</h1><ol class="lista-indice">%s</ol></section>' % li


def separador(cid, nombre, sub):
    return '<section class="separador %s"><div class="sep-banda"></div><p>CANAL</p><h1 class="sin-salto">%s</h1><h3>%s</h3></section>' % (cid, nombre, sub)


def main():
    partes = [portada(), indice()]
    partes.append('<section class="canal comun">%s</section>' % md(leer("informe_comun.md")))
    for cid, nombre, archivo, sub in CANALES:
        partes.append(separador(cid, nombre, sub))
        partes.append('<section class="canal %s">%s</section>' % (cid, md(leer(archivo))))

    anexos = ['<section class="canal anexo">']
    anexos.append("<h1>Anexo A — Puntuaciones vidIQ (score_title)</h1>")
    anexos.append("<p>Todas las puntuaciones obtenidas en esta investigación, con el ID de cada canal. Las letras finales (a, b, c...) son variantes del mismo título.</p>")
    anexos.append(tabla_tsv(os.path.join(DATOS, "puntuaciones.tsv"), titulos=["ID", "Tipo", "Título", "Score"]))
    anexos.append("<h1>Anexo B — Títulos B para la prueba A/B</h1>")
    anexos.append(tabla_tsv(os.path.join(DATOS, "puntuaciones_B.tsv"), titulos=["ID", "Título B", "Score B"]))
    anexos.append("<h1>Anexo C — Auditoría de las colas programadas</h1>")
    anexos.append(tabla_tsv(os.path.join(DATOS, "auditoria_colas.tsv"), titulos=["Canal", "Fecha", "Título programado", "Score", "Propuesta", "Score"]))
    anexos.append("<h1>Anexo D — Registro de créditos de vidIQ</h1>")
    anexos.append("<p>Total gastado: 1.880 créditos (comprobado con vidiq_balance: 6.469 → 4.589).</p>")
    anexos.append(tabla_tsv(os.path.join(DATOS, "ledger.tsv"), titulos=["#", "Herramienta", "Créditos", "Propósito"]))
    anexos.append("</section>")
    partes.append("".join(anexos))

    with open(os.path.join(BASE, "estilo_informe.css"), encoding="utf-8") as f:
        css = f.read()
    cuerpo = re.sub(r"\b([DET]-(?:L|S|ES)\d{1,2}[a-e]?)\b", r'<span class="nw">\1</span>', "".join(partes))
    doc = '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Hoja de ruta maestra 2026</title><style>%s</style></head><body>%s</body></html>' % (css, cuerpo)
    with open(SALIDA_HTML, "w", encoding="utf-8") as f:
        f.write(doc)

    js = os.path.join(BASE, "imprimir_pdf.js")
    r = subprocess.run(["node", js, SALIDA_HTML, SALIDA_PDF])
    if r.returncode != 0:
        sys.exit("No se pudo generar el PDF.")
    print("PDF:", SALIDA_PDF)


if __name__ == "__main__":
    main()
