import { loadFont } from "@remotion/fonts";
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  Img,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
} from "remotion";

// Reel "Recorrido en 6 estaciones" — Racksa Ecuador (2026-10-25)
const AZUL = "#0F4C9D";
const NAVY = "#082A5C";
const DORADO = "#FAC70C";
const ROJO = "#E1462A";

loadFont({ family: "Poppins", url: staticFile("Poppins-Medium.ttf"), weight: "500" });
loadFont({ family: "Poppins", url: staticFile("Poppins-Bold.ttf"), weight: "700" });

const FPS = 30;
const INTRO = 66;
const EST = 45;
const SOLAPE = 12;
const CIERRE = 96;
const TOTAL = INTRO + EST * 6 + CIERRE; // 432 f = 14,4 s
const PANEL_Y = 1290;

const ESTACIONES = [
  { foto: "f1.jpg", l1: "Rack", l2: "selectivo" },
  { foto: "f2.jpg", l1: "Perchas", l2: "de picking" },
  { foto: "f3.jpg", l1: "Rack", l2: "cantilever" },
  { foto: "f4.jpg", l1: "Mezzanines", l2: "y entrepisos" },
  { foto: "f5.jpg", l1: "Apiladores", l2: "y montacargas" },
  { foto: "f6.jpg", l1: "Piso epóxico", l2: "y señalización" },
];

const salida = Easing.bezier(0.16, 1, 0.3, 1);
const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const Sello: React.FC<{ l1: string; l2: string; d: number }> = ({ l1, l2, d }) => (
  <div
    style={{
      width: d, height: d, borderRadius: "50%", background: DORADO,
      display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
      boxShadow: "0 12px 30px rgba(0,0,0,.35)", position: "relative", color: NAVY,
    }}
  >
    <div style={{ position: "absolute", inset: 12, borderRadius: "50%", border: `4px dashed ${NAVY}` }} />
    <div style={{ fontWeight: 700, fontSize: d * 0.17, lineHeight: 1 }}>{l1}</div>
    <div style={{ fontWeight: 500, fontSize: d * 0.1, marginTop: 6 }}>{l2}</div>
  </div>
);

const Intro: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: NAVY }}>
      <Img
        src={staticFile("intro.jpg")}
        style={{
          width: "100%", height: "100%", objectFit: "cover",
          scale: interpolate(f, [0, INTRO + SOLAPE], [1.12, 1.0], cl),
        }}
      />
      <AbsoluteFill
        style={{ background: "linear-gradient(180deg, rgba(8,42,92,0) 30%, rgba(8,42,92,.7) 50%, rgba(8,42,92,.97) 66%)" }}
      />
      <AbsoluteFill style={{ opacity: interpolate(f, [INTRO - 6, INTRO + 4], [1, 0], cl) }}>
      <div
        style={{
          position: "absolute", left: 64, top: 1040, fontSize: 34, fontWeight: 700, color: "white",
          letterSpacing: 4, opacity: interpolate(f, [4, 16], [0, 1], cl),
        }}
      >
        RACKSA ECUADOR · INGENIERÍA INTRALOGÍSTICA
        <div style={{ width: 120, height: 8, background: ROJO, marginTop: 14 }} />
      </div>
      <div
        style={{
          position: "absolute", left: 64, right: 64, top: 1130, color: "white", fontWeight: 700,
          fontSize: 104, lineHeight: 1.08,
          translate: interpolate(f, [6, 26], ["0px 60px", "0px 0px"], { ...cl, easing: salida }),
          opacity: interpolate(f, [6, 20], [0, 1], cl),
        }}
      >
        todo para{" "}
        <span style={{ position: "relative", whiteSpace: "nowrap" }}>
          <span
            style={{
              position: "absolute", left: -10, right: -10, top: "10%", bottom: "-2%", background: DORADO,
              transformOrigin: "left", scale: `${interpolate(f, [22, 38], [0, 1], { ...cl, easing: salida })} 1`,
            }}
          />
          <span style={{ position: "relative", color: interpolate(f, [22, 32], [0, 1], cl) > 0.5 ? NAVY : "white" }}>
            tu bodega
          </span>
        </span>
        <br />
        en un solo equipo
      </div>
      <div
        style={{
          position: "absolute", right: 60, top: 760,
          scale: interpolate(f, [18, 32], [0, 1], { ...cl, easing: Easing.spring({ damping: 12 }) }),
          rotate: interpolate(f, [18, INTRO], ["-30deg", "-8deg"], cl),
        }}
      >
        <Sello l1="ECUADOR" l2="a nivel nacional" d={250} />
      </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Estacion: React.FC<{ i: number }> = ({ i }) => {
  const f = useCurrentFrame();
  const e = ESTACIONES[i];
  return (
    <AbsoluteFill
      style={{
        clipPath: `inset(${interpolate(f, [0, SOLAPE], [100, 0], { ...cl, easing: salida })}% 0 0 0)`,
      }}
    >
      <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: PANEL_Y, overflow: "hidden" }}>
        <Img
          src={staticFile(e.foto)}
          style={{
            width: "100%", height: "100%", objectFit: "cover",
            scale: interpolate(f, [0, EST + SOLAPE], [1.1, 1.0], cl),
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

const Panel: React.FC = () => {
  const f = useCurrentFrame(); // relativo al inicio de las estaciones
  const activa = Math.min(5, Math.max(0, Math.floor(f / EST)));
  const local = f - activa * EST;
  const e = ESTACIONES[activa];
  return (
    <div
      style={{
        position: "absolute", left: 0, top: PANEL_Y, width: 1080, height: 1920 - PANEL_Y, background: NAVY,
        translate: interpolate(f, [0, SOLAPE], ["0px 640px", "0px 0px"], { ...cl, easing: salida }),
      }}
    >
      <div style={{ height: 10, background: DORADO }} />
      <div style={{ display: "flex", gap: 12, padding: "34px 64px 0" }}>
        {ESTACIONES.map((_, k) => (
          <div key={k} style={{ flex: 1, height: 10, borderRadius: 5, background: "rgba(255,255,255,.18)", overflow: "hidden" }}>
            <div
              style={{
                height: "100%", background: k === activa ? DORADO : "white",
                width: k < activa ? "100%" : k > activa ? "0%" : `${interpolate(local, [SOLAPE / 2, EST + SOLAPE / 2], [0, 100], cl)}%`,
              }}
            />
          </div>
        ))}
      </div>
      <div style={{ display: "flex", alignItems: "center", padding: "40px 64px 0", gap: 30 }}>
        <div
          style={{
            fontSize: 250, fontWeight: 700, color: DORADO, lineHeight: 1, width: 330,
            translate: interpolate(local, [0, 10], ["0px 40px", "0px 0px"], { ...cl, easing: salida }),
            opacity: interpolate(local, [0, 8], [0, 1], cl),
          }}
        >
          0{activa + 1}
        </div>
        <div
          style={{
            color: "white", fontWeight: 700, fontSize: 92, lineHeight: 1.05,
            translate: interpolate(local, [3, 14], ["50px 0px", "0px 0px"], { ...cl, easing: salida }),
            opacity: interpolate(local, [3, 11], [0, 1], cl),
          }}
        >
          {e.l1}
          <div style={{ fontWeight: 500, fontSize: 64, color: "rgba(255,255,255,.85)" }}>{e.l2}</div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 64, right: 64, top: 410, display: "flex", justifyContent: "space-between", fontSize: 31, fontWeight: 500, color: "rgba(255,255,255,.8)", whiteSpace: "nowrap", gap: 20 }}>
        <span>Diseño y montaje en todo Ecuador</span>
        <span style={{ color: DORADO, fontWeight: 700 }}>racksaecuador.com.ec</span>
      </div>
    </div>
  );
};

const Logo: React.FC<{ w: number }> = ({ w }) => (
  <Img src={staticFile("LOGO_RACKSA_transparente.png")} style={{ width: w }} />
);

const Tel: React.FC<{ t: string; d: number; f: number }> = ({ t, d, f }) => (
  <div
    style={{
      display: "flex", alignItems: "center", gap: 28, fontSize: 76, fontWeight: 700, color: "white",
      opacity: interpolate(f, [d, d + 8], [0, 1], cl),
      translate: interpolate(f, [d, d + 12], ["0px 30px", "0px 0px"], { ...cl, easing: salida }),
    }}
  >
    <div style={{ width: 78, height: 78, borderRadius: 39, background: DORADO, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <svg width="40" height="40" viewBox="0 0 24 24">
        <path fill={NAVY} d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.46.57 3.6a1 1 0 0 1-.25 1z" />
      </svg>
    </div>
    {t}
  </div>
);

const Cierre: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${AZUL} 0%, ${NAVY} 60%)`,
        clipPath: `inset(${interpolate(f, [0, 14], [PANEL_Y / 19.2, 0], { ...cl, easing: salida })}% 0 0 0)`,
        alignItems: "center", paddingTop: 330, fontFamily: "Poppins",
      }}
    >
      <div style={{ scale: interpolate(f, [6, 22], [0.7, 1], { ...cl, easing: Easing.spring({ damping: 14 }) }), opacity: interpolate(f, [6, 14], [0, 1], cl) }}>
        <Logo w={800} />
      </div>
      <div style={{ marginTop: 26, fontSize: 40, fontWeight: 700, color: DORADO, letterSpacing: 3, opacity: interpolate(f, [12, 20], [0, 1], cl) }}>
        CALIDAD Y CONFIANZA A TIEMPO
      </div>
      <div style={{ width: 760, height: 4, background: "rgba(255,255,255,.25)", margin: "50px 0 54px" }} />
      <div style={{ display: "flex", flexDirection: "column", gap: 40 }}>
        <Tel t="099 182 0185" d={16} f={f} />
        <Tel t="099 399 9091" d={21} f={f} />
        <Tel t="093 995 7939" d={26} f={f} />
      </div>
      <div style={{ marginTop: 56, fontSize: 46, fontWeight: 500, color: "white", opacity: interpolate(f, [32, 40], [0, 1], cl) }}>
        proyectos@racksaecuador.com.ec
      </div>
      <div style={{ marginTop: 16, fontSize: 46, fontWeight: 700, color: DORADO, opacity: interpolate(f, [36, 44], [0, 1], cl) }}>
        www.racksaecuador.com.ec
      </div>
    </AbsoluteFill>
  );
};

export const Reel: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: NAVY, fontFamily: "Poppins" }}>
      <Sequence durationInFrames={INTRO + SOLAPE}>
        <Intro />
      </Sequence>
      {ESTACIONES.map((_, i) => (
        <Sequence key={i} from={INTRO + i * EST} durationInFrames={EST + SOLAPE}>
          <Estacion i={i} />
        </Sequence>
      ))}
      <Sequence from={INTRO} durationInFrames={EST * 6 + SOLAPE}>
        <Panel />
      </Sequence>
      {/* logo fijo sobre las fotos */}
      <Sequence from={0} durationInFrames={INTRO + EST * 6 + SOLAPE}>
        <div style={{ position: "absolute", left: 48, top: 170, background: NAVY, padding: "14px 22px", borderRadius: 18, boxShadow: "0 8px 24px rgba(0,0,0,.35)" }}>
          <Logo w={250} />
        </div>
      </Sequence>
      <Sequence from={INTRO + EST * 6}>
        <Cierre />
      </Sequence>
    </AbsoluteFill>
  );
};

export const MyComposition = () => {
  return (
    <Composition id="ReelRacksa" component={Reel} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} />
  );
};
