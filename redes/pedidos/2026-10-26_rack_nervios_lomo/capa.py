"""Formato nuevo 2026-10-26: "lomo lateral". Franja vertical azul a la izquierda como lomo de catálogo,
con el logo y el titular girado 90°; a la derecha un collage de 3 fotos grandes (una horizontal arriba,
dos abajo) y pie de contactos a todo el ancho. Rack selectivo con nervios de soporte.
Capa PNG 2x, transparente en las 3 celdas. Fotos en Canva (Subidos, 2026-10-26):
  arriba     IMG-20261026-WA0022 (MAHZIMK02Sg, 1600x1200)
  abajo izq. IMG-20261026-WA0018 (MAHZIN9oHrQ, 716x1600)
  abajo der. IMG-20261026-WA0020 (MAHZIHqaMqo, 716x1600)"""
import os, sys
P = "/mnt/project-files/racksa_proyecto/publicidad"
O = os.path.dirname(os.path.abspath(__file__))
os.chdir(P); sys.path.insert(0, P)
import racksa_plantillas as rp
from racksa_plantillas import NAVY, NAVY_D, GOLD, WHITE
from PIL import Image, ImageDraw

S = 2
W, H = 1080 * S, 1350 * S
B = lambda t: rp.B(int(t * S)); M = lambda t: rp.M(int(t * S))
k = lambda v: int(round(v * S))

LOMO = 220                      # ancho del lomo
G = 12                          # separación entre fotos
FOOT = 1120                     # inicio del pie
X0 = LOMO + G
YM = 600                        # corte entre foto de arriba y fila de abajo
XM = X0 + (1080 - X0 - G) // 2  # corte entre las dos fotos de abajo
CELDAS = [(X0, 0, 1080, YM), (X0, YM + G, XM, FOOT), (XM + G, YM + G, 1080, FOOT)]


def girado(c, txt, f, col, cx, y_base, esp):
    """Texto girado 90° (se lee de abajo hacia arriba), centrado en cx y terminando en y_base."""
    w = int(rp.ancho(txt, f, esp)); h = int(f.size * 1.3)
    t = Image.new("RGBA", (w + k(4), h), (0, 0, 0, 0))
    rp.espaciado(ImageDraw.Draw(t), (0, 0), txt, f, col, esp)
    t = t.rotate(90, expand=True)
    c.alpha_composite(t, (int(cx - t.size[0] / 2), int(y_base - t.size[1])))


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    # separadores blancos entre fotos
    d.rectangle([k(LOMO), 0, k(X0), k(FOOT)], fill=WHITE)
    d.rectangle([k(X0), k(YM), W, k(YM + G)], fill=WHITE)
    d.rectangle([k(XM), k(YM), k(XM + G), k(FOOT)], fill=WHITE)
    # lomo
    d.rectangle([0, 0, k(LOMO), k(FOOT)], fill=NAVY)
    d.rectangle([k(LOMO - 8), 0, k(LOMO), k(FOOT)], fill=GOLD)
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(160)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    pad = k(12); bx, by = k(16), k(30)
    d.rectangle([bx, by, bx + lw + 2 * pad, by + lg.size[1] + 2 * pad], fill=WHITE)
    c.alpha_composite(lg, (bx + pad, by + pad))
    base = k(FOOT - 50)
    girado(c, "NERVIOS DE SOPORTE", B(64), GOLD, k(76), base, k(2))
    girado(c, "Tu carga, bien apoyada.", B(40), WHITE, k(150), base, 0)
    d = ImageDraw.Draw(c)
    # rótulo pequeño en la foto superior
    t = "RACK SELECTIVO"; f = B(24); tw = rp.ancho(t, f, k(3))
    d.rectangle([k(X0 + 24), k(26), k(X0 + 24 + 30) + tw, k(70)], fill=NAVY_D)
    rp.espaciado(d, (k(X0 + 39), k(34)), t, f, WHITE, k(3))
    # pie de contactos a todo el ancho
    d.rectangle([0, k(FOOT), W, H], fill=NAVY_D)
    d.rectangle([0, k(FOOT), W, k(FOOT + 6)], fill=GOLD)
    d.text((W / 2, k(FOOT + 34)), "Racksa Ecuador  ·  Diseño, suministro e instalación a nivel nacional",
           font=B(26), fill=GOLD, anchor="ma")
    tel = "   ·   ".join(rp.TELS); ft = B(38); tw = d.textlength(tel, font=ft); yy = k(FOOT + 88)
    c.alpha_composite(rp._wa(k(38)), (int(W / 2 - tw / 2) - k(52), yy + k(6))); d = ImageDraw.Draw(c)
    d.text((W / 2 - tw / 2, yy), tel, font=ft, fill=WHITE); yy += k(68)
    fm = M(26); items = [(rp._mail(k(28)), rp.MAIL), (rp._web(k(26)), rp.WEB)]
    gap = k(40); anchos = [ic.size[0] + k(10) + d.textlength(t, font=fm) for ic, t in items]
    x = W / 2 - (sum(anchos) + gap) / 2
    for (ic, t), a in zip(items, anchos):
        c.alpha_composite(ic, (int(x), yy + k(9))); d = ImageDraw.Draw(c)
        d.text((x + ic.size[0] + k(10), yy), t, font=fm, fill=WHITE); x += a + gap
    return c


def llenar(im, w, h, cx=0.5, cy=0.5):
    s = max(w / im.size[0], h / im.size[1]); im = im.resize((int(im.size[0] * s) + 1, int(im.size[1] * s) + 1), Image.LANCZOS)
    x = int((im.size[0] - w) * cx); y = int((im.size[1] - h) * cy)
    return im.crop((x, y, x + w, y + h))


def preview(cp, fotos):
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    for (x0, y0, x1, y1), (f, cx, cy) in zip(CELDAS, fotos):
        base.paste(llenar(Image.open(f).convert("RGB"), k(x1 - x0), k(y1 - y0), cx, cy), (k(x0), k(y0)))
    base.alpha_composite(cp)
    return base.convert("RGB").resize((1080, 1350), Image.LANCZOS)


if __name__ == "__main__":
    cp = capa(); cp.save(os.path.join(O, "capa_lomo.png"))
    print("celdas", CELDAS)
    fotos = [(sys.argv[1], 0.5, 0.3), (sys.argv[2], 0.5, 0.5), (sys.argv[3], 0.5, 0.5)]
    preview(cp, fotos).save(os.path.join(O, "vista_previa_borrador.jpg"), quality=92)
    print("ok")
