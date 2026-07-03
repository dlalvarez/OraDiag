# Tasks: Gobierno y Constitución SDD

**Input**: Design documents from `/specs/000-gobierno-y-constitucion/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md`, `.specify/memory/constitution.md`

**Tests**: No se generan pruebas `pytest` ni pruebas automatizadas para Fase 0. La validación es documental y se realiza mediante revisión de archivos y comandos Git básicos.

**Organization**: Las tareas están agrupadas por historia de usuario para permitir validar cada bloque de gobierno de forma independiente.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo porque revisa archivos distintos o no depende de tareas incompletas.
- **[Story]**: Historia de usuario asociada (`US1`, `US2`, `US3`).
- Todas las tareas incluyen una ruta de archivo explícita.

## Phase 1: Setup (Preparación documental)

**Purpose**: Confirmar que los artefactos de la spec activa existen antes de validar contenido.

- [ ] T001 Verificar que `.specify/feature.json` apunta a `specs/000-gobierno-y-constitucion`.
- [ ] T002 Verificar que `specs/000-gobierno-y-constitucion/spec.md` existe y corresponde a Fase 0.
- [ ] T003 Verificar que `specs/000-gobierno-y-constitucion/plan.md` existe y corresponde a Fase 0.
- [ ] T004 [P] Verificar que `specs/000-gobierno-y-constitucion/research.md` existe como investigación documental mínima.
- [ ] T005 [P] Verificar que `specs/000-gobierno-y-constitucion/data-model.md` existe y declara modelo documental, no runtime.
- [ ] T006 [P] Verificar que `specs/000-gobierno-y-constitucion/quickstart.md` existe como guía de validación documental.

---

## Phase 2: Foundational (Reglas de cierre documental)

**Purpose**: Establecer las condiciones que bloquean cualquier cierre de Fase 0 si fallan.

- [ ] T007 Verificar que `specs/000-gobierno-y-constitucion/plan.md` declara que Fase 0 no implementa código ni runtime.
- [ ] T008 Verificar que `specs/000-gobierno-y-constitucion/plan.md` excluye CLI, modelos Python, Evidence Payload, fixtures, motor RCA, reportes, Oracle, SSH, listener, collectors, SQL y alert log reales.
- [ ] T009 Verificar que `specs/000-gobierno-y-constitucion/research.md` registra que Fase 0 no implementa funcionalidad.
- [ ] T010 Verificar que `specs/000-gobierno-y-constitucion/quickstart.md` valida ausencia de implementación funcional.
- [ ] T011 Revisar `git status --short` y confirmar que no aparecen archivos de código fuente fuera de artefactos documentales de Fase 0.

**Checkpoint**: Si alguna tarea foundational falla, no cerrar Fase 0; registrar la inconsistencia como pendiente en `specs/000-gobierno-y-constitucion/tasks.md`.

---

## Phase 3: User Story 1 - Gobierno documental ratificado (Priority: P1)

**Goal**: Validar que la fuente normativa principal y las fuentes rectoras de Fase 0 están declaradas y trazables.

**Independent Test**: Revisar los documentos indicados y confirmar que la jerarquía documental queda explícita: constitución como fuente principal, Documento Rector como complemento y documentos de gobierno como soporte.

- [ ] T012 [P] [US1] Verificar que `.specify/memory/constitution.md` existe y declara que gobierna specs, planes, tareas, implementaciones y PRs.
- [ ] T013 [P] [US1] Verificar que `docs/CONTRIBUTING.md` declara `.specify/memory/constitution.md` como fuente normativa principal.
- [ ] T014 [P] [US1] Verificar que `docs/CONTRIBUTING.md` declara `docs/DOCUMENTO_RECTOR.md` como documento rector complementario.
- [ ] T015 [US1] Verificar que `specs/000-gobierno-y-constitucion/spec.md` referencia `.specify/memory/constitution.md` como fuente normativa principal.
- [ ] T016 [US1] Verificar que `specs/000-gobierno-y-constitucion/spec.md` referencia las fuentes rectoras obligatorias indicadas para Fase 0.
- [ ] T017 [US1] Verificar que `specs/000-gobierno-y-constitucion/plan.md` usa evidencia documental, no evidencia técnica de diagnóstico.
- [ ] T018 [US1] Registrar cualquier inconsistencia de jerarquía documental como pendiente en `specs/000-gobierno-y-constitucion/tasks.md`.

**Checkpoint**: US1 completa cuando la jerarquía documental está validada o cualquier inconsistencia queda registrada como pendiente.

---

## Phase 4: User Story 2 - Reglas mínimas para artefactos SDD futuros (Priority: P2)

**Goal**: Validar que futuras specs, planes y tareas quedan gobernadas por la constitución y el roadmap agrupado.

**Independent Test**: Revisar spec, plan, roadmap y modelo documental para confirmar que futuras specs, planes y tareas tienen campos mínimos, Constitution Check y límites de fase.

- [ ] T019 [P] [US2] Verificar que `docs/ROADMAP.md` contiene la agrupación oficial de specs `000` a `008`.
- [ ] T020 [P] [US2] Verificar que `docs/ROADMAP.md` declara `000-gobierno-y-constitucion` como Fase 0.
- [ ] T021 [P] [US2] Verificar que `docs/ROADMAP.md` mantiene Fase 0 como gobierno documental y fuera de alcance funcional.
- [ ] T022 [US2] Verificar que `specs/000-gobierno-y-constitucion/spec.md` exige que futuras specs declaren fase, fuentes rectoras, alcance, fuera de alcance, evidencia, errores/timeouts, seguridad, pruebas, trazabilidad y desviaciones.
- [ ] T023 [US2] Verificar que `specs/000-gobierno-y-constitucion/spec.md` exige Constitution Check explícito para planes futuros.
- [ ] T024 [US2] Verificar que `specs/000-gobierno-y-constitucion/spec.md` exige tareas futuras pequeñas, verificables y sin adelantar fases.
- [ ] T025 [US2] Verificar que `specs/000-gobierno-y-constitucion/data-model.md` define Spec SDD, Plan SDD y Lista de Tareas como entidades documentales de gobierno.
- [ ] T026 [US2] Verificar que `specs/000-gobierno-y-constitucion/plan.md` incluye Constitution Check y Post-Design Constitution Check en PASS.
- [ ] T027 [US2] Registrar cualquier contradicción entre `docs/ROADMAP.md` y `specs/000-gobierno-y-constitucion/spec.md` como pendiente en `specs/000-gobierno-y-constitucion/tasks.md`, sin modificar el roadmap.

**Checkpoint**: US2 completa cuando las reglas mínimas para artefactos futuros están validadas o cualquier contradicción queda registrada como pendiente.

---

## Phase 5: User Story 3 - Control de PRs y desviaciones (Priority: P3)

**Goal**: Validar que el cierre de Fase 0 protege PRs futuros y controla desviaciones.

**Independent Test**: Revisar CONTRIBUTING, Decision Log, matriz de trazabilidad, backlog y spec para confirmar que las desviaciones requieren autorización explícita y que el backlog no autoriza implementación por sí mismo.

- [ ] T028 [P] [US3] Verificar que `docs/CONTRIBUTING.md` exige declarar fase relacionada, alcance, documentación, pruebas y desviaciones en PRs.
- [ ] T029 [P] [US3] Verificar que `docs/CONTRIBUTING.md` incluye control explícito de `propuesta de desviación`.
- [ ] T030 [P] [US3] Verificar que `docs/DECISION_LOG.md` existe como registro de decisiones relevantes.
- [ ] T031 [P] [US3] Verificar que `docs/TRACEABILITY_MATRIX.md` existe como mecanismo de trazabilidad.
- [ ] T032 [P] [US3] Verificar que `docs/BACKLOG.md` existe como repositorio de ideas futuras no implementables sin spec, plan y tareas.
- [ ] T033 [US3] Verificar que `specs/000-gobierno-y-constitucion/spec.md` declara que cualquier cambio fuera de constitución, spec activa, plan aprobado o roadmap es `propuesta de desviación`.
- [ ] T034 [US3] Verificar que `specs/000-gobierno-y-constitucion/data-model.md` define Propuesta de Desviación con autorización humana explícita.
- [ ] T035 [US3] Verificar que `specs/000-gobierno-y-constitucion/research.md` no resuelve automáticamente aclaraciones fuera de alcance.
- [ ] T036 [US3] Registrar cualquier desviación no autorizada detectada como pendiente en `specs/000-gobierno-y-constitucion/tasks.md`.

**Checkpoint**: US3 completa cuando PRs, backlog, decisiones, trazabilidad y desviaciones quedan validados o cualquier desviación queda registrada como pendiente.

---

## Phase 6: Finalización documental

**Purpose**: Preparar el cierre documental de Fase 0 sin ejecutar implementación.

- [ ] T037 Verificar que `specs/000-gobierno-y-constitucion/tasks.md` no contiene tareas de código, CLI, modelos Python, Evidence Payload, fixtures, motor RCA, reportes, Oracle, SSH, listener, collectors, SQL ni alert log reales.
- [ ] T038 Verificar que `specs/000-gobierno-y-constitucion/quickstart.md` puede ejecutarse como revisión documental de cierre de Fase 0.
- [ ] T039 Revisar `git status --short` y confirmar que los cambios preparados corresponden a artefactos SDD documentales de Fase 0.
- [ ] T040 Preparar mensaje de commit sugerido en `specs/000-gobierno-y-constitucion/tasks.md` con alcance documental de Fase 0.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No tiene dependencias.
- **Phase 2 Foundational**: Depende de Phase 1 y bloquea las historias si detecta implementación funcional.
- **US1 Gobierno documental ratificado**: Depende de Phase 2.
- **US2 Reglas mínimas para artefactos futuros**: Depende de Phase 2; puede ejecutarse después de US1 o en paralelo si ya pasó Foundational.
- **US3 Control de PRs y desviaciones**: Depende de Phase 2; puede ejecutarse después de US1 o en paralelo si ya pasó Foundational.
- **Phase 6 Finalización documental**: Depende de US1, US2 y US3.

### User Story Dependencies

- **US1 (P1)**: Prioridad mínima para cierre; valida jerarquía documental.
- **US2 (P2)**: Depende de que exista la jerarquía documental, pero sus revisiones son independientes por archivo.
- **US3 (P3)**: Depende de que exista la jerarquía documental, pero sus revisiones son independientes por archivo.

### Parallel Opportunities

- T004, T005 y T006 pueden ejecutarse en paralelo.
- T012, T013 y T014 pueden ejecutarse en paralelo.
- T019, T020 y T021 pueden ejecutarse en paralelo.
- T028, T029, T030, T031 y T032 pueden ejecutarse en paralelo.

---

## Parallel Example: Documental

```bash
# Revisiones paralelas posibles por archivos distintos:
Task: "Verificar docs/CONTRIBUTING.md"
Task: "Verificar docs/DECISION_LOG.md"
Task: "Verificar docs/TRACEABILITY_MATRIX.md"
Task: "Verificar docs/BACKLOG.md"
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Completar Phase 1 y Phase 2.
2. Completar US1 para validar jerarquía documental.
3. Detener y validar que la constitución es fuente normativa principal.

### Incremental Delivery

1. Completar US1 para jerarquía documental.
2. Completar US2 para reglas de artefactos SDD futuros.
3. Completar US3 para PRs, trazabilidad, backlog y desviaciones.
4. Completar Phase 6 para preparar cierre documental y commit.

### Scope Guard

- No ejecutar `$speckit-implement`.
- No crear ni modificar código.
- No resolver automáticamente contradicciones documentales fuera de alcance.
- Registrar inconsistencias como pendientes en `specs/000-gobierno-y-constitucion/tasks.md`.

---

## Notes

- Todas las tareas son documentales.
- Las tareas marcadas `[P]` revisan archivos distintos o no dependen de tareas incompletas.
- La tarea final de commit solo prepara el mensaje; no realiza commit.
