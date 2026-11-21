# OraDiag

OraDiag es un framework Python para diagnóstico y análisis de causa raíz (RCA)
asistido de incidentes Oracle. Ayuda a investigar problemas ya reportados o en
curso, encontrar una causa probable soportada por evidencia técnica y entregar
recomendaciones seguras.

## Qué problema resuelve

Durante un incidente, OraDiag recolecta evidencia técnica de solo lectura,
la ancla a la ventana del incidente y la correlaciona para producir una
conclusión RCA: causa probable con su cadena de evidencia, factores
contribuyentes, hallazgos relacionados e incidentales, hipótesis descartadas y
lo que no pudo evaluarse, con un nivel de confianza explicado.

## Qué no es

- No es un health check general (eso es OraHealth).
- No es una herramienta de capacity planning.
- No es un buscador de anomalías sin relación causal.
- No consulta tablas de negocio ni investiga datos funcionales.
- No ejecuta acciones correctivas: solo las recomienda.

## Cómo obtiene evidencia

- **Núcleo SQL (obligatorio)**: consultas de solo lectura contra la instancia.
  Funciona igual en Amazon RDS for Oracle, on-premise y OCI.
- **Fuentes licenciadas (opcionales)**: ASH y AWR, solo con licencia de
  Diagnostics Pack declarada.
- **Adaptadores de plataforma (opcionales)**: métricas, eventos y logs de AWS
  RDS, SSH on-premise u OCI.

Plataforma inicial: Amazon RDS for Oracle Enterprise Edition.

## Principios

1. La evidencia manda sobre el síntoma.
2. La causa sale de una cadena de evidencia correlacionada con la ventana del
   incidente, no de la severidad de los hallazgos.
3. Errores, timeouts y permisos insuficientes producen diagnóstico parcial,
   nunca un cuelgue.
4. Las revisiones OK importan: descartan hipótesis.
5. Solo lectura estricta y mínimos privilegios.
6. Los packs de Oracle solo se usan con licencia declarada.
7. El núcleo depende solo de Oracle; las plataformas son adaptadores.

## Estado

Replanteamiento en curso en la rama `develop-claude`: constitución v2.0.0 y
documentación rectora actualizadas; siguiente paso, la planeación de la spec
`003-modelo-de-evidencia-y-motor-causal`. El código existente en `src/` y
`tests/` pertenece a una implementación anterior y será retirado.

## Documentación

- Constitución: `.specify/memory/constitution.md`
- Guía para Claude Code: `CLAUDE.md`
- Roadmap: `docs/ROADMAP.md`
- Arquitectura: `docs/ARCHITECTURE.md`
- Decisiones: `docs/DECISION_LOG.md`
