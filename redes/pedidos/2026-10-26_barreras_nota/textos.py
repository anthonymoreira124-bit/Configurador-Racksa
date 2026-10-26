"""Textos IG y LinkedIn de las 3 piezas de barreras contra inundación (2026-10-26), formato FORMATO_TEXTOS.md."""
import json, os
O = os.path.dirname(os.path.abspath(__file__))
CIERRE = ("💡 Diseñamos, implementamos y mantenemos bodegas que producen más.\n\n"
          "Racksa Ecuador\nCALIDAD Y CONFIANZA A TIEMPO\n📞 099 182 0185\n📞 099 399 9091\n📞 093 995 7939\n"
          "📩 proyectos@racksaecuador.com.ec\n🌐 https://www.racksaecuador.com.ec")
IG_TAGS = "#Guayaquil #Quito #Ecuador #Bodegas #Inundaciones"
LI_TAGS = "#Inundaciones #FenomenoDelNino #AceroInoxidable #SeguridadIndustrial #Bodegas #Logistica #Guayaquil #Ecuador"
PIEZAS = {
 "nota": dict(
   gancho="🌧️ Minimiza el impacto del fenómeno de El Niño en tu bodega.",
   checks=["Sistema de barreras contra inundación en acero inoxidable",
           "Para bodegas, plantas industriales y oficinas",
           "Instalación en sitio con nuestro equipo",
           "Cobertura a nivel nacional"],
   contexto="Las lluvias fuertes ya llegaron a Guayaquil y a todo el país. Una sola entrada de agua puede detener la operación y dañar mercadería y equipos.",
   pregunta="¿Tu bodega está lista para la próxima lluvia?"),
 "pronostico": dict(
   gancho="🌧️ El pronóstico no lo controlas. El agua en tu bodega, sí.",
   checks=["Barreras contra inundación en acero inoxidable",
           "Protegen los accesos de tu bodega o planta",
           "Fabricación e instalación en sitio",
           "Cobertura a nivel nacional"],
   contexto="Con semanas de lluvia por delante, lo que sí se puede decidir es cómo llega preparada tu bodega.",
   pregunta="¿Cuántos accesos de tu bodega quedan expuestos cuando llueve fuerte?"),
 "boletin": dict(
   gancho="📰 Bodegas que se preparan siguen operando cuando llueve.",
   checks=["Sistema de barreras contra inundación en acero inoxidable",
           "Para bodegas, plantas industriales y oficinas",
           "Fabricación e instalación en sitio, a nivel nacional",
           "Minimiza el impacto de El Niño en tu operación"],
   contexto="En temporada de lluvias, la diferencia entre parar y seguir trabajando está en los accesos protegidos a tiempo.",
   pregunta="¿Tu operación puede darse el lujo de parar por una inundación?"),
}


def ig(p):
    return p["gancho"] + "\n\n" + "\n".join("✅ " + c for c in p["checks"]) + "\n\n" + CIERRE + "\n\n" + IG_TAGS


def li(p):
    return (p["gancho"] + "\n\n" + p["contexto"] + "\n\n" + "\n".join("✅ " + c for c in p["checks"]) +
            "\n\n" + p["pregunta"] + "\n\n" + CIERRE + "\n\n" + LI_TAGS)


if __name__ == "__main__":
    out = {k: {"ig": ig(p), "li": li(p)} for k, p in PIEZAS.items()}
    json.dump(out, open(os.path.join(O, "textos.json"), "w"), ensure_ascii=False, indent=1)
    carpetas = {"nota": "2026-10-26_barreras_nota", "pronostico": "2026-10-26_barreras_pronostico", "boletin": "2026-10-26_barreras_boletin"}
    for k, c in carpetas.items():
        with open(os.path.join(O, "..", c, "TEXTOS.md"), "w") as f:
            f.write(f"# Barreras contra inundación · {k} (2026-10-26)\n\n## Instagram\n{out[k]['ig']}\n\n## LinkedIn\n{out[k]['li']}\n")
    print("ok")
