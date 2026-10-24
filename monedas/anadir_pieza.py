"""Añade al inventario una pieza que no viene de una factura de Biddr: compras
directas a un comerciante o piezas sin factura.

Uso:
    python3 monedas/anadir_pieza.py --id solidus_teodosio_1 \\
        --descripcion "Theodosius II ... RIC 292" --coste 514.45 --moneda EUR \\
        --fecha "29 Sep 2025" --casa "Demeter Coins" --factura 2025092901 \\
        --foto ruta/foto.jpg --notas "..."

Sin --casa ni --factura, la pieza queda como "sin factura". Repetir con el
mismo --id sustituye la pieza.
"""
import argparse
import shutil
from pathlib import Path

from procesar_factura import RAIZ, IMAGENES, cargar_inventario, guardar_inventario


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True)
    ap.add_argument("--descripcion", required=True)
    ap.add_argument("--tipo", default="moneda", choices=["moneda", "billete"])
    ap.add_argument("--coste", type=float, help="lo que costó, con todos los gastos")
    ap.add_argument("--moneda", default="EUR")
    ap.add_argument("--fecha", help='fecha de compra, p. ej. "29 Sep 2025"')
    ap.add_argument("--casa", help="comerciante o casa de subastas")
    ap.add_argument("--factura", help="número de factura")
    ap.add_argument("--foto", help="imagen con anverso y reverso")
    ap.add_argument("--notas")
    a = ap.parse_args()

    foto = None
    if a.foto:
        IMAGENES.mkdir(parents=True, exist_ok=True)
        foto = f"img/{a.id}{Path(a.foto).suffix.lower()}"
        shutil.copyfile(a.foto, RAIZ / "datos" / foto)

    con_factura = bool(a.casa or a.factura)
    inv = cargar_inventario()
    inv["piezas"] = [p for p in inv["piezas"] if p["id"] != a.id]
    inv["piezas"].append({
        "id": a.id,
        "tipo": a.tipo,
        "origen": "compra directa" if con_factura else "sin factura",
        "subasta": None,
        "casa": a.casa,
        "factura": a.factura,
        "fecha_compra": a.fecha,
        "lote": None,
        "descripcion": a.descripcion,
        "martillo": None,
        "coste_total": a.coste,
        "moneda": a.moneda,
        "foto": foto,
        "valor_estimado": None,
        "notas": a.notas,
    })
    guardar_inventario(inv)
    print(f"Añadida: {a.id} ({a.coste} {a.moneda})")


if __name__ == "__main__":
    main()
