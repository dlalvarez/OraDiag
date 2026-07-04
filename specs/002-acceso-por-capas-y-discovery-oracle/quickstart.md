# Quickstart: Acceso por capas y Discovery Oracle

## Purpose

Guía de validación futura para Spec 002. La validación debe ser local, segura y basada en fakes/doubles/mocks.

## Prerequisites

- Python 3.12+.
- `uv` instalado.
- Repositorio local de OraDiag.
- Spec 001 validada.
- Ningún Oracle real.
- Ningún SSH real.
- Ningún listener real.
- Ninguna credencial real.
- Ningún archivo `.sql`.
- Ninguna conectividad productiva.

## Install

```bash
uv sync
```

## Run Test Suite

```bash
uv run pytest
```

Expected:

- Pruebas de Spec 001 siguen pasando.
- Pruebas futuras de Spec 002 usan fakes/doubles/mocks.
- No se requiere infraestructura real.

## Validate Layer Access With Fakes

Las tareas futuras deben agregar escenarios automatizados equivalentes a:

```bash
uv run pytest tests/unit/test_layer_access_models.py
uv run pytest tests/unit/test_layer_fake_backend.py
uv run pytest tests/integration/test_cli_layered_access_fake.py
```

Expected:

- Una capa accesible produce `AccessLayer(available=true)` y contexto/evidencia compatible.
- Una capa con timeout produce `Limitation(type=timeout)` y no cuelga la ejecución.
- Permisos insuficientes producen `Limitation(type=insufficient_permissions)`.
- Capa no disponible no aborta capas independientes.
- No aparecen secretos, SQL crudo ni comandos OS en resultados.

## Validate Oracle Discovery With Fakes

Las tareas futuras deben agregar escenarios automatizados equivalentes a:

```bash
uv run pytest tests/unit/test_oracle_discovery_models.py
uv run pytest tests/unit/test_oracle_discovery_fake.py
uv run pytest tests/integration/test_cli_oracle_discovery_fake.py
```

Expected:

- Discovery parcial conserva versión, database name, instancia, host o DBID visibles.
- CDB/PDB, RAC, ASM, standby, servicios o listener no visibles quedan `unknown`, `not_evaluated` o con limitación.
- Standby solo aparece si el fake lo marca como visible y correspondiente al alcance.
- Discovery no genera causa RCA por sí mismo.

## Validate Evidence Integration

Las tareas futuras deben agregar escenarios automatizados equivalentes a:

```bash
uv run pytest tests/contract/test_layer_access_contract.py
uv run pytest tests/contract/test_oracle_discovery_contract.py
uv run pytest tests/contract/test_evidence_integration_contract.py
```

Expected:

- `LayerExecutionResult` se transforma antes de entrar al RCA.
- `OracleDiscoveryContext` se convierte en contexto/evidencia neutral o limitaciones.
- `RCAEngine` sigue aceptando solo `EvidencePayload`.
- Reporters solo serializan `DiagnosticResult`.

## CLI Validation Shape

Spec 002 debe preservar la CLI existente:

```bash
uv run oradiag run \
  --config examples/lab/config.yaml \
  --target lab_orcl_01 \
  --profile diag_all \
  --symptom availability_down \
  --fixture tests/fixtures/lab/insufficient_access.yaml \
  --output json
```

Expected:

- La ruta de fixture de Spec 001 sigue funcionando.
- Las rutas fake/double futuras se agregan sin romper `--fixture`.
- El resultado no contiene SQL crudo, secretos ni conectividad real.

## Out Of Scope Validation

Confirmar que Spec 002 no introduce:

- `tasks.md` durante `speckit-plan`;
- conectores Oracle reales productivos;
- SSH real productivo;
- listener real productivo;
- archivos `.sql`;
- tablas de negocio;
- datos funcionales;
- IA;
- alert log;
- waits, sesiones o bloqueos;
- storage, FRA, TEMP, UNDO, redo o archive;
- AWR/ASH;
- SQLite o histórico;
- endpoints/API web;
- dashboards;
- reportes markdown/html.
