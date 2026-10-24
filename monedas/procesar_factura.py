"""Procesa una factura de Biddr: extrae los lotes y sus fotos, marca en una
copia del PDF los lotes que se conservan y los añade al inventario.

Uso:
    python3 monedas/procesar_factura.py facturas/Factura.pdf 236 327 329
"""
import io
import json
import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

RAIZ = Path(__file__).resolve().parent.parent
INVENTARIO = RAIZ / "datos" / "inventario.json"
IMAGENES = RAIZ / "datos" / "img"
SALIDA = RAIZ / "salida"

COL_LOTE_MAX_X = 90      # el número de lote está en la columna izquierda
COL_DESC_X = (200, 480)  # columna de descripción
COL_PRECIO_X = 480       # columna "Hammer"


def cargar_inventario():
    if INVENTARIO.exists():
        return json.loads(INVENTARIO.read_text(encoding="utf-8"))
    return {"subastas": [], "piezas": []}


def guardar_inventario(inv):
    INVENTARIO.parent.mkdir(parents=True, exist_ok=True)
    INVENTARIO.write_text(json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8")


def numero(texto):
    return float(texto.replace(",", ""))


def leer_cabecera(texto):
    cab = {}
    m = re.search(r"^(.+?) - Invoice (\S+)", texto, re.M)
    if m:
        cab["subasta"] = m.group(1).strip()
        cab["factura"] = m.group(2)
    m = re.search(r"^\s*(\S.*?),\s+(\d{1,2} \w{3} \d{4})\s*$", texto, re.M)
    if m:
        cab["lugar"], cab["fecha"] = m.group(1).strip(), m.group(2)
    # "Buyer's premium (+16.50%)" o "Buyer's commission" con el porcentaje en otra línea
    m = re.search(r"Buyer's (?:premium|commission).*?([\d.,]+) ([A-Z]{3})", texto)
    if m:
        cab["comision"] = numero(m.group(1))
        cab["moneda"] = m.group(2)
    m = re.search(r"\(\+([\d.]+)%\)", texto)
    cab["comision_pct"] = numero(m.group(1)) if m else 0.0
    for clave, patron in [("martillo_total", r"Total hammer\s+([\d.,]+)"),
                          ("envio", r"Shipping costs[^\d]*?([\d.,]+) \w+"),
                          ("gastos_pago", r"Payment fees[^\d]*?([\d.,]+) \w+"),
                          ("total", r"^\s+Total\s+([\d.,]+)")]:
        m = re.search(patron, texto, re.M)
        cab[clave] = numero(m.group(1)) if m else 0.0
    return cab


def leer_lotes(pdf):
    """Devuelve la lista de lotes con su descripción, precio, foto y posición."""
    lotes = []
    en_tabla = False
    for n_pag, pag in enumerate(pdf.pages):
        palabras = pag.extract_words()
        cab = next((w for w in palabras if w["text"] == "Lot" and w["x0"] < COL_LOTE_MAX_X), None)
        if cab:
            inicio, en_tabla = cab["top"], True
        elif en_tabla:
            # Páginas de continuación: la tabla empieza bajo el logotipo, sin cabecera.
            inicio = 0
        else:
            continue
        fin = next((w["top"] for w in palabras
                    if w["text"] == "Lots" and w["top"] > inicio), None)
        if fin is None:
            # La tabla sigue en la página siguiente; acaba en el pie con los datos del vendedor.
            fin = min((w["top"] for w in palabras if w["text"] == "•"), default=pag.height)
        else:
            en_tabla = False
        inicios = [w for w in palabras
                   if w["x0"] < COL_LOTE_MAX_X and inicio < w["top"] < fin - 8
                   and re.fullmatch(r"\d+[a-zA-Z]?", w["text"])]
        for i, w in enumerate(inicios):
            arriba = w["top"] - 4
            abajo = inicios[i + 1]["top"] - 4 if i + 1 < len(inicios) else fin - 8
            fila = [p for p in palabras if arriba <= p["top"] < abajo]
            if i + 1 == len(inicios):
                # Último lote de la página: la franja acaba bajo su texto o su foto.
                bordes = [p["bottom"] for p in fila]
                bordes += [im["bottom"] for im in pag.images if arriba <= im["top"] < abajo]
                abajo = max(bordes) + 6
            lineas = {}
            for p in fila:
                if COL_DESC_X[0] <= p["x0"] < COL_DESC_X[1]:
                    lineas.setdefault(round(p["top"]), []).append(p["text"])
            desc = " ".join(" ".join(v) for _, v in sorted(lineas.items()))
            desc = re.sub(r"(\w)- (\w)", r"\1\2", desc)
            precio = [p["text"] for p in fila if p["x0"] >= COL_PRECIO_X]
            img = next((im for im in pag.images
                        if arriba <= im["top"] < abajo and im["x0"] < COL_DESC_X[0]), None)
            lotes.append({
                "lote": w["text"],
                "descripcion": desc,
                "martillo": numero(precio[0]) if precio else 0.0,
                "_img": img["stream"].get_rawdata() if img else None,
                "_pagina": n_pag,
                "_caja": (arriba, abajo),
            })
    return lotes


def marcar_pdf(origen, destino, lotes, conservados):
    lector = PdfReader(origen)
    escritor = PdfWriter()
    for n_pag, pagina in enumerate(lector.pages):
        ancho, alto = float(pagina.mediabox.width), float(pagina.mediabox.height)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(ancho, alto))
        for lote in (l for l in lotes if l["_pagina"] == n_pag):
            arriba, abajo = lote["_caja"]
            y0, h = alto - abajo, abajo - arriba
            if lote["lote"] in conservados:
                c.setFillColor(Color(0.2, 0.75, 0.3, alpha=0.22))
                c.setStrokeColor(Color(0.1, 0.55, 0.2))
                c.rect(48, y0, ancho - 96, h, fill=1, stroke=1)
                c.setFillColor(Color(0.1, 0.5, 0.2))
                etiqueta = "ME LA QUEDO"
            else:
                c.setFillColor(Color(0.5, 0.5, 0.5, alpha=0.25))
                c.rect(48, y0, ancho - 96, h, fill=1, stroke=0)
                c.setStrokeColor(Color(0.45, 0.45, 0.45))
                c.setLineWidth(1.2)
                c.line(52, y0 + h / 2, ancho - 52, y0 + h / 2)
                c.setFillColor(Color(0.4, 0.4, 0.4))
                etiqueta = "VENDIDA"
            c.setFont("Helvetica-Bold", 7)
            c.drawRightString(ancho - 52, y0 + 3, etiqueta)
        c.showPage()
        c.save()
        buf.seek(0)
        pagina.merge_page(PdfReader(buf).pages[0])
        escritor.add_page(pagina)
    with open(destino, "wb") as f:
        escritor.write(f)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    origen = Path(sys.argv[1])
    conservados = set(sys.argv[2:])

    with pdfplumber.open(origen) as pdf:
        cab = leer_cabecera("\n".join(p.extract_text(layout=True) for p in pdf.pages))
        lotes = leer_lotes(pdf)
        titulo = (pdf.metadata.get("Title") or "").strip()
    # El título del PDF de Biddr es "Casa - Subasta"; si falta, queda la subasta sola.
    cab["casa"] = titulo.rsplit(" - ", 1)[0] if " - " in titulo else ""

    faltan = conservados - {l["lote"] for l in lotes}
    if faltan:
        sys.exit(f"Estos lotes no están en la factura: {', '.join(sorted(faltan))}")
    suma = sum(l["martillo"] for l in lotes)
    if abs(suma - cab.get("martillo_total", suma)) > 0.01:
        sys.exit(f"La suma de lotes ({suma}) no cuadra con el total de la factura "
                 f"({cab['martillo_total']}); revisar la lectura.")

    id_subasta = f"{cab['subasta']} / {cab['factura']}"
    inv = cargar_inventario()
    inv["subastas"] = [s for s in inv["subastas"] if s["id"] != id_subasta]
    inv["piezas"] = [p for p in inv["piezas"] if p.get("subasta") != id_subasta]
    inv["subastas"].append({"id": id_subasta, **cab, "archivo": origen.name,
                            "lotes": len(lotes), "conservados": sorted(conservados)})

    # Coste real de cada lote: martillo + comisión + parte proporcional de envío y gastos.
    extra = cab["envio"] + cab["gastos_pago"]
    IMAGENES.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"\W+", "_", id_subasta).strip("_").lower()
    for l in lotes:
        if l["lote"] not in conservados:
            continue
        foto = None
        if l["_img"]:
            foto = f"img/{slug}_{l['lote']}.jpg"
            (RAIZ / "datos" / foto).write_bytes(l["_img"])
        coste = l["martillo"] * (1 + cab["comision_pct"] / 100) + extra * l["martillo"] / suma
        inv["piezas"].append({
            "id": f"{slug}_{l['lote']}",
            "tipo": "moneda",
            "origen": "subasta",
            "subasta": id_subasta,
            "casa": cab["casa"],
            "fecha_compra": cab.get("fecha"),
            "lote": l["lote"],
            "descripcion": l["descripcion"],
            "martillo": l["martillo"],
            "coste_total": round(coste, 2),
            "moneda": cab["moneda"],
            "foto": foto,
            "valor_estimado": None,
        })
    guardar_inventario(inv)

    SALIDA.mkdir(exist_ok=True)
    destino = SALIDA / f"{origen.stem}_marcada.pdf"
    marcar_pdf(origen, destino, lotes, conservados)

    print(f"{id_subasta}: {len(lotes)} lotes, conservados {len(conservados)}")
    for l in lotes:
        marca = "✔" if l["lote"] in conservados else "✘"
        print(f"  {marca} {l['lote']:>5}  {l['martillo']:>8.2f}  {l['descripcion'][:70]}")
    print(f"PDF marcado: {destino}")


if __name__ == "__main__":
    main()
