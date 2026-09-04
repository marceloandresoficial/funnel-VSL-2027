#!/usr/bin/env python3
"""Recorta cada imagen a la resolución que de verdad se ve en pantalla.

`optimizar.py` las deja todas a 760 px porque no sabe dónde se usan. Pero una
cara de la franja se dibuja en un círculo de 46 px y una captura en una tarjeta
de 338 px: guardar 760 px es pagar cuatro veces por píxeles que nadie mira. Los
anchos de abajo salen de medir la página publicada a 1440 px y a 430 px, y se
multiplican por 1,5 para que en pantallas retina siga viéndose nítida.

El depósito (`pool`) no se toca: es el archivo del que sale un recorte nuevo si
alguna foto vuelve a usarse más grande.
"""
import base64, io, json, sys, time
from PIL import Image

CALIDAD = 80
RETINA  = 2.0
SUELO   = 96              # por debajo de esto no compensa afinar más

#  id / prefijo  →  ancho máximo medido en pantalla (px CSS)
VISTO = {
    "cara-":      46,
    "ig-":       294,
    "captura-":  338,
    "transfer-": 351,
    "vida-":     476,
    "foto-marcelo":   317,
    "foto-instagram": 253,
    "foto-escenario": 269,
}
TECHO = 760               # nada supera lo que ya había

def objetivo(clave_rec):
    visto = None
    for pref, px in VISTO.items():
        if clave_rec == pref or clave_rec.startswith(pref):
            visto = px; break
    if visto is None: return TECHO
    return min(TECHO, max(SUELO, round(visto * RETINA / 8) * 8))

def encoger(uri, ancho):
    if not (isinstance(uri, str) and uri.startswith("data:image")): return uri, 0
    try: crudo = base64.b64decode(uri.split(",", 1)[1])
    except Exception: return uri, 0
    try: im = Image.open(io.BytesIO(crudo))
    except Exception: return uri, 0
    if im.width <= ancho: return uri, 0            # nunca agrandar
    if im.mode not in ("RGB", "RGBA"): im = im.convert("RGB")
    im = im.resize((ancho, max(1, round(im.height * ancho / im.width))), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=CALIDAD, method=6)
    nuevo = buf.getvalue()
    if len(nuevo) >= len(crudo): return uri, 0
    return "data:image/webp;base64," + base64.b64encode(nuevo).decode(), len(crudo) - len(nuevo)

def main(ruta="estado.json", pagina="vsl"):
    e = json.load(io.open(ruta, encoding="utf-8"))
    rec = e["pags"][pagina]["recursos"]
    antes = sum(len(v) for v in rec.values() if str(v).startswith("data:")) * 0.75
    tocadas = 0
    for k, v in list(rec.items()):
        nueva, ahorro = encoger(v, objetivo(k))
        if ahorro:
            rec[k] = nueva; tocadas += 1
            print(f"  {k:32s} → {objetivo(k):3d} px  −{ahorro/1024:5.0f} KB")
    despues = sum(len(v) for v in rec.values() if str(v).startswith("data:")) * 0.75
    e["ts"] = int(time.time() * 1000)
    json.dump(e, io.open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n  {tocadas} imágenes recortadas")
    print(f"  recursos de «{pagina}»: {antes/1048576:.2f} → {despues/1048576:.2f} MB")

if __name__ == "__main__":
    main(*sys.argv[1:])
