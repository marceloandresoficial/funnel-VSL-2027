#!/usr/bin/env python3
"""
Revisión estática de las páginas del funnel.

Caza las tres cosas que ya nos rompieron la página en silencio:

  1 · un #id que el JS toca y que no existe en el HTML
      (un null ahí aborta TODO el resto del <script>)
  2 · una clase usada en el markup que no tiene ni una regla de CSS
      (así el icono de 24×24 de «pago recibido» se estiró a pantalla completa)
  3 · JS que no compila o CSS con las llaves descuadradas

    python3 revisar.py        → 0 si todo bien, 1 si hay algo que mirar
"""

import re, io, sys, glob, os, subprocess, pathlib

RAIZ = pathlib.Path(__file__).parent
CAB  = re.compile(r"^<!--PAGINA\s+(\{.*?\})\s*-->\s*", re.S)
EXTERNAS = ("vt-", "vturb", "icl", "fa-", "wistia")     # clases de terceros


def clases_de_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return set(re.findall(r"\.([A-Za-z][\w-]*)", css))


def revisar(ruta, kit_css, kit_js):
    txt = io.open(ruta, encoding="utf-8").read()
    m = CAB.match(txt)
    cuerpo = txt[m.end():] if m else txt
    css = "".join(re.findall(r"<style[^>]*>(.*?)</style>", cuerpo, re.S))
    js  = "\n;\n".join(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", cuerpo, re.S))
    markup = re.sub(r"<(script|style).*?</\1>", "", cuerpo, flags=re.S)

    fallos = []

    # 1 · ids que el JS toca y no existen
    ids = set(re.findall(r'\bid="([^"]+)"', markup))
    ids |= set(re.findall(r"\bid=\\?[\"']([A-Za-z][\w-]*)", js))     # los que crea el propio JS
    for uso in sorted(set(re.findall(r'\$\(\s*["\']#([\w-]+)["\']', js))):
        if uso in ids:
            continue
        # ¿está protegido?  pon()/txt()/?.  o un  if(!$("#x")) return
        crudo = re.search(r'\$\(\s*["\']#' + re.escape(uso) + r'["\']\s*\)\s*\.\w+\s*=', js)
        if crudo:
            fallos.append("#%s no existe y se le escribe directo" % uso)

    # 2 · clases sin una sola regla
    usadas = set()
    for a in re.findall(r'class\s*=\s*"([^"{}]*)"', cuerpo):
        usadas |= set(a.split())
    for a in re.findall(r'class="([^"]*?)\$\{[^}]*\}([^"]*)"', cuerpo):
        usadas |= set((a[0] + " " + a[1]).split())
    definidas = clases_de_css(css) | clases_de_css(kit_css)
    for c in sorted(usadas - definidas):
        if not c.startswith(EXTERNAS):
            fallos.append(".%s se usa pero no tiene CSS" % c)

    # 3 · sintaxis
    if css.count("{") != css.count("}"):
        fallos.append("CSS con las llaves descuadradas (%d abren, %d cierran)"
                      % (css.count("{"), css.count("}")))
    tmp = RAIZ / ".revisar.tmp.js"
    tmp.write_text(kit_js + "\n;\n" + js, encoding="utf-8")
    r = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
    tmp.unlink(missing_ok=True)
    if r.returncode != 0:
        fallos.append("el JS no compila: " + r.stderr.strip().splitlines()[0][:120])

    return fallos


def main():
    kit_css = (RAIZ / "paginas/_kit.css").read_text(encoding="utf-8")
    kit_js  = (RAIZ / "paginas/_kit.js").read_text(encoding="utf-8")
    total = 0
    for f in sorted(glob.glob(str(RAIZ / "paginas/*.html"))):
        fallos = revisar(f, kit_css, kit_js)
        total += len(fallos)
        print(("✓ " if not fallos else "✗ ") + os.path.basename(f))
        for x in fallos:
            print("    · " + x)
    print("\n%s" % ("Todo limpio." if not total else "%d cosa/s que mirar." % total))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
