"""Formato nuevo 2026-10-26: "nota adhesiva". Titular en banda blanca, foto grande y una nota amarilla
pegada con cinta sobre la foto (girada, con sombra) que lleva el mensaje de El Niño. Barreras contra
inundación en acero inoxidable. Capa PNG 2x, transparente donde va la foto.
Foto en Canva: IMG-20261022-WA0089 (MAHY9nvv0h8, 3120x4160) -> 1080x1440 en (0, FOTO_T)."""
import os, sys
P = "/mnt/project-files/racksa_proyecto/publicidad"
O = os.path.dirname(os.path.abspath(__file__))
os.chdir(P); sys.path.insert(0, P)
import racksa_plantillas as rp
from racksa_plantillas import NAVY, NAVY_D, GOLD, WHITE
from PIL import Image, ImageDraw, ImageFilter

S = 2
W, H = 1080 * S, 1350 * S
B = lambda t: rp.B(int(t * S)); M = lambda t: rp.M(int(t * S))
k = lambda v: int(round(v * S))
FOTO = "banco/hearth_83692942_barrera_instalando.jpg"
TOPB = 262                      # fin de la banda del titular
FOOT = 1110                     # inicio del pie
FOTO_T = -330                   # top de la foto 1080x1440 en Canva
PAPEL = (255, 228, 120)


def nota():
    w, h = k(520), k(350)
    n = Image.new("RGBA", (w, h), PAPEL + (255,))
    d = ImageDraw.Draw(n)
    d.polygon([(w - k(46), h), (w, h - k(46)), (w, h)], fill=(232, 200, 90, 255))     # esquina doblada
    rp.espaciado(d, (k(34), k(40)), "NOTA", B(24), NAVY, k(4))
    d.rectangle([k(34), k(76), k(110), k(80)], fill=NAVY)
    y = k(100)
    for ln in ["Minimiza el impacto", "del fenómeno de El Niño", "en tu bodega."]:
        d.text((k(34), y), ln, font=B(35), fill=NAVY_D); y += k(52)
    d.text((k(34), y + k(14)), "Actúa antes de la próxima lluvia.", font=M(24), fill=NAVY)
    lienzo = Image.new("RGBA", (w + k(120), h + k(120)), (0, 0, 0, 0))
    sombra = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rectangle([k(70), k(76), k(70) + w, k(76) + h], fill=(0, 0, 0, 120))
    lienzo.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(k(14))))
    lienzo.alpha_composite(n, (k(60), k(60)))
    cinta = Image.new("RGBA", (k(170), k(46)), (245, 245, 240, 170))                   # cinta adhesiva
    lienzo.alpha_composite(cinta, (k(60) + w // 2 - k(85), k(40)))
    return lienzo.rotate(-4, resample=Image.BICUBIC, expand=True)


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, k(TOPB)], fill=WHITE)
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(180)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    c.alpha_composite(lg, (k(44), k(32))); d = ImageDraw.Draw(c)
    t = "ACERO INOXIDABLE"; f = B(24); tx = k(1036) - rp.ancho(t, f, k(3)); ty = k(46)
    d.rectangle([tx - k(26), ty + k(6), tx - k(14), ty + k(26)], fill=GOLD)
    rp.espaciado(d, (tx, ty), t, f, NAVY, k(3))
    d.text((k(44), k(116)), "Sistema de barreras", font=B(58), fill=NAVY_D)
    d.text((k(44), k(180)), "contra inundación", font=B(58), fill=NAVY)
    d.rectangle([0, k(TOPB - 6), W, k(TOPB)], fill=GOLD)
    n = nota(); c.alpha_composite(n, (k(450), k(TOPB - 64)))
    d = ImageDraw.Draw(c)
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
    return c


def preview(cp):
    im = Image.open(FOTO).convert("RGB"); s = W / im.size[0]
    im = im.resize((W, int(im.size[1] * s)), Image.LANCZOS)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255)); base.paste(im, (0, k(FOTO_T)))
    base.alpha_composite(cp)
    return base.convert("RGB").resize((1080, 1350), Image.LANCZOS)


cp = capa(); cp.save(os.path.join(O, "capa_nota.png"))
preview(cp).save(os.path.join(O, "vista_previa.jpg"), quality=95)
print("ok")
