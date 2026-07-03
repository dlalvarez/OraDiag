<!--
Sync Impact Report
Version change: plantilla inicial -> 1.0.0
Modified principles:
- N/A -> I. OraDiag es RCA, no health check
- N/A -> II. La evidencia manda
- N/A -> III. El sintoma es pista, no verdad
- N/A -> IV. Separacion causal obligatoria
- N/A -> V. Revisiones OK visibles
- N/A -> VI. Dominios causales y frontera de datos
- N/A -> VII. Prohibicion estricta de tablas de negocio
- N/A -> VIII. Fallas controladas y diagnostico parcial
- N/A -> IX. Seguridad, minimos privilegios y recomendaciones seguras
- N/A -> X. Perfiles, contratos, formatos y pruebas gobernados por el modelo
- N/A -> XI. Trazabilidad, roadmap y control de desviaciones
Added sections:
- Restricciones Tecnicas y de Alcance
- Proceso SDD, Specs y Pull Requests
- Agrupacion Oficial Inicial de Specs
- Asuntos Pendientes y Aclaraciones Requeridas
Removed sections:
- Placeholder SECTION_2_NAME
- Placeholder SECTION_3_NAME
Templates requiring updates:
- updated .specify/templates/plan-template.md
- updated .specify/templates/spec-template.md
- updated .specify/templates/tasks-template.md
- n/a .specify/templates/commands/*.md (no existe directorio de comandos)
Follow-up TODOs:
- Alinear docs/ROADMAP.md con la agrupacion 001 si se ratifica el alcance de
  RCA minimo simulado y salidas console/json en Fase 1.
-->
# Constitucion de OraDiag/OraRCA

## Core Principles

### I. OraDiag es RCA, no health check
OraDiag MUST investigar incidentes Oracle ya reportados o en curso. Su objetivo
constitucional es identificar una causa probable soportada por evidencia tecnica,
no listar anomalias generales, evaluar salud preventiva, hacer capacity planning,
auditar funcionalmente, explorar datos de negocio ni convertirse en un
caza-problemas generico. Toda spec MUST preservar la diferencia entre OraDiag,
OraHealth y OraParity; las decisiones de esos proyectos no se pueden copiar por
analogia automatica.

Rationale: el valor de OraDiag esta en reducir ambiguedad durante incidentes
concretos mediante RCA, no en ampliar el alcance por similitud con otros
proyectos.

### II. La evidencia manda
Toda conclusion relevante MUST estar soportada por evidencia positiva, evidencia
negativa o una limitacion explicita. OraDiag MUST declarar cuando una causa es
probable, cuando una hipotesis es debil y cuando no existe evidencia suficiente.
El sistema MUST NOT emitir causa probable, severidad causal o recomendacion
operativa como certeza sin evidencia trazable.

Rationale: una conclusion sin evidencia crea ruido, sesgo y riesgo operativo.

### III. El sintoma es pista, no verdad
El sintoma reportado por el usuario MAY priorizar revisiones, ordenar hipotesis
y aportar contexto de presentacion, pero MUST NOT decidir la causa por si solo.
Si el sintoma contradice la evidencia, OraDiag MUST reportar la contradiccion.
Si no hay sintoma, el analisis MUST usar `unspecified` o el perfil aplicable sin
fabricar causalidad.

Rationale: el sintoma puede introducir sesgo de anclaje; la evidencia tecnica
debe prevalecer.

### IV. Separacion causal obligatoria
Todo diagnostico relevante MUST diferenciar, segun evidencia disponible:
`primary_cause`, `contributing_factor`, `related_finding`,
`incidental_finding`, `ruled_out`, `not_evaluated` y `unknown`. OraDiag MUST NOT
confundir un hallazgo incidental, una anomalia real o una severidad tecnica con
la causa probable principal sin correlacion suficiente.

Rationale: separar roles causales evita reportes ruidosos y recomendaciones
desproporcionadas.

### V. Revisiones OK visibles
Las revisiones OK MUST conservarse y mostrarse cuando ayuden a descartar
hipotesis, explicar confianza o justificar que un dominio no tiene evidencia
causal. Un resultado OK MAY ser evidencia negativa importante y MUST NOT
ocultarse por el solo hecho de no ser un problema.

Rationale: el RCA necesita evidencia negativa para reducir ambiguedad y evitar
conclusiones incompletas.

### VI. Dominios causales y frontera de datos
Todo diagnostico relevante MUST intentar clasificar el causante probable en uno
de estos dominios cuando exista evidencia suficiente: Sistema Operativo,
Infraestructura, Almacenamiento, Base de datos, Aplicacion, Usuario, Datos o
Indeterminado. El dominio Datos solo representa una frontera: si las fuentes
tecnicas bajo alcance no explican el incidente, el analisis debe continuar fuera
de OraDiag con equipos funcionales o de aplicacion.

Rationale: el dominio causal orienta al equipo correcto, pero no amplia el
alcance de recoleccion ni autoriza datos funcionales.

### VII. Prohibicion estricta de tablas de negocio
OraDiag MUST NOT consultar tablas de negocio, datos funcionales ni inferir
significado funcional de datos de aplicacion. Solo MAY usar fuentes tecnicas
definidas por fase: catalogo, diccionario, vistas dinamicas, logs, listener,
sistema operativo, infraestructura accesible y otros origenes tecnicos
documentados. La presencia del dominio Datos, perfiles avanzados o fixtures de
laboratorio MUST NOT relajar esta prohibicion.

Rationale: el proyecto diagnostica causas tecnicas observables y no debe invadir
el ambito funcional o de negocio.

### VIII. Fallas controladas y diagnostico parcial
Errores, timeouts, permisos insuficientes, capas no disponibles y datos
incompletos MUST convertirse en evidencia, limitaciones o revisiones no
evaluadas. Ningun conector, consulta, collector, scanner o reporter MAY quedar
colgado indefinidamente ni tumbar toda la ejecucion si existen capas
independientes evaluables. El diagnostico parcial es preferible a una ejecucion
colgada o fallida sin reporte.

Rationale: durante incidentes reales, los accesos parciales son normales y deben
mejorar el diagnostico, no impedirlo.

### IX. Seguridad, minimos privilegios y recomendaciones seguras
OraDiag MUST operar con privilegios tecnicos minimos. Passwords, tokens,
secretos y cadenas sensibles MUST NOT guardarse en el repositorio ni exponerse
en logs o reportes. La falta de permisos MUST reportarse como limitacion, no
como razon para escalar privilegios automaticamente. Las recomendaciones MUST
indicar alcance, riesgo, prerequisitos y validacion humana cuando una accion sea
destructiva, irreversible, riesgosa o productiva.

Rationale: el diagnostico no debe introducir nuevos riesgos de seguridad u
operacion.

### X. Perfiles, contratos, formatos y pruebas gobernados por el modelo
Los perfiles de ejecucion agrupan revisiones y capas, pero MUST NOT alterar las
reglas de causalidad ni fabricar certeza. El modelo formal de evidencia,
diagnostico, hallazgos, causalidad, limitaciones y reportes gobierna el diseno:
los fixtures no definen el modelo. El intercambio formal entre
collectors/providers/scanners y el motor RCA MUST ser un Evidence Payload
estricto, serializable a JSON, versionado y validado contra modelos internos. El
motor RCA MUST NOT consumir YAML directamente ni depender del origen de la
evidencia. YAML MAY usarse para escenarios humanos de prueba o laboratorio; JSON
MUST usarse para intercambio formal de evidencia y salida estructurada del motor
RCA.

Toda funcionalidad MUST tener pruebas automatizadas. Las pruebas MUST validar,
segun aplique, que OraDiag no emite causa probable sin evidencia, no confunde
hallazgos incidentales con causa principal, conserva OK relevantes, convierte
errores/timeouts/permisos insuficientes en limitaciones, respeta el sintoma como
pista, no consulta ni modela datos de negocio y mantiene salida JSON estable.

Rationale: el contrato estable permite evolucionar collectors y motor RCA sin
acoplarlos a fixtures, YAML o implementaciones prematuras.

### XI. Trazabilidad, roadmap y control de desviaciones
Cada spec, plan, tarea, implementacion y pull request MUST poder rastrearse a
esta constitucion, al roadmap, a la documentacion rectora y a las decisiones
aplicables. Cualquier idea, mejora, decision tecnica o funcionalidad fuera de la
constitucion, spec activa, plan aprobado o roadmap MUST marcarse como
`propuesta de desviación` y MUST NOT incorporarse sin justificacion explicita y
autorizacion humana. Las desviaciones por preferencia, facilidad, gusto personal
o analogia con OraHealth/OraParity estan prohibidas.

Rationale: la trazabilidad protege el alcance del proyecto y evita crecimiento
accidental fuera del RCA de incidentes Oracle.

## Restricciones Tecnicas y de Alcance

OraDiag MUST usar Python 3.12+, `uv`, Typer para CLI, PyYAML para configuracion
o escenarios humanos, Pydantic para modelos y validacion cuando aplique, y
pytest para pruebas automatizadas.

La primera implementacion funcional, correspondiente a
`001-core-rca-sin-conectividad-real`, MUST construir core diagnostico, modelos,
CLI, configuracion, Evidence Payload, fixtures de laboratorio, motor RCA minimo
simulado y salidas console/json. Esa implementacion MUST NOT incluir conexion
Oracle real, SSH real, listener real, collectors reales, consultas SQL reales ni
lectura real de alert log.

La documentacion, reportes humanos y mensajes principales MUST estar en espanol.
Los identificadores tecnicos internos MAY estar en ingles cuando sea conveniente
para estabilidad de codigo, enums o serializacion.

Las fuentes normativas iniciales son:
`docs/DOCUMENTO_RECTOR.md`, `docs/ARCHITECTURE.md`, `docs/RCA_MODEL.md`,
`docs/EVIDENCE_MODEL.md`, `docs/CAUSAL_DOMAINS.md`,
`docs/SYMPTOM_HANDLING.md`, `docs/ERROR_HANDLING_AND_TIMEOUTS.md`,
`docs/SECURITY_AND_ACCESS.md`, `docs/EXECUTION_PROFILES.md`,
`docs/ROADMAP.md`, `docs/BACKLOG.md`, `docs/DECISION_LOG.md`,
`docs/TRACEABILITY_MATRIX.md` y `docs/CONTRIBUTING.md`.

## Proceso SDD, Specs y Pull Requests

Toda spec MUST declarar fase o agrupacion del roadmap, fuentes rectoras
aplicables, restricciones fuera de alcance, criterios de evidencia, riesgos de
seguridad, manejo de errores/timeouts, pruebas esperadas y trazabilidad a
decisiones existentes.

Todo plan MUST incluir un Constitution Check verificable antes de diseno e
implementacion. El check MUST cubrir RCA vs health check, evidencia, sintoma,
separacion causal, OK visibles, dominios causales, prohibicion de tablas de
negocio, fallas controladas, seguridad, recomendaciones, perfiles, contrato de
evidencia, roadmap, pruebas, idioma y desviaciones.

Toda lista de tareas MUST incluir actividades explicitas para pruebas,
trazabilidad y actualizacion documental cuando el cambio afecte reglas, modelos,
contratos, reportes o decisiones. Las tareas MUST NOT adelantar fases futuras.

Todo pull request MUST declarar la fase o spec relacionada, demostrar
cumplimiento constitucional, listar pruebas ejecutadas o justificadas, indicar
documentacion actualizada y marcar cualquier `propuesta de desviación` aceptada.

## Agrupacion Oficial Inicial de Specs

- `000-gobierno-y-constitucion`: Fase 0, Gobierno documental.
- `001-core-rca-sin-conectividad-real`: Fase 1, CLI, configuracion, perfiles,
  modelos base, Evidence Payload, fixtures de laboratorio y RCA engine minimo
  simulado.
- `002-acceso-por-capas-y-discovery-oracle`: Fases 2 y 3, conectividad por
  capas y Discovery Oracle.
- `003-errores-usuarios-y-autenticacion`: Fases 4 y 5, alert log, errores
  criticos, usuario y autenticacion.
- `004-sesiones-bloqueos-y-waits`: Fases 6 y 7, sesiones, bloqueos y wait
  analysis.
- `005-espacio-almacenamiento-y-redo`: Fases 8 y 9, Storage, FRA, TEMP, UNDO,
  redo, archive y log switches.
- `006-correlacion-rca-y-reportes`: Fases 10 y 11, correlacion RCA avanzada y
  reportes maduros.
- `007-topologias-oracle-avanzadas`: Fase 12, RAC, ASM, Multitenant y Standby
  avanzado.
- `008-historico-y-extensiones`: Fases 13 y 14, historico de incidentes y
  extensiones futuras.

## Asuntos Pendientes y Aclaraciones Requeridas

- `docs/ROADMAP.md` describe la Fase 1 como CLI, configuracion, perfiles y
  modelos base, mientras esta constitucion exige en
  `001-core-rca-sin-conectividad-real` un motor RCA minimo simulado y salidas
  console/json. Se requiere decision humana para alinear el texto del roadmap
  sin agregar fases nuevas.
- `docs/ROADMAP.md` ubica la correlacion RCA inicial en Fase 10 y reportes
  maduros en Fase 11. Hasta que se aclare la alineacion, cualquier trabajo de
  Fase 1 relacionado con RCA o reportes MUST permanecer minimo, simulado,
  contractual y sin conectividad real.

## Governance

Esta constitucion supersede practicas informales y gobierna specs, planes,
tareas, implementaciones y pull requests de OraDiag/OraRCA. La documentacion
rectora sigue siendo fuente normativa complementaria siempre que no contradiga
esta constitucion.

Las enmiendas constitucionales MUST:
- declarar motivo, alcance y documentos afectados;
- actualizar el Sync Impact Report;
- usar versionado semantico;
- registrar decisiones relevantes en `docs/DECISION_LOG.md` cuando corresponda;
- actualizar plantillas Spec Kit y documentos rectores afectados;
- identificar desviaciones, migraciones y riesgos de compatibilidad.

Versionado:
- MAJOR para redefinir o remover principios, relajar prohibiciones o cambiar el
  alcance constitucional del proyecto.
- MINOR para agregar principios, secciones normativas o nuevas obligaciones
  verificables.
- PATCH para aclaraciones, correcciones de redaccion o refinamientos sin cambio
  semantico.

Toda revision de cumplimiento MUST verificar que no queden placeholders,
conclusiones sin evidencia, alcance fuera del roadmap, referencias a tablas de
negocio, secretos expuestos, recomendaciones peligrosas sin validacion humana ni
desviaciones no autorizadas.

**Version**: 1.0.0 | **Ratified**: 2026-07-03 | **Last Amended**: 2026-07-03
