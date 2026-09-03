#!/usr/bin/env python3
"""Recomprime las imágenes del estado a los mismos números que el estudio.

El depósito del historial (`pool`) se indexa por un hash del contenido, así que
recomprimir sin re-calcular la clave dejaba la entrada vieja anclada por los
snapshots antiguos y el navegador creaba otra: el pool se duplicaba en cada
pasada. Aquí se re-indexa y se reescriben las referencias del historial.
"""
import base64, io, json, sys, time
from PIL import Image

TECHO_PX, CALIDAD = 760, 80          # idénticos a studio.html

D36 = "0123456789abcdefghijklmnopqrstuvwxyz"
def b36(n):
    if not n: return "0"
    o = ""
    while n: o = D36[n % 36] + o; n //= 36
    return o

def clave(t):
    """Mismo hash que `clave()` en studio.html, con la aritmética de 32 bits de JS."""
    h = 0
    for ch in t:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        if h >= 0x80000000: h -= 0x100000000
    return b36(h & 0xFFFFFFFF) + b36(len(t))

def encoger(uri):
    """Devuelve la versión ligera, o el original si ya no se puede mejorar."""
    if not (isinstance(uri, str) and uri.startswith("data:image")): return uri
    try: crudo = base64.b64decode(uri.split(",", 1)[1])
    except Exception: return uri
    try: im = Image.open(io.BytesIO(crudo))
    except Exception: return uri
    if im.mode not in ("RGB", "RGBA"): im = im.convert("RGB")
    if im.width > TECHO_PX:
        im = im.resize((TECHO_PX, round(im.height * TECHO_PX / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=CALIDAD, method=6)
    nuevo = buf.getvalue()
    if len(nuevo) >= len(crudo): return uri
    return "data:image/webp;base64," + base64.b64encode(nuevo).decode()

def main(ruta="estado.json"):
    e = json.load(io.open(ruta, encoding="utf-8"))
    antes = sum(len(v) for p in e["pags"].values()
                for v in (p.get("recursos") or {}).values() if str(v).startswith("data:"))
    antes += sum(len(v) for v in (e.get("pool") or {}).values())

    for p in e["pags"].values():
        rec = p.get("recursos") or {}
        for k, v in list(rec.items()): rec[k] = encoger(v)

    pool, mapa, nuevo = e.get("pool") or {}, {}, {}
    for k, v in pool.items():
        v2 = encoger(v)
        k2 = clave(v2)                    # la clave sigue al contenido, como en el estudio
        mapa[k], nuevo[k2] = k2, v2
    e["pool"] = nuevo

    hist = json.dumps(e.get("historial") or [])
    for viejo, nuev in mapa.items():
        if viejo != nuev: hist = hist.replace(f"@pool:{viejo}", f"@pool:{nuev}")
    e["historial"] = json.loads(hist)

    despues = sum(len(v) for p in e["pags"].values()
                  for v in (p.get("recursos") or {}).values() if str(v).startswith("data:"))
    despues += sum(len(v) for v in nuevo.values())
    e["ts"] = int(time.time() * 1000)
    json.dump(e, io.open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"  pool: {len(pool)} → {len(nuevo)} entradas "
          f"({len(pool)-len(nuevo)} duplicadas colapsadas)")
    print(f"  imágenes: {antes*0.75/1024/1024:.2f} → {despues*0.75/1024/1024:.2f} MB")

if __name__ == "__main__":
    main(*sys.argv[1:])
