<!--
Sync Impact Report
Version change: 1.0.0 -> 2.0.0 (MAJOR)
Motivo: replanteamiento del proyecto para implementarlo desde cero con Claude Code,
con Amazon RDS for Oracle como plataforma inicial y un núcleo independiente de
plataforma.
Modified principles:
- I. OraDiag es RCA, no health check (se elimina la referencia a OraParity)
- VI. Dominios causales y frontera de datos (Infraestructura incluye plataforma gestionada)
- X. Contratos y pruebas (se precisa la separación evidencia -> motor)
- XI. Trazabilidad (se agrega el flujo planeación/implementación)
Added principles:
- XII. Núcleo SQL independiente de plataforma
- XIII. Licenciamiento Oracle explícito
- XIV. Solo lectura estricta
- XV. Correlación causal, no suma de severidades
Changed sections:
- Restricciones Técnicas y de Alcance: plataforma inicial RDS, python-oracledb thin,
  se elimina la restricción "sin conectividad real" de la antigua spec 001.
- Agrupación Oficial de Specs: 001 y 002 quedan como históricas (superseded);
  nueva agrupación desde 003.
- Asuntos Pendientes: se cierran los de v1.0.0 y se registran los nuevos.
Templates requiring updates:
- .specify/templates/plan-template.md: Constitution Check con XII-XV (hecho).
- .specify/templates/spec-template.md: tabla de fuentes, grants y licencias (hecho).
- .specify/templates/tasks-template.md: guardrails XII-XIV (hecho).
- Integración de Spec Kit: cambiar de Codex a Claude Code (pendiente).
Follow-up TODOs:
- Confirmar licenciamiento de Diagnostics/Tuning Pack (ver Asuntos Pendientes).
- Decidir el retiro del código de la implementación anterior (ver Asuntos Pendientes).
-->
# Constitución de OraDiag

## Core Principles

### I. OraDiag es RCA, no health check
OraDiag MUST investigar incidentes Oracle ya reportados o en curso. Su objetivo
es identificar una causa probable soportada por evidencia técnica, no listar
anomalías generales, evaluar salud preventiva, hacer capacity planning, auditar
funcionalmente ni explorar datos de negocio. Toda spec MUST preservar la
diferencia entre OraDiag (RCA de incidentes) y OraHealth (salud preventiva);
las decisiones de OraHealth no se copian por analogía automática.

Rationale: el valor de OraDiag está en reducir ambigüedad durante incidentes
concretos, no en ampliar alcance por similitud con otros proyectos.

### II. La evidencia manda
Toda conclusión relevante MUST estar soportada por evidencia positiva, evidencia
negativa o una limitación explícita. OraDiag MUST declarar cuándo una causa es
probable, cuándo una hipótesis es débil y cuándo no existe evidencia suficiente.
El sistema MUST NOT emitir causa probable, severidad causal o recomendación
operativa como certeza sin evidencia trazable.

Rationale: una conclusión sin evidencia crea ruido, sesgo y riesgo operativo.

### III. El síntoma es pista, no verdad
El síntoma reportado MAY priorizar revisiones, ordenar hipótesis y aportar
contexto, pero MUST NOT decidir la causa por sí solo. Si el síntoma contradice
la evidencia, OraDiag MUST reportar la contradicción. Sin síntoma, el análisis
MUST usar `unspecified` sin fabricar causalidad.

Rationale: el síntoma introduce sesgo de anclaje; la evidencia técnica prevalece.

### IV. Separación causal obligatoria
Todo diagnóstico MUST diferenciar, según evidencia: `primary_cause`,
`contributing_factor`, `related_finding`, `incidental_finding`, `ruled_out`,
`not_evaluated` y `unknown`. OraDiag MUST NOT confundir un hallazgo incidental,
una anomalía real o una severidad técnica alta con la causa principal sin
correlación suficiente (ver XV).

Rationale: separar roles causales evita reportes ruidosos y recomendaciones
desproporcionadas.

### V. Revisiones OK visibles
Las revisiones OK MUST conservarse y mostrarse cuando ayuden a descartar
hipótesis, explicar confianza o justificar que un dominio no tiene evidencia
causal. Un OK MAY ser evidencia negativa importante y MUST NOT ocultarse.

Rationale: el RCA necesita evidencia negativa para reducir ambigüedad.

### VI. Dominios causales y frontera de datos
Todo diagnóstico MUST intentar clasificar el causante probable en uno de estos
dominios: Sistema Operativo, Infraestructura (incluye la plataforma gestionada:
RDS, OCI u on-premise), Almacenamiento, Base de datos, Aplicación, Usuario,
Datos o Indeterminado. Datos es solo una frontera: si las fuentes técnicas no
explican el incidente, el análisis continúa fuera de OraDiag con equipos
funcionales o de aplicación.

Rationale: el dominio orienta al equipo correcto sin ampliar el alcance de
recolección.

### VII. Prohibición estricta de tablas de negocio
OraDiag MUST NOT consultar tablas de negocio, datos funcionales ni inferir
significado funcional de datos de aplicación. Solo MAY usar fuentes técnicas:
diccionario, vistas dinámicas `V$`/`GV$`, vistas `DBA_` técnicas, alert log,
métricas de plataforma y otras fuentes técnicas documentadas por spec. Los
valores de bind variables y el texto completo de SQL MUST tratarse como
potencialmente sensibles: se recolectan solo cuando una spec lo justifique y se
enmascaran en reportes por defecto.

Rationale: el proyecto diagnostica causas técnicas observables y opera en un
entorno bancario.

### VIII. Fallas controladas y diagnóstico parcial
Errores, timeouts, permisos insuficientes, vistas no accesibles y datos
incompletos MUST convertirse en evidencia, limitaciones o revisiones
`not_evaluated`. Ninguna conexión, consulta, collector o reporter MAY quedar
colgado indefinidamente ni tumbar la ejecución si existen fuentes
independientes evaluables. Toda consulta MUST tener timeout explícito
(`call_timeout` en python-oracledb). El diagnóstico parcial es preferible a una
ejecución fallida sin reporte.

Rationale: durante incidentes reales, los accesos parciales son normales.

### IX. Seguridad, mínimos privilegios y recomendaciones seguras
OraDiag MUST operar con un usuario dedicado y privilegios mínimos, derivables
de las vistas declaradas por cada revisión. Passwords, tokens y secretos MUST
NOT guardarse en el repositorio ni aparecer en logs o reportes; las credenciales
se obtienen de variables de entorno o de un gestor de secretos referenciado.
La falta de permisos MUST reportarse como limitación, nunca como razón para
escalar privilegios. Las recomendaciones MUST indicar alcance, riesgo,
prerrequisitos y validación humana cuando la acción sea destructiva,
irreversible o afecte producción.

Rationale: el diagnóstico no debe introducir nuevos riesgos.

### X. Contratos y pruebas gobernados por el modelo
El intercambio entre fuentes de evidencia y el motor RCA MUST ser un Evidence
Payload estricto, versionado, serializable a JSON y validado con modelos
Pydantic. El motor RCA MUST NOT conocer el origen de la evidencia (SQL,
fixture, adaptador de plataforma) ni consumir YAML directamente. YAML MAY
usarse para escenarios de laboratorio y configuración humana. Los fixtures no
definen el modelo.

Toda funcionalidad MUST tener pruebas automatizadas que validen, según aplique:
que no se emite causa sin evidencia, que los incidentales no se confunden con la
causa, que los OK relevantes se conservan, que errores/timeouts/permisos se
convierten en limitaciones, que el síntoma no decide, que no se consultan datos
de negocio, que no se usan funcionalidades licenciadas sin declaración (XIII) y
que la salida JSON es estable.

Rationale: el contrato estable permite evolucionar fuentes y motor por separado.

### XI. Trazabilidad, roadmap y control de desviaciones
Cada spec, plan, tarea, implementación y pull request MUST rastrearse a esta
constitución, al roadmap y a las decisiones aplicables. Toda idea fuera de la
constitución, spec activa, plan aprobado o roadmap MUST marcarse como
`propuesta de desviación` y MUST NOT incorporarse sin justificación y
autorización humana.

La planeación (constitución, roadmap, specs, planes y tareas) se realiza y
aprueba antes de implementar. La implementación con Claude Code MUST seguir el
`tasks.md` aprobado de la spec activa; si durante la implementación aparece un
hallazgo que invalida la spec, se detiene la tarea afectada y se propone el
ajuste a la spec, en lugar de improvisar en código.

Rationale: la trazabilidad protege el alcance y evita crecimiento accidental.

### XII. Núcleo SQL independiente de plataforma
El núcleo de OraDiag MUST depender únicamente de Oracle Database: toda la
evidencia obligatoria se obtiene por SQL de solo lectura contra la instancia.
Esto garantiza el mismo comportamiento en Amazon RDS for Oracle, on-premise y
OCI. Las fuentes específicas de una plataforma (CloudWatch, eventos RDS, SSH,
APIs de OCI) MUST implementarse como adaptadores opcionales que agregan
evidencia y confianza, nunca como requisito para ejecutar un diagnóstico. Sin
adaptador, los dominios que dependen de él quedan `not_evaluated`.

Ningún módulo del núcleo MAY importar SDKs de proveedores cloud ni librerías
SSH. Esta regla MUST verificarse con una prueba automatizada.

Rationale: evitar dependencia de un proveedor y conservar portabilidad entre
cloud y on-premise.

### XIII. Licenciamiento Oracle explícito
Las funcionalidades de Oracle Diagnostics Pack y Tuning Pack MUST estar
deshabilitadas por defecto y solo MAY usarse cuando el target declare
explícitamente la licencia en su configuración (`diagnostic_pack: licensed`,
`tuning_pack: licensed`). OraDiag MUST NOT inferir la licencia a partir de
parámetros de la base.

Cuando se declare la licencia, OraDiag MUST verificar que
`control_management_pack_access` sea coherente; si no lo es, las fuentes
licenciadas quedan `not_evaluated` y se reporta la inconsistencia.

Se consideran licenciadas, como mínimo: `V$ACTIVE_SESSION_HISTORY`,
`GV$ACTIVE_SESSION_HISTORY`, `DBA_HIST_*`, `DBA_ADDM_*`, `DBA_ADVISOR_*`,
`DBMS_WORKLOAD_REPOSITORY`, `DBMS_ADDM` (Diagnostics) y `V$SQL_MONITOR`,
`V$SQL_PLAN_MONITOR`, `DBMS_SQLTUNE`, `DBMS_SQL_MONITOR` (Tuning). La lista
MUST validarse contra el documento *Database Licensing Information* de cada
versión soportada antes de cada spec que agregue vistas. Toda consulta a estas
fuentes MUST vivir en un módulo aislado y protegido por la declaración de
licencia, con prueba automatizada que lo garantice.

Rationale: en un banco, usar un pack sin licencia es un riesgo de auditoría
real, y Oracle registra su uso en `DBA_FEATURE_USAGE_STATISTICS`.

### XIV. Solo lectura estricta
OraDiag MUST ejecutar únicamente consultas `SELECT` y lecturas equivalentes. MUST
NOT ejecutar DML, DDL, `ALTER SYSTEM`, `ALTER SESSION` que cambie
comportamiento observable de la base, crear objetos, generar archivos en el
servidor ni invocar procedimientos que modifiquen estado (incluidos los de
`rdsadmin` que generan reportes en disco). Las acciones correctivas solo se
recomiendan; nunca se ejecutan. Las consultas MUST evitar barridos costosos sin
filtro sobre vistas grandes en producción y declarar su ventana temporal.

Rationale: una herramienta de diagnóstico no puede empeorar un incidente.

### XV. Correlación causal, no suma de severidades
La causa principal MUST surgir de una correlación explícita entre evidencias:
coincidencia temporal con la ventana del incidente, relación causal plausible
entre hallazgos (por ejemplo, bloqueador -> sesiones en espera -> lentitud) y
ausencia de explicaciones alternativas con evidencia equivalente. Una severidad
alta sin relación temporal o causal con el incidente MUST clasificarse como
`incidental_finding` o `related_finding`, no como causa. Cada conclusión MUST
exponer la cadena de evidencia que la sostiene y el motivo de su nivel de
confianza.

Rationale: la versión anterior del motor sumaba pesos por severidad; eso no es
RCA.

## Restricciones Técnicas y de Alcance

OraDiag MUST usar Python 3.12+, `uv`, Typer para CLI, Pydantic para modelos y
validación, PyYAML para configuración y escenarios de laboratorio, pytest para
pruebas y `python-oracledb` en modo thin para la conexión a Oracle (sin Oracle
Client instalado). Los adaptadores de plataforma MUST declararse como
dependencias opcionales (`extras`).

Plataforma inicial: Amazon RDS for Oracle, Enterprise Edition. Plataformas
futuras: Oracle on-premise y OCI, mediante el mismo núcleo y adaptadores
propios. Las particularidades de RDS (sin `SYS`, permisos vía
`rdsadmin.rdsadmin_util.grant_sys_object`, sin acceso al host) MUST
documentarse en cada spec que agregue vistas o fuentes.

La implementación anterior (antiguas specs 001 y 002) no se reutiliza como
base de código. Sus documentos se conservan como referencia histórica.

La documentación, reportes y mensajes visibles MUST estar en español. Los
identificadores técnicos (enums, claves JSON, nombres de código) MAY estar en
inglés por estabilidad.

Fuentes normativas: esta constitución, `CLAUDE.md` y `docs/` (en especial
`ARCHITECTURE.md`, `RCA_MODEL.md`, `EVIDENCE_MODEL.md`, `CAUSAL_DOMAINS.md`,
`SYMPTOM_HANDLING.md`, `ERROR_HANDLING_AND_TIMEOUTS.md`,
`SECURITY_AND_ACCESS.md`, `EXECUTION_PROFILES.md`, `ROADMAP.md` y
`DECISION_LOG.md`). Si un documento de `docs/` contradice esta constitución,
prevalece la constitución y el documento MUST corregirse.

## Proceso SDD, Specs y Pull Requests

Toda spec MUST declarar: agrupación del roadmap, fuentes rectoras, fuera de
alcance, vistas Oracle y grants requeridos (con su equivalente en RDS),
clasificación de licenciamiento de cada fuente, criterios de evidencia, manejo
de errores y timeouts, riesgos de seguridad, pruebas esperadas y trazabilidad.

Todo plan MUST incluir un Constitution Check verificable que cubra los
principios I a XV.

Toda lista de tareas MUST incluir pruebas, trazabilidad y actualización
documental cuando el cambio afecte reglas, modelos, contratos, reportes o
decisiones. Las tareas MUST NOT adelantar specs futuras.

Todo pull request MUST declarar la spec relacionada, demostrar cumplimiento
constitucional, listar pruebas ejecutadas, indicar documentación actualizada y
marcar cualquier `propuesta de desviación` aceptada. Ramas: trabajo integrado
en `develop-claude`; una rama por spec desde ella; `main` solo recibe versiones
estables.

## Agrupación Oficial de Specs

Históricas (no se implementan de nuevo):
- `000-gobierno-y-constitucion`: gobierno documental v1 (vigente en lo que no
  contradiga esta versión).
- `001-core-rca-sin-conectividad-real`: superseded por 003.
- `002-acceso-por-capas-y-discovery-oracle`: superseded por 004.

Vigentes:
- `003-modelo-de-evidencia-y-motor-causal`: Evidence Payload v2, modelo causal
  con ventana temporal y cadenas de evidencia, motor RCA determinístico,
  fixtures de laboratorio, CLI y salidas console/json. Sin conexión Oracle.
- `004-conexion-oracle-y-discovery`: conexión thin con timeouts, preflight de
  vistas, discovery (versión, edición, CDB/PDB, RAC, plataforma),
  declaración y verificación de licencias, generador de grants mínimos.
- `005-sesiones-bloqueos-y-waits`: sesiones, cadenas de bloqueo, waits en vivo,
  métricas recientes (`V$SYSMETRIC_HISTORY`), histogramas y `V$OSSTAT`.
- `006-fuentes-licenciadas-ash-awr`: ASH y AWR protegidos por licencia, RCA de
  incidentes pasados por ventana temporal.
- `007-errores-alert-log-y-autenticacion`: alert log por SQL, errores ORA-
  críticos, cuentas y autenticación.
- `008-almacenamiento-redo-temp-undo`: tablespaces, TEMP, UNDO, FRA, redo y log
  switches.
- `009-correlacion-avanzada-y-reportes`: correlación multi-dominio y reportes
  markdown/html.
- `010-adaptadores-de-plataforma`: adaptador AWS RDS (métricas, eventos, logs)
  y adaptador on-premise (SSH); OCI cuando aplique.
- `011-topologias-avanzadas`: RAC, Multitenant y Data Guard.
- `012-historico-y-extensiones`: histórico de incidentes y extensiones opt-in.

## Asuntos Pendientes y Aclaraciones Requeridas

- **Licenciamiento de packs**: no está confirmado si las instancias RDS tienen
  Diagnostics y Tuning Pack licenciados. Hasta confirmarlo, toda spec trata las
  fuentes licenciadas como opcionales y deshabilitadas por defecto. Bloquea la
  ejecución de la spec 006 contra bases reales, no su planeación.
- **Versiones Oracle soportadas**: confirmar las versiones de las RDS objetivo
  (se asume 19c como base). Afecta las vistas disponibles y la lista de
  licenciamiento.
- **Código anterior**: decidir en un commit explícito el retiro de `src/` y
  `tests/` de la implementación previa antes de iniciar la implementación de la
  spec 003.
- **Exposición de datos a modelos de IA**: si OraDiag se expone en el futuro
  como servidor MCP o integración con IA, requiere una spec propia con
  aprobación de seguridad; no está en alcance.

## Governance

Esta constitución gobierna specs, planes, tareas, implementaciones y pull
requests de OraDiag. Las enmiendas MUST declarar motivo, alcance y documentos
afectados, actualizar el Sync Impact Report, usar versionado semántico,
registrar la decisión en `docs/DECISION_LOG.md` y actualizar plantillas y
documentos afectados.

Versionado: MAJOR para redefinir o remover principios, relajar prohibiciones o
cambiar el alcance; MINOR para agregar principios u obligaciones verificables;
PATCH para aclaraciones sin cambio semántico.

Toda revisión de cumplimiento MUST verificar que no queden placeholders,
conclusiones sin evidencia, alcance fuera del roadmap, referencias a tablas de
negocio, secretos expuestos, fuentes licenciadas sin protección, operaciones
de escritura ni desviaciones no autorizadas.

**Version**: 2.0.0 | **Ratified**: 2026-07-03 | **Last Amended**: 2026-11-21
