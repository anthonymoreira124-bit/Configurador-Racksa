"""Formato nuevo 2026-10-26: "boletín de prensa". Portada de periódico propio de Racksa: cabecera con
filetes dobles y fecha de edición, titular serif a todo el ancho, foto grande a la izquierda con pie de
foto y columna angosta de texto a la derecha; pie de contactos azul. Barreras contra inundación.
Composición 2x local con la foto de Canva (copia en banco/hearth_e54e56bd_barrera_cajero.jpg)."""
import os, sys
P = "/mnt/project-files/racksa_proyecto/publicidad"
O = os.path.dirname(os.path.abspath(__file__))
os.chdir(P); sys.path.insert(0, P)
import racksa_plantillas as rp
from racksa_plantillas import NAVY, NAVY_D, GOLD, WHITE
from PIL import Image, ImageDraw, ImageFont

S = 2
W, H = 1080 * S, 1350 * S
B = lambda t: rp.B(int(t * S)); M = lambda t: rp.M(int(t * S))
SB = lambda t: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", int(t * S))
SI = lambda t: ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", int(t * S))
k = lambda v: int(round(v * S))
FOTO = "banco/hearth_e54e56bd_barrera_cajero.jpg"
PAPEL = (247, 244, 236)
TINTA = (24, 28, 38)
FOOT = 1110
FX0, FX1, FY0, FY1 = 44, 700, 372, 1020          # foto
CX0 = 728                                        # columna de texto


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
    c = Image.new("RGBA", (W, H), PAPEL + (255,))
    d = ImageDraw.Draw(c)
    # cabecera del boletín
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(150)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    c.alpha_composite(lg, (k(44), k(30))); d = ImageDraw.Draw(c)
    d.text((k(1036), k(28)), "BOLETÍN RACKSA", font=SB(54), fill=TINTA, anchor="ra")
    d.rectangle([k(44), k(110), k(1036), k(114)], fill=TINTA)
    d.rectangle([k(44), k(120), k(1036), k(121)], fill=TINTA)
    d.text((k(44), k(130)), "EDICIÓN TEMPORADA DE LLUVIAS", font=B(20), fill=NAVY)
    d.text((k(1036), k(130)), "ECUADOR · 2026", font=B(20), fill=NAVY, anchor="ra")
    d.rectangle([k(44), k(162), k(1036), k(163)], fill=TINTA)
    # titular
    d.text((k(44), k(180)), "Bodegas que se preparan", font=SB(56), fill=TINTA)
    d.text((k(44), k(262)), "siguen operando cuando llueve", font=SB(56), fill=TINTA)
    d.rectangle([k(44), k(346), k(1036), k(347)], fill=TINTA)
    # foto grande
    im = Image.open(FOTO).convert("RGB")
    c.paste(rp.cover(im, k(FX1 - FX0), k(FY1 - FY0), 0.5), (k(FX0), k(FY0)))
    d = ImageDraw.Draw(c)
    d.text((k(FX0), k(FY1 + 12)), "Barrera de acero inoxidable instalada por Racksa Ecuador.", font=SI(26), fill=TINTA)
    d.rectangle([k(714), k(FY0), k(715), k(FY1 + 46)], fill=TINTA)       # filete entre columnas
    # columna de texto
    y = FY0
    rp.espaciado(d, (k(CX0), k(y)), "INUNDACIONES", B(22), NAVY, k(3)); y += 40
    d.rectangle([k(CX0), k(y), k(CX0 + 60), k(y + 5)], fill=GOLD); y += 26
    for ln in ["Sistema de", "barreras contra", "inundación en", "acero inoxidable."]:
        d.text((k(CX0), k(y)), ln, font=B(34), fill=NAVY_D); y += 46
    y += 24
    for ln in ["Para bodegas,", "plantas industriales", "y oficinas."]:
        d.text((k(CX0), k(y)), ln, font=M(28), fill=TINTA); y += 40
    y += 24
    for ln in ["Fabricación e", "instalación en sitio,", "a nivel nacional."]:
        d.text((k(CX0), k(y)), ln, font=M(28), fill=TINTA); y += 40
    y += 30
    d.rectangle([k(CX0), k(y), k(1036), k(y + 2)], fill=TINTA); y += 22
    for ln in ["“Minimiza el", "impacto de El Niño", "en tu bodega.”"]:
        d.text((k(CX0), k(y)), ln, font=SI(36), fill=NAVY); y += 44
    pie(c, d)
    return c.convert("RGB").resize((1080, 1350), Image.LANCZOS)


pieza().save(os.path.join(O, "barreras_boletin.jpg"), quality=95)
print("ok")
