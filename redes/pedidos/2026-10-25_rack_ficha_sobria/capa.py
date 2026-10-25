"""Formato nuevo 2026-10-25: "ficha técnica sobria" (estilo suizo: panel blanco, filetes finos,
3 columnas de especificaciones) para rack selectivo. Capa PNG 2x transparente donde va la foto.
Foto en Canva: IMG-20260921-WA0011 (MAHY_hy2aQ8), 1536x2048 -> 1080x1440 en (0, FOTO_T). Uso: python3 capa.py"""
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
FOTO = "banco/1Q44wQ6hCnVVPbBdCcpZcAmxliXqzEx6I.jpg"
FOTO_T = -170
PANEL = 770
GRIS = (96, 106, 122)
LINEA = (214, 219, 226)


def logo_tarjeta(c, x=40, y=40, w=220):
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(w)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    pad = k(16); box = (k(x), k(y), k(x) + lw + 2 * pad, k(y) + lg.size[1] + 2 * pad)
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rectangle([box[0], box[1] + k(4), box[2], box[3] + k(4)], fill=(0, 0, 0, 90))
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(k(10))))
    ImageDraw.Draw(c).rectangle(box, fill=WHITE)
    c.alpha_composite(lg, (box[0] + pad, box[1] + pad))


def pie(c, y0):
    d = ImageDraw.Draw(c)
    d.rectangle([0, k(y0), W, H], fill=NAVY_D)
    tel = "   ·   ".join(rp.TELS); ft = B(36); tw = d.textlength(tel, font=ft); y = k(y0 + 30)
    c.alpha_composite(rp._wa(k(38)), (int(W / 2 - tw / 2) - k(52), y + k(6))); d = ImageDraw.Draw(c)
    d.text((W / 2 - tw / 2, y), tel, font=ft, fill=WHITE); y += k(62)
    fm = M(26); items = [(rp._mail(k(28)), rp.MAIL), (rp._web(k(26)), rp.WEB)]
    gap = k(44); anchos = [ic.size[0] + k(10) + d.textlength(t, font=fm) for ic, t in items]
    x = W / 2 - (sum(anchos) + gap) / 2
    for (ic, t), a in zip(items, anchos):
        c.alpha_composite(ic, (int(x), y + k(10))); d = ImageDraw.Draw(c)
        d.text((x + ic.size[0] + k(10), y), t, font=fm, fill=WHITE); x += a + gap


def ficha(c):
    d = ImageDraw.Draw(c)
    d.rectangle([0, k(PANEL), W, k(1180)], fill=WHITE)
    d.rectangle([0, k(PANEL), W, k(PANEL + 6)], fill=GOLD)          # filete dorado fino
    x0, x1 = 64, 1016; y = PANEL + 40
    rp.espaciado(d, (k(x0), k(y)), "RACK SELECTIVO PESADO", B(24), NAVY, k(4))
    d.text((k(x1), k(y)), "Racksa Ecuador", font=M(24), fill=GRIS, anchor="ra")
    y += 46
    d.text((k(x0), k(y)), "Estructura pensada al milímetro.", font=B(50), fill=NAVY_D)
    y += 92
    d.line([(k(x0), k(y)), (k(x1), k(y))], fill=LINEA, width=k(2))
    cols = [("PUNTAL", "90 × 70 mm", "espesor 2,0 mm"),
            ("VIGA TIPO CAJÓN", "100 × 50 mm", "espesor 1,5 mm"),
            ("ACABADO", "Epoxi en polvo", "60–80 µm, curado 180 °C")]
    cw = (x1 - x0) / 3; yc = y + 26
    for i, (lab, v1, v2) in enumerate(cols):
        cx = x0 + i * cw + (0 if i == 0 else 30)
        if i:
            d.line([(k(x0 + i * cw), k(yc)), (k(x0 + i * cw), k(yc + 118))], fill=LINEA, width=k(2))
        d.text((k(cx), k(yc)), lab, font=B(22), fill=GRIS)
        d.text((k(cx), k(yc + 32)), v1, font=B(38), fill=NAVY_D)
        d.text((k(cx), k(yc + 84)), v2, font=M(23), fill=GRIS)
    y = yc + 140
    d.line([(k(x0), k(y)), (k(x1), k(y))], fill=LINEA, width=k(2))
    d.text((k(x0), k(y + 14)), "Diseño basado en ANSI/RMI MH16.1 · AISI S100 · NEC-SE", font=M(23), fill=NAVY)


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    logo_tarjeta(c)
    ficha(c)
    pie(c, 1180)
    return c


def preview(cp):
    im = Image.open(FOTO).convert("RGB"); s = W / im.size[0]
    im = im.resize((W, int(im.size[1] * s)), Image.LANCZOS)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255)); base.paste(im, (0, k(FOTO_T)))
    base.alpha_composite(cp)
    return base.convert("RGB").resize((1080, 1350), Image.LANCZOS)


cp = capa(); cp.save(os.path.join(O, "capa_ficha.png"))
preview(cp).save(os.path.join(O, "vista_previa.jpg"), quality=95)
print("ok")
