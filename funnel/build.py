#!/usr/bin/env python3
"""
Ensambla el Estudio de Funnel.

Entradas
  studio.html         · el cascarón del estudio (fuente única de la UI)
  paginas/_kit.css    · tokens y componentes compartidos
  paginas/_kit.js     · comportamiento compartido + puente con el estudio
  paginas/<slug>.html · cada página del funnel, con cabecera <!--PAGINA {...} -->

Salidas
  artifact.html · cuerpo listo para publicar como Artifact
  index.html    · documento completo, desplegable en cualquier hosting
"""

import json, re, pathlib, sys

RAIZ = pathlib.Path(__file__).parent
PAGS = RAIZ / "paginas"

FUENTES = ("https://fonts.googleapis.com/css2?"
           "family=Archivo:wght@400;500;600;700;800;900"
           "&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300;1,6..72,400"
           "&family=JetBrains+Mono:wght@400;500;700&display=swap")

# El orden es el orden del funnel.
ORDEN = ["vsl", "vsl-retargeting", "sesion-confirmada",
         "preparacion", "programa", "bio-instagram"]

CAB = re.compile(r"^<!--PAGINA\s+(\{.*?\})\s*-->\s*", re.S)
ETIQ = re.compile(r"<[a-zA-Z][^>]*\bdata-res=[\"'][^\"']+[\"'][^>]*>", re.S)
RID  = re.compile(r"data-res=[\"']([^\"']+)[\"']")


def contar_recursos(html):
    """Inventario estático: cuántos recursos declara la página, por obligatoriedad.
    Los generados por JS (avatares de la crew) son opcionales y no cuentan aquí."""
    req, opc = set(), set()
    for etiqueta in ETIQ.findall(html):
        m = RID.search(etiqueta)
        if not m:
            continue
        (opc if "data-res-opcional" in etiqueta else req).add(m.group(1))
    return {"req": len(req - opc), "opc": len(opc)}


def leer_pagina(slug):
    f = PAGS / f"{slug}.html"
    if not f.exists():
        sys.exit(f"✗ Falta {f}")
    txt = f.read_text(encoding="utf-8")
    m = CAB.match(txt)
    if not m:
        sys.exit(f"✗ {f.name} no tiene cabecera <!--PAGINA {{...}} -->")
    meta = json.loads(m.group(1))
    meta.setdefault("slug", slug)
    html = txt[m.end():].strip()
    meta["recursos"] = contar_recursos(html)
    return meta, html


def plantilla_esbozo():
    """El esbozo de 'vsl' sirve de molde para las páginas nuevas del estudio."""
    _, html = leer_pagina("vsl")
    html = re.sub(r"(<div class=\"esbozo-paso rv\">)Paso \d+( del funnel</div>)",
                  r"\1Paso __PASO__\2", html)
    html = re.sub(r"(<div class=\"esbozo-icono rv\"[^>]*>)[^<]*(</div>)", r"\1○\2", html)
    html = re.sub(r"(<h1 class=\"rv\"[^>]*>)[^<]*(</h1>)", r"\1__NOMBRE__\2", html)
    html = re.sub(r"(<p class=\"esbozo-rol rv\"[^>]*>)[^<]*(</p>)", r"\1__ROL__\2", html)
    return html


EST_RE = re.compile(r"<!--ESTADO-->(.*?)<!--/ESTADO-->", re.S)
EST_IN = re.compile(r"<script[^>]*>(.*)</script>", re.S)


def estado_de(html):
    """Saca el JSON de estado de un documento del estudio ya publicado."""
    m = EST_RE.search(html)
    if not m:
        return None
    inner = EST_IN.search(m.group(1))
    if not inner:
        return None
    crudo = inner.group(1).replace("<\\/", "</").strip()
    try:
        return json.loads(crudo)
    except json.JSONDecodeError:
        return None


def estado_actual():
    """Estado que debe sobrevivir a este build.

    Prioridad: estado.json (lo que importaste del artifact publicado) y, si no,
    lo que ya tuviera el artifact.html local. Así un rebuild NUNCA borra los
    recursos ni las ediciones que Marcelo cargó en el estudio.
    """
    f = RAIZ / "estado.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            sys.exit("✗ estado.json no es JSON válido")
    prev = RAIZ / "artifact.html"
    if prev.exists():
        return estado_de(prev.read_text(encoding="utf-8"))
    return None


def importar(ruta):
    """build.py --importar <artifact-descargado.html> → estado.json"""
    st = estado_de(pathlib.Path(ruta).read_text(encoding="utf-8"))
    if st is None:
        sys.exit("✗ Ese archivo no tiene un bloque <!--ESTADO--> con estado guardado")
    (RAIZ / "estado.json").write_text(
        json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(p.get("recursos", {})) for p in (st.get("pags") or {}).values())
    e = sum(len(p.get("estilos", {})) + len(p.get("textos", {}))
            for p in (st.get("pags") or {}).values())
    print(f"✓ estado.json guardado · {n} recursos, {e} ediciones, "
          f"{len(st.get('extra', {}))} páginas creadas en el estudio")


def main():
    paginas, listas = {}, 0
    for slug in ORDEN:
        meta, html = leer_pagina(slug)
        paginas[slug] = {"meta": meta, "html": html}
        listas += meta.get("estado") == "listo"
        r = meta["recursos"]
        print(f"  · {meta['nombre']:<22} {len(html)//1024:>4} KB   "
              f"{meta.get('estado','esbozo'):<7} {r['req']} oblig. + {r['opc']} opc.")

    fuente = {
        "orden":   ORDEN,
        "paginas": paginas,
        "kitCss":  (PAGS / "_kit.css").read_text(encoding="utf-8"),
        "kitJs":   (PAGS / "_kit.js").read_text(encoding="utf-8"),
        "fuentes": FUENTES,
        "esbozo":  plantilla_esbozo(),
    }

    # </script> dentro de un <script type="application/json"> cerraría la etiqueta.
    blob = json.dumps(fuente, ensure_ascii=False).replace("</", "<\\/")

    shell = (RAIZ / "studio.html").read_text(encoding="utf-8")
    if "/*__PAGINAS__*/" not in shell:
        sys.exit("✗ studio.html no tiene el marcador /*__PAGINAS__*/")
    cuerpo = shell.replace("/*__PAGINAS__*/", blob)

    # El trabajo hecho dentro del estudio sobrevive al rebuild.
    est = estado_actual()
    if est is not None:
        crudo = json.dumps(est, ensure_ascii=False).replace("</", "<\\/")
        cuerpo = EST_RE.sub(
            lambda _: '<!--ESTADO--><script type="application/json" id="estadoGuardado">'
                      + crudo + "</script><!--/ESTADO-->",
            cuerpo, count=1)
        rec = sum(len(p.get("recursos", {})) for p in (est.get("pags") or {}).values())
        edi = sum(len(p.get("estilos", {})) + len(p.get("textos", {}))
                  for p in (est.get("pags") or {}).values())
        print(f"  ↻ estado conservado: {rec} recursos, {edi} ediciones")

    (RAIZ / "artifact.html").write_text(cuerpo, encoding="utf-8")

    cabecera = "\n".join([
        "<!doctype html>", '<html lang="es">', "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="theme-color" content="#0B0A0E">',
        '<meta name="robots" content="noindex, nofollow">',
        '<meta name="description" content="Estudio interno del funnel Escalling™. No es una página pública.">',
        '<link rel="icon" href="data:image/svg+xml,'
        "%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 40 40%27%3E"
        "%3Crect width=%2740%27 height=%2740%27 fill=%27%230B0A0E%27/%3E"
        "%3Ccircle cx=%2720%27 cy=%2720%27 r=%2714%27 fill=%27none%27 stroke=%27%23D6A544%27 stroke-width=%272%27/%3E"
        "%3Ccircle cx=%2720%27 cy=%2720%27 r=%275%27 fill=%27%23D6A544%27/%3E%3C/svg%3E\">",
    ])
    (RAIZ / "index.html").write_text(
        cabecera + "\n" + cuerpo + "\n</body>\n</html>\n", encoding="utf-8")

    kb = (RAIZ / "index.html").stat().st_size // 1024
    print(f"\n✓ {len(ORDEN)} páginas ({listas} lista/s, {len(ORDEN)-listas} esbozo/s)")
    print(f"✓ artifact.html + index.html · {kb} KB")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--importar":
        importar(sys.argv[2])
    else:
        main()
