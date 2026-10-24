"""Capas PNG transparentes (diseño, textos, logo) para armar en Canva sobre las fotos de Anthony.
Las fotos van debajo en Canva; la capa tapa todo menos los huecos de foto.
Uso: python3 capas.py  -> capa_01.png, capa_02.png y vistas previas con fotos del banco.
"""
import os, sys, glob
P = "/mnt/project-files/racksa_proyecto/publicidad"
O = os.path.dirname(os.path.abspath(__file__))
os.chdir(P); sys.path.insert(0, P)
import racksa_plantillas as rp
from racksa_plantillas import B, M, NAVY, NAVY_D, GOLD, RED, WHITE
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1350
INK = (14, 27, 48)
# huecos de foto (x0, y0, x1, y1) -> se usan también para colocar las fotos en Canva
H1 = [(40, 392, 532, 1000), (548, 392, 1040, 1000)]


def logo(base, x, y, w):
    lg = Image.open(rp.LOGO).convert("RGBA")
    lg = lg.resize((w, int(lg.size[1] * w / lg.size[0])), Image.LANCZOS)
    base.alpha_composite(lg, (x, y)); return lg.size


def sombra(base, box, r, blur=18, a=70, dy=10):
    s = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([box[0], box[1] + dy, box[2], box[3] + dy], r, fill=(0, 0, 0, a))
    base.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))


def contactos(base, y0):
    d = ImageDraw.Draw(base)
    d.rectangle([0, y0, W, H], fill=NAVY_D)
    rp._tricolor(d, y0, 8)
    tel = "   ·   ".join(rp.TELS); ft = B(37); tw = d.textlength(tel, font=ft); y = y0 + 34
    base.alpha_composite(rp._wa(38), (int(W / 2 - tw / 2) - 52, y + 6)); d = ImageDraw.Draw(base)
    d.text((W / 2 - tw / 2, y), tel, font=ft, fill=WHITE); y += 60
    fm = M(26); items = [(rp._mail(25), rp.MAIL), (rp._web(25), rp.WEB)]
    tot = sum(d.textlength(t, font=fm) + 36 for _, t in items) + 50; x = W / 2 - tot / 2
    for icon, t in items:
        base.alpha_composite(icon, (int(x), y + 8)); d = ImageDraw.Draw(base)
        d.text((x + 36, y), t, font=fm, fill=WHITE); x += 36 + d.textlength(t, font=fm) + 50


def pill(d, x, y, txt, bg, fg, f, pad=26, h=56, tr=2):
    tw = rp.ancho(txt, f, tr)
    d.rounded_rectangle([x, y, x + tw + 2 * pad, y + h], radius=h // 2, fill=bg)
    rp.espaciado(d, (x + pad, y + (h - f.size) // 2 - 4), txt, f, fg, tr)
    return tw + 2 * pad


def capa1():
    c = Image.new("RGBA", (W, H), (246, 247, 250, 255))
    d = ImageDraw.Draw(c)
    # cabecera
    logo(c, 40, 34, 250)
    f = B(22); tw = rp.ancho("COBERTURA NACIONAL", f, 3) + 52
    d.rounded_rectangle([W - 40 - tw, 46, W - 40, 98], 26, outline=NAVY, width=3)
    rp.espaciado(d, (W - 40 - tw + 26, 58), "COBERTURA NACIONAL", f, NAVY, 3)
    d.text((40, 150), "Tu bodega no necesita", font=B(62), fill=INK)
    d.text((40, 222), "más espacio.", font=B(62), fill=INK)
    t = "Necesita orden."; fb = B(62); w2 = d.textlength(t, font=fb)
    x2 = 40 + d.textlength("más espacio. ", font=fb)
    d.rectangle([x2 - 8, 262, x2 + w2 + 8, 294], fill=GOLD)
    d.text((x2, 222), t, font=fb, fill=INK)
    d.text((42, 312), "Ordenamos tu bodega con racks a la medida de tu carga.", font=M(27), fill=(90, 100, 118))
    # huecos de foto con esquinas redondeadas
    for b in H1:
        sombra(c, b, 26)
    d = ImageDraw.Draw(c)
    hole = Image.new("L", (W, H), 255)
    for b in H1:
        ImageDraw.Draw(hole).rounded_rectangle(b, 26, fill=0)
    c.putalpha(Image.composite(c.split()[3], Image.new("L", (W, H), 0), hole))
    d = ImageDraw.Draw(c)
    # etiquetas antes / después
    f = B(26)
    pill(d, H1[0][0] + 22, H1[0][3] - 78, "ANTES", (25, 28, 34), WHITE, f)
    pill(d, H1[1][0] + 22, H1[1][3] - 78, "CON RACKSA", GOLD, INK, f)
    # flecha central
    cx, cy, r = W // 2, (H1[0][1] + H1[0][3]) // 2, 44
    sombra(c, (cx - r, cy - r, cx + r, cy + r), r, 10, 90, 6); d = ImageDraw.Draw(c)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY, outline=WHITE, width=5)
    d.line([(cx - 20, cy), (cx + 14, cy)], fill=GOLD, width=8)
    d.polygon([(cx + 2, cy - 17), (cx + 22, cy), (cx + 2, cy + 17)], fill=GOLD)
    # beneficios + CTA
    y = 1028; xs = [40, 380, 700]
    for x, t in zip(xs, ("Más espacio", "Más orden", "Más seguridad")):
        d.ellipse([x, y + 6, x + 40, y + 46], fill=NAVY)
        d.line([(x + 10, y + 27), (x + 18, y + 35), (x + 31, y + 17)], fill=GOLD, width=5)
        d.text((x + 54, y + 4), t, font=B(32), fill=INK)
    t = "AGENDA TU VISITA TÉCNICA"; f = B(30); tw = rp.ancho(t, f, 2)
    bx = (W - tw - 90) // 2
    d.rounded_rectangle([bx, 1100, bx + tw + 90, 1172], 36, fill=GOLD)
    rp.espaciado(d, (bx + 45, 1116), t, f, INK, 2)
    contactos(c, 1196)
    c.save(O + "/capa_01.png")
    return c


def capa2():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c.alpha_composite(rp.vgrad(W, 820, 250, 0, NAVY_D, 0.75), (0, 0))
    c.alpha_composite(rp.vgrad(W, 300, 0, 200, NAVY_D, 1.3), (0, H - 154 - 300))
    d = ImageDraw.Draw(c)
    # logo sobre tarjeta blanca
    sombra(c, (40, 36, 330, 140), 22, 14, 90, 8); d = ImageDraw.Draw(c)
    d.rounded_rectangle([40, 36, 330, 140], 22, fill=WHITE)
    logo(c, 58, 50, 254)
    d = ImageDraw.Draw(c)
    f = B(22); tw = rp.ancho("COBERTURA NACIONAL", f, 3) + 52
    d.rounded_rectangle([W - 40 - tw, 62, W - 40, 114], 26, outline=WHITE, width=3)
    rp.espaciado(d, (W - 40 - tw + 26, 74), "COBERTURA NACIONAL", f, WHITE, 3)
    pill(d, 40, 196, "APROVECHA CADA METRO DE TU BODEGA", GOLD, INK, B(25), 28, 58, 2)
    for xy, t, f, col in (((34, 268), "¡Crece hacia", B(118), WHITE), ((34, 396), "arriba!", B(118), GOLD),
                          ((40, 548), "Rack selectivo  ·  Perchas  ·  Montaje en sitio", B(32), WHITE)):
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0] + 2, xy[1] + 4), t, font=f, fill=(0, 0, 0, 200))
        c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
        ImageDraw.Draw(c).text(xy, t, font=f, fill=col)
    d = ImageDraw.Draw(c)
    contactos(c, H - 154)
    c.save(O + "/capa_02.png")
    return c


def vista(capa, fotos, out):
    v = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    for img, b in fotos:
        v.paste(rp.cover(img, b[2] - b[0], b[3] - b[1], .5), b[:2])
    v.alpha_composite(capa); v.convert("RGB").save(out, quality=85)


if __name__ == "__main__":
    f = lambda i: Image.open(glob.glob(P + "/banco/" + i + "*.jpg")[0]).convert("RGB")
    vista(capa1(), [(f("1Kmmzauj0Fly"), H1[0]), (f("1D-0enO7zClN"), H1[1])], "/tmp/claude-0/cv/v1.jpg")
    vista(capa2(), [(f("1SG5e2vAOh7"), (0, 0, W, H))], "/tmp/claude-0/cv/v2.jpg")
    print("ok")
