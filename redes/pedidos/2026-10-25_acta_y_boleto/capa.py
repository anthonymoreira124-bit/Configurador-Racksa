"""Formatos nuevos 2026-10-25:
 A) piso epóxico  -> "acta de entrega en portapapeles" con checks a mano y sello ENTREGADO
 B) rack selectivo -> "boleto / pase de abordar" Origen: stock Racksa -> Destino: tu bodega
Genera capa PNG 2x (2160x2700) transparente donde va la foto + vista previa con la foto.
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
INK = (24, 30, 44)
PAPEL = (252, 251, 246)

FOTOS = {
    "A": ("banco/1B4pYnJuWIi5CyRYK4k-QBzF2Mz_FQrKs.jpg", -380, 800),   # (foto, y en página 1x, alto visible)
    "B": ("banco/1KxV5a_ME8VGAUC30RymamDLtoqj9TsAp.jpg", -150, 860),
}


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
    """Banda de contacto: 3 teléfonos + correo + web, centrado y grande."""
    d = ImageDraw.Draw(c)
    d.rectangle([0, k(y0), W, H], fill=NAVY_D)
    d.rectangle([0, k(y0), int(W * .6), k(y0 + 8)], fill=NAVY)
    d.rectangle([int(W * .6), k(y0), int(W * .85), k(y0 + 8)], fill=GOLD)
    d.rectangle([int(W * .85), k(y0), W, k(y0 + 8)], fill=RED)
    tel = "   ·   ".join(rp.TELS); ft = B(36); tw = d.textlength(tel, font=ft); y = k(y0 + 34)
    c.alpha_composite(rp._wa(k(38)), (int(W / 2 - tw / 2) - k(52), y + k(6))); d = ImageDraw.Draw(c)
    d.text((W / 2 - tw / 2 + k(0), y), tel, font=ft, fill=WHITE); y += k(62)
    fm = M(26); items = [(rp._mail(k(28)), rp.MAIL), (rp._web(k(26)), rp.WEB)]
    gap = k(44); anchos = [ic.size[0] + k(10) + d.textlength(t, font=fm) for ic, t in items]
    x = W / 2 - (sum(anchos) + gap) / 2
    for (ic, t), a in zip(items, anchos):
        c.alpha_composite(ic, (int(x), y + k(10))); d = ImageDraw.Draw(c)
        d.text((x + ic.size[0] + k(10), y), t, font=fm, fill=WHITE); x += a + gap


def check(d, x, y, s=1.0, col=(20, 120, 70)):
    pts = [(k(x), k(y + 18 * s)), (k(x + 14 * s), k(y + 34 * s)), (k(x + 44 * s), k(y - 6 * s))]
    d.line(pts, fill=col, width=k(8 * s), joint="curve")


def sello(c, cx, cy, txt1, txt2, ang=-14, col=RED):
    w, h = k(330), k(140)
    st = Image.new("RGBA", (w + k(20), h + k(20)), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
    d.rounded_rectangle([k(10), k(10), w + k(10), h + k(10)], k(16), outline=col + (235,), width=k(7))
    d.rounded_rectangle([k(22), k(22), w - k(2), h - k(2)], k(10), outline=col + (235,), width=k(3))
    d.text((st.size[0] / 2, k(70)), txt1, font=B(52), fill=col + (235,), anchor="mm")
    d.text((st.size[0] / 2, k(118)), txt2, font=B(20), fill=col + (235,), anchor="mm")
    st = st.rotate(ang, resample=Image.BICUBIC, expand=True)
    c.alpha_composite(st, (k(cx) - st.size[0] // 2, k(cy) - st.size[1] // 2))


def pieza_A():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rectangle([0, k(800), W, H], fill=NAVY)                       # fondo bajo la foto
    logo_tarjeta(c)
    # hoja en portapapeles, ligeramente girada
    hw, hh = k(900), k(440)
    hoja = Image.new("RGBA", (hw + k(60), hh + k(90)), (0, 0, 0, 0)); h = ImageDraw.Draw(hoja)
    bx = (k(30), k(50), k(30) + hw, k(50) + hh)
    h.rounded_rectangle([bx[0] - k(14), bx[1] - k(14), bx[2] + k(14), bx[3] + k(14)], k(22), fill=(120, 84, 52))  # tabla
    h.rectangle(bx, fill=PAPEL)
    cx = (bx[0] + bx[2]) // 2                                       # pinza metálica
    h.rounded_rectangle([cx - k(110), k(16), cx + k(110), k(84)], k(14), fill=(178, 184, 192), outline=(120, 126, 136), width=k(3))
    h.rounded_rectangle([cx - k(54), k(4), cx + k(54), k(40)], k(12), outline=(120, 126, 136), width=k(6))
    x0 = bx[0] + k(44); y = bx[1] + k(62)
    h.text((x0, y), "ACTA DE ENTREGA", font=B(26), fill=NAVY); y += k(40)
    h.text((x0, y), "Piso epóxico", font=B(58), fill=INK); y += k(84)
    h.line([(x0, y), (bx[2] - k(44), y)], fill=(200, 200, 194), width=k(2)); y += k(20)
    for t in ["Acabado brillante y uniforme", "Superficie sin juntas, fácil de limpiar", "Señalización de pasillos y áreas"]:
        h.rounded_rectangle([x0, y + k(6), x0 + k(44), y + k(50)], k(6), outline=INK, width=k(4))
        check(h, (x0 / S) + 6, (y / S) + 14, 1.05)
        h.text((x0 + k(68), y + k(2)), t, font=B(31), fill=INK)
        y += k(64)
    hoja = hoja.rotate(1.6, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0))
    px, py = (W - hoja.size[0]) // 2, k(700)
    sh.paste((0, 0, 0, 150), (px + k(6), py + k(16)), hoja.split()[3])
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(k(16))))
    c.alpha_composite(hoja, (px, py))
    sello(c, 780, 858, "ENTREGADO", "RACKSA ECUADOR", -8)
    pie(c, 1176)
    return c


def boleto(c, y0, alto=380):
    x0, x1 = 50, 1030; y1 = y0 + alto; corte = 790
    box = (k(x0), k(y0), k(x1), k(y1))
    sombra(c, box, k(22), 18, 150, 10)
    t = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle(box, k(22), fill=PAPEL)
    d.rounded_rectangle([k(x0), k(y0), k(x1), k(y0 + 74)], k(22), fill=NAVY)
    d.rectangle([k(x0), k(y0 + 40), k(x1), k(y0 + 74)], fill=NAVY)
    d.rectangle([k(corte), k(y0), k(x1), k(y0 + 74)], fill=GOLD)
    # muescas del troquel y línea perforada
    for yy in (y0, y1):
        d.ellipse([k(corte - 20), k(yy - 20), k(corte + 20), k(yy + 20)], fill=(0, 0, 0, 0))
    yy = y0 + 30
    while yy < y1 - 30:
        d.ellipse([k(corte - 4), k(yy), k(corte + 4), k(yy + 8)], fill=(170, 172, 168)); yy += 22
    # cabecera
    rp.espaciado(d, (k(x0 + 36), k(y0 + 20)), "PASE DE ENTREGA", B(28), WHITE, k(3))
    d.text((k(corte - 36), k(y0 + 20)), "RACK SELECTIVO", font=B(28), fill=GOLD, anchor="ra")
    d.text(((k(corte) + k(x1)) / 2, k(y0 + 38)), "N° 001", font=B(28), fill=NAVY_D, anchor="mm")
    # origen -> destino
    ya = y0 + 104
    d.text((k(x0 + 36), k(ya)), "ORIGEN", font=B(22), fill=(110, 118, 132))
    d.text((k(corte - 36), k(ya)), "DESTINO", font=B(22), fill=(110, 118, 132), anchor="ra")
    fo = B(58)
    d.text((k(x0 + 36), k(ya + 30)), "STOCK", font=fo, fill=NAVY_D)
    d.text((k(corte - 36), k(ya + 30)), "TU BODEGA", font=fo, fill=NAVY_D, anchor="ra")
    # flecha entre las dos palabras
    ax0 = x0 + 36 + d.textlength("STOCK", font=fo) / S + 22
    ax1 = corte - 36 - d.textlength("TU BODEGA", font=fo) / S - 22
    ax0, ax1, ay = int(ax0), int(ax1), ya + 70
    for xx in range(ax0, ax1 - 20, 22):
        d.line([(k(xx), k(ay)), (k(xx + 11), k(ay))], fill=RED, width=k(5))
    d.polygon([(k(ax1), k(ay)), (k(ax1 - 26), k(ay - 16)), (k(ax1 - 26), k(ay + 16))], fill=RED)
    d.line([(k(x0 + 36), k(ya + 132)), (k(corte - 36), k(ya + 132))], fill=(214, 214, 206), width=k(2))
    # campos
    campos = [("SALIDA", "Entrega inmediata"), ("COBERTURA", "Nacional")]
    xs = [x0 + 36, x0 + 480]
    for (lab, val), xx in zip(campos, xs):
        d.text((k(xx), k(ya + 150)), lab, font=B(22), fill=(110, 118, 132))
        d.text((k(xx), k(ya + 178)), val, font=B(40), fill=RED if lab == "SALIDA" else NAVY_D)
    # talón
    lg = Image.open(rp.LOGO).convert("RGBA"); lw = k(190)
    lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    t.alpha_composite(lg, (int((k(corte) + k(x1)) / 2 - lw / 2), k(y0 + 104)))
    d = ImageDraw.Draw(t)
    cxs = (k(corte) + k(x1)) / 2
    d.text((cxs, k(y0 + 250)), "En stock", font=B(34), fill=NAVY_D, anchor="mm")
    d.text((cxs, k(y0 + 296)), "listo para", font=M(26), fill=(90, 98, 112), anchor="mm")
    d.text((cxs, k(y0 + 330)), "despachar", font=M(26), fill=(90, 98, 112), anchor="mm")
    c.alpha_composite(t)


def pieza_B():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rectangle([0, k(860), W, H], fill=NAVY)
    logo_tarjeta(c)
    boleto(c, 760)
    pie(c, 1176)
    return c


def preview(capa, clave):
    f, fy, _ = FOTOS[clave]
    im = Image.open(f).convert("RGB"); s = W / im.size[0]
    im = im.resize((W, int(im.size[1] * s)), Image.LANCZOS)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255)); base.paste(im, (0, k(fy)))
    base.alpha_composite(capa)
    return base.convert("RGB").resize((1080, 1350), Image.LANCZOS)


for clave, fn, nom in [("A", pieza_A, "piso_acta"), ("B", pieza_B, "rack_boleto")]:
    capa = fn(); capa.save(os.path.join(O, f"capa_{nom}.png"))
    preview(capa, clave).save(os.path.join(O, f"RACKSA_{nom}.jpg"), quality=95)
    print("ok", nom)
