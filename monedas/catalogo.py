"""Genera el catálogo en PDF con todas las piezas del inventario.

Uso:
    python3 monedas/catalogo.py
"""
import json
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

RAIZ = Path(__file__).resolve().parent.parent
INVENTARIO = RAIZ / "datos" / "inventario.json"
TITULOS = RAIZ / "datos" / "titulos.json"
VALORACION = RAIZ / "datos" / "valoracion.json"
DESTINO = RAIZ / "salida" / "catalogo_coleccion.pdf"

# Unidades de cada divisa por euro, para dar todo el coste en euros.
# USD: cambio de referencia del BCE del 08/08/2025 (factura de GSA Numis del 10/08/2025).
CAMBIO = {"EUR": 1.0, "USD": 1.1648}
NOTA_CAMBIO = "Importes en USD convertidos a 1 EUR = 1,1648 USD (referencia BCE, 08/08/2025)."

GRANATE = colors.HexColor("#5a1a1a")
GRIS = colors.HexColor("#666666")
FONDO = colors.HexColor("#f6f3ee")

estilos = getSampleStyleSheet()
TITULO = ParagraphStyle("titulo", parent=estilos["Title"], textColor=GRANATE, fontSize=24)
SUBT = ParagraphStyle("subt", parent=estilos["Normal"], textColor=GRIS, alignment=1)
H2 = ParagraphStyle("h2", parent=estilos["Heading2"], textColor=GRANATE)
NOMBRE = ParagraphStyle("nombre", parent=estilos["Normal"], fontName="Helvetica-Bold",
                        fontSize=10.5, leading=13, textColor=GRANATE)
TEXTO = ParagraphStyle("texto", parent=estilos["Normal"], fontSize=8.5, leading=11)
DATO = ParagraphStyle("dato", parent=TEXTO, textColor=GRIS)


def dinero(valor, moneda):
    return f"{valor:,.2f} {moneda}".replace(",", "X").replace(".", ",").replace("X", ".")


def foto(pieza, ancho):
    if not pieza.get("foto"):
        return Paragraph("<i>sin foto</i>", DATO)
    ruta = RAIZ / "datos" / pieza["foto"]
    w, h = ImageReader(str(ruta)).getSize()
    return Image(str(ruta), width=ancho, height=ancho * h / w)


def en_euros(p):
    return p["coste_total"] / CAMBIO[p["moneda"]] if p.get("coste_total") is not None else None


def horquilla(v):
    return f"{dinero(v['min'], '€')} – {dinero(v['max'], '€')}" if v else ""


def ficha(n, p, titulo, val=None):
    nombre = titulo or p["descripcion"].split(". ")[0]
    if p["origen"] == "subasta":
        procedencia = f"{p['casa']} · {p['subasta']} · lote {p['lote']} · {p.get('fecha_compra') or ''}"
    elif p["origen"] == "compra directa":
        procedencia = " · ".join(x for x in (p.get("casa"), p.get("factura") and
                                            f"factura {p['factura']}", p.get("fecha_compra")) if x)
    else:
        procedencia = "Sin factura"
    coste = dinero(p["coste_total"], p["moneda"]) if p.get("coste_total") is not None else "—"
    if p.get("coste_total") is not None and p["moneda"] != "EUR":
        coste += f" (≈ {dinero(en_euros(p), 'EUR')})"
    valor = horquilla(val) or "____________"
    texto = [
        Paragraph(f"{n}. {escape(nombre)}", NOMBRE),
        Spacer(1, 2),
        Paragraph(escape(p["descripcion"]), TEXTO),
        Spacer(1, 4),
        Paragraph(f"<b>Procedencia:</b> {escape(procedencia)}", DATO),
        Paragraph(f"<b>Coste total</b>{' (martillo + comisión + envío)' if p.get('martillo') else ''}:"
                  f" {coste}", DATO),
        Paragraph(f"<b>Valor estimado:</b> {valor}", DATO),
    ]
    if val:
        texto.insert(-1, Paragraph(f"<b>Estado</b> (según foto): {escape(val['estado'])}", DATO))
    if p.get("notas"):
        texto.append(Paragraph(f"<b>Notas:</b> {escape(p['notas'])}", DATO))
    t = Table([[foto(p, 62 * mm), texto]], colWidths=[66 * mm, None])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), FONDO),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8cfc2")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([t, Spacer(1, 6)])


def orden(p):
    """Por fecha de compra y número de lote; lo que no tiene factura, al final."""
    try:
        fecha = datetime.strptime(p.get("fecha_compra") or "", "%d %b %Y")
    except ValueError:
        fecha = datetime.max
    lote = p.get("lote") or ""
    return (fecha, p.get("subasta") or "", int(lote) if lote.isdigit() else 0, lote)


def pie(c, doc):
    c.saveState()
    c.setFont("Helvetica", 7.5)
    c.setFillColor(GRIS)
    c.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Página {doc.page}")
    c.restoreState()


def main():
    inv = json.loads(INVENTARIO.read_text(encoding="utf-8"))
    piezas = sorted(inv["piezas"], key=orden)
    DESTINO.parent.mkdir(exist_ok=True)

    titulos = json.loads(TITULOS.read_text(encoding="utf-8")) if TITULOS.exists() else {}
    titulo = lambda p: titulos.get(p["id"], [None])[0]
    valoracion = (json.loads(VALORACION.read_text(encoding="utf-8"))
                  if VALORACION.exists() else {"piezas": {}})
    val = lambda p: valoracion["piezas"].get(p["id"])
    epoca = lambda p: titulos.get(p["id"], [None, "Sin clasificar"])[1]

    por_epoca = defaultdict(lambda: [0, 0.0])
    por_tipo = defaultdict(int)
    for p in piezas:
        por_epoca[epoca(p)][0] += 1
        por_epoca[epoca(p)][1] += en_euros(p) or 0
        por_tipo[p["tipo"]] += 1

    story = [
        Spacer(1, 40 * mm),
        Paragraph("Catálogo de la colección", TITULO),
        Spacer(1, 4 * mm),
        Paragraph(f"Actualizado el {date.today().strftime('%d/%m/%Y')}", SUBT),
        Spacer(1, 15 * mm),
    ]
    grupos = defaultdict(list)
    for p in piezas:
        if p.get("subasta"):
            grupo = f"{p['casa']} · {p['subasta']}"
        elif p["origen"] == "compra directa":
            grupo = " · ".join(x for x in (p.get("casa"), p.get("factura") and
                                          f"factura {p['factura']}") if x)
        else:
            grupo = "Sin factura"
        grupos[grupo].append(p)
    total = sum(v for _, v in por_epoca.values())
    resumen = [["Piezas", str(len(piezas))]]
    resumen += [[tipo.capitalize() + "s", str(n)] for tipo, n in sorted(por_tipo.items())]
    resumen += [["Compras (subastas y comerciantes)", str(len(grupos))]]
    resumen += [["Invertido", dinero(total, "EUR")]]
    vals = [val(p) for p in piezas if val(p)]
    if vals:
        resumen += [["Valor estimado hoy",
                     horquilla({"min": sum(v["min"] for v in vals), "max": sum(v["max"] for v in vals)})]]
    resumen += [["", ""], ["Por época", ""]]
    resumen += [[f"   {e}  ({n})", dinero(v, "EUR")]
                for e, (n, v) in sorted(por_epoca.items(), key=lambda x: -x[1][1])]
    t = Table(resumen, colWidths=[85 * mm, 40 * mm], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("LINEBELOW", (0, 0), (-1, 3 + bool(vals)), 0.4, colors.HexColor("#d8cfc2")),
        ("FONTNAME", (0, 3), (-1, 3 + bool(vals)), "Helvetica-Bold"),
        ("FONTNAME", (0, 5 + bool(vals)), (0, 5 + bool(vals)), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [t, Spacer(1, 10 * mm), Paragraph(NOTA_CAMBIO, SUBT)]
    if vals:
        story += [Spacer(1, 2 * mm), Paragraph(
            f"Valor estimado a {escape(valoracion['fecha'])}: {escape(valoracion['nota'])}", SUBT)]
    story.append(PageBreak())

    # Índice: una línea por pieza, con hueco para apuntar el valor.
    filas = [["Nº", "Pieza", "Coste (EUR)", "Valor estimado"]]
    n = 0
    for lista in grupos.values():
        for p in lista:
            n += 1
            filas.append([str(n), Paragraph(escape(titulo(p) or p["descripcion"].split(". ")[0]), TEXTO),
                          dinero(en_euros(p), "€") if p.get("coste_total") is not None else "—",
                          horquilla(val(p))])
    filas.append(["", Paragraph("<b>Total</b>", TEXTO), dinero(total, "€"),
                  horquilla({"min": sum(v["min"] for v in vals), "max": sum(v["max"] for v in vals)})
                  if vals else ""])
    t = Table(filas, colWidths=[10 * mm, 92 * mm, 26 * mm, 42 * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 0), (-1, 0), GRANATE),
        ("ALIGN", (2, 0), (3, -1), "RIGHT"),
        ("FONTNAME", (2, -1), (3, -1), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#d8cfc2")),
        ("LINEBELOW", (3, 1), (3, -2), 0.6, GRIS),
    ]))
    story += [Paragraph("Índice", H2), t, PageBreak()]

    n = 0
    for grupo, lista in grupos.items():
        story.append(Paragraph(escape(grupo), H2))
        for p in lista:
            n += 1
            story.append(ficha(n, p, titulo(p), val(p)))

    doc = SimpleDocTemplate(str(DESTINO), pagesize=A4, title="Catálogo de la colección",
                            leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=18 * mm)
    doc.build(story, onFirstPage=pie, onLaterPages=pie)
    print(f"Catálogo: {DESTINO} ({len(piezas)} piezas)")


if __name__ == "__main__":
    main()
