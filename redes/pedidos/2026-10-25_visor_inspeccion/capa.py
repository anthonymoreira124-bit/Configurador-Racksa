"""Formato nuevo 2026-10-25: "visor de inspección" (foto a página completa con esquinas de enfoque,
retícula y datos discretos tipo cámara; contactos en barra delgada). Percha de carga larga.
Capa PNG 2x. Foto en Canva: IMG-20260929-WA0040 (MAHY_vSoOFU), 1200x1600 -> 1080x1440 en (0, FOTO_T)."""
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
FOTO = "banco/1nxxDm2ofUlacDtEibltCJUuEXCQpTtxQ.jpg"
FOTO_T = -40
BARRA = 1196          # inicio de la barra de contactos
FX0, FY0, FX1, FY1 = 44, 44, 1036, BARRA - 32   # marco del visor


def grad(c, y0, y1, a0, a1):
    g = Image.new("L", (1, k(y1 - y0)))
    for i in range(g.size[1]):
        g.putpixel((0, i), int(a0 + (a1 - a0) * (i / max(1, g.size[1] - 1)) ** 1.4))
    im = Image.new("RGBA", (W, g.size[1]), (6, 18, 40, 0)); im.putalpha(g.resize((W, g.size[1])))
    c.alpha_composite(im, (0, k(y0)))


def esquinas(d, col=WHITE, L=78, t=5):
    for (x, y, sx, sy) in [(FX0, FY0, 1, 1), (FX1, FY0, -1, 1), (FX0, FY1, 1, -1), (FX1, FY1, -1, -1)]:
        d.rectangle(sorted([k(x), k(x + sx * L)]) + [0, 0], fill=None) if False else None
        xs = sorted([x, x + sx * L]); ys = sorted([y, y + sy * L])
        d.rectangle([k(xs[0]), k(y - (t if sy < 0 else 0)), k(xs[1]), k(y + (t if sy > 0 else 0))], fill=col)
        d.rectangle([k(x - (t if sx < 0 else 0)), k(ys[0]), k(x + (t if sx > 0 else 0)), k(ys[1])], fill=col)


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grad(c, 0, 300, 190, 0)                 # oscurece arriba para el rótulo
    grad(c, 640, BARRA, 0, 238)             # oscurece abajo para el titular
    d = ImageDraw.Draw(c)
    esquinas(d)
    # retícula central discreta
    cx, cy = 540, 560
    for a, b in [((cx - 26, cy), (cx - 8, cy)), ((cx + 8, cy), (cx + 26, cy)), ((cx, cy - 26), (cx, cy - 8)), ((cx, cy + 8), (cx, cy + 26))]:
        d.line([(k(a[0]), k(a[1])), (k(b[0]), k(b[1]))], fill=(255, 255, 255, 200), width=k(3))
    # escala vertical a la derecha
    for i in range(13):
        y = 300 + i * 34; L = 26 if i % 3 == 0 else 14
        d.line([(k(FX1 - 22 - L), k(y)), (k(FX1 - 22), k(y))], fill=(255, 255, 255, 170), width=k(3))
    # logo en tarjeta blanca dentro del marco
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(200)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    pad = k(14); bx = (k(FX0 + 30), k(FY0 + 30)); box = (bx[0], bx[1], bx[0] + lw + 2 * pad, bx[1] + lg.size[1] + 2 * pad)
    d.rectangle(box, fill=WHITE); c.alpha_composite(lg, (bx[0] + pad, bx[1] + pad)); d = ImageDraw.Draw(c)
    # rótulo superior derecho tipo cámara
    t = "INSPECCIÓN TÉCNICA"; f = B(24)
    tx = k(FX1 - 30) - rp.ancho(t, f, k(3)); ty = k(FY0 + 44)
    d.ellipse([tx - k(30), ty + k(8), tx - k(14), ty + k(24)], fill=GOLD)
    rp.espaciado(d, (tx, ty), t, f, WHITE, k(3))
    d.text((k(FX1 - 30), k(FY0 + 82)), "Racksa Ecuador", font=M(22), fill=(220, 228, 240), anchor="ra")
    # bloque inferior: dato + titular
    x0 = FX0 + 36; y = FY1 - 262
    d.rectangle([k(x0), k(y + 6), k(x0 + 8), k(y + 36)], fill=GOLD)
    rp.espaciado(d, (k(x0 + 22), k(y + 4)), "PERCHA DE CARGA LARGA", B(26), GOLD, k(3))
    y += 52
    d.text((k(x0), k(y)), "Revisada nivel por nivel", font=B(54), fill=WHITE)
    d.text((k(x0), k(y + 68)), "antes de entregar.", font=B(54), fill=WHITE)
    d.text((k(x0), k(y + 150)), "Estructura modular · niveles a la medida · cobertura nacional", font=M(25), fill=(220, 228, 240))
    # barra delgada de contactos
    d.rectangle([0, k(BARRA), W, H], fill=NAVY_D)
    d.rectangle([0, k(BARRA), W, k(BARRA + 5)], fill=GOLD)
    tel = "   ·   ".join(rp.TELS); ft = B(34); tw = d.textlength(tel, font=ft); yy = k(BARRA + 24)
    c.alpha_composite(rp._wa(k(34)), (int(W / 2 - tw / 2) - k(48), yy + k(6))); d = ImageDraw.Draw(c)
    d.text((W / 2 - tw / 2, yy), tel, font=ft, fill=WHITE); yy += k(56)
    fm = M(24); items = [(rp._mail(k(26)), rp.MAIL), (rp._web(k(24)), rp.WEB)]
    gap = k(40); anchos = [ic.size[0] + k(10) + d.textlength(t, font=fm) for ic, t in items]
    x = W / 2 - (sum(anchos) + gap) / 2
    for (ic, t), a in zip(items, anchos):
        c.alpha_composite(ic, (int(x), yy + k(9))); d = ImageDraw.Draw(c)
        d.text((x + ic.size[0] + k(10), yy), t, font=fm, fill=WHITE); x += a + gap
    return c


def preview(cp):
    im = Image.open(FOTO).convert("RGB"); s = W / im.size[0]
    im = im.resize((W, int(im.size[1] * s)), Image.LANCZOS)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255)); base.paste(im, (0, k(FOTO_T)))
    base.alpha_composite(cp)
    return base.convert("RGB").resize((1080, 1350), Image.LANCZOS)


cp = capa(); cp.save(os.path.join(O, "capa_visor.png"))
preview(cp).save(os.path.join(O, "vista_previa.jpg"), quality=95)
print("ok")
