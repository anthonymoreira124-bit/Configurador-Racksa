---
name: racksa-videos-dinamicos
description: Úsala cuando Anthony pida editar o crear un video/reel dinámico de Racksa Ecuador (cortes rápidos, textos animados, subtítulos, motion graphics) con HyperFrames, Remotion o ffmpeg.
---

# Videos dinámicos Racksa Ecuador

Estilo tomado de 2 reels de referencia (publicidad/videos/referencias/): cortes cada 2–3 s,
paneles gráficos que entran sobre el video, rótulos "PASO 1/2/3", palabra clave resaltada
en color, subtítulos de 1 a 3 palabras, cierre con llamado a la acción.

## Carpetas (en /mnt/project-files/racksa_proyecto/publicidad/videos/)
- `crudos/`: clips de Anthony (obra, montaje, bodega, montacargas).
- `referencias/`: videos de otros creadores cuyo estilo queremos.
- `exports/`: videos terminados (MP4 1080x1920, H.264, <10 MB para Typefully).

## Hoja de estilo Racksa (estilo.md)
- Letras: Poppins Bold/ExtraBold, mayúsculas en titulares; una palabra clave en dorado #FAC70C.
- Colores: azul #0F4C9D, azul profundo #082A5C, dorado #FAC70C, rojo #E1462A, blanco.
- Subtítulos: 1 a 3 palabras, blancos con borde/sombra, lejos de los bordes (zona segura
  IG/TikTok: 250 px arriba, 350 px abajo).
- Cortes: cada 2–3 s; zoom suave (Ken Burns) en fotos; transiciones de barrido/empuje.
- Duración: 12–20 s. Mostrar los clips "antes" completos.
- Cierre OBLIGATORIO (~3.6 s): publicidad/redes/plantillas/cierre_video_con_web.jpg
  (logo, 3 teléfonos, correo y web).
- Datos: solo afirmaciones aprobadas (publicidad/datos/DATOS_APROBADOS.md). Escribir "Racksa Ecuador".
- Antes de renderizar: proponer el guion en TEXTO (escenas + textos) y esperar aprobación.

## Instalar en cada hilo (el contenedor es temporal)
```bash
pip install -q yt-dlp                       # bajar videos de referencia
npm i -g hyperframes@0.8.226                # o usar npx hyperframes
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
export HYPERFRAMES_SKIP_SKILLS=1            # las skills ya están en .claude/skills del repo
hyperframes telemetry disable
```
- cdn.jsdelivr.net está bloqueado: copiar `recursos/gsap.min.js` (de esta skill) al proyecto
  y cambiar en index.html el `<script src="https://cdn.jsdelivr.net/.../gsap.min.js">` por `gsap.min.js`.
- Remotion (alternativa): render con `--browser-executable=` la misma ruta de chrome-headless-shell.
- Subtítulos automáticos (`hyperframes transcribe`, Whisper) necesitan descargar el modelo
  desde huggingface.co; si da 403, el dominio no está permitido en la red del proyecto.
  Mientras tanto, escribir los textos a mano.

## Flujo
1. `hyperframes init <nombre> --non-interactive --resolution portrait` en un directorio de trabajo.
2. Leer la skill `hyperframes` (contrato de render) y usar `hyperframes-registry` para
   transiciones/títulos ya hechos antes de construirlos a mano.
3. Componer: clips de `crudos/` + paneles con la paleta + rótulos + cierre.
4. `hyperframes check`, luego `hyperframes snapshot` para revisar fotogramas.
5. `hyperframes render -o salida.mp4`; si pesa >10 MB, re-codificar a ~4.5 Mbps con ffmpeg.
6. Guardar en `exports/` y entregar a Anthony.
