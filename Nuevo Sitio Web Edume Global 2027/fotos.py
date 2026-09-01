#!/usr/bin/env python3
"""
Empaqueta las fotos de clientes dentro de paginas/_fotos.js

Las fotos viajan embebidas en la página. Así, al pegar el bloque en
GoHighLevel, las caras ya están dentro: no dependen de ningún servidor
ni de que alguien recuerde subirlas.

    python3 fotos.py            → regenera paginas/_fotos.js

Para añadir una cara: deja el JPG en recursos/clientes/ y añade su línea
a FOTOS. La clave es la que usa la página (data-res="foto-<clave>").
"""

import subprocess, base64, pathlib, json, sys

RAIZ = pathlib.Path(__file__).parent
ORIG = RAIZ / "recursos" / "clientes"
TMP = pathlib.Path("/tmp/edume-fotos")

ANCHO = 320      # las tarjetas del collage miden 290 px
CALIDAD = 42     # suficiente para una foto en movimiento

FOTOS = [
    ("liss",    "marcelo-y-liss-5"),
    ("jime",    "jime-y-marcelo"),
    ("ignacio", "marcelo-e-ignacio"),
    ("omar",    "marcelo-y-omar"),
    ("carmen",  "marcelo-y-carmen"),
    ("alex",    "marcelo-y-alex"),
    ("hector",  "marcelo-y-hector"),
    ("kristel", "marcelo-y-kristel"),
    ("adrian",  "marcelo-y-adrian"),
    ("ara",     "marcelo-y-ara"),
    ("ynes",    "marcelo-e-ynes"),
    ("roberta", "marcelo-y-roberta"),
    ("mario",   "marcelo-y-mario"),
    ("evelyn",  "marcelo-y-evelyn"),
    ("jordi",   "marcelo-y-jordi"),
]


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    datos, total = {}, 0
    for clave, nom in FOTOS:
        origen = ORIG / f"{nom}.jpg"
        if not origen.exists():
            sys.exit(f"✗ Falta {origen}")
        destino = TMP / f"{clave}.jpg"
        subprocess.run(
            ["sips", "-Z", str(ANCHO), "-s", "format", "jpeg",
             "-s", "formatOptions", str(CALIDAD), str(origen), "--out", str(destino)],
            capture_output=True, check=True)
        b = destino.read_bytes()
        total += len(b)
        datos[clave] = "data:image/jpeg;base64," + base64.b64encode(b).decode()

    js = (
        "/* ═══════════════════════════════════════════════════════════════════\n"
        "   FOTOS DE CLIENTES · Edume Global™\n"
        f"   Generado desde recursos/clientes/ a {ANCHO} px. Van embebidas para\n"
        "   que la página viaje entera: al pegarla en GoHighLevel las caras ya\n"
        "   están dentro, sin depender de ningún servidor.\n"
        "   Regenerar: python3 fotos.py\n"
        "   ═══════════════════════════════════════════════════════════════════ */\n"
        "window.FOTOS_EDUME = " + json.dumps(datos, ensure_ascii=False) + ";\n"
    )
    salida = RAIZ / "paginas" / "_fotos.js"
    salida.write_text(js, encoding="utf-8")
    print(f"✓ paginas/_fotos.js · {len(datos)} fotos · "
          f"{total//1024} KB de imagen → {len(js)//1024} KB de archivo")


if __name__ == "__main__":
    main()
