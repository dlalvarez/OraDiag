# Documento Rector de OraDiag

## Propósito

Explicar en lenguaje operativo qué es OraDiag, qué no es y cómo razona. La
fuente normativa es `.specify/memory/constitution.md`; este documento la
complementa y, si la contradice, prevalece la constitución.

## Definición

OraDiag es una herramienta Python de diagnóstico técnico y RCA asistido para
incidentes Oracle ya reportados o en curso. Su objetivo es identificar la causa
probable del incidente, clasificar su dominio causante, exponer la cadena de
evidencia que la sostiene, declarar lo que no pudo evaluarse y recomendar
acciones seguras.

## Alcance

OraDiag obtiene evidencia de tres tipos de fuentes, en este orden de prioridad:

1. **Núcleo SQL (obligatorio).** Consultas de solo lectura contra la instancia:
   diccionario, vistas dinámicas `V$`/`GV$`, vistas `DBA_` técnicas, sesiones,
   bloqueos, waits, métricas recientes, estadísticas del host vistas desde la
   base, redo, TEMP, UNDO, FRA y alert log por SQL. Funciona igual en Amazon
   RDS for Oracle, on-premise y OCI.
2. **Fuentes licenciadas (opcionales).** ASH y AWR, solo si el target declara
   la licencia de Diagnostics Pack y la base es coherente con esa declaración.
3. **Adaptadores de plataforma (opcionales).** Métricas, eventos y logs propios
   de la plataforma (AWS RDS, SSH en on-premise, OCI). Agregan evidencia de host,
   volumen e infraestructura; el diagnóstico funciona sin ellos.

Plataforma inicial: Amazon RDS for Oracle Enterprise Edition.

## Fuera de alcance

No es health check, capacity planning, auditoría funcional, explorador de datos
de negocio ni buscador genérico de anomalías. No consulta tablas de negocio ni
infiere significado funcional de los datos. No ejecuta acciones correctivas:
solo las recomienda.

## Principios no negociables

1. **RCA primero**: encontrar la causa probable del incidente, no listar anomalías.
2. **Evidencia obligatoria**: toda conclusión necesita evidencia o una limitación explícita.
3. **Síntoma como pista**: el síntoma prioriza, pero no decide la causa.
4. **Correlación causal**: la causa sale de una cadena de evidencia correlacionada con la ventana del incidente, no de la severidad.
5. **Roles causales claros**: causa principal, factores contribuyentes, hallazgos relacionados, incidentales, descartados y no evaluados.
6. **Revisiones OK visibles**: los OK descartan hipótesis y explican la confianza.
7. **Fallas controladas**: errores, timeouts y permisos insuficientes producen diagnóstico parcial, nunca un cuelgue.
8. **Solo lectura**: únicamente `SELECT`; nada que cambie el estado de la base o del servidor.
9. **Licencias explícitas**: los packs de Oracle solo se usan con licencia declarada.
10. **Portabilidad**: el núcleo depende solo de Oracle; las plataformas son adaptadores.
11. **Sin datos de negocio**: solo fuentes técnicas; texto de SQL y binds se tratan como sensibles.
12. **Recomendaciones seguras**: con alcance, riesgo, prerrequisitos y validación humana cuando aplique.

## RCA frente a health check

Un health check evalúa el estado general. OraDiag investiga un incidente
concreto en una ventana de tiempo. Un parámetro fuera de recomendación es
incidental si no explica el síntoma en esa ventana; una revisión OK puede ser
central si descarta una hipótesis.

## Ventana del incidente

Todo diagnóstico se ancla a una ventana temporal: "ahora" para incidentes en
curso o un intervalo declarado para incidentes pasados. La ventana determina
qué evidencia es relevante y qué hallazgos son incidentales. Sin fuentes con
histórico (packs o adaptadores), un incidente pasado se diagnostica con
confianza reducida y así se declara.

## Fallas parciales

Cada fuente es independiente. Si un adaptador de plataforma falla, el núcleo
SQL sigue. Si la conexión SQL falla, los adaptadores configurados aún pueden
aportar evidencia de plataforma. Si nada es accesible, el resultado es un
diagnóstico `Indeterminado` que explica exactamente qué se intentó y por qué
falló.

## Recomendaciones

Toda recomendación indica alcance, riesgo, prerrequisitos y si requiere
validación humana o ventana de mantenimiento. Nunca se ejecuta desde OraDiag.
