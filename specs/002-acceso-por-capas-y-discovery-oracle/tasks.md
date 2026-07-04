# Tasks: Acceso por capas y Discovery Oracle

**Input**: Design documents from `specs/002-acceso-por-capas-y-discovery-oracle/`

**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `checklists/requirements.md`

**Tests**: Automated tests are REQUIRED by the OraDiag constitution. Implement test tasks before implementation tasks in each phase.

**Organization**: Tasks are grouped by setup, foundational work, user stories, guardrails and final validation. Each user story remains independently testable after the foundational phase.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files or depends only on completed earlier phases.
- **[Story]**: User story label from `spec.md`.
- Every task includes an exact file path.

## Phase 1: Setup and Spec 002 Guardrails

**Purpose**: Create safe implementation skeletons and shared guardrail tests without changing behavior.

- [ ] T001 Create empty package directories with `__init__.py` in `src/oradiag/layers/` and `src/oradiag/discovery/`
- [ ] T002 [P] Create unit test modules with initial failing assertions for Spec 002 model imports and guardrail constants in `tests/unit/test_layer_access_models.py`, `tests/unit/test_oracle_discovery_models.py`, `tests/unit/test_evidence_integration.py`, and `tests/unit/test_spec002_scope_guardrails.py`
- [ ] T003 [P] Create contract test modules with initial failing assertions for documented contract symbols and required mapping functions in `tests/contract/test_layer_access_contract.py`, `tests/contract/test_oracle_discovery_contract.py`, and `tests/contract/test_evidence_integration_contract.py`
- [ ] T004 [P] Create integration test modules with initial failing assertions that fake Spec 002 CLI/config paths are explicit and do not use real infrastructure in `tests/integration/test_cli_layered_access_fake.py` and `tests/integration/test_cli_oracle_discovery_fake.py`
- [ ] T005 Add Spec 002 scope constants for allowed layer ids and prohibited future-scope tokens in `src/oradiag/layers/scope.py`
- [ ] T006 Add tests that allowed Spec 002 layer ids are exactly `database/sql_access`, `listener/network`, `os/ssh`, `storage_context`, and `authentication/access` in `tests/unit/test_spec002_scope_guardrails.py`
- [ ] T007 Add tests that prohibited future-scope tokens include `.sql`, business tables, functional data, IA, AWR/ASH, alert log, waits, sessions, locks, FRA, TEMP, UNDO, redo, archive, SQLite, endpoints web, dashboards, markdown/html reports, user account diagnosis, and storage capacity in `tests/unit/test_spec002_scope_guardrails.py`

---

## Phase 2: Foundational Models and Shared Validation

**Purpose**: Define shared model primitives that block all user stories.

**Critical**: No user story implementation should start before this phase is complete.

- [ ] T008 Add tests for `AccessLayerDefinition`, `LayerExecutionRequest`, `LayerExecutionResult`, `LayerLimitation`, `LayerStatus`, `LayerVisibility`, and `LayerRecoverability` validation in `tests/unit/test_layer_access_models.py`
- [ ] T009 Add tests that `TIMEOUT`, `ERROR`, `SKIPPED`, and `available=False` require at least one limitation in `tests/unit/test_layer_access_models.py`
- [ ] T010 Add tests that layer request/result metadata rejects secret-like keys, SQL fragments, OS command fragments, SSH command fragments, and connection-string keys in `tests/unit/test_layer_access_models.py`
- [ ] T011 Add tests that layer ids are declarative and reject unknown ids or future-scope ids in `tests/unit/test_layer_access_models.py`
- [ ] T012 Implement layer access Pydantic models and enums in `src/oradiag/layers/models.py`
- [ ] T013 Implement shared layer validation helpers for secret-like metadata and prohibited command fragments in `src/oradiag/layers/validation.py`
- [ ] T014 Export layer model symbols from `src/oradiag/layers/__init__.py`
- [ ] T015 Add tests that `ProfileLayerSelection` accepts declarative layers, discovery groups, and timeout overrides but rejects causal rules, confidence controls, SQL, OS commands, SSH commands, hosts with secrets, and secret-like metadata in `tests/unit/test_config_models.py`
- [ ] T016 Extend `ProfileConfig` or add compatible nested config models for `ProfileLayerSelection` without breaking existing profile fields in `src/oradiag/config/models.py`
- [ ] T017 Add loader tests that existing `examples/lab/config.yaml` remains valid after Spec 002 config model changes in `tests/unit/test_config_loader.py`

**Checkpoint**: Shared layer/config models exist, Spec 001 config still loads, and guardrail tests fail before implementation then pass after implementation.

---

## Phase 3: User Story 1 - Acceso por capas tolerante a fallas (Priority: P1)

**Goal**: Evaluate independent access layers with controlled status, timeout, permission and availability outcomes.

**Independent Test**: Fake layer execution returns one accessible layer and one failed layer; execution preserves the accessible result and records the failed layer as limitation without aborting.

### Tests for User Story 1

- [ ] T018 [P] [US1] Add contract tests for the layer access request/result shape in `tests/contract/test_layer_access_contract.py`
- [ ] T019 [P] [US1] Add tests for deterministic fake backend scenarios `ok`, `timeout`, `permission_denied`, `unavailable`, `not_applicable`, and `error` in `tests/unit/test_layer_fake_backend.py`
- [ ] T020 [P] [US1] Add tests that timeout fake execution terminates without sleeping beyond a controlled test boundary in `tests/unit/test_layer_fake_backend.py`
- [ ] T021 [P] [US1] Add tests that a permission-denied fake result maps to `insufficient_permissions` and not automatic privilege escalation in `tests/unit/test_layer_fake_backend.py`
- [ ] T022 [P] [US1] Add tests that an unavailable layer maps to `layer_unavailable` and does not abort sibling layer execution in `tests/unit/test_layer_orchestrator.py`
- [ ] T023 [P] [US1] Add tests that a not-applicable layer maps to `not_applicable` and `SKIPPED` in `tests/unit/test_layer_orchestrator.py`

### Implementation for User Story 1

- [ ] T024 [P] [US1] Define the `LayerBackend` protocol in `src/oradiag/layers/base.py`
- [ ] T025 [P] [US1] Implement deterministic fake/double backend inputs and results in `src/oradiag/layers/fake.py`
- [ ] T026 [US1] Implement layer orchestration that executes independent backends and wraps backend exceptions as controlled `LayerExecutionResult` objects in `src/oradiag/layers/orchestrator.py`
- [ ] T027 [US1] Implement timeout-result handling in `src/oradiag/layers/orchestrator.py` using configured timeout values without real network calls
- [ ] T028 [US1] Add default Spec 002 layer definitions and scope boundaries in `src/oradiag/layers/definitions.py`
- [ ] T029 [US1] Export fake backend, backend protocol, definitions and orchestrator from `src/oradiag/layers/__init__.py`

**Checkpoint**: User Story 1 can be validated without discovery or RCA integration by running `uv run pytest tests/unit/test_layer_access_models.py tests/unit/test_layer_fake_backend.py tests/unit/test_layer_orchestrator.py tests/contract/test_layer_access_contract.py`.

---

## Phase 4: User Story 2 - Discovery Oracle técnico inicial (Priority: P1)

**Goal**: Produce partial Oracle technical context from fake/double discovery sources without inferring unseen topology or causal conclusions.

**Independent Test**: Fake discovery returns visible version/name/instance/DBID plus unknown RAC/ASM/standby/listener fields; visible fields are preserved and unknown fields have no invented values.

### Tests for User Story 2

- [ ] T030 [P] [US2] Add contract tests for `OracleDiscoveryContext`, `OracleDiscoveryField`, and `DiscoverySource` shape in `tests/contract/test_oracle_discovery_contract.py`
- [ ] T031 [P] [US2] Add tests for visible discovery fields including version, database name, instance, host, and DBID in `tests/unit/test_oracle_discovery_models.py`
- [ ] T032 [P] [US2] Add tests that `unknown`, `not_evaluated`, and `not_applicable` discovery fields cannot carry invented values in `tests/unit/test_oracle_discovery_models.py`
- [ ] T033 [P] [US2] Add tests that standby appears only when the fake marks it visible and corresponding to scope in `tests/unit/test_oracle_discovery_fake.py`
- [ ] T034 [P] [US2] Add tests that ASM visibility is accepted only as context and never includes capacity analysis in `tests/unit/test_oracle_discovery_fake.py`
- [ ] T035 [P] [US2] Add tests that listener and service visibility are accepted only as context and never include troubleshooting conclusions in `tests/unit/test_oracle_discovery_fake.py`
- [ ] T036 [P] [US2] Add tests that partial discovery preserves visible fields when one source times out or lacks permissions in `tests/unit/test_oracle_discovery_fake.py`

### Implementation for User Story 2

- [ ] T037 [P] [US2] Implement discovery Pydantic models for `OracleDiscoveryContext`, `OracleDiscoveryField`, `DiscoverySource`, and visibility states in `src/oradiag/discovery/models.py`
- [ ] T038 [P] [US2] Implement fake Oracle discovery source scenarios for full, partial, timeout, permission-limited, standby-visible, asm-visible, and listener-visible contexts in `src/oradiag/discovery/fake.py`
- [ ] T039 [US2] Implement discovery aggregation that merges visible fields, limitations, and source statuses without inference in `src/oradiag/discovery/orchestrator.py`
- [ ] T040 [US2] Add boundary validation for standby, ASM, listener, services, CDB/PDB, and unknown fields in `src/oradiag/discovery/validation.py`
- [ ] T041 [US2] Export discovery models, fake source, validation, and orchestrator from `src/oradiag/discovery/__init__.py`

**Checkpoint**: User Story 2 can be validated without CLI or RCA integration by running `uv run pytest tests/unit/test_oracle_discovery_models.py tests/unit/test_oracle_discovery_fake.py tests/contract/test_oracle_discovery_contract.py`.

---

## Phase 5: User Story 3 - Conversión de errores en limitaciones (Priority: P1)

**Goal**: Convert all layer/discovery failures to traceable limitations and non-evaluated reviews.

**Independent Test**: Timeout, error, permission denied, unavailable, not applicable and incomplete data all produce explicit limitations with scope, message and impact.

### Tests for User Story 3

- [ ] T042 [P] [US3] Add tests for mapping `LayerLimitation` to existing `Limitation` with type, scope, message and impact in `tests/unit/test_evidence_integration.py`
- [ ] T043 [P] [US3] Add tests that `TIMEOUT`, `ERROR`, and `SKIPPED` layer results produce `ReviewResult` with required limitations in `tests/unit/test_evidence_integration.py`
- [ ] T044 [P] [US3] Add tests that `available=False` layer results produce `AccessLayer` with limitations in `tests/unit/test_evidence_integration.py`
- [ ] T045 [P] [US3] Add tests that discovery source failures produce `ReviewResult(TIMEOUT|ERROR|SKIPPED)` and limitations in `tests/unit/test_evidence_integration.py`
- [ ] T046 [P] [US3] Add tests that all-failed layer/discovery input still builds a valid partial `EvidencePayload` with insufficient evidence candidates only in `tests/unit/test_evidence_integration.py`

### Implementation for User Story 3

- [ ] T047 [US3] Implement conversion from layer limitations to `Limitation` in `src/oradiag/providers/layered.py`
- [ ] T048 [US3] Implement conversion from layer results to `AccessLayer` and `ReviewResult` in `src/oradiag/providers/layered.py`
- [ ] T049 [US3] Implement conversion from discovery failures to `ReviewResult` and `Limitation` in `src/oradiag/providers/layered.py`
- [ ] T050 [US3] Implement controlled provider error classes for layer/discovery integration failures in `src/oradiag/providers/layered.py`
- [ ] T051 [US3] Export the layered provider integration symbols from `src/oradiag/providers/__init__.py`

**Checkpoint**: User Story 3 validates controlled failure conversion by running `uv run pytest tests/unit/test_evidence_integration.py`.

---

## Phase 6: User Story 4 - Validación con dobles antes de conectividad real (Priority: P2)

**Goal**: Ensure Spec 002 can be implemented and tested entirely with fakes/doubles/mocks.

**Independent Test**: A fake-backed provider produces deterministic layer and discovery outcomes without Oracle real, SSH real, listener real, credentials or `.sql` files.

### Tests for User Story 4

- [ ] T052 [P] [US4] Add tests that fake layer backends require no Oracle, SSH, listener, credentials, sockets, files under `sql/`, or `.sql` files in `tests/unit/test_layer_fake_backend.py`
- [ ] T053 [P] [US4] Add tests that fake discovery sources are deterministic for repeated inputs in `tests/unit/test_oracle_discovery_fake.py`
- [ ] T054 [P] [US4] Add tests that fake scenario selection is declarative and rejects SQL, OS commands and secret-like metadata in `tests/unit/test_layer_fake_backend.py`
- [ ] T055 [P] [US4] Add integration tests for fake-backed layered provider execution without infrastructure real in `tests/integration/test_cli_layered_access_fake.py`

### Implementation for User Story 4

- [ ] T056 [US4] Implement fake scenario definitions for layer outcomes in `src/oradiag/layers/fake.py`
- [ ] T057 [US4] Implement fake discovery scenario definitions in `src/oradiag/discovery/fake.py`
- [ ] T058 [US4] Implement `LayeredFakeEvidenceProvider` that composes fake layer execution, fake discovery and evidence integration in `src/oradiag/providers/layered.py`
- [ ] T059 [US4] Add deterministic fake scenario names and descriptions for tests in `src/oradiag/providers/layered.py`

**Checkpoint**: User Story 4 validates fakes/doubles by running `uv run pytest tests/unit/test_layer_fake_backend.py tests/unit/test_oracle_discovery_fake.py tests/integration/test_cli_layered_access_fake.py`.

---

## Phase 7: User Story 5 - Integración con EvidencePayload (Priority: P2)

**Goal**: Produce `EvidencePayload` compatible with Spec 001 from layer/discovery results while keeping RCAEngine isolated.

**Independent Test**: The layered fake provider returns a validated `EvidencePayload`; RCAEngine receives only that payload and never backends, layer requests, SQL, SSH or listener details.

### Tests for User Story 5

- [ ] T060 [P] [US5] Add contract tests for evidence integration mapping from layer/discovery sources to `AccessLayer`, `ReviewResult`, `Observation`, and `Limitation` in `tests/contract/test_evidence_integration_contract.py`
- [ ] T061 [P] [US5] Add tests that discovery visible fields become neutral context observations or info reviews, not positive causal evidence, in `tests/unit/test_evidence_integration.py`
- [ ] T062 [P] [US5] Add tests that inaccessible layers never map to positive evidence in `tests/unit/test_evidence_integration.py`
- [ ] T063 [P] [US5] Add tests that `RCAEngine.evaluate()` is only called with `EvidencePayload` and rejects layer backend/request/result/discovery objects without requiring functional engine changes unless a minimal controlled input-type guard is missing in `tests/unit/test_rca_engine_input_contract.py`
- [ ] T064 [P] [US5] Add tests that JSON/console reporters serialize `DiagnosticResult` without recalculating discovery or layer causal logic in `tests/unit/test_json_reporter.py` and `tests/unit/test_console_reporter.py`
- [ ] T065 [P] [US5] Add integration tests that a fake-backed `EvidencePayload` can be evaluated without changing RCA scoring in `tests/integration/test_cli_oracle_discovery_fake.py`

### Implementation for User Story 5

- [ ] T066 [US5] Implement integration records for mapping traceability in `src/oradiag/providers/layered.py`
- [ ] T067 [US5] Implement neutral context observation creation for Oracle discovery fields in `src/oradiag/providers/layered.py`
- [ ] T068 [US5] Implement final `EvidencePayload` assembly from target config, profile selection, layer results, discovery context and limitations in `src/oradiag/providers/layered.py`
- [ ] T069 [US5] Ensure `RCAEngine` remains unchanged except for tests proving it rejects non-`EvidencePayload` inputs in `src/oradiag/rca/engine.py`
- [ ] T070 [US5] Ensure reporters remain unchanged except for tests proving they serialize only `DiagnosticResult` in `src/oradiag/reports/json.py` and `src/oradiag/reports/console.py`

**Checkpoint**: User Story 5 validates EvidencePayload integration by running `uv run pytest tests/contract/test_evidence_integration_contract.py tests/unit/test_evidence_integration.py tests/unit/test_rca_engine_input_contract.py tests/integration/test_cli_oracle_discovery_fake.py`.

---

## Phase 8: CLI, Config and Profile Integration

**Purpose**: Integrate fake-friendly Spec 002 execution with the existing CLI/config flow without breaking `--fixture`.

- [ ] T071 Add tests that existing `oradiag run --fixture ... --output json` behavior remains compatible in `tests/contract/test_cli_run_json.py`
- [ ] T072 Add tests that existing `oradiag run --fixture ... --output console` behavior remains compatible in `tests/contract/test_cli_run_console.py`
- [ ] T073 Add tests for fake-friendly Spec 002 CLI/config path using declarative config and no credentials in `tests/integration/test_cli_layered_access_fake.py`
- [ ] T074 Add tests that `ProfileConfig` accepts Spec 002 layer ids and timeout overrides while rejecting future-scope activation in `tests/unit/test_profiles.py`
- [ ] T075 Extend CLI orchestration to select the existing `FixtureEvidenceProvider` when `--fixture` is present and the fake layered provider only through the explicit Spec 002 fake path in `src/oradiag/cli/app.py`
- [ ] T076 Extend config resolution for declarative Spec 002 layer selection and timeout values without secrets in `src/oradiag/config/loader.py`
- [ ] T077 Add controlled CLI error messages for invalid Spec 002 layer/profile configuration in `src/oradiag/cli/app.py`
- [ ] T078 Update `examples/lab/config.yaml` only if needed to add declarative Spec 002 fake-friendly layer/profile examples without credentials, SQL, OS commands or future-scope checks

**Checkpoint**: CLI/config compatibility validates by running `uv run pytest tests/contract/test_cli_run_json.py tests/contract/test_cli_run_console.py tests/integration/test_cli_layered_access_fake.py tests/unit/test_profiles.py`.

---

## Phase 9: Scope Guard and Future-Phase Boundaries

**Purpose**: Prove Spec 002 does not implement or allow future phases.

- [ ] T079 Add guardrail tests that no `.sql` files exist and no `sql/` implementation folder is introduced in `tests/unit/test_spec002_scope_guardrails.py`
- [ ] T080 Add guardrail tests that no Oracle real connector, SSH real connector, listener real connector, sockets or network client dependencies are introduced in `tests/unit/test_spec002_scope_guardrails.py`
- [ ] T081 Add guardrail tests that no business table, functional data, IA, AWR/ASH, alert log, wait, session, lock, storage/FRA/redo, historical store, SQLite, endpoint web, dashboard, markdown report or html report module is introduced in `tests/unit/test_spec002_scope_guardrails.py`
- [ ] T082 Add guardrail tests that `authentication/access` has no account-locked, password-expired, failed-login-audit or user-causal diagnosis logic in `tests/unit/test_spec002_scope_guardrails.py`
- [ ] T083 Add guardrail tests that `storage_context` has no capacity, FRA, TEMP, UNDO, redo, archive or ASM capacity analysis logic in `tests/unit/test_spec002_scope_guardrails.py`
- [ ] T084 Add guardrail tests that `listener/network` has no deep listener/network troubleshooting or service diagnosis logic in `tests/unit/test_spec002_scope_guardrails.py`
- [ ] T085 Add guardrail tests that standby is only represented as visible technical context and not as DR/Data Guard generic diagnosis in `tests/unit/test_spec002_scope_guardrails.py`
- [ ] T086 Add implementation safeguards for prohibited tokens and future-scope boundaries in `src/oradiag/layers/scope.py`

**Checkpoint**: Guardrails validate by running `uv run pytest tests/unit/test_spec002_scope_guardrails.py`.

---

## Phase 10: Final Validation and Quickstart Closure

**Purpose**: Validate full Spec 002 implementation and ensure no deviation entered.

- [ ] T087 Run `uv sync`
- [ ] T088 Run `uv run pytest tests/unit/test_layer_access_models.py tests/unit/test_layer_fake_backend.py tests/unit/test_layer_orchestrator.py`
- [ ] T089 Run `uv run pytest tests/unit/test_oracle_discovery_models.py tests/unit/test_oracle_discovery_fake.py`
- [ ] T090 Run `uv run pytest tests/unit/test_evidence_integration.py tests/contract/test_layer_access_contract.py tests/contract/test_oracle_discovery_contract.py tests/contract/test_evidence_integration_contract.py`
- [ ] T091 Run `uv run pytest tests/integration/test_cli_layered_access_fake.py tests/integration/test_cli_oracle_discovery_fake.py`
- [ ] T092 Run `uv run pytest tests/unit/test_spec002_scope_guardrails.py`
- [ ] T093 Run `uv run pytest`
- [ ] T094 Run the existing fixture quickstart command `uv run oradiag run --config examples/lab/config.yaml --target lab_orcl_01 --profile diag_all --symptom availability_down --fixture tests/fixtures/lab/insufficient_access.yaml --output json`
- [ ] T095 Verify quickstart Spec 002 fake/double validation commands in `specs/002-acceso-por-capas-y-discovery-oracle/quickstart.md`
- [ ] T096 Run `git status --short`
- [ ] T097 Run `git diff --stat`
- [ ] T098 Verify every task in `specs/002-acceso-por-capas-y-discovery-oracle/tasks.md` is completed or explicitly deferred by human-approved scope decision before closing
- [ ] T099 Verify no `propuesta de desviación` was implemented without explicit human authorization in `specs/002-acceso-por-capas-y-discovery-oracle/tasks.md`

---

## Dependencies and Execution Order

### Phase Dependencies

- Phase 1 Setup has no dependencies.
- Phase 2 Foundational depends on Phase 1 and blocks all user stories.
- Phases 3, 4 and 5 are P1 and can proceed after Phase 2; execute in order if one engineer owns the work.
- Phases 6 and 7 are P2 and depend on Phases 3, 4 and 5.
- Phase 8 depends on Phases 6 and 7.
- Phase 9 can start after Phase 2 but must finish before final validation.
- Phase 10 depends on all selected implementation phases.

### User Story Dependencies

- **US1 Acceso por capas tolerante a fallas**: depends on Phase 2 only.
- **US2 Discovery Oracle técnico inicial**: depends on Phase 2 only.
- **US3 Conversión de errores en limitaciones**: depends on Phase 2 and uses models from US1/US2 when available.
- **US4 Validación con dobles/fakes/mocks**: depends on US1 and US2 model/backends.
- **US5 Integración con EvidencePayload**: depends on US1, US2 and US3.

### Test-First Rule

- Test tasks in each phase must be written before implementation tasks in that same phase.
- Contract tests must fail before model/provider implementation and pass after implementation.

## Parallel Execution Examples

### PR 1: modelos base y pruebas contractuales de acceso por capas

```text
Task: T008 Add tests for AccessLayerDefinition and LayerExecutionResult validation
Task: T009 Add tests for mandatory limitations
Task: T010 Add tests for secret and command rejection
Task: T018 Add contract tests for layer access request/result shape
```

### PR 2: modelos de discovery y pruebas contractuales

```text
Task: T030 Add oracle discovery contract tests
Task: T031 Add visible field tests
Task: T032 Add unknown/not_evaluated tests
Task: T033 Add standby visibility tests
```

### PR 3: fakes/doubles y orquestación

```text
Task: T019 Add deterministic fake backend tests
Task: T020 Add timeout boundary tests
Task: T024 Define LayerBackend protocol
Task: T025 Implement fake/double backend
Task: T026 Implement orchestrator
```

### PR 4: mapeo hacia EvidencePayload

```text
Task: T042 Add LayerLimitation mapping tests
Task: T060 Add evidence integration contract tests
Task: T047 Implement limitation conversion
Task: T068 Implement final EvidencePayload assembly
```

### PR 5: CLI/config/perfiles fake-friendly

```text
Task: T071 Preserve fixture JSON CLI behavior
Task: T073 Add fake-friendly CLI integration tests
Task: T075 Extend CLI orchestration
Task: T076 Extend config resolution
```

### PR 6: guardrails, quickstart validation and closure

```text
Task: T079 Add no .sql guardrail tests
Task: T080 Add no real connector guardrail tests
Task: T087 Run uv sync
Task: T093 Run uv run pytest
Task: T098 Verify no pending tasks
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1) for layer execution with fakes and controlled failures.
3. Stop and validate US1 independently.

### Incremental Delivery

1. PR 1: foundational layer models and contract tests.
2. PR 2: discovery models and contract tests.
3. PR 3: fake/double backends and orchestration.
4. PR 4: EvidencePayload integration.
5. PR 5: CLI/config/perfiles fake-friendly.
6. PR 6: guardrails and final quickstart validation.

## Scope Guard

Implementation tasks must not introduce:

- Oracle real;
- SSH real;
- listener real;
- `.sql` files;
- SQL crudo in RCA;
- comandos OS crudos in RCA;
- tablas de negocio;
- datos funcionales;
- IA;
- AWR/ASH;
- alert log;
- waits, sessions or locks;
- storage/FRA/TEMP/UNDO/redo/archive capacity analysis;
- markdown/html reports;
- histórico or SQLite;
- endpoints/API web;
- dashboards;
- user account diagnosis for `authentication/access`;
- storage capacity diagnosis for `storage_context`;
- deep listener/network troubleshooting for `listener/network`;
- DR/Data Guard generic diagnosis from standby context.

## No Deviations

No `propuesta de desviación` is authorized for Spec 002 tasks. If an implementation task appears to require scope outside Fases 2 and 3, stop and request human authorization before changing code.
