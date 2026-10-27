"""Formato nuevo 2026-10-27: "orden de trabajo cumplida". Foto grande vertical a la izquierda (escalera
tipo avión con rack selectivo y piso epóxico), columna azul a la derecha con una orden de trabajo de
papel (borde dentado, ítems marcados y sello ENTREGADO) y debajo la foto del cantilever; pie de contactos.
Capa PNG 2x transparente en las 2 fotos. Fotos en Canva (Subidos, 2026-10-27):
  izquierda IMG-20261027-WA0028 (MAHZOd3GYd8, 3120x4160)
  derecha   IMG-20261027-WA0048 (MAHZOWCy8fo, 3120x4160, cantilever)"""
import os, sys
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
FOOT = 1110
XL = 640                                   # fin de la foto izquierda
FOTO_IZQ = (0, 0, XL, FOOT)
FOTO_DER = (XL + 22, 800, 1058, 1088)       # cantilever
PX0, PX1, PY0, PY1 = XL + 30, 1050, 34, 772  # papel de la orden
PAPEL = (252, 250, 244)
TINTA = (28, 32, 44)
ITEMS = ["Rack selectivo", "Escalera tipo avión", "Piso epóxico", "Cantilever"]


def check(d, x, y, s):
    d.rectangle([k(x), k(y), k(x + s), k(y + s)], outline=NAVY, width=k(3))
    d.line([(k(x + 6), k(y + s * 0.55)), (k(x + s * 0.42), k(y + s - 7)), (k(x + s + 6), k(y - 6))],
           fill=(22, 140, 70), width=k(6), joint="curve")


def sello(txt):
    f = B(30); w = int(rp.ancho(txt, f, k(4))) + k(44); h = k(66)
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    col = (200, 40, 40, 235)
    d.rounded_rectangle([k(2), k(2), w - k(2), h - k(2)], radius=k(8), outline=col, width=k(5))
    rp.espaciado(d, (k(22), k(12)), txt, f, col, k(4))
    return s.rotate(8, resample=Image.BICUBIC, expand=True)


def orden(c):
    w, h = k(PX1 - PX0), k(PY1 - PY0)
    p = Image.new("RGBA", (w, h + k(16)), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rectangle([0, 0, w, h], fill=PAPEL)
    z = k(16)                                  # borde dentado inferior
    pts = [(0, h)]
    for i in range(0, w + z, z):
        pts += [(i + z // 2, h + z), (i + z, h)]
    d.polygon(pts + [(w, h)], fill=PAPEL)
    x = k(26); y = k(26)
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(150)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    p.alpha_composite(lg, (x, y)); d = ImageDraw.Draw(p)
    y += lg.size[1] + k(16)
    rp.espaciado(d, (x, y), "ORDEN DE TRABAJO", B(22), NAVY, k(3)); y += k(36)
    for yy in (y, y + k(6)):
        d.line([(x, yy), (w - x, yy)], fill=TINTA, width=k(2) if yy == y else k(1))
    y += k(22)
    d.text((x, y), "Lo hicimos", font=B(46), fill=NAVY_D); y += k(56)
    d.text((x, y), "todo.", font=B(46), fill=NAVY_D)
    d.rectangle([x, y + k(50), x + k(120), y + k(57)], fill=GOLD); y += k(84)
    for it in ITEMS:
        check(d, x / S, y / S + 4, 30)
        d.text((x + k(48), y), it, font=B(29), fill=TINTA); y += k(54)
        d.line([(x, y - k(10)), (w - x, y - k(10))], fill=(210, 205, 195), width=k(1))
    y += k(4)
    d.text((x, y), "Una bodega completa,", font=M(24), fill=TINTA); y += k(32)
    d.text((x, y), "un solo proveedor.", font=M(24), fill=TINTA)
    s = sello("ENTREGADO"); p.alpha_composite(s, (w - s.size[0] - k(14), h - s.size[1] - k(20)))
    sombra = Image.new("RGBA", (w + k(60), h + k(80)), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rectangle([k(14), k(22), w + k(14), h + k(22)], fill=(0, 0, 0, 140))
    c.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(k(12))), (k(PX0) - k(14), k(PY0) - k(14)))
    c.alpha_composite(p, (k(PX0), k(PY0)))


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    # columna azul derecha, con hueco para la foto del cantilever
    d.rectangle([k(XL), 0, W, k(FOOT)], fill=NAVY_D)
    x0, y0, x1, y1 = FOTO_DER
    d.rectangle([k(x0), k(y0), k(x1), k(y1)], fill=(0, 0, 0, 0))
    d.rectangle([k(XL), 0, k(XL + 6), k(FOOT)], fill=GOLD)
    # rótulo del cantilever
    t = "CANTILEVER"; f = B(22); tw = rp.ancho(t, f, k(3))
    d.rectangle([k(x0), k(y1 - 46), k(x0 + 28) + tw, k(y1)], fill=NAVY_D)
    rp.espaciado(d, (k(x0 + 14), k(y1 - 38)), t, f, WHITE, k(3))
    orden(c); d = ImageDraw.Draw(c)
    # rótulo sobre la foto grande
    t = "ESCALERA TIPO AVIÓN · RACK · PISO EPÓXICO"; f = B(22); tw = rp.ancho(t, f, k(2))
    d.rectangle([k(24), k(FOOT - 70), k(52) + tw, k(FOOT - 24)], fill=NAVY_D)
    d.rectangle([k(24), k(FOOT - 70), k(30), k(FOOT - 24)], fill=GOLD)
    rp.espaciado(d, (k(42), k(FOOT - 62)), t, f, WHITE, k(2))
    # pie de contactos
    d.rectangle([0, k(FOOT), W, H], fill=NAVY_D)
    d.rectangle([0, k(FOOT), W, k(FOOT + 6)], fill=GOLD)
    d.text((W / 2, k(FOOT + 30)), "Racksa Ecuador  ·  Diseño, suministro e instalación a nivel nacional", font=B(26), fill=GOLD, anchor="ma")
    tel = "   ·   ".join(rp.TELS); ft = B(38); tw = d.textlength(tel, font=ft); yy = k(FOOT + 86)
    c.alpha_composite(rp._wa(k(38)), (int(W / 2 - tw / 2) - k(52), yy + k(6))); d = ImageDraw.Draw(c)
    d.text((W / 2 - tw / 2, yy), tel, font=ft, fill=WHITE); yy += k(70)
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


if __name__ == "__main__":
    cp = capa(); cp.save(os.path.join(O, "capa_orden.png"))
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    for (x0, y0, x1, y1), (f, cx, cy) in zip([FOTO_IZQ, FOTO_DER], [(sys.argv[1], 0.4, 0.5), (sys.argv[2], 0.5, 0.5)]):
        base.paste(llenar(Image.open(f).convert("RGB"), k(x1 - x0), k(y1 - y0), cx, cy), (k(x0), k(y0)))
    base.alpha_composite(cp)
    base.convert("RGB").resize((1080, 1350), Image.LANCZOS).save(os.path.join(O, "vista_previa_borrador.jpg"), quality=92)
    print("ok")
