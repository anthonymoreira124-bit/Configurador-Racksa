"""Formato nuevo 'regla de nivel de agua' para barreras contra inundación, 2026-10-24.
Capa PNG 2x (2160x2700) para Canva: foto a página completa, regla limnimétrica a la derecha,
línea de nivel en el borde superior de la barrera y agua translúcida abajo.
Foto en Canva: IMG-20261022-WA0089 (MAHY9nvv0h8), 3120x4160. Colocar foto 1080x1440 en (0,-120).
Uso: python3 capa.py"""
import os, sys, math
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
FOTO_T = -120
NIVEL = 686            # borde superior de la barrera en la página (1x)
GX0, GX1, GY0, GY1 = 952, 1032, 300, 1200   # regla (1x)
AGUA = (24, 120, 190)


def grad(w, h, a0, a1, p=1.0, col=NAVY_D):
    g = Image.new("L", (1, h))
    for i in range(h):
        g.putpixel((0, i), int(a0 + (a1 - a0) * (i / (h - 1)) ** p))
    im = Image.new("RGBA", (w, h), col + (0,)); im.putalpha(g.resize((w, h))); return im


def txt(c, xy, t, f, col, blur=6, **kw):
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).text((xy[0] + k(2), xy[1] + k(4)), t, font=f, fill=(0, 0, 0, 200), **kw)
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(k(blur))))
    ImageDraw.Draw(c).text(xy, t, font=f, fill=col, **kw)


def sombra(c, box, r, blur=14, a=110, dy=6):
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([box[0], box[1] + dy, box[2], box[3] + dy], r, fill=(0, 0, 0, a))
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))


def regla(c):
    box = (k(GX0), k(GY0), k(GX1), k(GY1))
    sombra(c, box, k(6), k(12), 120, k(6))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle(box, k(6), fill=(250, 250, 246))
    # franja de alerta a la derecha: rojo arriba, amarillo, verde abajo
    zx0 = k(GX1 - 16)
    d.rectangle([zx0, k(GY0 + 6), k(GX1) - k(1), k(GY1)], fill=NAVY)
    # patrón tipo "E" de regla limnimétrica
    y = GY0 + 24
    while y + 50 <= GY1:
        for j in range(3):
            yy = y + j * 20
            d.rectangle([k(GX0 + 12), k(yy), k(GX0 + 50), k(yy + 8)], fill=(20, 24, 30))
        d.rectangle([k(GX0 + 12), k(y), k(GX0 + 20), k(y + 48)], fill=(20, 24, 30))
        y += 80
    d.rounded_rectangle(box, k(6), outline=(160, 165, 172), width=k(2))


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c.alpha_composite(grad(W, k(420), 235, 0, 1.1), (0, 0))
    regla(c)
    # agua translúcida al pie de la barrera
    ya = 1080
    agua = Image.new("RGBA", (W, H), (0, 0, 0, 0)); da = ImageDraw.Draw(agua)
    pts = [(0, H)]
    for x in range(0, W + 1, k(6)):
        pts.append((x, k(ya) + k(10) * math.sin(x / k(46)) + k(5) * math.sin(x / k(17))))
    pts.append((W, H)); da.polygon(pts, fill=AGUA + (215,))
    for x in range(0, W, k(4)):
        y = k(ya) + k(10) * math.sin(x / k(46)) + k(5) * math.sin(x / k(17))
        da.ellipse([x - k(3), y - k(3), x + k(3), y + k(3)], fill=(200, 235, 255, 200))
    c.alpha_composite(agua)
    c.alpha_composite(grad(W, k(130), 0, 120, 1.0, (6, 40, 80)), (0, k(1080)))
    # logo en tarjeta blanca arriba a la derecha
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(220)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS); lh = lg.size[1]
    bx = (W - k(40) - lw - k(40), k(40), W - k(40), k(40) + lh + k(32))
    sombra(c, bx, k(16)); d = ImageDraw.Draw(c)
    d.rounded_rectangle(bx, k(16), fill=WHITE)
    c.alpha_composite(lg, (bx[0] + k(20), bx[1] + k(16)))
    # titular
    txt(c, (k(44), k(40)), "Barreras contra", B(76), WHITE)
    txt(c, (k(44), k(126)), "inundación", B(76), WHITE)
    txt(c, (k(46), k(226)), "Acero inoxidable  ·  Uso industrial", B(34), GOLD)
    d = ImageDraw.Draw(c)
    # línea de nivel en el borde de la barrera
    y = k(NIVEL)
    x = k(40)
    while x < k(GX0 - 30):
        d.line([(x, y), (x + k(22), y)], fill=GOLD, width=k(5)); x += k(36)
    d.polygon([(k(GX0 - 4), y), (k(GX0 - 30), y - k(16)), (k(GX0 - 30), y + k(16))], fill=GOLD)
    f = B(25); t = "EL AGUA SE QUEDA AFUERA"; tw = rp.ancho(t, f, k(2)) + k(48)
    pb = (k(40), y - k(72), k(40) + tw, y - k(20))
    sombra(c, pb, k(26)); d = ImageDraw.Draw(c)
    d.rounded_rectangle(pb, k(26), fill=NAVY_D)
    rp.espaciado(d, (pb[0] + k(24), pb[1] + k(11)), t, f, GOLD, k(2))
    # beneficios sobre el agua
    t = "Acero inoxidable  ·  Instalación en sitio  ·  Cobertura nacional"
    txt(c, (k(484), k(1146)), t, B(26), WHITE, 4, anchor="mm")
    # pie
    y0 = H - k(150)
    d = ImageDraw.Draw(c)
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
    c.save(O + "/capa_regla.png", optimize=True)
    return c


if __name__ == "__main__":
    c = capa()
    foto = Image.open(P + "/banco/hearth_83692942_barrera_instalando.jpg").convert("RGB")
    v = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    v.paste(foto.resize((W, k(1440)), Image.LANCZOS), (0, k(FOTO_T))); v.alpha_composite(c)
    v.convert("RGB").resize((1080, 1350), Image.LANCZOS).save("/tmp/claude-0/cv/regla.jpg", quality=90)
    print("ok")
