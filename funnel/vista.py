#!/usr/bin/env python3
"""Arma la página tal cual queda al pegarla, para poder mirarla.

El estudio la compone en vivo dentro de su iframe; aquí se hace lo mismo sin
estudio: el HTML de la página, el kit, y un arranque que vuelca encima el estado
guardado —imágenes, textos, estilos, orden, franja— en el mismo orden que
`aplicarTodo`, y después hace la misma poda que `htmlFinal` antes de publicar.
"""
import json, io, pathlib, re

RAIZ = pathlib.Path(__file__).parent
FUENTES = ("https://fonts.googleapis.com/css2?"
           "family=Archivo:wght@400;500;600;700;800;900"
           "&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300;1,6..72,400"
           "&family=JetBrains+Mono:wght@400;500;700&display=swap")

esc_js   = lambda s: s.replace("</script", "<\\/script")
esc_json = lambda s: s.replace("<", "\\u003c")

RESET = ("html,body{margin:0!important;padding:0!important;border:0!important;"
         "width:100%!important;max-width:100%!important;min-height:100%;"
         "background:var(--ink,#0A0910)!important;color:var(--bone,#F4EFE6);"
         "overflow-x:hidden!important}"
         "html{background:var(--ink,#0A0910)!important}"
         "body>*{max-width:100%}img,video,iframe{max-width:100%}")

ARRANQUE = r"""
(() => {
  const ST = JSON.parse(document.getElementById("__estado").textContent);
  const K = window.KIT, d = document;
  if(!K) return;

  const EN_LINEA = /^(SPAN|B|STRONG|EM|I|SMALL|A|BR|S|U|SUP|SUB|CODE|MARK|Q|ABBR|TIME)$/;
  const limpiar = html => {
    const t = d.createElement("div"); t.innerHTML = html;
    for(const el of [...t.querySelectorAll("*")]){
      if(!EN_LINEA.test(el.tagName)){ el.replaceWith(...el.childNodes); continue; }
      for(const a of [...el.attributes])
        if(a.name !== "class" && a.name !== "href") el.removeAttribute(a.name);
    }
    return t.innerHTML;
  };
  const kebab = k => k.replace(/[A-Z]/g, m => "-" + m.toLowerCase());

  (ST.slotsNuevos || []).forEach(x => K.crearSlot(x.galeria, x));
  K.aplicarEstructura(ST.estructura);
  for(const [id, v] of Object.entries(ST.recursos || {})) if(v) K.aplicarRecurso(id, v);
  K.aplicarBorrados(ST.borrados || []);

  /* Una ruta que cae dentro de otra ya escrita no se aplica: el bloque de fuera
     manda sobre su propio contenido. */
  const hondura = r => r.split("-").length;
  const puestas = [];
  for(const r of Object.keys(ST.textos || {}).sort((a,b) => hondura(a)-hondura(b) || a.localeCompare(b))){
    if(puestas.some(p => r.startsWith(p + "-"))) continue;
    puestas.push(r);
    const el = K.porRuta(r); if(el) el.innerHTML = limpiar(ST.textos[r]);
  }
  for(const [r, css] of Object.entries(ST.estilos || {})){
    const el = K.porRuta(r); if(el) Object.assign(el.style, css);
  }

  /* Los tamaños del móvil son otro diseño, y valen solo por debajo de 640. */
  const reglas = [];
  for(const [r, css] of Object.entries(ST.estilosMovil || {})){
    const el = K.porRuta(r); if(!el) continue;
    el.setAttribute("data-r", r);
    const cuerpo = Object.entries(css || {}).map(([k,v]) => kebab(k)+":"+v+"!important").join(";");
    if(cuerpo) reglas.push(':root [data-r="'+r+'"]{'+cuerpo+"}");
  }
  if(reglas.length){
    const h = d.createElement("style"); h.id = "__movil";
    h.textContent = "@media(max-width:640px){" + reglas.join("") + "}";
    d.head.appendChild(h);
  }

  const filas = ST.datos?.franja;
  if(filas?.length){
    window.pintarFranja?.(filas);
    for(const [id, v] of Object.entries(ST.recursos || {})) if(v) K.aplicarRecurso(id, v);
  }
  K.refrescar();

  /* Poda de publicación: lo que es solo un hueco de foto y no tiene foto no se
     enseña, y una galería sin nada dentro sobra entera. */
  const CONTENIDO = ".cuenta, .portada, .tesela, .captura, .tf, .vida, .collage figure";
  const SOLO_FOTO = ".cuenta, .portada, .tesela, .captura, .vida, .collage figure";
  const GALERIAS  = ".mq, .portadas, .capturas, .muro, .tira, .collage";
  d.querySelectorAll("[data-oculto],[data-borrado]").forEach(e => e.remove());
  d.querySelectorAll(SOLO_FOTO).forEach(t => {
    const s = t.querySelector("[data-res]");
    if(s && !s.classList.contains("cargada")) t.remove();
  });
  d.querySelectorAll("[data-res][data-res-opcional]:not(.cargada)").forEach(e => e.remove());
  d.querySelectorAll(GALERIAS).forEach(g => { if(!g.querySelector(CONTENIDO)) g.remove(); });
  d.querySelectorAll("section[data-si-vacio]").forEach(s => { if(!s.querySelector(".cargada")) s.remove(); });
  K.refrescar();
})();
"""

def main(slug="vsl", salida="vista-final.html"):
    est = json.load(io.open(RAIZ/"estado.json", encoding="utf-8"))
    pag = est["pags"][slug]
    html = re.sub(r"^<!--PAGINA\s+\{.*?\}\s*-->\s*", "", (RAIZ/"paginas"/f"{slug}.html").read_text(encoding="utf-8"), flags=re.S)
    kitcss = (RAIZ/"paginas"/"_kit.css").read_text(encoding="utf-8")
    kitjs  = (RAIZ/"paginas"/"_kit.js").read_text(encoding="utf-8")
    guarda = {k: pag.get(k) for k in
              ("recursos","textos","estilos","estilosMovil","estructura","borrados","slotsNuevos","datos")}
    # El visor de artefactos bloquea imágenes de otros dominios, así que aquí van
    # incrustadas aunque la página publicada las sirva ya desde el CDN.
    import base64
    fotos = RAIZ / "subir-a-ghl"
    rec = dict(guarda["recursos"] or {})
    for k, v in rec.items():
        f = fotos / (k + ".webp")
        if isinstance(v, str) and v.startswith("http") and f.exists():
            rec[k] = "data:image/webp;base64," + base64.b64encode(f.read_bytes()).decode()
    guarda["recursos"] = rec

    doc = "\n".join([
        "<title>Imperio Holístico</title>",
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        f'<link rel="stylesheet" href="{FUENTES}">',
        "<style>" + kitcss + "</style>",
        "<style>" + RESET + "</style>",
        html,
        "<script>" + esc_js(kitjs) + "</script>",
        '<script type="application/json" id="__estado">' + esc_json(json.dumps(guarda, ensure_ascii=False)) + "</script>",
        "<script>" + ARRANQUE + "</script>",
    ])
    (RAIZ/salida).write_text(doc, encoding="utf-8")
    print(f"  {salida} · {len(doc.encode())/1048576:.2f} MB")

if __name__ == "__main__":
    main()
