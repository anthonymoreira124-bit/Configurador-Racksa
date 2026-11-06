#!/usr/bin/env bash
# Regenera el grafo de conocimiento (graphify) del configurador.
# La lógica de la app vive dentro de index.html; graphify no analiza JS embebido
# en HTML, así que se extrae el <script> principal a .graphify-src/index.html.js
# conservando los MISMOS números de línea que index.html.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v graphify >/dev/null || pip install -q graphifyy
mkdir -p .graphify-src
python3 - <<'PY'
import re
s = open('index.html', encoding='utf-8').read()
best = max(re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, re.S),
           key=lambda m: m.group(1).count('\n') if 'const LOGO' in m.group(1) else -1)
pre = s[:best.start(1)].count('\n')
code = re.sub(r'"data:[^"]{200,}"', '"data:..."', best.group(1))
open('.graphify-src/index.html.js', 'w', encoding='utf-8').write('\n' * pre + code)
PY
graphify extract . --code-only --no-gitignore --force >/dev/null
graphify cluster-only . --no-label >/dev/null
echo "Grafo actualizado: graphify-out/graph.json"
