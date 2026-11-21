# Plan: Gobierno y constitución (v2)

**Spec**: [spec.md](./spec.md) | **Fecha**: 2026-11-21 | **Rama**: `spec/000-revision-gobierno`

## Resumen

Revisión línea por línea de los artefactos generados en la v1 y su alineación
con la constitución 2.0.0. Trabajo exclusivamente documental y de
configuración de Spec Kit; no se crea ni modifica código.

## Alcance del cambio

| Artefacto | Acción |
|---|---|
| `.specify/memory/constitution.md` | Enmendada a 2.0.0 (commit previo) |
| `docs/` (13 documentos) | Reescritos o ajustados a la v2 |
| `README.md`, `.github/pull_request_template.md` | Actualizados |
| `specs/000-*` | Condensada en `spec.md` y `plan.md` |
| `specs/001-*`, `specs/002-*` | Marcadas como históricas con revisión de lo reutilizable |
| `.specify/templates/*` | Ajustadas a GOV-001 a GOV-003 y principios XII-XV |
| Integración de Spec Kit | Cambiada de Codex a Claude Code |

## Constitution Check

| Principio | Estado | Nota |
|---|---|---|
| I. RCA, no health check | PASS | Reforzado en docs y README |
| II. La evidencia manda | PASS | Sin cambios de fondo |
| III. Síntoma como pista | PASS | Se agrega la ventana del incidente como dato del reporte |
| IV. Separación causal | PASS | Sin cambios de fondo |
| V. OK visibles | PASS | Sin cambios de fondo |
| VI. Dominios causales | PASS | Dominios con fuentes del núcleo y de adaptadores |
| VII. Sin tablas de negocio | PASS | Se agrega tratamiento de SQL y binds como sensibles |
| VIII. Fallas controladas | PASS | Continuidad reescrita sin dependencia de SSH |
| IX. Seguridad | PASS | Se elimina el password en texto plano permitido en v1 |
| X. Contratos y pruebas | PASS | Origen de la evidencia explícito en el modelo |
| XI. Trazabilidad | PASS | Matriz reescrita con los principios I-XV |
| XII. Núcleo portable | PASS | Arquitectura, dominios y errores alineados |
| XIII. Licencias explícitas | PASS | Limitaciones `not_licensed` y `license_mismatch` |
| XIV. Solo lectura | PASS | Documentado en seguridad y plantillas |
| XV. Correlación causal | PASS | Modelo RCA con ventana, cadenas y criterios de confianza |

## Validación

- Búsqueda de referencias obsoletas: agrupación `000-008`, "Fase N" como unidad
  de trabajo, SSH como requisito, AWR como fase futura, OraParity.
- Revisión de que cada documento de `docs/` remite a la constitución como fuente
  superior.
- Verificación de los comandos de Spec Kit para Claude Code.
