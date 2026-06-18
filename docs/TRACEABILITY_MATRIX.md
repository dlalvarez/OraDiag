# Matriz de trazabilidad

| Principio rector | Archivo fuente | Fases relacionadas | Pruebas futuras |
|---|---|---:|---|
| No consultar tablas de negocio | DOCUMENTO_RECTOR, SECURITY_AND_ACCESS, CAUSAL_DOMAINS | 0-14 | Validar que collectors SQL usan solo fuentes técnicas |
| OraDiag no es health check | README, DOCUMENTO_RECTOR, RCA_MODEL | 0-14 | Casos donde anomalías incidentales no sean causa principal |
| Diferenciar causa principal e incidental | RCA_MODEL, EVIDENCE_MODEL | 1,10,11 | Pruebas de roles causales |
| Síntoma como pista, no verdad | SYMPTOM_HANDLING, DOCUMENTO_RECTOR | 1,10 | Síntoma contradictorio con evidencia |
| Manejo controlado de timeouts | ERROR_HANDLING_AND_TIMEOUTS | 2-14 | Timeouts simulados por capa |
| Evidencia obligatoria | EVIDENCE_MODEL, RCA_MODEL | 1,10,11 | Diagnóstico sin evidencia debe fallar validación |
| Mostrar revisiones OK | EVIDENCE_MODEL, DOCUMENTO_RECTOR | 4-11 | Reporte incluye OK y descartados |
| Clasificar dominio causante | CAUSAL_DOMAINS, RCA_MODEL | 10-14 | Casos por dominio |
| Soportar perfiles | EXECUTION_PROFILES, ROADMAP | 1-14 | Perfil selecciona revisiones sin cambiar RCA |
| Salidas console/json/markdown/html | ARCHITECTURE, ROADMAP | 11 | Snapshots de reportes |
