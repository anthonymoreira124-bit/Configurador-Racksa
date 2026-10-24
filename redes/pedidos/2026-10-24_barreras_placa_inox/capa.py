"""Formato nuevo 'placa de datos en acero inoxidable' para barreras contra inundación, 2026-10-24.
Capa PNG 2x (2160x2700) para Canva: hueco arriba para la foto, placa de acero cepillado con
tornillos y texto grabado abajo. Foto en Canva: IMG-20261022-WA0090 (MAHY9sRiCEM), 3120x4160.
Colocar foto 1080x1440 en (0,-430). Uso: python3 capa.py"""
import os, sys
import numpy as np
P = "/mnt/project-files/racksa_proyecto/publicidad"
O = os.path.dirname(os.path.abspath(__file__))
os.chdir(P); sys.path.insert(0, P)
import racksa_plantillas as rp
from racksa_plantillas import NAVY, NAVY_D, GOLD, RED, WHITE
from PIL import Image, ImageDraw, ImageFilter

S = 2
W, H = 1080 * S, 1350 * S
B = lambda t: rp.B(int(t * S)); M = lambda t: rp.M(int(t * S))
k = lambda v: int(round(v * S))
GRAFITO = (24, 29, 37); INK = (34, 40, 50); GRAB = (70, 78, 90)
PX0, PY0, PX1, PY1 = 50, 700, 1030, 1172  # placa (1x)


def grad(w, h, a0, a1, p=1.0, col=NAVY_D):
    g = Image.new("L", (1, h))
    for i in range(h):
        g.putpixel((0, i), int(a0 + (a1 - a0) * (i / (h - 1)) ** p))
    im = Image.new("RGBA", (w, h), col + (0,)); im.putalpha(g.resize((w, h))); return im


def txt(c, xy, t, f, col, blur=6, **kw):
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).text((xy[0] + k(2), xy[1] + k(4)), t, font=f, fill=(0, 0, 0, 190), **kw)
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(k(blur))))
    ImageDraw.Draw(c).text(xy, t, font=f, fill=col, **kw)


def grabado(d, xy, t, f, col=INK, **kw):
    """Texto grabado: brillo debajo, tinta oscura encima."""
    d.text((xy[0], xy[1] + k(2)), t, font=f, fill=(255, 255, 255, 170), **kw)
    d.text((xy[0], xy[1] - k(1)), t, font=f, fill=(0, 0, 0, 90), **kw)
    d.text(xy, t, font=f, fill=col, **kw)


def acero(w, h):
    rng = np.random.default_rng(7)
    n = rng.normal(0, 1, (h, w // 60 + 1))
    n = np.array(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR), float)
    fine = rng.normal(0, 1, (h, w)); fine = np.array(Image.fromarray(((fine + 4) * 32).clip(0, 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(0)).resize((w // 25, h)).resize((w, h), Image.BILINEAR), float)
    y = np.linspace(0, 1, h)[:, None]; x = np.linspace(0, 1, w)[None, :]
    base = 196 - 22 * y + 18 * np.exp(-((x - .3 - .4 * y) ** 2) / .03)  # brillo diagonal
    v = base + (n - 128) * .10 + (fine - 128) * .12
    rgb = np.stack([v - 4, v, v + 6], -1).clip(0, 255).astype(np.uint8)
    return Image.fromarray(rgb, "RGB").convert("RGBA")


def tornillo(c, cx, cy, r):
    d = ImageDraw.Draw(c)
    d.ellipse([cx - r - k(2), cy - r + k(1), cx + r + k(2), cy + r + k(4)], fill=(0, 0, 0, 70))
    g = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for i in range(r, 0, -1):
        v = int(150 + 80 * (1 - i / r))
        gd.ellipse([r - i - int(r * .25 * (1 - i / r)), r - i - int(r * .25 * (1 - i / r)), r + i, r + i], fill=(v, v, v + 5, 255))
    c.alpha_composite(g, (cx - r, cy - r)); d = ImageDraw.Draw(c)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(110, 116, 124), width=k(1))
    a = int(r * .6)
    d.line([(cx - a, cy - a), (cx + a, cy + a)], fill=(80, 86, 94), width=k(3))
    d.line([(cx - a, cy + a), (cx + a, cy - a)], fill=(80, 86, 94), width=k(3))


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rectangle([0, k(PY0 + 40), W, H], fill=GRAFITO)
    c.alpha_composite(grad(W, k(110), 0, 255, 1.0, GRAFITO), (0, k(PY0 - 70)))
    c.alpha_composite(grad(W, k(400), 230, 0, 1.0), (0, 0))
    # cabecera sobre la foto
    f = B(21); t = "USO INDUSTRIAL"; tw = rp.ancho(t, f, k(3)) + k(52)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([k(48), k(46), k(48) + tw, k(98)], k(26), fill=GOLD)
    rp.espaciado(d, (k(48) + k(26), k(58)), t, f, NAVY_D, k(3))
    txt(c, (k(46), k(124)), "Que el agua", B(92), WHITE)
    txt(c, (k(46), k(232)), "no frene tu operación.", B(64), GOLD)
    # placa de acero cepillado
    box = [k(PX0), k(PY0), k(PX1), k(PY1)]; r = k(18)
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([box[0], box[1] + k(14), box[2], box[3] + k(14)], r, fill=(0, 0, 0, 170))
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(k(18))))
    pl = acero(box[2] - box[0], box[3] - box[1])
    mk = Image.new("L", pl.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, pl.size[0] - 1, pl.size[1] - 1], r, fill=255)
    c.paste(pl, (box[0], box[1]), mk); d = ImageDraw.Draw(c)
    d.rounded_rectangle(box, r, outline=(235, 238, 242), width=k(2))
    d.rounded_rectangle([box[0] + k(3), box[1] + k(3), box[2] - k(3), box[3] - k(3)], r - k(3), outline=(120, 126, 134), width=k(1))
    # marco grabado interior
    m = 34
    d.rounded_rectangle([k(PX0 + m), k(PY0 + m), k(PX1 - m), k(PY1 - m)], k(8), outline=(255, 255, 255, 150), width=k(2))
    d.rounded_rectangle([k(PX0 + m), k(PY0 + m) - k(2), k(PX1 - m), k(PY1 - m) - k(2)], k(8), outline=(96, 104, 114), width=k(2))
    for cx, cy in [(PX0 + 17, PY0 + 17), (PX1 - 17, PY0 + 17), (PX0 + 17, PY1 - 17), (PX1 - 17, PY1 - 17)]:
        tornillo(c, k(cx), k(cy), k(10))
    d = ImageDraw.Draw(c)
    # logo en sello blanco
    X = PX0 + 62; y = PY0 + 54
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(205)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    lh = lg.size[1]
    d.rounded_rectangle([k(X) - k(16), k(y) - k(10), k(X) + lw + k(16), k(y) + lh + k(10)], k(12), fill=(255, 255, 255, 235))
    c.alpha_composite(lg, (k(X), k(y))); d = ImageDraw.Draw(c)
    yc = k(y) + lh // 2
    grabado(d, (k(PX1 - 62), yc - k(16)), "ACERO INOXIDABLE", B(26), GRAB, anchor="ra")
    grabado(d, (k(PX1 - 62), yc + k(16)), "Hecho por Racksa Ecuador", M(20), GRAB, anchor="ra")
    y = k(y) + lh + k(20)
    grabado(d, (k(X - 2), y), "BARRERA CONTRA INUNDACIÓN", B(48), INK); y += k(64)
    d.line([(k(X), y), (k(PX1 - 62), y)], fill=(255, 255, 255, 170), width=k(2))
    d.line([(k(X), y - k(2)), (k(PX1 - 62), y - k(2))], fill=(100, 108, 118), width=k(2)); y += k(12)
    filas = [("MATERIAL", "Acero inoxidable"), ("APLICACIÓN", "Bodegas, locales, oficinas y cajeros"),
             ("INSTALACIÓN", "En sitio con nuestro equipo"), ("COBERTURA", "Nacional")]
    for lab, val in filas:
        grabado(d, (k(X), y + k(8)), lab, B(21), GRAB)
        grabado(d, (k(X + 205), y), val, B(31), INK)
        y += k(49)
    # pie
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
    c.save(O + "/capa_placa.png", optimize=True)
    return c


if __name__ == "__main__":
    c = capa()
    foto = Image.open(P + "/banco/hearth_7d2ebea1_barrera_instalada.jpg").convert("RGB")
    v = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    v.paste(foto.resize((W, k(1440)), Image.LANCZOS), (0, -k(430))); v.alpha_composite(c)
    v.convert("RGB").resize((1080, 1350), Image.LANCZOS).save("/tmp/claude-0/cv/placa.jpg", quality=90)
    print("ok")
