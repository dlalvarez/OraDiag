# Research: Core RCA sin conectividad real

## Decision: Python 3.12+ con uv

**Rationale**: La constitucion exige Python 3.12+ y `uv`. Fase 1 debe actualizar el proyecto desde `>=3.11` a `>=3.12` y usar `uv` para resolver/ejecutar dependencias.

**Alternatives considered**:
- Mantener Python `>=3.11`: rechazado por contradiccion constitucional.
- Usar pip/venv como flujo principal: rechazado porque `uv` esta gobernado por la constitucion.

## Decision: Dependencias directas exactas

**Rationale**: El plan fija dependencias directas para una implementacion reproducible: `typer==0.26.8`, `PyYAML==6.0.3`, `pydantic==2.13.4` y `pytest==9.1.1`. `uv.lock` congelara transitivas durante implementacion.

**Alternatives considered**:
- Rangos amplios como `typer>=0.26`: rechazado para Fase 1 porque dificulta snapshots estables.
- Agregar librerias de logging, rich directo, jsonschema o snapshot testing: rechazado para mantener Fase 1 pequena.

## Decision: Typer para CLI minima

**Rationale**: La CLI debe exponer `version` y `run`, validar opciones y producir errores de uso controlados. Typer esta exigido por constitucion y encaja con una CLI pequena basada en tipos.

**Alternatives considered**:
- `argparse`: rechazado por contradiccion con la dependencia ratificada.
- CLI generica sin subcomandos: rechazado porque la spec requiere comando de version/identificacion y `run`.

## Decision: Pydantic como fuente de validacion del modelo formal

**Rationale**: Evidence Payload, observaciones, limitaciones, hallazgos y resultados necesitan validacion estructural y serializacion JSON estable. Pydantic permite definir enums, defaults controlados y validacion de entrada desde YAML/JSON.

**Alternatives considered**:
- Dataclasses sin validacion: rechazado porque el contrato debe validar payloads.
- JSON Schema manual como fuente primaria: rechazado para Fase 1; Pydantic puede generar o respaldar schemas futuros sin duplicar definiciones.

## Decision: PyYAML solo en bordes humanos

**Rationale**: YAML se usa para configuracion humana y fixtures de laboratorio, nunca como contrato formal del RCA engine. El provider transforma YAML a modelos internos antes de invocar RCA.

**Alternatives considered**:
- Que el engine lea YAML: rechazado por constitucion.
- Definir fixtures como modelo formal: rechazado porque los fixtures no gobiernan el diseno.

## Decision: EvidenceProvider neutral y FixtureEvidenceProvider de Fase 1

**Rationale**: El motor RCA debe depender de Evidence Payload/modelos internos, no del origen. `EvidenceProvider` es la abstraccion neutral reemplazable; `FixtureEvidenceProvider` es la unica implementacion de Fase 1.

**Alternatives considered**:
- Crear conectores Oracle/SSH/listener simulados: rechazado porque adelanta fases y normaliza nombres prohibidos.
- Pasar rutas de fixture al RCA engine: rechazado porque acopla el engine al origen.

## Decision: Evidence Payload JSON versionado

**Rationale**: El intercambio formal entre providers futuros y RCA engine necesita version estable, validacion y serializacion. El contrato inicial usa `schema_version` y campos suficientes para escenarios Fase 1.

**Alternatives considered**:
- JSON sin version: rechazado por falta de evolucion controlada.
- Contrato por fixture YAML: rechazado por acoplamiento a laboratorio.

## Decision: RCA minimo deterministico

**Rationale**: Fase 1 valida separacion causal con reglas explicables sobre evidencia simulada. El engine debe devolver causa probable solo con evidencia suficiente, clasificar hallazgos y emitir indeterminado ante evidencia pobre.

**Alternatives considered**:
- IA o LLM para resumir/diagnosticar: rechazado por fuera de alcance.
- Correlacion avanzada multicapas: rechazada porque pertenece a fases posteriores.

## Decision: Reporters console/json separados del engine

**Rationale**: El engine produce `DiagnosticResult`; reporters solo serializan/presentan. Esto evita que la salida controle la logica RCA y permite pruebas independientes.

**Alternatives considered**:
- Que el engine imprima directamente: rechazado por acoplamiento y dificultad de probar JSON estable.
- Markdown/HTML: rechazados por fuera de alcance de Fase 1.

## Decision: Tests como contrato ejecutable de Fase 1

**Rationale**: La constitucion exige pruebas automatizadas. Fase 1 debe probar guardrails: no YAML directo, no causa sin evidencia, OK visibles, limitaciones, JSON estable y ausencia de alcance prohibido.

**Alternatives considered**:
- Solo validacion manual: rechazada por contradiccion constitucional.
- Snapshots externos con librerias extra: rechazado para evitar dependencias adicionales; comparar dicts JSON ordenados es suficiente.
