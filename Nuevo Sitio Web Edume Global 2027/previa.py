#!/usr/bin/env python3
"""
Una página suelta, sin el estudio alrededor.

    python3 previa.py            → previa.html con la home
    python3 previa.py programa   → previa.html con esa página

Sirve para ver una página tal como la verá el visitante —el estudio pesa
y añade su propio cromado— y para abrirla en el móvil o enseñarla a
alguien sin darle acceso al estudio entero.

previa.html se regenera cada vez. No lo edites: edita paginas/<slug>.html.
"""

import re, sys, pathlib

RAIZ = pathlib.Path(__file__).parent
PAGS = RAIZ / "paginas"

FUENTES = ("https://fonts.googleapis.com/css2?"
           "family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;1,400;1,700"
           "&family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700"
           "&display=swap")

CAB = re.compile(r"^<!--PAGINA\s+(\{.*?\})\s*-->\s*", re.S)


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "inicio"
    f = PAGS / f"{slug}.html"
    if not f.exists():
        sys.exit(f"✗ No existe {f}")

    pagina = CAB.sub("", f.read_text(encoding="utf-8"))
    fotos = PAGS / "_fotos.js"
    cierre = "</scr" + "ipt>"

    doc = "\n".join([
        "<!doctype html>", '<html lang="es">', "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="robots" content="noindex, nofollow">',
        f'<link rel="preconnect" href="https://fonts.googleapis.com">',
        f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        f'<link rel="stylesheet" href="{FUENTES}">',
        "<style>" + (PAGS / "_kit.css").read_text(encoding="utf-8") + "</style>",
        ("<script>" + fotos.read_text(encoding="utf-8") + cierre) if fotos.exists() else "",
        "</head><body>",
        pagina,
        "<script>" + (PAGS / "_kit.js").read_text(encoding="utf-8") + cierre,
        "</body></html>",
    ])

    salida = RAIZ / "previa.html"
    salida.write_text(doc, encoding="utf-8")
    print(f"✓ previa.html · {slug} · {salida.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
