"""Formato nuevo 'portada de revista' (2026-10-24). Capa PNG transparente a 2x (2160x2700)
para poner encima de la foto en Canva y exportar nítido. Uso: python3 capa.py"""
import os, sys, glob
P = "/mnt/project-files/racksa_proyecto/publicidad"
O = os.path.dirname(os.path.abspath(__file__))
os.chdir(P); sys.path.insert(0, P)
import racksa_plantillas as rp
from racksa_plantillas import NAVY, NAVY_D, GOLD, RED, WHITE
from PIL import Image, ImageDraw, ImageFilter

S = 2
W, H = 1080 * S, 1350 * S
B = lambda t: rp.B(int(t * S)); M = lambda t: rp.M(int(t * S))
k = lambda v: int(v * S)
INK = (14, 27, 48)


def grad(w, h, a0, a1, horiz=False, p=1.0, col=NAVY_D):
    g = Image.new("L", (w if horiz else 1, 1 if horiz else h))
    n = w if horiz else h
    for i in range(n):
        t = (i / (n - 1)) ** p
        g.putpixel((i, 0) if horiz else (0, i), int(a0 + (a1 - a0) * t))
    g = g.resize((w, h))
    im = Image.new("RGBA", (w, h), col + (0,)); im.putalpha(g); return im


def txt(c, xy, t, f, col, sh=True, anchor="la", tr=0):
    if sh:
        s = Image.new("RGBA", c.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(s)
        if tr: rp.espaciado(ds, (xy[0] + k(2), xy[1] + k(4)), t, f, (0, 0, 0, 190), k(tr))
        else: ds.text((xy[0] + k(2), xy[1] + k(4)), t, font=f, fill=(0, 0, 0, 190), anchor=anchor)
        c.alpha_composite(s.filter(ImageFilter.GaussianBlur(k(6))))
    d = ImageDraw.Draw(c)
    if tr: rp.espaciado(d, xy, t, f, col, k(tr))
    else: d.text(xy, t, font=f, fill=col, anchor=anchor)


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c.alpha_composite(grad(W, k(420), 215, 0, p=0.9), (0, 0))            # arriba: cabecera
    c.alpha_composite(grad(k(700), H, 175, 0, horiz=True, p=1.3), (0, 0))  # izquierda: titulares
    c.alpha_composite(grad(W, k(560), 0, 240, p=1.1), (0, H - k(150) - k(560)))  # abajo
    d = ImageDraw.Draw(c)
    # franja superior de revista
    txt(c, (k(44), k(30)), "N.º 01  ·  OCTUBRE 2026", B(22), WHITE, tr=2)
    t = "COBERTURA NACIONAL"; f = B(22)
    txt(c, (W - k(44) - rp.ancho(t, f, k(2)), k(30)), t, f, GOLD, tr=2)
    # cabecera (masthead)
    txt(c, (k(36), k(48)), "RACKSA", B(228), WHITE)
    d = ImageDraw.Draw(c)
    d.rectangle([k(44), k(318), W - k(44), k(318) + k(5)], fill=GOLD)
    txt(c, (k(44), k(332)), "LA REVISTA DE LAS BODEGAS QUE CRECEN", B(24), WHITE, tr=3)
    # titulares de portada (columna izquierda)
    y = k(420)
    bloques = [("ESPECIAL", "Rack selectivo", "a la medida de tu carga"),
               ("EN STOCK", "Entrega inmediata", "contamos con el stock"),
               ("SERVICIO", "Montaje en sitio", "en todo el Ecuador")]
    for tag, t1, t2 in bloques:
        d = ImageDraw.Draw(c)
        f = B(20); tw = rp.ancho(tag, f, k(2))
        d.rectangle([k(44), y, k(44) + tw + k(24), y + k(36)], fill=GOLD)
        rp.espaciado(d, (k(56), y + k(5)), tag, f, INK, k(2))
        txt(c, (k(44), y + k(44)), t1, B(46), WHITE)
        txt(c, (k(46), y + k(104)), t2, M(28), WHITE)
        y += k(172)
    # titular principal abajo
    yb = H - k(150) - k(232)
    txt(c, (k(42), yb), "Tu bodega,", B(90), WHITE)
    txt(c, (k(42), yb + k(100)), "en orden.", B(90), GOLD)
    # sello con logo (como etiqueta de precio de portada)
    cx, cy, r = W - k(170), yb + k(95), k(128)
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).ellipse([cx - r, cy - r + k(10), cx + r, cy + r + k(10)], fill=(0, 0, 0, 120))
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(k(12))))
    d = ImageDraw.Draw(c)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    d.ellipse([cx - r + k(10), cy - r + k(10), cx + r - k(10), cy + r - k(10)], outline=GOLD, width=k(5))
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(200)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    c.alpha_composite(lg, (cx - lw // 2, cy - lg.size[1] // 2 - k(20)))
    d = ImageDraw.Draw(c)
    f = B(19); t = "AGENDA TU VISITA"; d.text((cx, cy + k(52)), t, font=f, fill=NAVY_D, anchor="mm")
    # pie con contactos
    y0 = H - k(150)
    d.rectangle([0, y0, W, H], fill=NAVY_D)
    d.rectangle([0, y0, int(W * .6), y0 + k(8)], fill=NAVY)
    d.rectangle([int(W * .6), y0, int(W * .85), y0 + k(8)], fill=GOLD)
    d.rectangle([int(W * .85), y0, W, y0 + k(8)], fill=RED)
    tel = "   ·   ".join(rp.TELS); ft = B(37); tw = d.textlength(tel, font=ft); y = y0 + k(32)
    c.alpha_composite(rp._wa(k(38)), (int(W / 2 - tw / 2) - k(52), y + k(6))); d = ImageDraw.Draw(c)
    d.text((W / 2 - tw / 2, y), tel, font=ft, fill=WHITE); y += k(60)
    fm = M(26); items = [(rp._mail(k(25)), rp.MAIL), (rp._web(k(25)), rp.WEB)]
    tot = sum(d.textlength(t, font=fm) + k(36) for _, t in items) + k(50); x = W / 2 - tot / 2
    for icon, t in items:
        c.alpha_composite(icon, (int(x), y + k(8))); d = ImageDraw.Draw(c)
        d.text((x + k(36), y), t, font=fm, fill=WHITE); x += k(36) + d.textlength(t, font=fm) + k(50)
    c.save(O + "/capa_portada.png", optimize=True)
    return c


if __name__ == "__main__":
    c = capa()
    foto = Image.open(glob.glob(P + "/banco/1u8eqLLmkr*.jpg")[0]).convert("RGB")
    v = Image.new("RGBA", (W, H)); v.paste(rp.cover(foto, W, H, .5), (0, 0)); v.alpha_composite(c)
    v.convert("RGB").resize((1080, 1350), Image.LANCZOS).save("/tmp/claude-0/cv/portada.jpg", quality=90)
    print("ok", os.path.getsize(O + "/capa_portada.png"))
