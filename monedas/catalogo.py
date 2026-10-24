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
DESTINO = RAIZ / "salida" / "catalogo_coleccion.pdf"

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


def ficha(n, p):
    nombre = p["descripcion"].split(". ")[0]
    if p["origen"] == "subasta":
        procedencia = f"{p['casa']} · {p['subasta']} · lote {p['lote']} · {p.get('fecha_compra') or ''}"
    else:
        procedencia = "Sin factura"
    coste = dinero(p["coste_total"], p["moneda"]) if p.get("coste_total") is not None else "—"
    valor = (dinero(p["valor_estimado"], p.get("moneda_valor", "EUR"))
             if p.get("valor_estimado") is not None else "____________")
    texto = [
        Paragraph(f"{n}. {escape(nombre)}", NOMBRE),
        Spacer(1, 2),
        Paragraph(escape(p["descripcion"]), TEXTO),
        Spacer(1, 4),
        Paragraph(f"<b>Procedencia:</b> {escape(procedencia)}", DATO),
        Paragraph(f"<b>Coste total</b> (martillo + comisión + envío): {coste}", DATO),
        Paragraph(f"<b>Valor estimado:</b> {valor}", DATO),
    ]
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

    por_moneda = defaultdict(float)
    por_tipo = defaultdict(int)
    for p in piezas:
        if p.get("coste_total") is not None:
            por_moneda[p["moneda"]] += p["coste_total"]
        por_tipo[p["tipo"]] += 1

    story = [
        Spacer(1, 40 * mm),
        Paragraph("Catálogo de la colección", TITULO),
        Spacer(1, 4 * mm),
        Paragraph(f"Actualizado el {date.today().strftime('%d/%m/%Y')}", SUBT),
        Spacer(1, 15 * mm),
    ]
    resumen = [["Piezas", str(len(piezas))]]
    resumen += [[tipo.capitalize() + "s", str(n)] for tipo, n in sorted(por_tipo.items())]
    resumen += [["Subastas", str(len(inv["subastas"]))]]
    resumen += [[f"Invertido ({m})", dinero(v, m)] for m, v in sorted(por_moneda.items())]
    t = Table(resumen, colWidths=[60 * mm, 50 * mm], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#d8cfc2")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [t, PageBreak()]

    grupos = defaultdict(list)
    for p in piezas:
        grupos[p.get("subasta") or "Sin factura"].append(p)
    n = 0
    for grupo, lista in grupos.items():
        story.append(Paragraph(escape(f"{lista[0].get('casa', '')} · {grupo}"
                                      if grupo != "Sin factura" else grupo), H2))
        for p in lista:
            n += 1
            story.append(ficha(n, p))

    doc = SimpleDocTemplate(str(DESTINO), pagesize=A4, title="Catálogo de la colección",
                            leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=18 * mm)
    doc.build(story, onFirstPage=pie, onLaterPages=pie)
    print(f"Catálogo: {DESTINO} ({len(piezas)} piezas)")


if __name__ == "__main__":
    main()
