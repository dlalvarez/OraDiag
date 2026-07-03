# Data Model: Core RCA sin conectividad real

## Enums controlados

- **ReviewStatus**: `OK`, `INFO`, `WARNING`, `PROBLEM`, `CRITICAL`, `TIMEOUT`, `ERROR`, `SKIPPED`, `UNKNOWN`.
- **Severity**: `info`, `warning`, `critical`, `blocker`.
- **Confidence**: `low`, `medium`, `high`.
- **CausalDomain**: `operating_system`, `infrastructure`, `storage`, `database`, `application`, `user`, `data`, `undetermined`.
- **CausalRole**: `primary_cause`, `contributing_factor`, `related_finding`, `incidental_finding`, `ruled_out`, `not_evaluated`, `unknown`.
- **SymptomCategory**: `cannot_connect`, `connection_hangs`, `errors`, `slow_performance`, `partial_impact`, `availability_down`, `unspecified`.
- **LimitationType**: `timeout`, `error`, `insufficient_permissions`, `layer_unavailable`, `not_applicable`, `incomplete_data`, `skipped`.
- **EvidencePolarity**: `positive`, `negative`, `neutral`.
- **OutputFormat**: `console`, `json`.

## Entity: DiagnosticScenario

Representa el escenario de laboratorio ya normalizado.

**Fields**:
- `id`: identificador estable del escenario.
- `name`: nombre humano en espanol.
- `symptom`: `SymptomCategory`.
- `target_id`: target seleccionado.
- `profile`: perfil seleccionado.
- `started_at`: timestamp opcional de ejecucion simulada.

**Validation rules**:
- `id`, `target_id` y `profile` son obligatorios.
- Si no hay sintoma, `symptom` debe ser `unspecified`.

## Entity: TargetContext

Representa contexto tecnico simulado del target, sin credenciales reales.

**Fields**:
- `target_id`: identificador de target.
- `display_name`: nombre humano.
- `environment`: etiqueta opcional como `lab`, `dev` o `example`.
- `metadata`: datos tecnicos no sensibles.

**Validation rules**:
- No debe contener passwords, tokens, connection strings reales ni secretos literales.

## Entity: AccessLayer

Representa una capa tecnica evaluable o simulada sin conectividad real.

**Fields**:
- `name`: nombre neutral de capa, por ejemplo `database`, `storage`, `network`, `user_access`.
- `available`: booleano.
- `status`: `ReviewStatus`.
- `limitations`: lista de `Limitation`.

**Validation rules**:
- Si `available` es false, debe existir al menos una limitacion.

## Entity: EvidenceProviderMetadata

Describe el origen de evidencia sin acoplar el RCA engine.

**Fields**:
- `provider_type`: para Fase 1 debe ser `fixture`.
- `provider_name`: nombre del provider.
- `source_ref`: identificador o ruta de fixture, usado solo para trazabilidad.
- `loaded_at`: timestamp opcional.

**Validation rules**:
- El RCA engine no debe depender de `source_ref`.

## Entity: ObservedSubject

Entidad tecnica observada.

**Fields**:
- `kind`: tipo neutral como `session`, `user`, `service`, `instance`, `storage_area`, `access_layer`, `component`.
- `id`: identificador estable dentro del payload.
- `name`: nombre humano opcional.
- `attributes`: mapa estructurado sin secretos.

**Validation rules**:
- `kind` e `id` son obligatorios.
- `attributes` no debe contener datos funcionales ni secretos.

## Entity: Observation

Dato tecnico individual observado.

**Fields**:
- `id`: identificador estable.
- `check_id`: revision asociada.
- `subject`: `ObservedSubject`.
- `status`: `ReviewStatus`.
- `severity`: `Severity`.
- `polarity`: `EvidencePolarity`.
- `candidate_domain`: `CausalDomain` opcional.
- `time_window`: ventana temporal opcional con inicio/fin.
- `message`: texto humano en espanol.
- `structured_data`: mapa de datos tecnicos simulados.

**Validation rules**:
- `TIMEOUT`, `ERROR` y `SKIPPED` deben producir limitaciones o revisiones no evaluadas.
- `CRITICAL` no implica `primary_cause` sin evaluacion causal.

## Entity: Limitation

Restriccion explicita del diagnostico.

**Fields**:
- `id`: identificador estable.
- `type`: `LimitationType`.
- `scope`: capa, revision o evidencia afectada.
- `message`: descripcion humana en espanol.
- `impact`: impacto sobre confianza o cobertura.

**Validation rules**:
- Toda limitacion debe tener `type`, `scope` y `message`.

## Entity: ReviewResult

Resultado de una revision tecnica simulada.

**Fields**:
- `check_id`: identificador de revision.
- `title`: titulo humano.
- `status`: `ReviewStatus`.
- `severity`: `Severity`.
- `observations`: lista de `Observation`.
- `limitations`: lista de `Limitation`.
- `ok_relevance`: texto opcional que explica por que un OK descarta hipotesis.

**Validation rules**:
- `OK` puede tener `ok_relevance` y debe conservarse si descarta hipotesis.
- `TIMEOUT`, `ERROR` y `SKIPPED` deben tener limitaciones.

## Entity: EvidencePayload

Contrato formal entre providers y RCA engine.

**Fields**:
- `schema_version`: version del contrato, inicial `1.0`.
- `scenario`: `DiagnosticScenario`.
- `target`: `TargetContext`.
- `provider`: `EvidenceProviderMetadata`.
- `access_layers`: lista de `AccessLayer`.
- `reviews`: lista de `ReviewResult`.
- `observations`: lista de `Observation`.
- `limitations`: lista de `Limitation`.

**Validation rules**:
- Debe serializarse a JSON.
- Debe validarse antes del RCA engine.
- No debe contener expected diagnosis/output.
- No debe depender de YAML ni de rutas de archivo para su semantica.

## Entity: DiagnosticFinding

Hallazgo derivado de evidencia validada.

**Fields**:
- `id`: identificador estable.
- `title`: titulo humano.
- `description`: descripcion en espanol.
- `domain`: `CausalDomain`.
- `role`: `CausalRole`.
- `severity`: `Severity`.
- `confidence`: `Confidence`.
- `evidence_ids`: ids de observaciones/revisiones usadas.
- `limitation_ids`: ids de limitaciones relacionadas.

**Validation rules**:
- `primary_cause` requiere evidencia positiva suficiente.
- `incidental_finding` puede ser severo, pero no causa principal sin correlacion.
- `ruled_out` debe referenciar evidencia negativa u OK relevante.

## Entity: CausalAssessment

Evaluacion causal consolidada.

**Fields**:
- `status`: `determined` o `undetermined`.
- `primary_cause_id`: id de hallazgo principal opcional.
- `domain`: `CausalDomain`.
- `confidence`: `Confidence`.
- `reasoning`: explicacion breve y deterministica en espanol.
- `evidence_ids`: evidencias centrales.
- `contradictions`: lista de contradicciones entre sintoma y evidencia.

**Validation rules**:
- Si `status` es `undetermined`, `primary_cause_id` debe estar vacio y `confidence` debe ser `low`.
- El sintoma puede aparecer en `reasoning`, pero no como unica evidencia.

## Entity: Recommendation

Accion inicial prudente.

**Fields**:
- `id`: identificador estable.
- `title`: titulo humano.
- `description`: recomendacion en espanol.
- `risk`: `low`, `medium` o `high`.
- `prerequisites`: lista de condiciones.
- `requires_human_validation`: booleano.

**Validation rules**:
- Fase 1 no debe recomendar acciones destructivas ni cambios productivos automaticos.

## Entity: DiagnosticResult

Salida consolidada del diagnostico.

**Fields**:
- `schema_version`: version del contrato de resultado, inicial `1.0`.
- `tool`: nombre/version de OraDiag.
- `scenario`: resumen de escenario.
- `assessment`: `CausalAssessment`.
- `findings`: lista de `DiagnosticFinding`.
- `related_findings`: ids o hallazgos relacionados.
- `incidental_findings`: ids o hallazgos incidentales.
- `ok_reviews`: revisiones OK relevantes.
- `limitations`: lista de limitaciones.
- `recommendations`: lista de recomendaciones.
- `insufficient_evidence`: booleano.

**Validation rules**:
- Debe serializarse a JSON estable.
- Debe incluir advertencia si `insufficient_evidence` es true.
- Debe conservar hallazgos y OK relevantes aunque no sean causa principal.

## State transitions

- Fixture YAML humano -> datos crudos de laboratorio.
- Datos crudos -> `EvidencePayload` validado.
- `EvidencePayload` -> `DiagnosticFinding` y `CausalAssessment`.
- `DiagnosticFinding` + `CausalAssessment` -> `DiagnosticResult`.
- `DiagnosticResult` -> salida console o JSON.

No existe transicion YAML -> RCA engine ni fixture expected output -> RCA engine.
