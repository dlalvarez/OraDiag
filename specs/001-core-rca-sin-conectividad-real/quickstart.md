# Quickstart: Core RCA sin conectividad real

## Prerequisites

- Python 3.12+.
- `uv` instalado.
- Repositorio local de OraDiag.
- Ningun acceso Oracle, SSH, listener, red, alert log, SQL, AWR/ASH ni servicio externo.

## Install

```bash
uv sync
```

## Identify tool

```bash
uv run oradiag version
```

Expected:
- Muestra nombre/version de OraDiag.
- No requiere configuracion ni fixture.

## Run simulated diagnosis

```bash
uv run oradiag run \
  --config examples/lab/config.yaml \
  --target lab_orcl_01 \
  --profile diag_all \
  --symptom slow_performance \
  --fixture tests/fixtures/lab/slow_lock_contention.yaml \
  --output console
```

Expected:
- Salida en espanol.
- Causa probable si hay evidencia suficiente.
- Evidencias usadas, OK relevantes, limitaciones y recomendaciones prudentes.
- Ningun intento de conexion real.

## JSON output

```bash
uv run oradiag run \
  --config examples/lab/config.yaml \
  --target lab_orcl_01 \
  --profile diag_all \
  --symptom slow_performance \
  --fixture tests/fixtures/lab/slow_lock_contention.yaml \
  --output json
```

Expected:
- JSON valido conforme a [contracts/diagnostic-result.md](./contracts/diagnostic-result.md).
- Campos estables para pruebas automatizadas.

## Required lab scenarios

La implementacion debe incluir fixtures para:

- lentitud por bloqueo/sesiones simuladas;
- problema de usuario/autenticacion simulado;
- evidencia insuficiente por timeouts/errores/permisos;
- hallazgo severo incidental;
- revisiones OK que descartan hipotesis;
- todo tecnico OK con frontera Aplicacion/Datos.

## Tests

```bash
uv run pytest
```

Expected coverage:
- CLI basica.
- Configuracion YAML.
- Modelos Pydantic.
- Evidence Payload JSON.
- FixtureEvidenceProvider.
- Prohibicion de YAML directo al RCA engine.
- RCA minimo por escenarios.
- JSON estable.
- Console basica en espanol.
- Ausencia de SQL, conectividad real, alert log real, IA, tablas de negocio y datos funcionales.

## Out of scope validation

Durante revision de Fase 1, confirmar que no existen:

- carpetas `sql/`, `oracle/`, `ssh/`, `listener/`, `awr/`, `ash/`, `alert_log/`;
- clases `OracleConnector`, `SSHConnector`, `ListenerCollector` o equivalentes reales;
- archivos `.sql`;
- dependencias de Oracle, SSH, web APIs, IA o bases de datos locales;
- fixtures usados como modelo formal del RCA engine.
