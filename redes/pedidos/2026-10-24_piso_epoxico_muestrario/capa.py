"""Formato nuevo 'muestrario de colores' (paint chips) para piso epóxico, 2026-10-24.
Capa PNG 2x (2160x2700) para Canva: hueco arriba para la foto, tres muestras tipo carta de color abajo.
Foto en Canva: 20250527_121836 (MAHG2e35WbM), 8160x6120. Colocar foto 1080x810 en (0,-10).
Uso: python3 capa.py"""
import os, sys, glob
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
INK = (14, 27, 48); PAPEL = (244, 243, 239); GRIS = (150, 156, 162)
FOTO_Y1 = 800  # borde inferior del hueco de foto (1x)


def grad(w, h, a0, a1, p=1.0, col=NAVY_D):
    g = Image.new("L", (1, h))
    for i in range(h):
        g.putpixel((0, i), int(a0 + (a1 - a0) * (i / (h - 1)) ** p))
    im = Image.new("RGBA", (w, h), col + (0,)); im.putalpha(g.resize((w, h))); return im


def sombra(c, box, r, blur=16, a=80, dy=10):
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([box[0], box[1] + dy, box[2], box[3] + dy], r, fill=(0, 0, 0, a))
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))


def txt(c, xy, t, f, col, blur=6):
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).text((xy[0] + k(2), xy[1] + k(4)), t, font=f, fill=(0, 0, 0, 180))
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(k(blur))))
    ImageDraw.Draw(c).text(xy, t, font=f, fill=col)


def capa():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rectangle([0, k(FOTO_Y1), W, H], fill=PAPEL)
    c.alpha_composite(grad(W, k(430), 225, 0, 1.0), (0, 0))
    # logo en pestaña blanca
    sombra(c, (k(40), k(-20), k(330), k(120)), k(22), k(14), 90, k(6))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([k(40), k(-20), k(330), k(120)], k(22), fill=WHITE)
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(250)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    c.alpha_composite(lg, (k(60), k(18)))
    d = ImageDraw.Draw(c)
    f = B(21); t = "COBERTURA NACIONAL"; tw = rp.ancho(t, f, k(3)) + k(52)
    d.rounded_rectangle([W - k(40) - tw, k(40), W - k(40), k(92)], k(26), outline=WHITE, width=k(3))
    rp.espaciado(d, (W - k(40) - tw + k(26), k(52)), t, f, WHITE, k(3))
    txt(c, (k(40), k(150)), "Piso epóxico", B(104), WHITE)
    txt(c, (k(44), k(278)), "Brillo, orden y limpieza en cada metro.", M(34), WHITE)
    # muestras tipo carta de color
    chips = [((128, 134, 140), "ACABADO", "Brillante", "Acabado uniforme"),
             (NAVY, "SUPERFICIE", "Sin juntas", "Fácil de limpiar"),
             (GOLD, "SEGURIDAD", "Señalizado", "Pasillos y áreas")]
    cw, ch, gap = 312, 360, 22
    x0 = (1080 - 3 * cw - 2 * gap) / 2; y0 = FOTO_Y1 - 70
    for i, (col, cod, t1, t2) in enumerate(chips):
        x = x0 + i * (cw + gap)
        box = (k(x), k(y0), k(x + cw), k(y0 + ch))
        sombra(c, box, k(14), k(18), 70, k(10)); d = ImageDraw.Draw(c)
        d.rounded_rectangle(box, k(14), fill=WHITE)
        # bloque de color con brillo (efecto epóxico)
        sw = Image.new("RGBA", (k(cw - 28), k(170)), col + (255,))
        gl = grad(k(cw - 28), k(170), 90, 0, 1.4, (255, 255, 255))
        sw.alpha_composite(gl)
        mk = Image.new("L", sw.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, sw.size[0], sw.size[1]], k(8), fill=255)
        c.paste(sw, (k(x + 14), k(y0 + 14)), mk); d = ImageDraw.Draw(c)
        d.text((k(x + 22), k(y0 + 198)), cod, font=B(20), fill=GRIS)
        d.text((k(x + 22), k(y0 + 226)), t1, font=B(38), fill=INK)
        d.text((k(x + 22), k(y0 + 280)), t2, font=M(25), fill=(80, 88, 104))
        cx = k(x + cw - 40); cy = k(y0 + 212)
        d.ellipse([cx - k(18), cy - k(18), cx + k(18), cy + k(18)], fill=NAVY)
        d.line([(cx - k(8), cy), (cx - k(2), cy + k(7)), (cx + k(9), cy - k(7))], fill=GOLD, width=k(4))
    # línea de invitación
    t = "Oficinas  ·  Bodegas  ·  Andenes  ·  Áreas técnicas"; f = M(27)
    d.text((W / 2, k(1150)), t, font=f, fill=INK, anchor="mm")
    # pie
    y0 = H - k(150)
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
    c.save(O + "/capa_muestrario.png", optimize=True)
    return c


if __name__ == "__main__":
    c = capa()
    fs = glob.glob(P + "/banco/1P1dL7YrMG1d*.jpg") or glob.glob(P + "/banco/*.jpg")
    foto = Image.open(fs[0]).convert("RGB")
    v = Image.new("RGBA", (W, H), (0, 0, 0, 255)); v.paste(rp.cover(foto, W, k(FOTO_Y1 + 10), .5), (0, 0)); v.alpha_composite(c)
    v.convert("RGB").resize((1080, 1350), Image.LANCZOS).save("/tmp/claude-0/cv/muestrario.jpg", quality=90)
    print("ok", fs[0][-40:])
