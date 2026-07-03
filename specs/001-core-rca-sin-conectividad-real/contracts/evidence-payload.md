# Contract: Evidence Payload JSON

## Purpose

Evidence Payload es el contrato formal entre providers y el RCA engine. En Fase 1 solo lo produce `FixtureEvidenceProvider`, pero el contrato no depende de fixtures ni de YAML.

## Top-level shape

```json
{
  "schema_version": "1.0",
  "scenario": {},
  "target": {},
  "provider": {},
  "access_layers": [],
  "reviews": [],
  "observations": [],
  "limitations": []
}
```

## Required sections

- `schema_version`: version del contrato. Inicialmente `1.0`.
- `scenario`: id, nombre, target, perfil y sintoma normalizado.
- `target`: contexto tecnico simulado sin credenciales reales.
- `provider`: metadata de origen; en Fase 1 `provider_type` debe ser `fixture`.
- `access_layers`: capas tecnicas simuladas y disponibilidad.
- `reviews`: resultados de revisiones con estados controlados.
- `observations`: evidencia individual trazable.
- `limitations`: limitaciones globales o compartidas.

## Controlled values

- Estados: `OK`, `INFO`, `WARNING`, `PROBLEM`, `CRITICAL`, `TIMEOUT`, `ERROR`, `SKIPPED`, `UNKNOWN`.
- Severidad: `info`, `warning`, `critical`, `blocker`.
- Dominios: `operating_system`, `infrastructure`, `storage`, `database`, `application`, `user`, `data`, `undetermined`.
- Sintomas: `cannot_connect`, `connection_hangs`, `errors`, `slow_performance`, `partial_impact`, `availability_down`, `unspecified`.
- Polaridad de evidencia: `positive`, `negative`, `neutral`.

## Validation rules

- Debe validarse con modelos internos antes de llegar al RCA engine.
- `TIMEOUT`, `ERROR` y `SKIPPED` deben tener limitacion asociada.
- `OK` puede tener relevancia causal negativa y no debe descartarse automaticamente.
- No debe incluir `expected_output`, `expected_diagnosis` ni conclusiones de prueba.
- No debe contener secretos, credenciales reales, tablas de negocio ni datos funcionales.
- No debe requerir rutas de archivo para interpretar la evidencia.

## Fixture boundary

Fixture YAML puede contener una representacion humana distinta, pero su unica ruta valida hacia RCA es:

```text
fixture YAML -> FixtureEvidenceProvider -> EvidencePayload validado -> RCA engine
```

La ruta siguiente esta prohibida:

```text
fixture YAML -> RCA engine
```
