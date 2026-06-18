# OraDiag

OraDiag (también referido como OraRCA en discusiones iniciales) es un framework Python para diagnóstico y análisis de causa raíz (RCA) asistido de incidentes Oracle. Su propósito es ayudar a investigar problemas ya reportados o en curso, encontrar una causa probable soportada por evidencia técnica y entregar recomendaciones seguras.

## Qué problema resuelve

OraDiag busca reducir la ambigüedad durante incidentes Oracle mediante una investigación ordenada por capas: sistema operativo, infraestructura, listener, logs, catálogo, diccionario, vistas dinámicas, sesiones, bloqueos, waits, redo, almacenamiento y componentes Oracle bajo alcance. La salida esperada no será una lista indiscriminada de anomalías, sino una conclusión RCA con causa probable, factores contribuyentes, hallazgos relacionados, hallazgos incidentales, revisiones descartadas y revisiones no evaluadas.

## Qué no es OraDiag

- No es un health check general.
- No es una herramienta de capacity planning.
- No es un caza-problemas que reporte todo lo extraño sin relación causal.
- No investiga datos funcionales ni consulta tablas de negocio.
- No reemplaza al análisis funcional, de aplicación o de datos fuera del alcance técnico.

## Diferencia frente a OraHealth y OraCapacity

- **OraHealth**: orientado a estado general y cumplimiento de salud operativa.
- **OraCapacity**: orientado a tendencias, capacidad y planificación futura.
- **OraDiag**: orientado a RCA de incidentes específicos ya ocurridos o reportados, priorizando evidencia concreta y causalidad probable.

## Estado inicial del proyecto

La Fase 0 es exclusivamente documental. Este repositorio queda preparado para fases futuras, pero no contiene CLI real, conectores, collectors, checks, consultas SQL, motor RCA funcional, reportes reales ni histórico SQLite.

## Principios rectores

1. La evidencia manda sobre el síntoma.
2. El síntoma es una pista opcional, nunca una verdad diagnóstica.
3. Toda conclusión relevante debe tener evidencia o declarar sus limitaciones.
4. Los errores, timeouts y fallas parciales deben producir diagnóstico parcial, no crashes no controlados.
5. Las revisiones OK también son importantes porque descartan hipótesis.
6. Se debe diferenciar causa principal, factores contribuyentes, hallazgos relacionados e incidentales.
7. No se consultan tablas de negocio.
8. Las recomendaciones deben ser seguras, explícitas y proporcionales a la evidencia.

## Roadmap resumido

El proyecto avanzará desde gobierno documental, CLI y modelos base, conectividad por capas, discovery Oracle, alert log, usuario/autenticación, sesiones/bloqueos, wait analysis, storage, redo, correlación RCA, reportes, componentes avanzados RAC/ASM/Multitenant/Standby, histórico de incidentes y extensiones futuras.

Consulte `docs/ROADMAP.md` para el detalle formal por fase.
