"""Formato nuevo 2026-10-26: "pronóstico semanal". Titular en panel blanco, franja de pronóstico de 7 días
con íconos de lluvia/tormenta dibujados, foto grande limpia de la barrera instalada y pie de contactos.
Barreras contra inundación en acero inoxidable. Composición 2x local con la foto de Canva
IMG-20261022-WA0091 (copia en banco/hearth_7d2ebea1_barrera_instalada.jpg)."""
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
FOTO = "banco/hearth_7d2ebea1_barrera_instalada.jpg"
STRIP0, STRIP1 = 262, 432       # franja de pronóstico
FOOT = 1110
FOTO_Y0 = 0.45                  # desde dónde se recorta la foto (fracción de su alto)
GRIS = (238, 242, 248)
DIAS = [("LUN", "lluvia"), ("MAR", "tormenta"), ("MIÉ", "lluvia"), ("JUE", "lluvia"),
        ("VIE", "tormenta"), ("SÁB", "lluvia"), ("DOM", "lluvia")]


def icono(d, cx, cy, tipo):
    """Nube con gotas (lluvia) o con rayo (tormenta), centrada en cx, cy."""
    col = NAVY
    for (x, y, r) in [(-26, 6, 22), (0, -8, 30), (28, 6, 22)]:
        d.ellipse([k(cx + x - r), k(cy + y - r), k(cx + x + r), k(cy + y + r)], fill=col)
    d.rounded_rectangle([k(cx - 48), k(cy + 2), k(cx + 50), k(cy + 28)], radius=k(13), fill=col)
    if tipo == "lluvia":
        for x in (-26, 0, 26):
            d.line([k(cx + x + 6), k(cy + 40), k(cx + x - 2), k(cy + 60)], fill=(70, 130, 200), width=k(6))
    else:
        d.polygon([(k(cx + 6), k(cy + 34)), (k(cx - 14), k(cy + 62)), (k(cx - 1), k(cy + 62)),
                   (k(cx - 10), k(cy + 84)), (k(cx + 18), k(cy + 52)), (k(cx + 4), k(cy + 52)),
                   (k(cx + 14), k(cy + 34))], fill=GOLD)


def pie(c, d):
    d.rectangle([0, k(FOOT), W, H], fill=NAVY_D)
    d.rectangle([0, k(FOOT), W, k(FOOT + 6)], fill=GOLD)
    d.text((W / 2, k(FOOT + 30)), "Racksa Ecuador  ·  Instalación en sitio a nivel nacional", font=B(28), fill=GOLD, anchor="ma")
    tel = "   ·   ".join(rp.TELS); ft = B(38); tw = d.textlength(tel, font=ft); yy = k(FOOT + 86)
    c.alpha_composite(rp._wa(k(38)), (int(W / 2 - tw / 2) - k(52), yy + k(6))); d = ImageDraw.Draw(c)
    d.text((W / 2 - tw / 2, yy), tel, font=ft, fill=WHITE); yy += k(70)
    fm = M(26); items = [(rp._mail(k(28)), rp.MAIL), (rp._web(k(26)), rp.WEB)]
    gap = k(40); anchos = [ic.size[0] + k(10) + d.textlength(t, font=fm) for ic, t in items]
    x = W / 2 - (sum(anchos) + gap) / 2
    for (ic, t), a in zip(items, anchos):
        c.alpha_composite(ic, (int(x), yy + k(9))); d = ImageDraw.Draw(c)
        d.text((x + ic.size[0] + k(10), yy), t, font=fm, fill=WHITE); x += a + gap


def pieza():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    # foto grande y limpia entre la franja y el pie
    im = Image.open(FOTO).convert("RGB"); s = W / im.size[0]
    im = im.resize((W, int(im.size[1] * s)), Image.LANCZOS)
    y0 = int(im.size[1] * FOTO_Y0); alto = k(FOOT - STRIP1)
    c.paste(im.crop((0, y0, W, y0 + alto)), (0, k(STRIP1)))
    d = ImageDraw.Draw(c)
    # cabecera
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(180)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    c.alpha_composite(lg, (k(44), k(32))); d = ImageDraw.Draw(c)
    t = "TEMPORADA DE LLUVIAS"; f = B(24); tx = k(1036) - rp.ancho(t, f, k(3)); ty = k(46)
    d.rectangle([tx - k(26), ty + k(6), tx - k(14), ty + k(26)], fill=GOLD)
    rp.espaciado(d, (tx, ty), t, f, NAVY, k(3))
    d.text((k(44), k(116)), "El pronóstico no lo controlas.", font=B(52), fill=NAVY_D)
    l2 = "El agua en tu bodega, sí."; f2 = B(52); w2 = d.textlength(l2, font=f2)
    d.rectangle([k(44), k(214), k(44) + w2, k(234)], fill=GOLD)
    d.text((k(44), k(176)), l2, font=f2, fill=NAVY_D)
    # franja de pronóstico
    d.rectangle([0, k(STRIP0), W, k(STRIP1)], fill=GRIS)
    cw = 1080 / 7
    for i, (dia, tipo) in enumerate(DIAS):
        cx = cw * i + cw / 2
        if i: d.line([k(cw * i), k(STRIP0 + 22), k(cw * i), k(STRIP1 - 22)], fill=(200, 208, 222), width=k(2))
        d.text((k(cx), k(STRIP0 + 18)), dia, font=B(24), fill=NAVY, anchor="ma")
        icono(d, cx, STRIP0 + 86, tipo)
    d.rectangle([0, k(STRIP1 - 6), W, k(STRIP1)], fill=NAVY)
    # rótulo sobre la foto (abajo a la izquierda, sin tapar la barrera)
    r1 = "SISTEMA DE BARRERAS CONTRA INUNDACIÓN"; r2 = "Acero inoxidable · instalada por Racksa Ecuador"
    f1, f2 = B(26), M(24); bw = max(rp.ancho(r1, f1, k(2)), d.textlength(r2, font=f2)) + k(48)
    by = k(FOOT - 128)
    d.rectangle([k(32), by, k(32) + bw, by + k(96)], fill=NAVY_D)
    d.rectangle([k(32), by, k(40), by + k(96)], fill=GOLD)
    rp.espaciado(d, (k(60), by + k(14)), r1, f1, WHITE, k(2))
    d.text((k(60), by + k(54)), r2, font=f2, fill=GOLD)
    pie(c, d)
    return c.convert("RGB").resize((1080, 1350), Image.LANCZOS)


pieza().save(os.path.join(O, "barreras_pronostico.jpg"), quality=95)
print("ok")
