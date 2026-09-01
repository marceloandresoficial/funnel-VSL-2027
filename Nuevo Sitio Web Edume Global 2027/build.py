#!/usr/bin/env python3
"""
Ensambla el Estudio del Sitio · Edume Global™

Entradas
  sitio.json          · el mapa del sitio: qué páginas hay, en qué orden y área
  estudio.html        · el cascarón del estudio (fuente única de la UI)
  paginas/_kit.css    · tokens y componentes compartidos
  paginas/_kit.js     · comportamiento compartido + puente con el estudio
  paginas/<slug>.html · cada página, con cabecera <!--PAGINA {...} -->

Salidas
  artifact.html · cuerpo listo para publicar como Artifact
  index.html    · documento completo, desplegable en cualquier hosting

Una página que aparece en sitio.json y no existe en paginas/ se crea como
esbozo: así el mapa del sitio manda, y basta añadir una entrada para que
la página exista y se pueda abrir en el estudio.
"""

import json, re, pathlib, sys

RAIZ = pathlib.Path(__file__).parent
PAGS = RAIZ / "paginas"

FUENTES = ("https://fonts.googleapis.com/css2?"
           "family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;1,400;1,700"
           "&family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700"
           "&display=swap")

CAB = re.compile(r"^<!--PAGINA\s+(\{.*?\})\s*-->\s*", re.S)
ETIQ = re.compile(r"<[a-zA-Z][^>]*\bdata-res=[\"'][^\"']+[\"'][^>]*>", re.S)
RID = re.compile(r"data-res=[\"']([^\"']+)[\"']")


def mapa():
    f = RAIZ / "sitio.json"
    if not f.exists():
        sys.exit("✗ Falta sitio.json · es el mapa del sitio")
    try:
        m = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"✗ sitio.json no es JSON válido · {e}")
    if not m.get("paginas"):
        sys.exit("✗ sitio.json no tiene ni una página")
    return m


def contar_recursos(html):
    """Inventario estático: cuántos recursos declara la página, por obligatoriedad.
    Los generados por JS son opcionales y no cuentan aquí."""
    req, opc = set(), set()
    for etiqueta in ETIQ.findall(html):
        m = RID.search(etiqueta)
        if not m:
            continue
        (opc if "data-res-opcional" in etiqueta else req).add(m.group(1))
    return {"req": len(req - opc), "opc": len(opc)}


def esbozo_de(e):
    """Una página que aún no existe: nace con el Kit puesto y su ficha a la vista."""
    meta = {
        "nombre": e["nombre"], "slug": e["slug"], "icono": e.get("icono", "○"),
        "grupo": e.get("grupo", ""), "descripcion": e.get("descripcion", ""),
        "origen": e.get("origen", ""), "estado": "esbozo",
    }
    origen = e.get("origen", "")
    fila_origen = (f'\n        <li><b>Origen en Kajabi:</b> <code>{origen}</code></li>'
                   if origen else
                   '\n        <li>Falta el enlace de la página equivalente en Kajabi.</li>')
    return "<!--PAGINA " + json.dumps(meta, ensure_ascii=False) + " -->\n" + f"""<style>
/* Esbozo · hereda el Kit de Edume. Se sustituye cuando construyamos la página. */
.esbozo{{min-height:100vh;display:grid;place-items:center;padding-block:120px;
  background:var(--crema-claro)}}
.esbozo-in{{max-width:720px;width:100%;text-align:center}}
.esbozo-area{{font-family:var(--sys);font-size:12px;font-weight:700;letter-spacing:.18em;
  text-transform:uppercase;color:var(--violeta);display:flex;align-items:center;gap:12px;
  justify-content:center;margin-bottom:26px}}
.esbozo-area::before,.esbozo-area::after{{content:"";width:34px;height:1px;background:var(--violeta);opacity:.45}}
.esbozo-icono{{font-size:2.4rem;line-height:1;color:var(--violeta);margin-bottom:22px}}
.esbozo-in h1{{font-family:var(--alma);font-size:36px;line-height:1;color:var(--tinta)}}
.esbozo-rol{{font-family:var(--alma);font-size:20px;line-height:1.3;color:var(--gris);margin:18px 0 0}}
.esbozo-nota{{margin-top:40px;border:1px dashed #59595955;border-radius:12px;
  padding:32px;text-align:left;background:var(--crema)}}
.esbozo-nota h2{{font-family:var(--sys);font-size:14px;font-weight:700;color:var(--tinta);
  margin-bottom:18px;display:flex;align-items:center;gap:10px}}
.esbozo-nota h2 i{{width:7px;height:7px;border-radius:50%;background:var(--violeta);flex:none}}
.esbozo-nota ul{{list-style:none;margin:0;padding:0;display:grid;gap:13px}}
.esbozo-nota li{{display:flex;gap:13px;font-size:14px;color:var(--gris);line-height:1.5;align-items:flex-start}}
.esbozo-nota li::before{{content:"";flex:none;width:15px;height:15px;border-radius:4px;margin-top:2px;
  border:1px solid #59595966}}
.esbozo-nota code{{font-family:ui-monospace,Menlo,monospace;font-size:.85em;color:var(--violeta);word-break:break-all}}
.esbozo-pie{{margin-top:28px;font-size:13px;color:var(--gris);opacity:.8;line-height:1.6}}
</style>

<main class="esbozo" id="top">
  <div class="contenedor esbozo-in">
    <div class="esbozo-area rv">{meta['grupo'] or 'Sitio'}</div>
    <div class="esbozo-icono rv" style="--d:60ms">{meta['icono']}</div>
    <h1 class="rv" style="--d:100ms">{meta['nombre']}</h1>
    <p class="esbozo-rol rv" style="--d:160ms">{meta['descripcion']}</p>

    <div class="esbozo-nota rv" style="--d:220ms">
      <h2><i></i> Pendiente de construir</h2>
      <ul>{fila_origen}
        <li>Cuál es el objetivo único de esta página y qué acción tiene que provocar.</li>
        <li>Qué bloques quieres: video, prueba social, objeciones, precio, FAQ…</li>
        <li>Qué recursos va a tener: videos, imágenes, enlaces, formularios.</li>
      </ul>
      <p class="esbozo-pie">
        La página ya existe en el sitio y hereda el Kit de Marca. El resto del estudio
        (<code>PC/Móvil</code>, <code>Editar texto</code>, <code>Recursos</code>,
        <code>Código</code>) ya funciona sobre ella.
      </p>
    </div>
  </div>
</main>
"""


def leer_pagina(e):
    """Devuelve (meta, html). Si el archivo no existe, lo crea como esbozo."""
    slug = e["slug"]
    f = PAGS / f"{slug}.html"
    nueva = not f.exists()
    if nueva:
        f.write_text(esbozo_de(e), encoding="utf-8")
    txt = f.read_text(encoding="utf-8")
    m = CAB.match(txt)
    if not m:
        sys.exit(f"✗ {f.name} no tiene cabecera <!--PAGINA {{...}} -->")
    meta = json.loads(m.group(1))
    # El mapa manda sobre la ficha: renombrar en sitio.json renombra la página.
    meta.update({k: v for k, v in e.items() if k in
                 ("nombre", "icono", "grupo", "descripcion", "origen") and v})
    meta.setdefault("slug", slug)
    html = txt[m.end():].strip()
    meta["recursos"] = contar_recursos(html)
    return meta, html, nueva


def plantilla_esbozo():
    """El molde de las páginas que se creen desde el propio estudio."""
    return esbozo_de({"slug": "__SLUG__", "nombre": "__NOMBRE__",
                      "icono": "○", "grupo": "Sitio",
                      "descripcion": "__ROL__"}).split("-->", 1)[1].strip()


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
    recursos ni las ediciones cargadas en el estudio.
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
    m = mapa()
    orden, paginas, listas, creadas = [], {}, 0, 0
    grupo_ant = None
    for e in m["paginas"]:
        meta, html, nueva = leer_pagina(e)
        slug = meta["slug"]
        orden.append(slug)
        paginas[slug] = {"meta": meta, "html": html}
        listas += meta.get("estado") == "listo"
        creadas += nueva
        if meta.get("grupo") != grupo_ant:
            grupo_ant = meta.get("grupo")
            print(f"\n  {grupo_ant or 'Sin área'}")
        r = meta["recursos"]
        print(f"  · {meta['nombre']:<24} {len(html)//1024:>4} KB   "
              f"{meta.get('estado','esbozo'):<7} {r['req']} oblig. + {r['opc']} opc."
              f"{'   ← creada' if nueva else ''}")

    fuente = {
        "sitio":   {"nombre": m.get("nombre", ""), "dominio": m.get("dominio", "")},
        "orden":   orden,
        "paginas": paginas,
        "kitCss":  (PAGS / "_kit.css").read_text(encoding="utf-8"),
        "kitJs":   (PAGS / "_kit.js").read_text(encoding="utf-8"),
        # Fotos de clientes embebidas · las genera fotos.py
        "fotosJs": (PAGS / "_fotos.js").read_text(encoding="utf-8")
                   if (PAGS / "_fotos.js").exists() else "",
        "fuentes": FUENTES,
        "esbozo":  plantilla_esbozo(),
    }

    # </script> dentro de un <script type="application/json"> cerraría la etiqueta.
    blob = json.dumps(fuente, ensure_ascii=False).replace("</", "<\\/")

    shell = (RAIZ / "estudio.html").read_text(encoding="utf-8")
    if "/*__PAGINAS__*/" not in shell:
        sys.exit("✗ estudio.html no tiene el marcador /*__PAGINAS__*/")
    cuerpo = shell.replace("/*__PAGINAS__*/", blob)
    cuerpo = cuerpo.replace("edumeglobal.com/", m.get("dominio", "edumeglobal.com") + "/")

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
        print(f"\n  ↻ estado conservado: {rec} recursos, {edi} ediciones")

    (RAIZ / "artifact.html").write_text(cuerpo, encoding="utf-8")

    cabecera = "\n".join([
        "<!doctype html>", '<html lang="es">', "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="theme-color" content="#0B0A0E">',
        '<meta name="robots" content="noindex, nofollow">',
        '<meta name="description" content="Estudio interno del sitio de Edume Global™. No es una página pública.">',
        '<link rel="icon" href="data:image/svg+xml,'
        "%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 40 40%27%3E"
        "%3Crect width=%2740%27 height=%2740%27 fill=%27%230B0A0E%27/%3E"
        "%3Ccircle cx=%2720%27 cy=%2720%27 r=%2714%27 fill=%27none%27 stroke=%27%23D6A544%27 stroke-width=%272%27/%3E"
        "%3Ccircle cx=%2720%27 cy=%2720%27 r=%275%27 fill=%27%23D6A544%27/%3E%3C/svg%3E\">",
    ])
    (RAIZ / "index.html").write_text(
        cabecera + "\n" + cuerpo + "\n</body>\n</html>\n", encoding="utf-8")

    kb = (RAIZ / "index.html").stat().st_size // 1024
    print(f"\n✓ {len(orden)} páginas ({listas} lista/s, {len(orden)-listas} esbozo/s"
          f"{f', {creadas} nueva/s' if creadas else ''})")
    print(f"✓ artifact.html + index.html · {kb} KB")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--importar":
        importar(sys.argv[2])
    else:
        main()
