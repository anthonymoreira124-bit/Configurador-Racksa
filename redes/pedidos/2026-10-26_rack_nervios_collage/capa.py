"""Formato nuevo 2026-10-26: "collage dentro del rack". El diseño ES un rack: puntales azules perforados
separan tres fotos verticales grandes, viga naranja arriba y viga inferior con el rótulo; textos arriba
en panel blanco sobrio y contactos abajo. Rack selectivo con nervios de soporte.
Capa PNG 2x, transparente en las 3 celdas. Fotos en Canva (Subidos, 2026-10-26):
  celda 1 IMG-20261026-WA0018 (MAHZIN9oHrQ, 716x1600)
  celda 2 IMG-20261026-WA0022 (MAHZIMK02Sg, 1600x1200, recorte vertical)
  celda 3 IMG-20261026-WA0020 (MAHZIHqaMqo, 716x1600)"""
import os, sys
P = "/mnt/project-files/racksa_proyecto/publicidad"
O = os.path.dirname(os.path.abspath(__file__))
os.chdir(P); sys.path.insert(0, P)
import racksa_plantillas as rp
from racksa_plantillas import NAVY, NAVY_D, GOLD, RED, WHITE
from PIL import Image, ImageDraw

S = 2
W, H = 1080 * S, 1350 * S
B = lambda t: rp.B(int(t * S)); M = lambda t: rp.M(int(t * S))
k = lambda v: int(round(v * S))

U = 22                                  # ancho de puntal
TOP = 270                               # inicio de la viga superior
VS = 30                                 # alto viga superior
Y0, Y1 = TOP + VS, 1040                 # celdas de fotos
VI = 70                                 # alto viga inferior
FOOT = Y1 + VI                          # inicio del pie de contactos
PX = [0, 353, 705, 1058]                # x de cada puntal
CELDAS = [(PX[i] + U, Y0, PX[i + 1], Y1) for i in range(3)]
ETIQ = [("01", "Soporte para pallets"), ("02", "Para carga pesada"), ("03", "Instalados por Racksa")]
NAV = (15, 76, 157)


def puntal(d, x):
    d.rectangle([k(x), k(TOP), k(x + U), k(Y1 + VI)], fill=NAV)
    d.rectangle([k(x + U - 4), k(TOP), k(x + U), k(Y1 + VI)], fill=(10, 56, 120))     # canto en sombra
    y = TOP + 40
    while y < Y1 + VI - 30:                                                           # perforaciones
        d.rounded_rectangle([k(x + 8), k(y), k(x + 14), k(y + 14)], radius=k(2), fill=NAVY_D)
        y += 34


def viga(d, y0, h):
    d.rectangle([0, k(y0), W, k(y0 + h)], fill=RED)
    d.rectangle([0, k(y0 + h - 5), W, k(y0 + h)], fill=(176, 50, 28))                # canto inferior


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    # panel superior blanco
    d.rectangle([0, 0, W, k(TOP)], fill=WHITE)
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(190)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    c.alpha_composite(lg, (k(44), k(34))); d = ImageDraw.Draw(c)
    t = "RACK SELECTIVO"; f = B(24); tx = k(1036) - rp.ancho(t, f, k(3)); ty = k(48)
    d.rectangle([tx - k(26), ty + k(6), tx - k(14), ty + k(26)], fill=GOLD)
    rp.espaciado(d, (tx, ty), t, f, NAVY, k(3))
    d.text((k(44), k(118)), "Nervios de soporte:", font=B(60), fill=NAVY_D)
    l2 = "tu carga, bien apoyada."; f2 = B(60)
    w2 = d.textlength(l2, font=f2)
    d.rectangle([k(44), k(206), k(44) + w2, k(230)], fill=GOLD)                        # subrayado dorado
    d.text((k(44), k(178)), l2, font=f2, fill=NAVY_D)
    # celdas: degradado inferior suave para la etiqueta
    for (x0, y0, x1, y1) in CELDAS:
        g = Image.new("RGBA", (k(x1 - x0), k(170)), (6, 18, 40, 0))
        for i in range(g.size[1]):
            a = int(200 * (i / g.size[1]) ** 1.6)
            ImageDraw.Draw(g).line([(0, i), (g.size[0], i)], fill=(6, 18, 40, a))
        c.alpha_composite(g, (k(x0), k(y1 - 170)))
    d = ImageDraw.Draw(c)
    # estructura del rack
    for x in PX:
        puntal(d, x)
    viga(d, TOP, VS)                    # las vigas van delante de los puntales
    viga(d, Y1, VI)
    # etiquetas por celda
    for (x0, y0, x1, y1), (n, txt) in zip(CELDAS, ETIQ):
        d.text((k(x0 + 18), k(y1 - 104)), n, font=B(34), fill=GOLD)
        palabras = txt.split(" "); mitad = (len(palabras) + 1) // 2
        lineas = [" ".join(palabras[:mitad]), " ".join(palabras[mitad:])]
        d.text((k(x0 + 76), k(y1 - 106)), lineas[0], font=B(27), fill=WHITE)
        d.text((k(x0 + 76), k(y1 - 72)), lineas[1], font=B(27), fill=WHITE)
    # rótulo sobre la viga inferior
    t = "DISEÑO · SUMINISTRO · INSTALACIÓN"; f = B(30)
    rp.espaciado(d, (W / 2 - rp.ancho(t, f, k(4)) / 2, k(Y1 + 15)), t, f, WHITE, k(4))
    # pie de contactos
    d.rectangle([0, k(FOOT), W, H], fill=NAVY_D)
    d.text((W / 2, k(FOOT + 30)), "Racksa Ecuador  ·  Cobertura a nivel nacional", font=B(28), fill=GOLD, anchor="ma")
    tel = "   ·   ".join(rp.TELS); ft = B(36); tw = d.textlength(tel, font=ft); yy = k(FOOT + 88)
    c.alpha_composite(rp._wa(k(36)), (int(W / 2 - tw / 2) - k(50), yy + k(6))); d = ImageDraw.Draw(c)
    d.text((W / 2 - tw / 2, yy), tel, font=ft, fill=WHITE); yy += k(70)
    fm = M(26); items = [(rp._mail(k(28)), rp.MAIL), (rp._web(k(26)), rp.WEB)]
    gap = k(40); anchos = [ic.size[0] + k(10) + d.textlength(t, font=fm) for ic, t in items]
    x = W / 2 - (sum(anchos) + gap) / 2
    for (ic, t), a in zip(items, anchos):
        c.alpha_composite(ic, (int(x), yy + k(9))); d = ImageDraw.Draw(c)
        d.text((x + ic.size[0] + k(10), yy), t, font=fm, fill=WHITE); x += a + gap
    return c


def llenar(im, w, h, cx=0.5):
    s = max(w / im.size[0], h / im.size[1]); im = im.resize((int(im.size[0] * s) + 1, int(im.size[1] * s) + 1), Image.LANCZOS)
    x = int((im.size[0] - w) * cx); y = (im.size[1] - h) // 2
    return im.crop((x, y, x + w, y + h))


def preview(cp, fotos):
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    for (x0, y0, x1, y1), (f, cx) in zip(CELDAS, fotos):
        base.paste(llenar(Image.open(f).convert("RGB"), k(x1 - x0), k(y1 - y0), cx), (k(x0), k(y0)))
    base.alpha_composite(cp)
    return base.convert("RGB").resize((1080, 1350), Image.LANCZOS)


if __name__ == "__main__":
    cp = capa(); cp.save(os.path.join(O, "capa_collage.png"))
    fotos = [(sys.argv[1], 0.5), (sys.argv[2], 0.3), (sys.argv[3], 0.5)]
    preview(cp, fotos).save(os.path.join(O, "vista_previa_borrador.jpg"), quality=92)
    print("ok")
