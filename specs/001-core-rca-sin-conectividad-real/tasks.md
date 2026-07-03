# Tasks: Core RCA sin conectividad real

**Input**: Design documents from `/specs/001-core-rca-sin-conectividad-real/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/cli.md`, `contracts/evidence-payload.md`, `contracts/diagnostic-result.md`, `.specify/memory/constitution.md`

**Tests**: Automated tests are REQUIRED by the OraDiag constitution. Tests are listed before or alongside the implementation they validate.

**Organization**: Tasks are grouped by setup/foundation and then by user story to preserve independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it affects different files and has no dependency on incomplete tasks.
- **[Story]**: User story from `spec.md` (`US1` to `US5`).
- Every task includes an explicit file path.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the Python project and package/test layout without implementing behavior.

- [ ] T001 Update Python requirement, project metadata, direct dependencies, dev dependency, and CLI entrypoint in `pyproject.toml`.
- [ ] T002 Create package marker files for CLI/config/models/providers/rca/reports in `src/oradiag/__init__.py`, `src/oradiag/cli/__init__.py`, `src/oradiag/config/__init__.py`, `src/oradiag/models/__init__.py`, `src/oradiag/providers/__init__.py`, `src/oradiag/rca/__init__.py`, and `src/oradiag/reports/__init__.py`.
- [ ] T003 Create planned implementation module placeholders in `src/oradiag/cli/app.py`, `src/oradiag/config/loader.py`, `src/oradiag/config/models.py`, `src/oradiag/models/enums.py`, `src/oradiag/models/evidence.py`, `src/oradiag/models/diagnostic.py`, `src/oradiag/providers/base.py`, `src/oradiag/providers/fixture.py`, `src/oradiag/rca/engine.py`, `src/oradiag/reports/console.py`, and `src/oradiag/reports/json.py`.
- [ ] T004 [P] Create test package/layout markers in `tests/unit/__init__.py`, `tests/integration/__init__.py`, `tests/contract/__init__.py`, and `tests/fixtures/__init__.py`.
- [ ] T005 [P] Create example/lab directories for non-secret inputs in `examples/lab/.gitkeep` and `tests/fixtures/lab/.gitkeep`.
- [ ] T006 Verify `.gitignore` covers Python/uv artifacts such as `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `dist/`, `*.egg-info/`, and local `.env*` in `.gitignore`.

**Checkpoint**: Project layout exists, but no runtime behavior is required yet.

---

## Phase 2: Foundational (Model and Contract First)

**Purpose**: Build the formal model and guardrails before fixtures, providers, RCA, reporters, or CLI behavior.

**Critical**: No fixture provider or RCA engine implementation should begin before this phase is complete.

- [ ] T007 [P] Add enum tests for review status, severity, confidence, domains, roles, symptom categories, limitation types, evidence polarity, and output formats in `tests/unit/test_enums.py`.
- [ ] T008 [P] Add Evidence Payload model validation and JSON serialization tests in `tests/unit/test_evidence_models.py`.
- [ ] T009 [P] Add Diagnostic Result model validation and JSON serialization tests in `tests/unit/test_diagnostic_models.py`.
- [ ] T010 [P] Add contract tests for Evidence Payload required fields and controlled values in `tests/contract/test_evidence_payload_contract.py`.
- [ ] T011 [P] Add contract tests for Diagnostic Result stable fields and insufficient-evidence semantics in `tests/contract/test_diagnostic_result_contract.py`.
- [ ] T012 Implement controlled enums from `data-model.md` in `src/oradiag/models/enums.py`.
- [ ] T013 Implement Evidence Payload Pydantic models including scenario, target, provider metadata, access layer, subject, observation, limitation, review result, and payload in `src/oradiag/models/evidence.py`.
- [ ] T014 Implement Diagnostic Result Pydantic models including finding, causal assessment, recommendation, and final result in `src/oradiag/models/diagnostic.py`.
- [ ] T015 Implement model validations for no expected diagnosis/output in payloads, no secret-like target metadata, limitation requirements for TIMEOUT/ERROR/SKIPPED, and undetermined assessment rules in `src/oradiag/models/evidence.py` and `src/oradiag/models/diagnostic.py`.
- [ ] T016 Export public model symbols from `src/oradiag/models/__init__.py`.
- [ ] T017 Add guardrail tests for prohibited package directories, prohibited class names, `.sql` files, and forbidden dependency names in `tests/unit/test_scope_guardrails.py`.

**Checkpoint**: The formal model is usable independently and guards the rest of the implementation.

---

## Phase 3: User Story 2 - Contrato formal de evidencia validado (Priority: P1)

**Goal**: Ensure all evidence reaches the RCA engine as validated Evidence Payload/models, never as YAML.

**Independent Test**: Load a lab fixture through the fixture provider and assert the RCA-facing object is an `EvidencePayload` with no expected diagnosis/output data.

### Tests for User Story 2

- [ ] T018 [P] [US2] Add neutral provider interface tests in `tests/unit/test_evidence_provider_base.py`.
- [ ] T019 [P] [US2] Add fixture transformation tests for YAML-to-EvidencePayload in `tests/unit/test_fixture_provider.py`.
- [ ] T020 [P] [US2] Add test that `expected_output` and `expected_diagnosis` remain test-only and are excluded from Evidence Payload in `tests/unit/test_fixture_provider_expected_sections.py`.
- [ ] T021 [P] [US2] Add test that the RCA engine public API rejects or has no supported path for YAML/raw dict input in `tests/unit/test_engine_rejects_yaml.py`.

### Implementation for User Story 2

- [ ] T022 [US2] Define neutral `EvidenceProvider` protocol or base class returning `EvidencePayload` in `src/oradiag/providers/base.py`.
- [ ] T023 [US2] Implement safe YAML loading helpers for fixture files using `PyYAML` in `src/oradiag/providers/fixture.py`.
- [ ] T024 [US2] Implement `FixtureEvidenceProvider` transformation from human YAML to `EvidencePayload` in `src/oradiag/providers/fixture.py`.
- [ ] T025 [US2] Ensure fixture expected sections are ignored by provider transformation and only available to tests through explicit test helpers in `src/oradiag/providers/fixture.py`.
- [ ] T026 [US2] Export provider symbols from `src/oradiag/providers/__init__.py`.

**Checkpoint**: US2 complete when Evidence Payload is validated and provider-origin independent.

---

## Phase 4: User Story 4 - Configuración y perfiles declarativos de laboratorio (Priority: P2)

**Goal**: Load human YAML configuration, targets, and profiles without secrets or causal side effects.

**Independent Test**: Load valid/invalid config files and confirm target/profile selection succeeds or fails with controlled errors.

### Tests for User Story 4

- [ ] T027 [P] [US4] Add config model tests for targets without credentials and declarative profiles in `tests/unit/test_config_models.py`.
- [ ] T028 [P] [US4] Add YAML loader tests for valid config, invalid YAML, missing target, missing profile, and secret-like values in `tests/unit/test_config_loader.py`.
- [ ] T029 [P] [US4] Add profile behavior test confirming `diag_all` groups checks but does not alter causal rules in `tests/unit/test_profiles.py`.

### Implementation for User Story 4

- [ ] T030 [US4] Implement config Pydantic models for target, profile, and app config in `src/oradiag/config/models.py`.
- [ ] T031 [US4] Implement config YAML loader and controlled config exceptions in `src/oradiag/config/loader.py`.
- [ ] T032 [US4] Implement profile lookup and required `diag_all` profile support in `src/oradiag/config/models.py`.
- [ ] T033 [US4] Create non-secret example config with target `lab_orcl_01` and profile `diag_all` in `examples/lab/config.yaml`.
- [ ] T034 [US4] Export config loader/model symbols from `src/oradiag/config/__init__.py`.

**Checkpoint**: US4 complete when config/profile selection works without triggering RCA or connectivity.

---

## Phase 5: User Story 3 - RCA mínimo determinístico y prudente (Priority: P2)

**Goal**: Classify causal roles and produce prudent determined/undetermined assessments from models only.

**Independent Test**: Run the engine directly against constructed `EvidencePayload` objects for the required RCA scenarios.

### Tests for User Story 3

- [ ] T035 [P] [US3] Add RCA test for slow lock contention as primary database cause in `tests/unit/test_rca_engine_lock_contention.py`.
- [ ] T036 [P] [US3] Add RCA test for simulated user authentication/access issue in `tests/unit/test_rca_engine_user_access.py`.
- [ ] T037 [P] [US3] Add RCA test for insufficient evidence from timeouts/errors/permissions producing undetermined result in `tests/unit/test_rca_engine_insufficient_evidence.py`.
- [ ] T038 [P] [US3] Add RCA test for severe incidental finding not becoming primary cause by severity alone in `tests/unit/test_rca_engine_incidental.py`.
- [ ] T039 [P] [US3] Add RCA test for OK reviews becoming ruled-out evidence or relevant OK output in `tests/unit/test_rca_engine_ok_reviews.py`.
- [ ] T040 [P] [US3] Add RCA test for all-technical-OK frontier toward application/data without business data in `tests/unit/test_rca_engine_data_boundary.py`.

### Implementation for User Story 3

- [ ] T041 [US3] Implement `RCAEngine` API that accepts only `EvidencePayload` and returns `DiagnosticResult` in `src/oradiag/rca/engine.py`.
- [ ] T042 [US3] Implement deterministic classification for lock contention and waits as database primary cause in `src/oradiag/rca/engine.py`.
- [ ] T043 [US3] Implement deterministic classification for user authentication/access evidence in `src/oradiag/rca/engine.py`.
- [ ] T044 [US3] Implement insufficient-evidence handling that returns undetermined, low confidence, and explicit limitations in `src/oradiag/rca/engine.py`.
- [ ] T045 [US3] Implement related, incidental, contributing, ruled_out, not_evaluated, and unknown role assignment rules in `src/oradiag/rca/engine.py`.
- [ ] T046 [US3] Implement preservation of relevant OK reviews and limitation propagation in `src/oradiag/rca/engine.py`.
- [ ] T047 [US3] Implement application/data boundary conclusion using only technical OK/absence-of-technical-cause evidence in `src/oradiag/rca/engine.py`.
- [ ] T048 [US3] Export RCA engine symbols from `src/oradiag/rca/__init__.py`.

**Checkpoint**: US3 complete when the engine is deterministic, evidence-based, and independent of YAML/providers.

---

## Phase 6: User Story 1 - Diagnóstico simulado ejecutable desde CLI (Priority: P1) MVP

**Goal**: Provide an end-to-end simulated diagnosis command using target, profile, symptom, fixture, and output.

**Independent Test**: Execute `oradiag run` against lab fixtures and receive diagnosis output without real connectivity.

### Tests for User Story 1

- [ ] T049 [P] [US1] Add fixture file for slow lock contention scenario in `tests/fixtures/lab/slow_lock_contention.yaml`.
- [ ] T050 [P] [US1] Add fixture file for user authentication scenario in `tests/fixtures/lab/user_authentication.yaml`.
- [ ] T051 [P] [US1] Add fixture file for insufficient evidence scenario in `tests/fixtures/lab/insufficient_evidence.yaml`.
- [ ] T052 [P] [US1] Add fixture file for severe incidental finding scenario in `tests/fixtures/lab/incidental_severe_finding.yaml`.
- [ ] T053 [P] [US1] Add fixture file for OK reviews scenario in `tests/fixtures/lab/ok_reviews_rule_out.yaml`.
- [ ] T054 [P] [US1] Add fixture file for technical OK application/data boundary scenario in `tests/fixtures/lab/technical_ok_data_boundary.yaml`.
- [ ] T055 [P] [US1] Add integration test for `oradiag run` lock contention JSON output in `tests/integration/test_cli_run_lock_contention.py`.
- [ ] T056 [P] [US1] Add integration test for `oradiag run` insufficient evidence console output in `tests/integration/test_cli_run_insufficient_console.py`.

### Implementation for User Story 1

- [ ] T057 [US1] Implement CLI Typer app skeleton and shared option parsing in `src/oradiag/cli/app.py`.
- [ ] T058 [US1] Implement end-to-end `run` command orchestration config -> provider -> EvidencePayload -> RCAEngine -> reporter in `src/oradiag/cli/app.py`.
- [ ] T059 [US1] Implement controlled CLI error handling for config, target, profile, fixture, payload, and output errors in `src/oradiag/cli/app.py`.
- [ ] T060 [US1] Ensure `run` does not import or call any real connectivity, SQL, listener, alert log, AI, or external integration module in `src/oradiag/cli/app.py`.

**Checkpoint**: MVP complete when `oradiag run` works end-to-end over lab fixtures.

---

## Phase 7: User Story 5 - Salidas console y JSON verificables (Priority: P3)

**Goal**: Emit stable JSON and Spanish console output derived from `DiagnosticResult`.

**Independent Test**: Run the same scenario with `--output json` and `--output console` and verify stable structured fields plus readable Spanish output.

### Tests for User Story 5

- [ ] T061 [P] [US5] Add JSON reporter tests for stable field ordering/required keys and insufficient evidence warning fields in `tests/unit/test_json_reporter.py`.
- [ ] T062 [P] [US5] Add console reporter tests for Spanish headings, cause, confidence, evidence, OK reviews, limitations, and recommendations in `tests/unit/test_console_reporter.py`.
- [ ] T063 [P] [US5] Add CLI output selection tests for `--output console`, `--output json`, and invalid output in `tests/integration/test_cli_outputs.py`.

### Implementation for User Story 5

- [ ] T064 [US5] Implement JSON reporter from `DiagnosticResult` using stable Pydantic serialization in `src/oradiag/reports/json.py`.
- [ ] T065 [US5] Implement console reporter in Spanish from `DiagnosticResult` without recalculating causal logic in `src/oradiag/reports/console.py`.
- [ ] T066 [US5] Export reporter symbols from `src/oradiag/reports/__init__.py`.
- [ ] T067 [US5] Wire reporter selection into `oradiag run` in `src/oradiag/cli/app.py`.

**Checkpoint**: US5 complete when outputs are stable, readable, and contract-conformant.

---

## Phase 8: CLI Identification and Cross-Story Integration

**Purpose**: Add version command and cross-story integration checks after core flow exists.

- [ ] T068 [P] Add CLI version command test in `tests/integration/test_cli_version.py`.
- [ ] T069 Implement `oradiag version` command using package metadata fallback in `src/oradiag/cli/app.py`.
- [ ] T070 [P] Add end-to-end integration tests for all six required scenarios through `oradiag run --output json` in `tests/integration/test_cli_all_scenarios_json.py`.
- [ ] T071 [P] Add end-to-end integration tests for representative console outputs in Spanish in `tests/integration/test_cli_console_spanish.py`.
- [ ] T072 Add test ensuring fixture expected sections are used only by tests and not visible in CLI/RCA results in `tests/integration/test_expected_sections_not_in_results.py`.

---

## Phase 9: Guardrails and Scope Validation

**Purpose**: Prove Fase 1 did not introduce prohibited scope.

- [ ] T073 Add repository guardrail test for no forbidden directories `sql/`, `oracle/`, `ssh/`, `listener/`, `awr/`, `ash/`, or `alert_log/` in `tests/unit/test_scope_guardrails.py`.
- [ ] T074 Add repository guardrail test for no forbidden class names `OracleConnector`, `SSHConnector`, `ListenerCollector`, or real collector equivalents in `tests/unit/test_scope_guardrails.py`.
- [ ] T075 Add repository guardrail test for no `.sql` files in `tests/unit/test_scope_guardrails.py`.
- [ ] T076 Add dependency guardrail test for no Oracle, SSH, AI, web API, SQLite/database, or external integration dependencies in `tests/unit/test_scope_guardrails.py`.
- [ ] T077 Add secret guardrail test scanning `examples/lab/` and `tests/fixtures/lab/` for password/token/secret-like literal values in `tests/unit/test_scope_guardrails.py`.
- [ ] T078 Add test confirming no business-table or functional-data fields are required by Evidence Payload or Diagnostic Result contracts in `tests/contract/test_no_business_data_contract.py`.

---

## Phase 10: Final Validation and Documentation Review

**Purpose**: Run final checks and update feature documentation only if implementation changed expected usage.

- [ ] T079 Run dependency resolution with `uv sync` and keep generated lockfile changes if applicable in `uv.lock`.
- [ ] T080 Run all automated tests with `uv run pytest`.
- [ ] T081 Run `uv run oradiag version` and verify Spanish identification output.
- [ ] T082 Run `uv run oradiag run --config examples/lab/config.yaml --target lab_orcl_01 --profile diag_all --symptom slow_performance --fixture tests/fixtures/lab/slow_lock_contention.yaml --output console`.
- [ ] T083 Run `uv run oradiag run --config examples/lab/config.yaml --target lab_orcl_01 --profile diag_all --symptom slow_performance --fixture tests/fixtures/lab/slow_lock_contention.yaml --output json`.
- [ ] T084 Review and update `specs/001-core-rca-sin-conectividad-real/quickstart.md` only if command syntax or expected local validation changed.
- [ ] T085 Verify `git status --short` contains only files allowed by Spec 001 implementation scope and no modifications to future specs.
- [ ] T086 Verify no `propuesta de desviación` was implemented without explicit human authorization and document any finding in `specs/001-core-rca-sin-conectividad-real/tasks.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies.
- **Phase 2 Foundational**: Depends on Phase 1 and blocks all user stories.
- **US2 Evidence Contract**: Starts after Phase 2 because providers depend on models.
- **US4 Config/Profile**: Starts after Phase 2; can run in parallel with US2 after models exist.
- **US3 RCA Engine**: Depends on Phase 2 and benefits from US2 test fixtures, but engine tests should construct models directly.
- **US1 CLI Run MVP**: Depends on US2, US3, and US4.
- **US5 Reporters**: Depends on Diagnostic Result models and integrates with US1.
- **Phase 8 Integration**: Depends on US1 and US5.
- **Phase 9 Guardrails**: Can run after Phase 1, but final value comes after implementation files exist.
- **Phase 10 Final Validation**: Depends on all implementation phases.

### User Story Dependencies

- **US2 (P1)**: Contract foundation for all evidence providers and RCA engine.
- **US4 (P2)**: Provides config/profile inputs needed by CLI.
- **US3 (P2)**: Provides diagnostic behavior needed by CLI and reporters.
- **US1 (P1 MVP)**: End-to-end run command once provider/config/engine exist.
- **US5 (P3)**: Stable output layer derived from `DiagnosticResult`.

### Parallel Opportunities

- T004 and T005 can run in parallel after T001.
- T007 through T011 can be written in parallel before model implementation.
- T018 through T021 can be written in parallel for US2 tests.
- T027 through T029 can be written in parallel for US4 tests.
- T035 through T040 can be written in parallel for RCA scenario tests.
- T049 through T056 can be written in parallel because they use distinct fixture/test files.
- T061 through T063 can be written in parallel for reporter tests.
- T070 and T071 can be written in parallel after CLI flow exists.

---

## Parallel Example: Foundational Tests

```bash
Task: "Add enum tests in tests/unit/test_enums.py"
Task: "Add Evidence Payload model tests in tests/unit/test_evidence_models.py"
Task: "Add Diagnostic Result model tests in tests/unit/test_diagnostic_models.py"
Task: "Add Evidence Payload contract tests in tests/contract/test_evidence_payload_contract.py"
Task: "Add Diagnostic Result contract tests in tests/contract/test_diagnostic_result_contract.py"
```

## Parallel Example: Scenario Fixtures

```bash
Task: "Create tests/fixtures/lab/slow_lock_contention.yaml"
Task: "Create tests/fixtures/lab/user_authentication.yaml"
Task: "Create tests/fixtures/lab/insufficient_evidence.yaml"
Task: "Create tests/fixtures/lab/incidental_severe_finding.yaml"
Task: "Create tests/fixtures/lab/ok_reviews_rule_out.yaml"
Task: "Create tests/fixtures/lab/technical_ok_data_boundary.yaml"
```

---

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete US2 so evidence contract and fixture provider are safe.
3. Complete US4 for config/profile selection.
4. Complete US3 for RCA engine over models.
5. Complete US1 for `oradiag run` end-to-end with JSON output first.
6. Add US5 console output and final integrations.

### Incremental Delivery

1. Validate model/contract tests independently.
2. Validate provider transformation without RCA.
3. Validate RCA engine without CLI.
4. Validate CLI orchestration using provider + RCA + JSON reporter.
5. Validate console reporter.
6. Run guardrails and full quickstart.

### Scope Guard

- Do not implement real Oracle, SSH, listener, SQL, alert log, collectors, AWR/ASH, historical storage, SQLite, web API, IA, business tables, or functional data.
- Do not create files or folders for future specs.
- Do not create `.sql` files.
- Do not use OraHealth/OraParity decisions by analogy.

---

## Final Validation Criteria

- `uv sync` completes.
- `uv run pytest` passes.
- `uv run oradiag version` works.
- `uv run oradiag run ... --output console` works for at least lock contention and insufficient evidence scenarios.
- `uv run oradiag run ... --output json` produces stable `DiagnosticResult` JSON.
- Guardrail tests prove no forbidden folders, classes, files, dependencies, secrets, business data, YAML-direct-to-engine path, or future-phase functionality entered Fase 1.
