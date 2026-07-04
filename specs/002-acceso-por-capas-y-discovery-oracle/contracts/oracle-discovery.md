# Contract: Oracle Discovery

## Purpose

Define el contrato documental para Discovery Oracle inicial en Spec 002. Discovery obtiene contexto técnico observable y tolerante a fallas; no emite conclusiones RCA.

## Discovery Fields

Campos permitidos:

- `database_version`
- `database_name`
- `instance_name`
- `host_name`
- `dbid`
- `cdb`
- `pdbs`
- `rac`
- `asm`
- `standby`
- `services`
- `listener`

Cada campo debe registrar visibilidad:

```text
visible
unknown
not_evaluated
not_applicable
```

## Visibility Rules

- `visible` requiere valor observado y fuente trazable.
- `unknown` no puede incluir valor inventado.
- `not_evaluated` debe asociarse a limitación o fuente no evaluada.
- `not_applicable` debe explicar por qué no aplica al target/contexto.

## Source Rules

Toda fuente de discovery debe indicar:

- `source_id`
- `layer_id`
- `source_type`
- `status`
- `limitations`

Fuentes permitidas en Spec 002:

- fake/double de SQL access;
- fake/double de listener context;
- fake/double de OS context;
- futuras fuentes reales encapsuladas, sin SQL crudo en RCA.

## Partial Discovery

Discovery parcial es válido:

- Los campos visibles se conservan.
- Los campos no visibles quedan `unknown`, `not_evaluated` o `not_applicable`.
- Las fallas se registran como limitaciones.
- No se aborta todo discovery si una fuente independiente falla.

## Boundary Rules

- Discovery no produce `primary_cause`.
- Discovery no interpreta síntoma como causa.
- Standby solo aparece como contexto técnico si es visible y corresponde al alcance evaluado.
- ASM visible no habilita análisis de capacidad.
- Listener/servicios visibles no habilitan troubleshooting avanzado.
- CDB/PDB visible no habilita topología avanzada fuera de Spec 002.
- No se consulta tabla de negocio ni dato funcional.

## Evidence Mapping

| Discovery outcome | Evidence target | Rule |
|-------------------|-----------------|------|
| Field visible | `Observation` neutral or `ReviewResult` info | Contexto técnico observable. |
| Field unknown | No value, optional `ReviewResult(UNKNOWN)` | No inferir. |
| Source timeout | `Limitation(timeout)` + `ReviewResult(TIMEOUT)` | Continuar con otras fuentes. |
| Permission missing | `Limitation(insufficient_permissions)` | No escalamiento automático. |
| Source not applicable | `Limitation(not_applicable)` or `ReviewResult(SKIPPED)` | Explicar alcance. |

## Prohibited Outputs

Discovery no debe emitir:

- SQL crudo;
- comandos OS;
- connection strings;
- secretos;
- datos funcionales;
- hallazgos de performance;
- análisis de usuarios;
- análisis de storage/FRA/redo;
- alert log;
- waits, sesiones o bloqueos.
