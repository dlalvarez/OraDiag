# Documento Rector de OraDiag

## Propósito

Establecer la constitución del proyecto OraDiag para que toda fase, contribución y decisión futura mantenga foco en diagnóstico RCA de incidentes Oracle.

## Definición formal

OraDiag es una herramienta Python de diagnóstico técnico y RCA asistido para incidentes Oracle ya reportados o en curso. Su objetivo principal es identificar la causa probable del problema reportado, clasificar su dominio causante, documentar evidencia, declarar limitaciones y recomendar acciones seguras.

## Alcance

OraDiag puede consultar fuentes técnicas: sistema operativo, infraestructura accesible, listener, logs, alert log, catálogo, diccionario, vistas dinámicas Oracle, sesiones, bloqueos, waits, redo, archive, FRA, TEMP, UNDO, ASM, RAC, Multitenant y Standby cuando las fases futuras lo habiliten.

## Fuera de alcance

No es health check, capacity planning, auditoría funcional, explorador de datos de negocio ni caza-problemas genérico. No debe consultar tablas de negocio ni inferir significado funcional de los datos.

## Principios no negociables

1. **RCA primero**: encontrar causa probable del incidente, no listar anomalías sin relación.
2. **No tablas de negocio**: solo fuentes técnicas bajo alcance.
3. **Síntoma como pista**: el síntoma prioriza, pero no decide la causa.
4. **Evidencia obligatoria**: toda conclusión relevante necesita evidencia concreta o limitación explícita.
5. **Fallas controladas**: errores, timeouts, permisos insuficientes y respuestas parciales no deben tumbar la ejecución.
6. **Diagnóstico parcial**: es preferible entregar resultado limitado que quedar colgado.
7. **Roles causales claros**: separar causa principal, factores contribuyentes, hallazgos relacionados, incidentales, descartados y no evaluados.
8. **Revisiones OK visibles**: los resultados OK ayudan a descartar hipótesis.
9. **Recomendaciones seguras**: no sugerir acciones destructivas o irreversibles sin validación humana.
10. **Trazabilidad por fase**: cada fase debe actualizar documentación, matriz de trazabilidad, decisiones y backlog cuando corresponda.

## RCA vs health check

Un health check evalúa estado general. OraDiag investiga un incidente concreto. Un parámetro fuera de recomendación puede ser incidental si no explica el síntoma; una revisión OK puede ser central si descarta una hipótesis.

## Manejo de errores, timeouts y fallas parciales

Todo conector, consulta y collector futuro debe tener timeout y registrar `TIMEOUT`, `ERROR` o `SKIPPED` como resultado evaluable. Una falla de SSH no debe impedir intentar capas SQL si están disponibles; una falla SQL no debe impedir analizar logs o sistema operativo si existen credenciales.

## Evidencia y datos detallados

La evidencia puede incluir métricas, eventos de espera, wait_class, SQL_ID, sesiones, usuarios, módulos, servicios, inst_id, con_id, errores de alert log, estados de listener, uso de FRA, frecuencia de log switches, bloqueos y limitaciones de acceso.

## Recomendaciones

Las acciones recomendadas deben indicar alcance, riesgo, prerequisitos y necesidad de confirmación humana cuando aplique.
