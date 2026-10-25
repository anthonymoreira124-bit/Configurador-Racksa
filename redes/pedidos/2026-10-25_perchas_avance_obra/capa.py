"""Formato nuevo 2026-10-25: "avance de obra al 100%" (barra de progreso con 4 hitos) para perchas de carga media.
Equilibrado: titular con fuerza + diseño limpio. Capa PNG 2x transparente donde va la foto.
Foto en Canva: IMG-20260406-WA0035 (MAHY_luF8xw), 1536x2048 -> 1080x1440 en (0, FOTO_T). Uso: python3 capa.py"""
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
FOTO = "banco/1QQeat8wBKuX7zpxVxdVSR-1xeL7FLLxo.jpg"
FOTO_T = -230
PANEL = 790
CLARO = (208, 220, 238)


def logo_tarjeta(c, x=40, y=40, w=220):
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(w)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    pad = k(16); box = (k(x), k(y), k(x) + lw + 2 * pad, k(y) + lg.size[1] + 2 * pad)
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([box[0], box[1] + k(4), box[2], box[3] + k(4)], k(10), fill=(0, 0, 0, 90))
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(k(10))))
    ImageDraw.Draw(c).rounded_rectangle(box, k(10), fill=WHITE)
    c.alpha_composite(lg, (box[0] + pad, box[1] + pad))


def pie(c, y0):
    d = ImageDraw.Draw(c)
    d.rectangle([0, k(y0), W, H], fill=NAVY_D)
    d.line([(k(64), k(y0)), (k(1016), k(y0))], fill=(46, 84, 140), width=k(2))
    tel = "   ·   ".join(rp.TELS); ft = B(36); tw = d.textlength(tel, font=ft); y = k(y0 + 30)
    c.alpha_composite(rp._wa(k(38)), (int(W / 2 - tw / 2) - k(52), y + k(6))); d = ImageDraw.Draw(c)
    d.text((W / 2 - tw / 2, y), tel, font=ft, fill=WHITE); y += k(62)
    fm = M(26); items = [(rp._mail(k(28)), rp.MAIL), (rp._web(k(26)), rp.WEB)]
    gap = k(44); anchos = [ic.size[0] + k(10) + d.textlength(t, font=fm) for ic, t in items]
    x = W / 2 - (sum(anchos) + gap) / 2
    for (ic, t), a in zip(items, anchos):
        c.alpha_composite(ic, (int(x), y + k(10))); d = ImageDraw.Draw(c)
        d.text((x + ic.size[0] + k(10), y), t, font=fm, fill=WHITE); x += a + gap


def check(d, cx, cy, s=1.0, col=NAVY_D):
    d.line([(k(cx - 9 * s), k(cy)), (k(cx - 2 * s), k(cy + 7 * s)), (k(cx + 10 * s), k(cy - 7 * s))],
           fill=col, width=k(4.5 * s), joint="curve")


def panel(c):
    d = ImageDraw.Draw(c)
    d.rectangle([0, k(PANEL), W, k(1180)], fill=NAVY_D)
    x0, x1 = 64, 1016; y = PANEL + 44
    rp.espaciado(d, (k(x0), k(y)), "AVANCE DE OBRA", B(24), GOLD, k(4))
    d.text((k(x1), k(y)), "Perchas de carga media", font=M(24), fill=CLARO, anchor="ra")
    y += 44
    d.text((k(x0), k(y)), "Tu bodega, lista al 100%.", font=B(58), fill=WHITE)
    # barra de progreso
    yb = y + 118; bh = 22
    d.rounded_rectangle([k(x0), k(yb), k(x1 - 150), k(yb + bh)], k(bh / 2), fill=GOLD)
    d.text((k(x1), k(yb + bh / 2)), "100%", font=B(40), fill=GOLD, anchor="rm")
    hitos = ["Visita técnica", "Diseño", "Instalación", "Entrega"]
    span = (x1 - 150) - x0 - 36
    for i, t in enumerate(hitos):
        cx = x0 + 18 + span * i / 3; cy = yb + bh / 2
        d.ellipse([k(cx - 22), k(cy - 22), k(cx + 22), k(cy + 22)], fill=WHITE, outline=GOLD, width=k(4))
        check(d, cx, cy, 1.0)
        anchor = "la" if i == 0 else ("ra" if i == 3 else "ma")
        tx = x0 if i == 0 else (cx + 22 if i == 3 else cx)
        d.text((k(tx), k(cy + 40)), t, font=B(28), fill=WHITE, anchor=anchor)
    d.text((k(x0), k(yb + 120)), "Diseñamos, implementamos y mantenemos bodegas que producen más.", font=M(24), fill=CLARO)


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    logo_tarjeta(c)
    panel(c)
    pie(c, 1180)
    return c


def preview(cp):
    im = Image.open(FOTO).convert("RGB"); s = W / im.size[0]
    im = im.resize((W, int(im.size[1] * s)), Image.LANCZOS)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255)); base.paste(im, (0, k(FOTO_T)))
    base.alpha_composite(cp)
    return base.convert("RGB").resize((1080, 1350), Image.LANCZOS)


cp = capa(); cp.save(os.path.join(O, "capa_avance.png"))
preview(cp).save(os.path.join(O, "vista_previa.jpg"), quality=95)
print("ok")
