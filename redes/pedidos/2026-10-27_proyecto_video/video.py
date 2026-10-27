"""Formato de video nuevo 2026-10-27: "barrido antes / después con rótulos numerados". Arranca con la bodega
ANTES (desaturada, sello gris), un barrido con línea amarilla revela el DESPUÉS y cada tramo lleva un rótulo
numerado grande (01 Rack selectivo, 02 Piso epóxico, 03 Escalera tipo avión); cierra con la pantalla de
contactos obligatoria. 1080x1920, ~17 s, pista de audio en silencio (Anthony agrega música en IG).
Videos en banco/videos/: hearth_e29765f4_bodega_antes, hearth_fcd733ee_proyecto_recorrido,
hearth_6270bfd0_proyecto_piso, hearth_fc8eae9b_proyecto_escalera."""
import os, sys, subprocess
P = "/mnt/project-files/racksa_proyecto/publicidad"
O = os.path.dirname(os.path.abspath(__file__))
os.chdir(P); sys.path.insert(0, P)
import racksa_plantillas as rp
from racksa_plantillas import NAVY, NAVY_D, GOLD, WHITE
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1080, 1920, 30
V = "banco/videos/"
TMP = os.path.join(O, "tmp"); os.makedirs(TMP, exist_ok=True)
# (archivo, inicio, duración, tipo, rótulo)
TRAMOS = [
    ("hearth_e29765f4_bodega_antes.mp4", 0.0, 6.1, "antes", None),
    ("hearth_fcd733ee_proyecto_recorrido.mp4", 4.3, 3.2, "despues", ("01", "Rack selectivo")),
    ("hearth_6270bfd0_proyecto_piso.mp4", 2.6, 3.0, "despues", ("02", "Piso epóxico")),
    ("hearth_fc8eae9b_proyecto_escalera.mp4", 0.4, 3.8, "despues", ("03", "Escalera tipo avión")),
    ("hearth_fcd733ee_proyecto_recorrido.mp4", 17.6, 2.4, "despues", ("04", "Bodega lista para operar")),
]
CIERRE = 3.6
XF = 0.4                         # duración de cada transición


def logo(w):
    lg = Image.open(rp.LOGO).convert("RGBA")
    return lg.resize((w, int(lg.size[1] * w / lg.size[0])), Image.LANCZOS)


def caja_logo(c, x, y, w):
    lg = logo(w); pad = 14; d = ImageDraw.Draw(c)
    d.rectangle([x, y, x + w + 2 * pad, y + lg.size[1] + 2 * pad], fill=WHITE)
    c.alpha_composite(lg, (x + pad, y + pad))


def sombra_texto(c, xy, txt, f, col, anchor="la"):
    s = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).text((xy[0] + 3, xy[1] + 4), txt, font=f, fill=(0, 0, 0, 200), anchor=anchor)
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(c).text(xy, txt, font=f, fill=col, anchor=anchor)


def capa_antes():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rectangle([60, 230, 380, 330], fill=(40, 40, 44, 230))
    d.ellipse([88, 266, 116, 294], fill=(220, 50, 50))
    rp.espaciado(d, (136, 250), "ANTES", rp.B(54), WHITE, 6)
    sombra_texto(c, (W / 2, 1180), "Así recibimos", rp.B(84), WHITE, "ma")
    sombra_texto(c, (W / 2, 1285), "esta bodega.", rp.B(84), WHITE, "ma")
    return c


def capa_despues(num, txt, primero):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    caja_logo(c, 60, 210, 210); d = ImageDraw.Draw(c)
    d.rectangle([W - 380, 230, W - 60, 330], fill=GOLD)
    rp.espaciado(d, (W - 352, 250), "DESPUÉS", rp.B(52), NAVY_D, 5)
    # rótulo numerado
    f = rp.B(76 if len(txt) < 20 else 62); tw = d.textlength(txt, font=f)
    y0 = 1230; x0 = 60; bw = max(tw + 220, 620)
    d.rectangle([x0, y0, x0 + bw, y0 + 150], fill=NAVY_D + (240,))
    d.rectangle([x0, y0, x0 + 150, y0 + 150], fill=GOLD)
    d.text((x0 + 75, y0 + 75), num, font=rp.B(80), fill=NAVY_D, anchor="mm")
    d.text((x0 + 185, y0 + 75), txt, font=f, fill=WHITE, anchor="lm")
    d.rectangle([x0, y0 + 166, x0 + 600, y0 + 232], fill=(0, 0, 0, 160))
    d.text((x0 + 20, y0 + 199), "Hecho por Racksa Ecuador", font=rp.B(40), fill=GOLD, anchor="lm")
    return c


def cierre():
    c = Image.new("RGBA", (W, H), NAVY_D + (255,)); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, 14], fill=GOLD)
    lg = logo(560); pad = 30
    d.rectangle([W / 2 - 280 - pad, 170, W / 2 + 280 + pad, 170 + lg.size[1] + 2 * pad], fill=WHITE)
    c.alpha_composite(lg, (int(W / 2 - 280), 170 + pad)); d = ImageDraw.Draw(c)
    y = 170 + lg.size[1] + 2 * pad + 90
    d.text((W / 2, y), "Lo hicimos todo.", font=rp.B(96), fill=WHITE, anchor="ma"); y += 140
    for it in ["Rack selectivo", "Escalera tipo avión", "Piso epóxico", "Cantilever"]:
        d.text((W / 2, y), it, font=rp.B(54), fill=GOLD, anchor="ma"); y += 78
    y += 50
    d.rectangle([W / 2 - 200, y, W / 2 + 200, y + 4], fill=GOLD); y += 60
    for t in rp.TELS:
        tw = d.textlength(t, font=rp.B(64))
        c.alpha_composite(rp._wa(60), (int(W / 2 - tw / 2) - 78, y + 8)); d = ImageDraw.Draw(c)
        d.text((W / 2 - tw / 2, y), t, font=rp.B(64), fill=WHITE); y += 96
    y += 20
    for ic, t in [(rp._mail(44), rp.MAIL), (rp._web(42), rp.WEB)]:
        f = rp.M(42); tw = d.textlength(t, font=f) + ic.size[0] + 16; x = W / 2 - tw / 2
        c.alpha_composite(ic, (int(x), y + 12)); d = ImageDraw.Draw(c)
        d.text((x + ic.size[0] + 16, y), t, font=f, fill=WHITE); y += 70
    return c


def run(a):
    subprocess.run(a, check=True)


def tramo(i, f, t0, dur, tipo):
    out = os.path.join(TMP, f"t{i}.mp4")
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
          "unsharp=5:5:0.8:5:5:0.0,setsar=1,fps=30")
    if tipo == "antes":
        vf += ",eq=saturation=0.25:brightness=-0.06:contrast=1.05"
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0), "-t", str(dur), "-i", V + f, "-an", "-vf", vf,
         "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", out])
    return out


if __name__ == "__main__":
    clips, capas, durs = [], [], []
    for i, (f, t0, dur, tipo, rot) in enumerate(TRAMOS):
        clips.append(tramo(i, f, t0, dur, tipo)); durs.append(dur)
        cp = capa_antes() if tipo == "antes" else capa_despues(*rot, i == 1)
        p = os.path.join(TMP, f"c{i}.png"); cp.save(p); capas.append(p)
    # pantalla de cierre enviada por Anthony (2026-10-27) en lugar de la generada
    pc = os.path.join(TMP, "cierre.png")
    Image.open(os.path.join(O, "cierre_anthony.jpg")).convert("RGB").resize((W, H), Image.LANCZOS).save(pc)
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", str(CIERRE), "-i", pc, "-vf",
         f"zoompan=z='1+0.0006*on':d=1:s={W}x{H}:fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "16",
         os.path.join(TMP, "cierre.mp4")])
    clips.append(os.path.join(TMP, "cierre.mp4")); durs.append(CIERRE)
    # capa de texto sobre cada tramo (aparece con fundido) y luego transiciones xfade
    ins = []; fc = []
    for i, cl in enumerate(clips):
        ins += ["-i", cl]
    for i, cp in enumerate(capas):
        ins += ["-loop", "1", "-t", str(durs[i]), "-i", cp]
    n = len(clips)
    for i in range(len(capas)):
        fc.append(f"[{n + i}:v]format=rgba,fade=in:st=0.25:d=0.35:alpha=1[o{i}]")
        fc.append(f"[{i}:v][o{i}]overlay=0:0:shortest=1,format=yuv420p[v{i}]")
    fc.append(f"[{n - 1}:v]format=yuv420p[v{n - 1}]")
    acc = "v0"; t = durs[0]
    for i in range(1, n):
        tr = "wipeleft" if i == 1 else ("fadeblack" if i == n - 1 else "smoothleft")
        off = t - XF
        fc.append(f"[{acc}][v{i}]xfade=transition={tr}:duration={XF}:offset={off:.2f}[x{i}]")
        acc = f"x{i}"; t = off + durs[i]
    total = t
    out = os.path.join(O, "RACKSA_proyecto_antes_despues.mp4")
    run(["ffmpeg", "-v", "error", "-y"] + ins + ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo",
         "-filter_complex", ";".join(fc), "-map", f"[{acc}]", "-map", f"{n + len(capas)}:a",
         "-c:v", "libx264", "-b:v", "3.8M", "-maxrate", "4.5M", "-bufsize", "9M", "-preset", "slow",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", out])
    print("total", round(total, 2))
