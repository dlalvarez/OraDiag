# Contract: Diagnostic Result JSON

## Purpose

Diagnostic Result es la salida estructurada estable de Fase 1. Debe poder compararse en pruebas automatizadas y alimentar la salida console sin cambiar la logica RCA.

## Top-level shape

```json
{
  "schema_version": "1.0",
  "tool": {},
  "scenario": {},
  "assessment": {},
  "findings": [],
  "related_findings": [],
  "incidental_findings": [],
  "ok_reviews": [],
  "limitations": [],
  "recommendations": [],
  "insufficient_evidence": false
}
```

## Required semantics

- `assessment.status` debe ser `determined` o `undetermined`.
- `assessment.primary_cause_id` solo existe cuando hay evidencia suficiente.
- `assessment.domain` usa dominios aprobados.
- `assessment.confidence` usa `low`, `medium` o `high`.
- `findings` conserva todos los hallazgos relevantes con rol causal.
- `ok_reviews` conserva revisiones OK relevantes para descartar hipotesis.
- `limitations` explica errores, timeouts, permisos insuficientes, capas no disponibles y datos incompletos.
- `recommendations` contiene acciones prudentes, no destructivas y con riesgo/prerrequisitos.
- `insufficient_evidence` debe ser true cuando no existe causa probable responsable.

## Stability rules

- Mantener `schema_version`.
- Mantener nombres de campos estables dentro de Fase 1.
- Preferir arrays vacios sobre campos omitidos para listas requeridas.
- Usar ids estables de evidencia/hallazgos para trazabilidad.
- No incluir datos no deterministas salvo version/tool metadata controlada.

## Console relationship

La salida console debe derivarse de Diagnostic Result y presentarse en espanol. No debe recalcular causalidad ni ocultar limitaciones relevantes.
