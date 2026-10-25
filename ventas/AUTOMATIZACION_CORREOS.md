# Borradores automáticos de correos · Racksa Ecuador

El script no envía nada. Cada día hábil a las 9:00 deja los correos listos en **Borradores de Gmail** y actualiza el CRM. Tú revisas y das **Enviar**.

## Instalación (una sola vez, ~10 minutos, mejor en PC)
1. Sube `RACKSA_Prospectos_CRM_Nacional.xlsx` a Google Drive.
2. Ábrelo con **Hojas de cálculo de Google** y ve a *Archivo > Guardar como Hojas de cálculo de Google*.
3. En esa hoja: *Archivo > Configuración > Zona horaria* = **(GMT-05:00) Guayaquil**.
4. *Extensiones > Apps Script*. Borra lo que aparece, pega todo el contenido de `RACKSA_borradores_automaticos.gs` y guarda.
5. Recarga la hoja. Aparece el menú **Racksa**.
6. *Racksa > Preparar borradores ahora*. La primera vez Google pide permisos: elige tu cuenta, *Configuración avanzada > Ir al proyecto* y *Permitir*.
7. Revisa tus Borradores en Gmail. Si todo se ve bien: *Racksa > Activar todos los días*.

## Qué hace solo
| Momento | Acción |
|---|---|
| Día 0 | Borrador del primer correo (filas «Por contactar» con correo, prioridad A y B, máx. 15 por día) |
| Al enviarlo tú | La fila pasa a «Contactado» con fecha |
| 3 días hábiles | Borrador del seguimiento 1 |
| 7 días hábiles | Borrador del último seguimiento y recordatorio de llamar |
| 14 días sin respuesta | «Perdido / sin respuesta», reintentar en 3 meses |
| Si responden | «Respondió / interesado» y próximo paso «llamar / agendar visita» |
| Si responden NO o el correo rebota | «No aplica» |

## Tips
- Para que se preparen más correos, completa la columna **Correo** del CRM (solo 12 empresas lo traen verificado). Si pones el **nombre** del contacto, el saludo sale personalizado.
- Firma, límite diario y prioridades: hoja **Config**.
- No toques las columnas «Paso automático» ni «ID borrador».
- LinkedIn y WhatsApp siguen siendo manuales: textos en la hoja «Mensajes».
