# Graph Report - Configurador-Racksa  (2026-11-06)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 343 nodes · 1305 edges · 16 communities (11 shown, 5 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `12a8fe75`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15

## God Nodes (most connected - your core abstractions)
1. `fmt()` - 40 edges
2. `build3D()` - 39 edges
3. `PER()` - 35 edges
4. `svgEl()` - 35 edges
5. `drawPlan()` - 31 edges
6. `LB()` - 30 edges
7. `MZR()` - 30 edges
8. `render()` - 30 edges
9. `drawPlanManual()` - 29 edges
10. `DI()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `drawFrontPercha()` --calls--> `BANDEJAS_NIVEL()`  [EXTRACTED]
  .graphify-src/index.html.js → .graphify-src/index.html.js  _Bridges community 0 → community 4_
- `descargarDXF()` --calls--> `calc()`  [EXTRACTED]
  .graphify-src/index.html.js → .graphify-src/index.html.js  _Bridges community 0 → community 2_
- `descargarVisor3D()` --calls--> `calc()`  [EXTRACTED]
  .graphify-src/index.html.js → .graphify-src/index.html.js  _Bridges community 0 → community 5_
- `render()` --calls--> `calc()`  [EXTRACTED]
  .graphify-src/index.html.js → .graphify-src/index.html.js  _Bridges community 0 → community 6_
- `calcAuto()` --calls--> `niveles()`  [EXTRACTED]
  .graphify-src/index.html.js → .graphify-src/index.html.js  _Bridges community 0 → community 8_

## Import Cycles
- None detected.

## Communities (16 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (62): altOver(), areaEpoxi(), BANDEJAS_NIVEL(), calc(), calcAlt(), calcAuto(), calcManual(), capaVOk() (+54 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (43): ALM, armarDxf(), _best, CAMIONES, CAPAS_DXF, celdaBloqueada(), CHKS, CLARO (+35 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (42): cargarPdfJs(), CONDICIONES(), condLineas(), conSectorAsync(), construirExcel(), construirProforma(), descargarDXF(), descargarExcel() (+34 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (40): alzadoMuro(), anden3D(), caja3(), camion3D(), cil3(), codigoElem(), columnasDe(), conExterior() (+32 more)

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (37): aplicarDeck(), cajaPallet(), cargasPlan(), cB(), columnaPlan(), cota(), cotasInicio(), cR() (+29 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (34): aplicarSombras(), build3D(), camara(), capturas3D(), crearEquipo(), deck3D(), descargarVisor3D(), diFondo() (+26 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (32): abrirProyecto(), agregarFotos(), agregarSector(), aplicarCfg(), cargar(), cfgSector(), clon(), comprimir() (+24 more)

### Community 7 - "Community 7"
Cohesion: 0.28
Nodes (15): abrirGestor(), almAbrir(), almBorrar(), almCarpeta(), almGuardar(), almIni(), almListar(), almMeta() (+7 more)

### Community 8 - "Community 8"
Cohesion: 0.23
Nodes (13): aplicarSistema(), autoH(), diPrimerCarril(), fromInput(), maxBajoPiso(), maxNiveles(), maxNivelesDI(), niveles() (+5 more)

### Community 9 - "Community 9"
Cohesion: 0.29
Nodes (8): cajetin(), confirmar(), dialogo(), esc(), fechaCorta(), pedirTexto(), pintarAreaBar(), pintarGestor()

### Community 10 - "Community 10"
Cohesion: 0.67
Nodes (3): etiqueta3D(), zonaAB(), zonas3D()

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build3D()` connect `Community 5` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 6`, `Community 10`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.1195134849286092 - nodes in this community are weakly interconnected._
- **Why does `fmt()` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.043478260869565216 - nodes in this community are weakly interconnected._
- **Why does `svgEl()` connect `Community 4` to `Community 0`, `Community 1`, `Community 3`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.11382113821138211 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.10512820512820513 - nodes in this community are weakly interconnected._