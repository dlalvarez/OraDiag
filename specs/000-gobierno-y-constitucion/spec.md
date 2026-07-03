# Feature Specification: Gobierno y Constitución SDD

**Feature Branch**: `000-gobierno-y-constitucion`

**Created**: 2026-07-03

**Status**: Draft

**Input**: User description: "Crear la especificación SDD `000-gobierno-y-constitucion` para formalizar el gobierno documental de OraDiag/OraRCA como Fase 0."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Gobierno documental ratificado (Priority: P1)

Como mantenedor de OraDiag, quiero una especificación formal de Fase 0 que declare las fuentes normativas y rectoras del proyecto para que cualquier trabajo futuro tenga una base SDD verificable.

**Why this priority**: Sin una spec de gobierno, las futuras specs, planes, tareas e implementaciones no tienen un punto de entrada trazable hacia la constitución, el documento rector y el roadmap.

**Independent Test**: Puede validarse revisando que la spec `000-gobierno-y-constitucion` exista, referencie las fuentes rectoras obligatorias y declare que la constitución es la fuente normativa principal.

**Acceptance Scenarios**:

1. **Given** el repositorio con constitución ratificada, **When** un mantenedor revisa la spec de Fase 0, **Then** encuentra declaradas la constitución, la documentación rectora, el roadmap, el backlog, el decision log, la matriz de trazabilidad y las reglas de contribución.
2. **Given** una futura propuesta de cambio, **When** se busca su fuente de gobierno, **Then** la spec de Fase 0 indica que debe respetar la constitución, el documento rector, el roadmap, el backlog y el control de desviaciones.

---

### User Story 2 - Reglas mínimas para artefactos SDD futuros (Priority: P2)

Como autor de futuras specs, planes y tareas, quiero criterios mínimos explícitos para preparar artefactos SDD que no contradigan la constitución ni adelanten fases del roadmap.

**Why this priority**: Los artefactos futuros deben ser verificables antes de cualquier implementación para evitar cambios por analogía, preferencias personales o alcance no autorizado.

**Independent Test**: Puede validarse revisando que la spec enumere los campos mínimos requeridos para futuras specs, el Constitution Check obligatorio para planes y las reglas de tareas pequeñas, verificables y acotadas.

**Acceptance Scenarios**:

1. **Given** una nueva spec futura, **When** se compara contra esta spec de gobierno, **Then** la nueva spec declara fase o agrupación del roadmap, fuentes rectoras, alcance, fuera de alcance, criterios de evidencia, manejo de errores/timeouts, seguridad, pruebas, trazabilidad y desviaciones.
2. **Given** un nuevo plan futuro, **When** se revisa su contenido, **Then** incluye un Constitution Check explícito antes de avanzar.
3. **Given** una lista futura de tareas, **When** se revisa su alcance, **Then** cada tarea es pequeña, verificable y no adelanta fases futuras.

---

### User Story 3 - Control de PRs y desviaciones (Priority: P3)

Como revisor de pull requests, quiero reglas documentales claras para confirmar cumplimiento constitucional, pruebas, documentación y desviaciones autorizadas.

**Why this priority**: Los PRs son el punto de control donde se evita que el proyecto se convierta en health check, consulte datos de negocio o incorpore funcionalidad fuera de fase.

**Independent Test**: Puede validarse revisando que la spec defina lo que todo PR debe declarar y cómo se tratan los cambios fuera de constitución, spec activa, plan aprobado o roadmap.

**Acceptance Scenarios**:

1. **Given** un PR futuro, **When** se revisa contra esta spec, **Then** el PR declara spec/fase relacionada, cumplimiento constitucional, pruebas ejecutadas, documentación actualizada y desviaciones autorizadas si existieron.
2. **Given** una idea fuera de alcance, **When** aparece en una spec, plan, tarea o PR, **Then** se marca como `propuesta de desviación` y no se acepta sin autorización humana explícita.

### Edge Cases

- Si una futura propuesta no corresponde a ninguna fase o agrupación del roadmap, debe tratarse como `propuesta de desviación` y no avanzar sin autorización humana explícita.
- Si una futura spec intenta consultar tablas de negocio o datos funcionales, debe rechazarse por contradicción constitucional.
- Si una futura spec copia decisiones de OraHealth, OraParity u otro proyecto por analogía, debe corregirse o declararse como desviación no autorizada.
- Si un documento rector y una propuesta futura entran en tensión, la tensión debe registrarse como aclaración requerida sin inventar alcance nuevo.
- Si una tarea futura mezcla gobierno documental con implementación de diagnóstico, debe dividirse o rechazarse por adelantar fases.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La spec MUST registrar `000-gobierno-y-constitucion` como especificación de Fase 0: Gobierno documental.
- **FR-002**: La spec MUST declarar `.specify/memory/constitution.md` como fuente normativa principal de OraDiag/OraRCA.
- **FR-003**: La spec MUST declarar `docs/DOCUMENTO_RECTOR.md` como documento rector complementario.
- **FR-004**: La spec MUST declarar `docs/ROADMAP.md` como roadmap oficial agrupado por specs.
- **FR-005**: La spec MUST declarar `docs/BACKLOG.md` como repositorio de ideas futuras que no son implementables sin spec, plan y tareas aprobadas.
- **FR-006**: La spec MUST declarar `docs/DECISION_LOG.md` como registro de decisiones relevantes del proyecto.
- **FR-007**: La spec MUST declarar `docs/TRACEABILITY_MATRIX.md` como mecanismo de trazabilidad entre principios, documentos, fases y pruebas futuras.
- **FR-008**: La spec MUST declarar `docs/CONTRIBUTING.md` como reglas de contribución y revisión de PRs.
- **FR-009**: La spec MUST listar como fuentes rectoras aplicables la constitución, Documento Rector, arquitectura, modelos RCA y evidencia, dominios causales, manejo de síntomas, errores/timeouts, seguridad/acceso, perfiles, roadmap, backlog, decision log, matriz de trazabilidad y contribución.
- **FR-010**: La spec MUST establecer que toda futura spec declare fase o agrupación del roadmap, fuentes rectoras aplicables, alcance, fuera de alcance, criterios de evidencia, reglas de errores/timeouts, seguridad y mínimos privilegios, pruebas esperadas, trazabilidad y control de desviaciones.
- **FR-011**: La spec MUST establecer que todo plan futuro incluya un Constitution Check explícito.
- **FR-012**: La spec MUST establecer que toda lista de tareas futura sea verificable, pequeña y no adelante fases futuras.
- **FR-013**: La spec MUST establecer que todo PR futuro indique spec/fase relacionada, cumplimiento constitucional, pruebas ejecutadas, documentación actualizada y desviaciones autorizadas si existieron.
- **FR-014**: La spec MUST registrar la agrupación oficial inicial de specs del roadmap desde `000-gobierno-y-constitucion` hasta `008-historico-y-extensiones`.
- **FR-015**: La spec MUST confirmar que OraDiag es RCA de incidentes Oracle, no health check, capacity planning, auditoría funcional, explorador de datos de negocio ni caza-problemas genérico.
- **FR-016**: La spec MUST confirmar que ninguna fase futura puede consultar tablas de negocio, datos funcionales ni inferir significado funcional de datos de aplicación.
- **FR-017**: La spec MUST confirmar que cualquier cambio fuera de constitución, spec activa, plan aprobado o roadmap se trata como `propuesta de desviación`.
- **FR-018**: La spec MUST confirmar que Fase 0 no implementa funcionalidad de diagnóstico, CLI, modelos Python, Evidence Payload, fixtures, motor RCA, reportes, conectividad Oracle, SSH, listener ni collectors reales.
- **FR-019**: La spec MUST definir criterios de aceptación documentales, no técnicos de ejecución de código.
- **FR-020**: La spec MUST NOT agregar fases nuevas, eliminar fases existentes ni modificar el alcance general de OraDiag.

### Key Entities

- **Constitución SDD**: Fuente normativa principal que gobierna specs, planes, tareas, implementaciones y PRs.
- **Documento Rector**: Documento complementario que define propósito, alcance, fuera de alcance y principios no negociables de OraDiag.
- **Roadmap agrupado por specs**: Secuencia oficial de fases y agrupaciones `000` a `008` que limita el orden de trabajo.
- **Backlog**: Registro de ideas futuras que no autorizan implementación por sí mismas.
- **Decision Log**: Registro de decisiones relevantes y consecuencias.
- **Matriz de Trazabilidad**: Mecanismo para enlazar principios, documentos, fases y pruebas futuras.
- **Spec futura**: Artefacto SDD que debe declarar alcance, fuentes rectoras, evidencia, seguridad, pruebas, trazabilidad y desviaciones.
- **Plan futuro**: Artefacto SDD que debe incluir Constitution Check explícito.
- **Lista de tareas futura**: Artefacto SDD con tareas pequeñas, verificables y limitadas a la fase aprobada.
- **Pull Request futuro**: Cambio revisable que debe declarar spec/fase, cumplimiento constitucional, pruebas, documentación y desviaciones autorizadas.
- **Propuesta de desviación**: Cambio fuera de constitución, spec activa, plan aprobado o roadmap que requiere justificación y autorización humana explícita.

## Constitutional Alignment *(mandatory)*

### Roadmap and Scope

- **Roadmap grouping**: `000-gobierno-y-constitucion`, Fase 0: Gobierno documental.
- **Rector docs used**: `.specify/memory/constitution.md`, `docs/DOCUMENTO_RECTOR.md`, `docs/ARCHITECTURE.md`, `docs/RCA_MODEL.md`, `docs/EVIDENCE_MODEL.md`, `docs/CAUSAL_DOMAINS.md`, `docs/SYMPTOM_HANDLING.md`, `docs/ERROR_HANDLING_AND_TIMEOUTS.md`, `docs/SECURITY_AND_ACCESS.md`, `docs/EXECUTION_PROFILES.md`, `docs/ROADMAP.md`, `docs/BACKLOG.md`, `docs/DECISION_LOG.md`, `docs/TRACEABILITY_MATRIX.md` y `docs/CONTRIBUTING.md`.
- **Out of scope**: Implementar código, CLI, modelos Python, Evidence Payload, fixtures, motor RCA, reportes, conectividad Oracle, SSH, listener, collectors reales, consultas SQL reales, lectura real de alert log, nuevas fases o cambios funcionales fuera de la constitución.
- **Deviation status**: Ninguna desviación aceptada. Todo cambio futuro fuera de constitución, spec activa, plan aprobado o roadmap debe marcarse como `propuesta de desviación` y requerir autorización humana explícita.

### RCA and Evidence Rules

- **Incident/RCA focus**: Esta spec gobierna documentalmente que OraDiag es RCA de incidentes Oracle y no health check, capacity planning, auditoría funcional, explorador de datos de negocio ni caza-problemas genérico.
- **Evidence required**: Para Fase 0, la evidencia es documental: constitución ratificada, documentos rectores existentes, roadmap agrupado por specs, backlog, decision log, matriz de trazabilidad y reglas de contribución. Las futuras specs deben declarar evidencia positiva, evidencia negativa y limitaciones aplicables a su fase.
- **Symptom handling**: Fase 0 no procesa síntomas. La spec conserva la regla de que los síntomas futuros son pista de priorización, no verdad causal.
- **Causal roles**: Fase 0 no emite diagnósticos ni roles causales. La spec preserva la obligación futura de diferenciar `primary_cause`, `contributing_factor`, `related_finding`, `incidental_finding`, `ruled_out`, `not_evaluated` y `unknown`.
- **Visible OK reviews**: Fase 0 no ejecuta revisiones técnicas. La spec preserva la obligación futura de mantener visibles las revisiones OK cuando descarten hipótesis.
- **Causal domains**: Fase 0 no clasifica incidentes. La spec preserva los dominios aprobados y confirma que el dominio Datos no autoriza consultar tablas de negocio.

### Safety, Data and Error Boundaries

- **No business data**: Esta spec confirma que ninguna fase futura puede consultar tablas de negocio, datos funcionales ni inferir significado funcional de datos de aplicación.
- **Failures/timeouts**: Fase 0 no ejecuta conectores ni consultas. La spec exige que futuras specs declaren cómo errores, timeouts, permisos insuficientes y capas no disponibles se convertirán en limitaciones o revisiones no evaluadas.
- **Security/minimum privileges**: Fase 0 no gestiona secretos ni accesos. La spec exige que futuras specs y PRs respeten mínimos privilegios y protección de secretos según constitución y documentos rectores.
- **Recommendations**: Fase 0 no emite recomendaciones operativas sobre bases Oracle. La spec exige que futuras recomendaciones declaren alcance, riesgo, prerequisitos y validación humana cuando aplique.
- **Evidence Payload/format**: Fase 0 no crea Evidence Payload ni formato de salida. La spec preserva la obligación futura de que el intercambio formal de evidencia sea JSON serializable, versionado y validado, y que YAML se limite a escenarios humanos de laboratorio cuando aplique.
- **Language**: La especificación, documentación de gobierno, reportes humanos y mensajes principales deben mantenerse en español.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Existe `specs/000-gobierno-y-constitucion/spec.md` con 100% de las secciones obligatorias completadas y sin marcadores de aclaración pendiente.
- **SC-002**: La spec referencia el 100% de las fuentes rectoras obligatorias indicadas para Fase 0.
- **SC-003**: La spec registra las 9 agrupaciones oficiales de specs del roadmap, desde `000` hasta `008`, sin agregar ni eliminar fases.
- **SC-004**: La spec declara al menos una regla verificable para futuras specs, planes, tareas y PRs.
- **SC-005**: La spec declara explícitamente que Fase 0 no implementa funcionalidad de diagnóstico ni componentes técnicos de fases posteriores.
- **SC-006**: La spec contiene control explícito de `propuesta de desviación` para cambios fuera de constitución, spec activa, plan aprobado o roadmap.
- **SC-007**: La spec confirma explícitamente que OraDiag es RCA de incidentes Oracle, no health check, y que ninguna fase puede consultar tablas de negocio.
- **SC-008**: La revisión documental de la spec no encuentra contradicciones con la constitución ratificada.

## Assumptions

- La constitución SDD en `.specify/memory/constitution.md` ya está ratificada y gobierna esta spec.
- `docs/ROADMAP.md` ya contiene la agrupación oficial de specs alineada con la constitución.
- Fase 0 es exclusivamente documental y no requiere pruebas de ejecución de código.
- Las validaciones esperadas para esta spec son revisión documental, trazabilidad y consistencia con fuentes rectoras.
- Los documentos rectores listados existen y son insumos normativos o complementarios para el gobierno SDD.
