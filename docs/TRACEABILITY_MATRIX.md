# Matriz de trazabilidad

Relaciona cada principio de la constitución v2.0.0 con los documentos que lo
desarrollan, las specs donde se materializa y las pruebas que lo protegen. Cada
spec actualiza esta matriz al cerrarse.

| Principio | Documentos | Specs | Pruebas que lo protegen |
|---|---|---|---|
| I. RCA, no health check | DOCUMENTO_RECTOR, RCA_MODEL | 003-012 | Anomalías sin relación con el incidente quedan incidentales |
| II. La evidencia manda | EVIDENCE_MODEL, RCA_MODEL | 003-012 | Diagnóstico sin evidencia no produce causa principal |
| III. Síntoma como pista | SYMPTOM_HANDLING | 003, 009 | Síntoma contradictorio con la evidencia se reporta |
| IV. Separación causal | RCA_MODEL | 003, 009 | Roles causales por escenario de laboratorio |
| V. OK visibles | EVIDENCE_MODEL, RCA_MODEL | 003-012 | Reporte incluye OK relevantes y `ruled_out` |
| VI. Dominios causales | CAUSAL_DOMAINS | 003, 005-011 | Casos por dominio; Datos exige dominios técnicos evaluados |
| VII. Sin tablas de negocio | SECURITY_AND_ACCESS, CAUSAL_DOMAINS | 004-012 | Guardrail: solo vistas de la lista permitida |
| VIII. Fallas controladas | ERROR_HANDLING_AND_TIMEOUTS | 004-010 | Timeouts, ORA- y conexión fallida producen limitaciones |
| IX. Seguridad y privilegios | SECURITY_AND_ACCESS | 004, 010 | Sin secretos en logs y reportes; generador de grants |
| X. Contratos y pruebas | EVIDENCE_MODEL, ARCHITECTURE | 003-012 | Snapshot de JSON; motor independiente del origen |
| XI. Trazabilidad | CONTRIBUTING, esta matriz | Todas | Revisión de PR contra plantilla |
| XII. Núcleo portable | ARCHITECTURE | 003, 004, 010 | Guardrail de imports del núcleo |
| XIII. Licencias explícitas | ARCHITECTURE, SECURITY_AND_ACCESS | 004, 006 | Sin licencia declarada no se ejecuta ninguna consulta licenciada |
| XIV. Solo lectura | SECURITY_AND_ACCESS | 004-012 | Guardrail: solo sentencias `SELECT` |
| XV. Correlación causal | RCA_MODEL | 003, 009 | Hallazgo grave fuera de la ventana queda incidental |
