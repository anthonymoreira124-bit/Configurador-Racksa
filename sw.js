const CACHE = "racksa-0fe8b4c960be";
const ARCHIVOS = ["./", "fuentes/fuentes.css", "fuentes/ibm-plex-mono-latin-400-normal.woff2", "fuentes/ibm-plex-mono-latin-500-normal.woff2", "fuentes/poppins-latin-400-normal.woff2", "fuentes/poppins-latin-500-normal.woff2", "fuentes/poppins-latin-600-normal.woff2", "fuentes/poppins-latin-700-normal.woff2", "icono-192.png", "icono-512.png", "index.html", "libs/exceljs.min.js", "libs/jspdf.umd.min.js", "libs/pdf.min.js", "libs/pdf.worker.min.js", "manifest.webmanifest"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(ARCHIVOS))); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, {ignoreSearch: true}).then(r => r || fetch(e.request).catch(() => caches.match("./"))));
});
