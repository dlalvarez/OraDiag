# Implementation Plan: Core RCA sin conectividad real

**Branch**: `001-core-rca-sin-conectividad-real` | **Date**: 2026-07-03 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-core-rca-sin-conectividad-real/spec.md`

## Summary

Construir el primer nucleo funcional ejecutable de OraDiag sin conectividad real: CLI minima, configuracion YAML humana, perfiles declarativos, modelos Pydantic, Evidence Payload JSON, fixtures de laboratorio, provider de fixtures, motor RCA minimo deterministico y salidas console/json. El diseno mantiene el modelo formal como fuente de verdad: los fixtures YAML se transforman a Evidence Payload/modelos internos antes del RCA engine, y el engine no depende de YAML, paths ni providers especificos.

## Technical Context

**Language/Version**: Python 3.12+.

**Primary Dependencies**: `uv`; runtime directo `typer==0.26.8`, `PyYAML==6.0.3`, `pydantic==2.13.4`; desarrollo/pruebas `pytest==9.1.1`.

**Storage**: N/A. Fase 1 no usa persistencia, historico, SQLite ni estado durable.

**Testing**: `pytest` con pruebas unitarias, integracion CLI, contratos JSON y escenarios de laboratorio.

**Target Platform**: CLI local Python en Linux/macOS/Windows compatible con Python 3.12+, sin requerir Oracle, SSH, listener, red ni servicios externos.

**Project Type**: Aplicacion CLI Python con libreria interna.

**Performance Goals**: Los escenarios de laboratorio deben terminar en menos de 2 segundos por ejecucion local normal; el RCA minimo debe ser deterministico y no hacer esperas, polling ni I/O de red.

**Constraints**: Sin conexion Oracle real, SSH real, listener real, collectors reales, SQL real, alert log real, AWR/ASH, historico, SQLite, API web, integraciones externas, IA, tablas de negocio ni datos funcionales. El motor RCA consume solo modelos internos/Evidence Payload validado.

**Scale/Scope**: Fase 1 cubre un conjunto pequeno de escenarios de laboratorio para validar contratos y comportamiento base; no cubre correlacion multicapas avanzada ni topologias Oracle avanzadas.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **RCA scope**: PASS. La feature diagnostica incidentes simulados de laboratorio con RCA minimo; no implementa health check, capacity planning, auditoria funcional ni busqueda generica de anomalias.
- **Roadmap phase**: PASS. Corresponde a `001-core-rca-sin-conectividad-real`, Fase 1. No se adelantan fases 2 a 14.
- **No future phases early**: PASS. Providers futuros se mencionan solo como reemplazabilidad contractual; no se implementan conectores, collectors, discovery, alert log, historico, reportes maduros ni topologias avanzadas.
- **No real connectivity**: PASS. El unico origen de evidencia en Fase 1 es `FixtureEvidenceProvider`; no hay Oracle, SSH, listener, red ni archivos tecnicos reales.
- **No real collectors**: PASS. Se prohiben clases y paquetes con semantica de collector/conector real como `OracleConnector`, `SSHConnector`, `ListenerCollector`, `sql/`, `oracle/`, `ssh/`, `listener/`, `awr/`, `ash/` o `alert_log/`.
- **No real SQL**: PASS. No se crean archivos SQL ni consultas Oracle; cualquier dato SQL-like en fixtures es dato estructurado simulado.
- **No real alert log**: PASS. No se lee ni parsea alert log real; errores simulados son observaciones de fixture.
- **No AI**: PASS. El RCA minimo es deterministico, explicable y basado en reglas simples verificables.
- **No business tables**: PASS. No se consultan, modelan ni infieren tablas de negocio, datos funcionales ni significado de aplicacion.
- **Evidence**: PASS. Toda conclusion requiere evidencia positiva, evidencia negativa o limitacion explicita dentro del Evidence Payload validado.
- **Symptom handling**: PASS. El sintoma se representa como contexto de priorizacion; no decide causalidad por si solo.
- **Causal roles**: PASS. El modelo preserva `primary_cause`, `contributing_factor`, `related_finding`, `incidental_finding`, `ruled_out`, `not_evaluated` y `unknown`.
- **Visible OK reviews**: PASS. `ReviewResult` conserva estados OK relevantes y el reporte debe mostrarlos cuando descarten hipotesis o expliquen confianza.
- **Causal domains**: PASS. Solo se usan Sistema Operativo, Infraestructura, Almacenamiento, Base de datos, Aplicacion, Usuario, Datos e Indeterminado; Datos es frontera, no permiso de inspeccion funcional.
- **Failures and timeouts**: PASS. `TIMEOUT`, `ERROR`, permisos insuficientes, capas no disponibles y `SKIPPED` se modelan como limitaciones o revisiones no evaluadas.
- **Security**: PASS. Configuracion y fixtures no contienen credenciales reales; secretos literales deben rechazarse o tratarse como error controlado.
- **Recommendations**: PASS. Las recomendaciones iniciales son prudentes, no destructivas y orientadas a validar evidencia o escalar al equipo correcto.
- **Evidence contract**: PASS. JSON es contrato formal versionado de Evidence Payload y Diagnostic Result; YAML solo es formato humano para configuracion y laboratorio.
- **Fixtures do not define model**: PASS. El modelo y contratos se disenan primero; los fixtures compilan a esos modelos.
- **Tests**: PASS. La fase exige pruebas automatizadas para CLI, config, modelos, contratos, provider, RCA, salidas, limitaciones, OK relevantes, no YAML directo y no alcance prohibido.
- **Language**: PASS. Documentacion, mensajes principales, salida console y reportes humanos quedan en espanol; identificadores tecnicos estables pueden estar en ingles.
- **Deviations**: PASS. No hay desviaciones aceptadas. Cualquier cambio fuera de constitucion, spec activa, plan aprobado o roadmap es `propuesta de desviación`.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-rca-sin-conectividad-real/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── cli.md
│   ├── diagnostic-result.md
│   └── evidence-payload.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
pyproject.toml
src/oradiag/
├── __init__.py
├── cli/
│   ├── __init__.py
│   └── app.py
├── config/
│   ├── __init__.py
│   ├── loader.py
│   └── models.py
├── models/
│   ├── __init__.py
│   ├── diagnostic.py
│   ├── enums.py
│   └── evidence.py
├── providers/
│   ├── __init__.py
│   ├── base.py
│   └── fixture.py
├── rca/
│   ├── __init__.py
│   └── engine.py
└── reports/
    ├── __init__.py
    ├── console.py
    └── json.py

tests/
├── contract/
├── fixtures/
├── integration/
└── unit/
```

**Structure Decision**: Proyecto Python unico bajo `src/oradiag` y pruebas bajo `tests`. Los nombres son neutrales y no representan conectividad real. No se crean carpetas `sql/`, `oracle/`, `ssh/`, `listener/`, `awr/`, `ash/` ni `alert_log/`.

## Implementation Blocks

1. **Base de proyecto**: actualizar `pyproject.toml` a Python 3.12+, dependencias exactas, script `oradiag = "oradiag.cli.app:app"` y estructura de paquetes.
2. **Modelo formal primero**: definir enums y modelos Pydantic de evidencia, diagnostico, hallazgos, limitaciones, recomendaciones y resultado final.
3. **Contratos JSON**: documentar y validar Evidence Payload y Diagnostic Result como contratos versionados y serializables.
4. **Configuracion y perfiles**: cargar YAML humano con targets de ejemplo y perfiles declarativos, incluyendo `diag_all`; validar errores controlados.
5. **Fixtures de laboratorio**: implementar `FixtureEvidenceProvider` que transforma YAML humano a Evidence Payload/modelos internos; expected output queda solo para tests.
6. **RCA minimo**: reglas deterministicas pequenas para escenarios requeridos; no IA, no heuristicas opacas, no correlacion avanzada.
7. **Reportes y CLI**: salida console en espanol y JSON estable; comandos `version` y `run`.
8. **Pruebas obligatorias**: cubrir CLI, config, modelos, contratos, provider, RCA, salidas y guardrails de alcance.

## Phase 0: Research

La investigacion consolida decisiones tecnicas y alternativas rechazadas para mantener Fase 1 pequena, verificable y gobernada por el modelo.

**Output**: [research.md](./research.md)

## Phase 1: Design & Contracts

### Data Model

El modelo conceptual de Fase 1 define entidades internas, enums, relaciones, validaciones y transiciones de estado para Evidence Payload y Diagnostic Result.

**Output**: [data-model.md](./data-model.md)

### Contracts

Los contratos documentan interfaces locales, no APIs externas:

- [contracts/cli.md](./contracts/cli.md): comandos, opciones, errores y salidas.
- [contracts/evidence-payload.md](./contracts/evidence-payload.md): contrato JSON versionado de evidencia.
- [contracts/diagnostic-result.md](./contracts/diagnostic-result.md): contrato JSON estable de resultado diagnostico.

### Quickstart

La guia valida instalacion local, comandos esperados, escenarios de laboratorio y pruebas automatizadas sin conectividad real.

**Output**: [quickstart.md](./quickstart.md)

## Post-Design Constitution Check

- **RCA scope**: PASS. Los artefactos disenan RCA minimo simulado, no health check.
- **Roadmap phase**: PASS. Todos los artefactos pertenecen a `001-core-rca-sin-conectividad-real`.
- **No future phases early**: PASS. La estructura excluye conectividad, collectors reales, historico, reportes maduros y topologias avanzadas.
- **Evidence**: PASS. `data-model.md` y `contracts/evidence-payload.md` exigen evidencia/limitaciones antes de conclusiones.
- **Symptom handling**: PASS. El sintoma queda como campo de contexto y priorizacion, no como causalidad.
- **Causal roles**: PASS. El modelo y contrato incluyen roles constitucionales.
- **Visible OK reviews**: PASS. `ReviewResult` y `DiagnosticResult` conservan OK relevantes.
- **Causal domains**: PASS. Se limitan a dominios aprobados y Datos como frontera.
- **No business tables**: PASS. No hay modelo, contrato ni carpeta para datos funcionales o SQL real.
- **Failures and timeouts**: PASS. Limitaciones y revisiones no evaluadas son entidades de primer nivel.
- **Security**: PASS. Configuracion de Fase 1 usa targets sin secretos y trata secretos literales como error controlado.
- **Recommendations**: PASS. Recomendaciones se modelan como prudentes, no destructivas y con alcance/riesgo.
- **Evidence contract**: PASS. JSON versionado gobierna intercambio; YAML queda humano y previo a transformacion.
- **Tests**: PASS. `quickstart.md` y contratos definen pruebas requeridas.
- **Language**: PASS. Artefactos en espanol y reportes humanos en espanol.
- **Deviations**: PASS. No hay desviaciones aceptadas.

## Complexity Tracking

No hay violaciones constitucionales ni complejidad a justificar.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Aclaraciones Requeridas

Ninguna. `docs/ROADMAP.md` ya declara para Fase 1 el motor RCA minimo simulado y salidas console/json, por lo que la aclaracion historica del Sync Impact Report constitucional no bloquea esta planificacion.
