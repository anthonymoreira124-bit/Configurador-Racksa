"""Formato nuevo 2026-10-25: "cartel de pelea" (MONTACARGAS vs TU RACK) para protectores de columna.
Capa PNG 2x (2160x2700), transparente donde va la foto. Foto en Canva: IMG-20260601-WA0133 (MAHY9aUAfbA),
1536x2048 -> colocar a 1080x1440 en (0, FOTO_T). Uso: python3 capa.py"""
import os, sys, math
P = "/mnt/project-files/racksa_proyecto/publicidad"
O = os.path.dirname(os.path.abspath(__file__))
os.chdir(P); sys.path.insert(0, P)
import racksa_plantillas as rp
from racksa_plantillas import NAVY, NAVY_D, GOLD, RED, WHITE
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(P, "redes/pedidos/2026-10-25_acta_y_boleto"))

S = 2
W, H = 1080 * S, 1350 * S
B = lambda t: rp.B(int(t * S)); M = lambda t: rp.M(int(t * S))
k = lambda v: int(round(v * S))
FOTO = "banco/1FP7a3aNZHDQ80CNIT55gB-qF1zcFqjp3.jpg"
FOTO_T = -470
CORTE = 790


def sombra(c, box, r, blur=16, a=120, dy=8):
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([box[0], box[1] + k(dy), box[2], box[3] + k(dy)], r, fill=(0, 0, 0, a))
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(k(blur))))


def logo_tarjeta(c, x=40, y=40, w=230):
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(w)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    pad = k(18); box = (k(x), k(y), k(x) + lw + 2 * pad, k(y) + lg.size[1] + 2 * pad)
    sombra(c, box, k(14), 12, 110, 4)
    ImageDraw.Draw(c).rounded_rectangle(box, k(14), fill=WHITE)
    c.alpha_composite(lg, (box[0] + pad, box[1] + pad))


def pie(c, y0):
    d = ImageDraw.Draw(c)
    d.rectangle([0, k(y0), W, H], fill=NAVY_D)
    d.rectangle([0, k(y0), int(W * .6), k(y0 + 8)], fill=NAVY)
    d.rectangle([int(W * .6), k(y0), int(W * .85), k(y0 + 8)], fill=GOLD)
    d.rectangle([int(W * .85), k(y0), W, k(y0 + 8)], fill=RED)
    tel = "   ·   ".join(rp.TELS); ft = B(36); tw = d.textlength(tel, font=ft); y = k(y0 + 34)
    c.alpha_composite(rp._wa(k(38)), (int(W / 2 - tw / 2) - k(52), y + k(6))); d = ImageDraw.Draw(c)
    d.text((W / 2 - tw / 2, y), tel, font=ft, fill=WHITE); y += k(62)
    fm = M(26); items = [(rp._mail(k(28)), rp.MAIL), (rp._web(k(26)), rp.WEB)]
    gap = k(44); anchos = [ic.size[0] + k(10) + d.textlength(t, font=fm) for ic, t in items]
    x = W / 2 - (sum(anchos) + gap) / 2
    for (ic, t), a in zip(items, anchos):
        c.alpha_composite(ic, (int(x), y + k(10))); d = ImageDraw.Draw(c)
        d.text((x + ic.size[0] + k(10), y), t, font=fm, fill=WHITE); x += a + gap


def estrella(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2; a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def insignia(c, cx, cy, r=118):
    """Medalla dorada 'CAMPEÓN' estilo cinturón."""
    s = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.ellipse([k(cx - r), k(cy - r + 10), k(cx + r), k(cy + r + 10)], fill=(0, 0, 0, 140))
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(k(12))))
    d = ImageDraw.Draw(c)
    d.ellipse([k(cx - r), k(cy - r), k(cx + r), k(cy + r)], fill=GOLD, outline=NAVY_D, width=k(6))
    d.ellipse([k(cx - r + 16), k(cy - r + 16), k(cx + r - 16), k(cy + r - 16)], outline=NAVY_D, width=k(3))
    d.polygon([(k(x), k(y)) for x, y in estrella(cx, cy - 52, 22, 9)], fill=RED)
    d.text((k(cx), k(cy + 2)), "CAMPEÓN", font=B(31), fill=NAVY_D, anchor="mm")
    d.text((k(cx), k(cy + 40)), "DE LA BODEGA", font=B(19), fill=NAVY_D, anchor="mm")


def cartel(c, y0, y1):
    d = ImageDraw.Draw(c)
    d.rectangle([0, k(y0), W, k(y1)], fill=NAVY)
    # rayos sutiles desde el VS
    rays = Image.new("RGBA", c.size, (0, 0, 0, 0)); rd = ImageDraw.Draw(rays)
    cx, cy = 540, y0 + 150
    for i in range(24):
        a0 = math.radians(i * 15); a1 = math.radians(i * 15 + 6)
        rd.polygon([(k(cx), k(cy)), (k(cx + 900 * math.cos(a0)), k(cy + 900 * math.sin(a0))),
                    (k(cx + 900 * math.cos(a1)), k(cy + 900 * math.sin(a1)))], fill=(255, 255, 255, 16))
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rectangle([0, k(y0), W, k(y1)], fill=255)
    rays.putalpha(Image.composite(rays.split()[3], Image.new("L", c.size, 0), m))
    c.alpha_composite(rays); d = ImageDraw.Draw(c)
    # cinta superior
    t = "LA PELEA DE TODOS LOS DÍAS"; f = B(26); tw = rp.ancho(t, f, k(4)) + k(60)
    d.rectangle([W / 2 - tw / 2, k(y0 - 26), W / 2 + tw / 2, k(y0 + 30)], fill=RED)
    rp.espaciado(d, (W / 2 - tw / 2 + k(30), k(y0 - 14)), t, f, WHITE, k(4))
    # MONTACARGAS  VS  TU RACK
    fb = B(54); gap = 24; rv = 58
    wa = d.textlength("MONTACARGAS", font=fb) / S; wb = d.textlength("TU RACK", font=fb) / S
    x0 = 540 - (wa + wb + 2 * rv + 2 * gap) / 2; vx = x0 + wa + gap + rv
    d.text((k(x0), k(cy)), "MONTACARGAS", font=fb, fill=WHITE, anchor="lm")
    d.text((k(vx + rv + gap), k(cy)), "TU RACK", font=fb, fill=GOLD, anchor="lm")
    d.ellipse([k(vx - rv), k(cy - rv), k(vx + rv), k(cy + rv)], fill=RED, outline=WHITE, width=k(5))
    d.text((k(vx), k(cy + 2)), "VS", font=B(48), fill=WHITE, anchor="mm")
    # ganador
    y = cy + 100
    d.text((W / 2, k(y)), "Gana tu rack con", font=M(34), fill=(208, 220, 238), anchor="mm")
    d.text((W / 2, k(y + 56)), "protectores de columna", font=B(50), fill=WHITE, anchor="mm")


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    logo_tarjeta(c)
    insignia(c, 920, 200)
    cartel(c, 820, 1176)
    pie(c, 1176)
    return c


def preview(capa):
    im = Image.open(FOTO).convert("RGB"); s = W / im.size[0]
    im = im.resize((W, int(im.size[1] * s)), Image.LANCZOS)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255)); base.paste(im, (0, k(FOTO_T)))
    base.alpha_composite(capa)
    return base.convert("RGB").resize((1080, 1350), Image.LANCZOS)


cp = capa(); cp.save(os.path.join(O, "capa_pelea.png"))
preview(cp).save(os.path.join(O, "vista_previa.jpg"), quality=95)
print("ok")
