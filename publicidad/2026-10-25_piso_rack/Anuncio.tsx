import React from "react";
import { AbsoluteFill, Img, Still, staticFile } from "remotion";

// Pieza 4:5 "foto anotada": rack selectivo + piso epóxico (2026-10-25)
const NAVY = "#082A5C";
const DORADO = "#FAC70C";
const ROJO = "#E1462A";
const FOTO_H = 990;

type Nota = { x: number; y: number; px: number; py: number; t1: string; t2: string };

const Anotacion: React.FC<Nota> = ({ x, y, px, py, t1, t2 }) => (
  <>
    <svg width={1080} height={FOTO_H} style={{ position: "absolute", left: 0, top: 0 }}>
      <line x1={x} y1={y} x2={px} y2={py} stroke={DORADO} strokeWidth={6} />
      <circle cx={px} cy={py} r={22} fill={DORADO} fillOpacity={0.35} />
      <circle cx={px} cy={py} r={12} fill={DORADO} stroke={NAVY} strokeWidth={4} />
    </svg>
    <div
      style={{
        position: "absolute", left: x, top: y, translate: "0 -50%", background: NAVY,
        borderLeft: `12px solid ${DORADO}`, padding: "16px 26px 18px", boxShadow: "0 10px 26px rgba(0,0,0,.35)",
      }}
    >
      <div style={{ color: "white", fontWeight: 700, fontSize: 46, lineHeight: 1.05 }}>{t1}</div>
      <div style={{ color: DORADO, fontWeight: 500, fontSize: 32, marginTop: 4 }}>{t2}</div>
    </div>
  </>
);

const Tel: React.FC<{ t: string }> = ({ t }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 12, fontSize: 38, fontWeight: 700, color: "white", whiteSpace: "nowrap" }}>
    <div style={{ width: 46, height: 46, borderRadius: 23, background: DORADO, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <svg width="26" height="26" viewBox="0 0 24 24">
        <path fill={NAVY} d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.46.57 3.6a1 1 0 0 1-.25 1z" />
      </svg>
    </div>
    {t}
  </div>
);

export const Anuncio: React.FC = () => (
  <AbsoluteFill style={{ background: NAVY, fontFamily: "Poppins" }}>
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: FOTO_H, overflow: "hidden" }}>
      <Img src={staticFile("piso_rack_c.jpg")} style={{ width: 1080, height: 1000 }} />
      <Anotacion x={40} y={120} px={470} py={330} t1="Rack selectivo" t2="2.000 kg por nivel" />
      <Anotacion x={600} y={900} px={480} py={852} t1="Piso epóxico" t2="con señalización" />
    </div>
    <div style={{ position: "absolute", left: 0, top: FOTO_H, width: 1080, height: 10, background: DORADO }} />
    <div style={{ position: "absolute", left: 56, right: 56, top: FOTO_H + 34, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <div>
        <div style={{ color: "white", fontWeight: 700, fontSize: 56, lineHeight: 1.05 }}>
          Del{" "}
          <span style={{ background: DORADO, color: NAVY, padding: "0 12px" }}>piso</span> al último nivel
        </div>
        <div style={{ color: "rgba(255,255,255,.85)", fontWeight: 500, fontSize: 30, marginTop: 10 }}>
          Un solo equipo · a nivel nacional
        </div>
      </div>
      <Img src={staticFile("LOGO_RACKSA_transparente.png")} style={{ width: 215 }} />
    </div>
    <div style={{ position: "absolute", left: 56, right: 56, top: FOTO_H + 180, display: "flex", justifyContent: "space-between" }}>
      <Tel t="099 182 0185" />
      <Tel t="099 399 9091" />
      <Tel t="093 995 7939" />
    </div>
    <div style={{ position: "absolute", left: 56, right: 56, top: FOTO_H + 262, display: "flex", justifyContent: "space-between", fontSize: 27, fontWeight: 500, color: "white", gap: 20, whiteSpace: "nowrap" }}>
      <span>proyectos@racksaecuador.com.ec</span>
      <span style={{ color: DORADO, fontWeight: 700 }}>www.racksaecuador.com.ec</span>
    </div>
    <div style={{ position: "absolute", left: 0, bottom: 0, width: 1080, height: 8, background: ROJO }} />
  </AbsoluteFill>
);

export const AnuncioStill = () => <Still id="PisoRack" component={Anuncio} width={1080} height={1350} />;
