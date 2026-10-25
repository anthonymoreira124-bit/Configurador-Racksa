/**
 * RACKSA ECUADOR · Borradores automáticos para prospectos
 * Se pega en Google Sheets: Extensiones > Apps Script.
 * No envía nada: deja los correos en Borradores de Gmail y tú decides cuáles enviar.
 *
 * Cada día hábil:
 *  1. Detecta qué borradores enviaste tú y marca la fila como «Contactado».
 *  2. Detecta respuestas, pedidos de baja y rebotes, y actualiza el CRM.
 *  3. Prepara el borrador del seguimiento 1 (3 días hábiles) y del último (7 días hábiles).
 *  4. Cierra como «Perdido / sin respuesta» a los 14 días sin respuesta.
 *  5. Prepara el primer correo para las filas «Por contactar» con correo (hasta el límite diario).
 */

// Columnas de la hoja CRM (1 = A)
var C = {ID:1, EMPRESA:2, PROV:3, PRIO:4, NOMBRE:5, CARGO:6, TEL:7, CORREO:8, CANAL:9, ESTADO:10,
         F1:11, ULTIMA:12, RESULTADO:13, PROXIMO:14, F_PROX:15, NOTAS:19, PASO:20, BORRADOR:21};
var NCOL = 21;
// PASO: 0 = nada · B1/B2/B3 = borrador preparado (paso 1, 2 o 3) · 1/2/3 = correo de ese paso ya enviado

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Racksa')
    .addItem('1. Instalar datos (solo la primera vez)', 'instalar')
    .addItem('Preparar borradores ahora', 'procesar')
    .addSeparator()
    .addItem('Activar todos los días (9:00, lunes a viernes)', 'activar')
    .addItem('Desactivar', 'desactivar')
    .addToUi();
}

function activar() {
  desactivar();
  ScriptApp.newTrigger('procesarDiario').timeBased().everyDays(1).atHour(9).create();
  aviso_('Listo: cada día hábil a las 9:00 tendrás los borradores en Gmail.');
}

function desactivar() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'procesarDiario') ScriptApp.deleteTrigger(t);
  });
}

function procesarDiario() {
  var d = new Date().getDay();
  if (d === 0 || d === 6) return;
  procesar();
}

function procesar() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return;
  try { procesar_(); } finally { lock.releaseLock(); }
}

function procesar_() {
  var ss = SpreadsheetApp.getActive();
  var cfg = leerConfig_(ss);
  var prospectos = leerProspectos_(ss);
  var plantillas = leerPlantillas_(ss);
  var sh = ss.getSheetByName('CRM');
  var n = sh.getLastRow() - 1;
  if (n < 1) return;
  var rng = sh.getRange(2, 1, n, NCOL);
  var datos = rng.getValues();
  var hoy = new Date(); hoy.setHours(0, 0, 0, 0);
  var nuevos = 0, log = [];

  for (var i = 0; i < datos.length; i++) {
    var f = datos[i];
    var correo = String(f[C.CORREO - 1] || '').split(/[\/;, ]+/)[0].trim().toLowerCase();
    if (!correo || correo.indexOf('@') < 0) continue;
    var estado = String(f[C.ESTADO - 1] || '');
    var paso = String(f[C.PASO - 1] || '0');
    var p = prospectos[f[C.ID - 1]] || {};
    var empresa = String(f[C.EMPRESA - 1] || p.empresa || '');
    var t = plantillas[p.grupo] || plantillas['Manufactura'];
    if (!t) continue;

    // 1. ¿Enviaste el borrador pendiente?
    if (paso.charAt(0) === 'B') {
      if (borradorSigue_(f[C.BORRADOR - 1])) continue; // aún sin enviar
      var k = parseInt(paso.slice(1), 10);
      f[C.PASO - 1] = k; f[C.BORRADOR - 1] = ''; f[C.ULTIMA - 1] = hoy; f[C.CANAL - 1] = 'Correo';
      if (k === 1) {
        f[C.ESTADO - 1] = 'Contactado'; f[C.F1 - 1] = hoy;
        f[C.RESULTADO - 1] = 'Primer correo enviado';
        f[C.PROXIMO - 1] = 'Seguimiento 1 (borrador automático)'; f[C.F_PROX - 1] = sumarHabiles_(hoy, cfg.d1);
      } else if (k === 2) {
        f[C.RESULTADO - 1] = 'Seguimiento 1 enviado';
        f[C.PROXIMO - 1] = 'Último seguimiento (borrador automático)';
        f[C.F_PROX - 1] = sumarHabiles_(new Date(f[C.F1 - 1] || hoy), cfg.d2);
      } else {
        f[C.RESULTADO - 1] = 'Último seguimiento enviado';
        f[C.PROXIMO - 1] = 'Llamar por teléfono (último intento)'; f[C.F_PROX - 1] = sumarHabiles_(hoy, 2);
      }
      log.push('Enviado por ti: ' + empresa);
      continue;
    }

    // 2. Respuestas, bajas y rebotes
    if (estado === 'Contactado' && f[C.F1 - 1]) {
      var r = revisarRespuesta_(correo, f[C.F1 - 1]);
      if (r) {
        f[C.ULTIMA - 1] = hoy;
        if (r === 'rebote') {
          f[C.ESTADO - 1] = 'No aplica'; f[C.RESULTADO - 1] = 'El correo rebotó: buscar otro contacto';
          f[C.PROXIMO - 1] = ''; f[C.F_PROX - 1] = '';
        } else if (r === 'baja') {
          f[C.ESTADO - 1] = 'No aplica'; f[C.RESULTADO - 1] = 'Pidió no recibir más correos';
          f[C.PROXIMO - 1] = ''; f[C.F_PROX - 1] = '';
        } else {
          f[C.ESTADO - 1] = 'Respondió / interesado'; f[C.RESULTADO - 1] = 'Respondió por correo';
          f[C.PROXIMO - 1] = 'Leer respuesta y llamar / agendar visita'; f[C.F_PROX - 1] = hoy;
        }
        log.push((r === 'respuesta' ? 'RESPONDIÓ: ' : r + ': ') + empresa);
        continue;
      }
    }

    // 3 y 4. Seguimientos y cierre
    if (estado === 'Contactado' && f[C.F1 - 1]) {
      var f1 = new Date(f[C.F1 - 1]);
      var dh = diasHabiles_(f1, hoy), dc = Math.floor((hoy - f1) / 86400000);
      var asuntoRe = 'Re: ' + rellenar_(t.asunto, f, p, cfg);
      if (paso === '1' && dh >= cfg.d1) {
        preparar_(f, 2, correo, asuntoRe, rellenar_(t.seg1, f, p, cfg), cfg);
        log.push('Borrador seguimiento 1: ' + empresa);
      } else if (paso === '2' && dh >= cfg.d2) {
        preparar_(f, 3, correo, asuntoRe, rellenar_(t.ultimo, f, p, cfg), cfg);
        log.push('Borrador último seguimiento: ' + empresa);
      } else if (paso === '3' && dc >= cfg.dCierre) {
        f[C.ESTADO - 1] = 'Perdido / sin respuesta'; f[C.RESULTADO - 1] = 'Sin respuesta a 3 correos';
        f[C.PROXIMO - 1] = 'Reintentar en 3 meses'; f[C.F_PROX - 1] = sumarDias_(hoy, 90);
      }
      continue;
    }

    // 5. Primer correo
    if (estado === 'Por contactar' && nuevos < cfg.maxDia && cfg.prioridades.indexOf(String(f[C.PRIO - 1])) >= 0) {
      preparar_(f, 1, correo, rellenar_(t.asunto, f, p, cfg), rellenar_(t.cuerpo, f, p, cfg), cfg);
      log.push('Borrador primer correo: ' + empresa);
      nuevos++;
    }
  }
  rng.setValues(datos);
  ss.toast(log.length ? log.length + ' cambios. Revisa Borradores en Gmail.' : 'Nada nuevo hoy.', 'Racksa', 8);
}

// ---------- auxiliares ----------

function preparar_(f, k, correo, asunto, cuerpo, cfg) {
  var dr = GmailApp.createDraft(correo, asunto, cuerpo, {name: cfg.remitente});
  f[C.PASO - 1] = 'B' + k; f[C.BORRADOR - 1] = dr.getId();
  f[C.NOTAS - 1] = agregar_(f[C.NOTAS - 1], 'Borrador ' + k + ' listo ' + fecha_(new Date()));
}

function borradorSigue_(id) {
  if (!id) return false;
  try { GmailApp.getDraft(String(id)).getMessage(); return true; } catch (e) { return false; }
}

function revisarRespuesta_(correo, desde) {
  var q = ' after:' + Utilities.formatDate(new Date(desde), Session.getScriptTimeZone(), 'yyyy/MM/dd');
  if (GmailApp.search('from:(mailer-daemon OR postmaster) "' + correo + '"' + q, 0, 1).length) return 'rebote';
  var th = GmailApp.search('from:' + correo + q, 0, 1);
  if (!th.length) return '';
  var msgs = th[0].getMessages();
  for (var k = msgs.length - 1; k >= 0; k--) {
    if (msgs[k].getFrom().toLowerCase().indexOf(correo) >= 0) {
      var txt = msgs[k].getPlainBody().trim().toLowerCase();
      if (/^no\b[\s.!]*($|\n)/.test(txt) || txt.indexOf('no deseo recibir') >= 0) return 'baja';
      break;
    }
  }
  return 'respuesta';
}

function rellenar_(txt, f, p, cfg) {
  var nombre = String(f[C.NOMBRE - 1] || '').trim() || cfg.saludo;
  var empresa = String(f[C.EMPRESA - 1] || p.empresa || '').replace(/\s*\(.*\)\s*$/, '');
  return String(txt || '')
    .replace(/\[Nombre\]/g, nombre)
    .replace(/\[Empresa\]/g, empresa)
    .replace(/\[Ciudad\]/g, p.ciudad || 'su ciudad')
    .replace(/\[Tu nombre\]/g, cfg.firma);
}

function leerConfig_(ss) {
  var v = ss.getSheetByName('Config').getRange(2, 1, 12, 2).getValues();
  var m = {}; v.forEach(function (r) { if (r[0]) m[String(r[0]).trim()] = String(r[1]).trim(); });
  return {
    firma: m['Tu nombre (firma)'] || 'Racksa Ecuador',
    remitente: m['Nombre del remitente'] || 'Racksa Ecuador',
    maxDia: parseInt(m['Correos nuevos por día'], 10) || 15,
    d1: parseInt(m['Días hábiles para seguimiento 1'], 10) || 3,
    d2: parseInt(m['Días hábiles para último seguimiento'], 10) || 7,
    dCierre: parseInt(m['Días para cerrar sin respuesta'], 10) || 14,
    prioridades: (m['Solo prioridad'] || 'A,B').toUpperCase().split(/[\s,;]+/),
    saludo: m['Saludo si no hay nombre'] || 'equipo de Logística'
  };
}

function leerProspectos_(ss) {
  var sh = ss.getSheetByName('Prospectos');
  var v = sh.getRange(2, 1, sh.getLastRow() - 1, 8).getValues();
  var m = {};
  v.forEach(function (r) { if (r[0]) m[r[0]] = {ciudad: r[4], empresa: r[5], grupo: r[7]}; });
  return m;
}

function leerPlantillas_(ss) {
  var sh = ss.getSheetByName('Mensajes');
  var v = sh.getRange(2, 1, sh.getLastRow() - 1, 6).getValues();
  var m = {};
  v.forEach(function (r) {
    if (r[1] === 'Correo') m[r[0]] = {asunto: r[2], cuerpo: r[3], seg1: r[4], ultimo: r[5]};
  });
  return m;
}

function diasHabiles_(a, b) {
  var n = 0, d = new Date(a); d.setHours(0, 0, 0, 0);
  while (d < b) { d.setDate(d.getDate() + 1); var w = d.getDay(); if (w !== 0 && w !== 6) n++; }
  return n;
}
function sumarHabiles_(a, k) {
  var d = new Date(a); d.setHours(0, 0, 0, 0);
  while (k > 0) { d.setDate(d.getDate() + 1); var w = d.getDay(); if (w !== 0 && w !== 6) k--; }
  return d;
}
function sumarDias_(a, k) { var d = new Date(a); d.setDate(d.getDate() + k); return d; }
function fecha_(d) { return Utilities.formatDate(d, Session.getScriptTimeZone(), 'dd/MM/yyyy'); }
function agregar_(a, b) { return a ? a + ' · ' + b : b; }
function aviso_(t) { try { SpreadsheetApp.getUi().alert(t); } catch (e) { Logger.log(t); } }

// ---------- instalación de datos (descarga la base desde GitHub) ----------

var BASE = 'https://raw.githubusercontent.com/anthonymoreira124-bit/configurador-racksa/claude/project-thread-2t3ewj/ventas/datos/';
var NAVY = '#082A5C', GOLD = '#FAC70C';

function instalar() {
  var ss = SpreadsheetApp.getActive();
  ss.setSpreadsheetTimeZone('America/Guayaquil');
  var crm = ss.getSheetByName('CRM');
  if (crm && crm.getLastRow() > 1 && crm.getRange('L2:L').getValues().some(function (r) { return r[0]; })) {
    aviso_('El CRM ya tiene datos de seguimiento. No se reinstaló para no borrar tu trabajo.');
    return;
  }
  var hojas = [['Inicio', 'inicio.csv'], ['Prospectos', 'prospectos.csv'], ['CRM', 'crm.csv'],
               ['Mensajes', 'mensajes.csv'], ['Config', 'config.csv']];
  hojas.forEach(function (h, i) {
    var datos = Utilities.parseCsv(UrlFetchApp.fetch(BASE + h[1]).getContentText('UTF-8'));
    var sh = ss.getSheetByName(h[0]) || ss.insertSheet(h[0], i);
    sh.clear(); sh.clearConditionalFormatRules();
    var ancho = Math.max.apply(null, datos.map(function (r) { return r.length; }));
    datos = datos.map(function (r) { while (r.length < ancho) r.push(''); return r; });
    sh.getRange(1, 1, datos.length, ancho).setNumberFormat('@').setValues(datos);
    if (h[0] !== 'Inicio') {
      sh.getRange(1, 1, 1, ancho).setBackground(NAVY).setFontColor('#FFFFFF').setFontWeight('bold').setWrap(true);
      sh.setFrozenRows(1);
    }
  });
  ss.getSheets().forEach(function (sh) {
    if (['Inicio', 'Resumen', 'Prospectos', 'CRM', 'Mensajes', 'Config'].indexOf(sh.getName()) < 0 && ss.getSheets().length > 5) ss.deleteSheet(sh);
  });
  formatear_(ss);
  aviso_('Datos instalados. Revisa la hoja «Config» y luego usa Racksa > Preparar borradores ahora.');
}

function formatear_(ss) {
  var ini = ss.getSheetByName('Inicio');
  ini.setColumnWidth(1, 30).setColumnWidth(2, 900);
  ini.getRange('B:B').setWrap(true);
  ini.getRange('B2').setFontSize(18).setFontWeight('bold').setFontColor(NAVY);

  var p = ss.getSheetByName('Prospectos'), np = p.getLastRow();
  [70, 70, 80, 110, 110, 260, 190, 180, 220, 230, 200, 230, 220, 230, 260, 120, 120, 220, 140]
    .forEach(function (w, i) { p.setColumnWidth(i + 1, w); });
  p.getRange(2, 1, np - 1, 19).setWrap(true).setVerticalAlignment('top');
  p.setFrozenColumns(2);
  var reglasP = [];
  [['A', GOLD], ['B', '#DCE6F5'], ['C', '#EEEEEE']].forEach(function (x) {
    reglasP.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo(x[0]).setBackground(x[1])
      .setRanges([p.getRange(2, 2, np - 1, 1)]).build());
  });
  p.setConditionalFormatRules(reglasP);
  if (p.getFilter()) p.getFilter().remove();
  p.getRange(1, 1, np, 19).createFilter();

  var c = ss.getSheetByName('CRM'), filas = 400;
  [60, 240, 110, 70, 160, 140, 150, 200, 100, 170, 100, 100, 220, 220, 100, 80, 90, 110, 240, 80, 150]
    .forEach(function (w, i) { c.setColumnWidth(i + 1, w); });
  c.setFrozenColumns(2);
  c.getRange(2, 11, filas, 2).setNumberFormat('dd/mm/yyyy');
  c.getRange(2, 15, filas, 1).setNumberFormat('dd/mm/yyyy');
  c.getRange(2, 18, filas, 1).setNumberFormat('"$"#,##0.00');
  c.getRange(2, 20, filas, 2).setNumberFormat('General');
  var pasos = c.getRange(2, 20, c.getLastRow() - 1, 1);
  pasos.setValues(pasos.getValues().map(function (r) { return [r[0] === '' ? 0 : Number(r[0])]; }));
  var f = [];
  for (var i = 2; i <= filas + 1; i++) f.push(['=IF(L' + i + '="","",TODAY()-L' + i + ')']);
  c.getRange(2, 16, filas, 1).setFormulas(f);
  var est = ['Por contactar', 'Contactado', 'Respondió / interesado', 'Visita agendada', 'Levantamiento en bodega',
             'Proforma enviada', 'Negociación', 'Ganado', 'Perdido / sin respuesta', 'No aplica'];
  c.getRange(2, 10, filas, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(est, true).build());
  c.getRange(2, 9, filas, 1).setDataValidation(SpreadsheetApp.newDataValidation()
    .requireValueInList(['LinkedIn', 'WhatsApp', 'Correo', 'Llamada', 'Visita', 'Referido', 'Feria'], true).build());
  var r = c.getRange(2, 1, filas, 21), R = SpreadsheetApp.newConditionalFormatRule;
  c.setConditionalFormatRules([
    R().whenFormulaSatisfied('=$J2="Ganado"').setBackground('#C6EFCE').setRanges([r]).build(),
    R().whenFormulaSatisfied('=OR($J2="Perdido / sin respuesta",$J2="No aplica")').setBackground('#EDEDED').setFontColor('#888888').setRanges([r]).build(),
    R().whenFormulaSatisfied('=AND($O2<>"",$O2<TODAY())').setBackground('#F8CBAD').setRanges([r]).build(),
    R().whenFormulaSatisfied('=AND($O2<>"",$O2-TODAY()<=3)').setBackground('#FFF2CC').setRanges([r]).build()
  ]);
  if (c.getFilter()) c.getFilter().remove();
  c.getRange(1, 1, filas + 1, 21).createFilter();

  var m = ss.getSheetByName('Mensajes');
  [180, 90, 260, 520, 420, 380].forEach(function (w, i) { m.setColumnWidth(i + 1, w); });
  m.getRange(2, 1, m.getLastRow() - 1, 6).setWrap(true).setVerticalAlignment('top');

  var cf = ss.getSheetByName('Config');
  cf.setColumnWidth(1, 260).setColumnWidth(2, 200).setColumnWidth(3, 520);
  cf.getRange(2, 2, cf.getLastRow() - 1, 1).setBackground('#FFF7D6');

  var s = ss.getSheetByName('Resumen') || ss.insertSheet('Resumen', 1);
  s.clear();
  s.getRange('A1').setValue('Embudo de ventas (CRM)').setFontWeight('bold').setFontSize(14).setFontColor(NAVY);
  s.getRange('A2:B2').setValues([['Estado', 'Empresas']]).setBackground(NAVY).setFontColor('#FFFFFF').setFontWeight('bold');
  est.forEach(function (e, k) { s.getRange(3 + k, 1, 1, 2).setValues([[e, '=COUNTIF(CRM!$J:$J,A' + (3 + k) + ')']]); });
  var k = est.length + 3;
  s.getRange(k, 1, 2, 2).setValues([['Monto en proformas (sin IVA)', '=SUM(CRM!R:R)'],
    ['Seguimientos vencidos', '=COUNTIFS(CRM!O:O,"<"&TODAY(),CRM!O:O,"<>")']]);
  s.getRange('D1').setValue('Prospectos por región').setFontWeight('bold').setFontSize(14).setFontColor(NAVY);
  s.getRange('D2:E2').setValues([['Región', 'Empresas']]).setBackground(NAVY).setFontColor('#FFFFFF').setFontWeight('bold');
  ['Costa', 'Sierra', 'Amazonía', 'Insular'].forEach(function (g, j) {
    s.getRange(3 + j, 4, 1, 2).setValues([[g, '=COUNTIF(Prospectos!$C:$C,D' + (3 + j) + ')']]);
  });
  s.setColumnWidth(1, 240).setColumnWidth(4, 160);
  ss.setActiveSheet(ini);
}
