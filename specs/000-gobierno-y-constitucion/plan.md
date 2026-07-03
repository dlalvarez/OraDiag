# Implementation Plan: Gobierno y Constitución SDD

**Branch**: `000-gobierno-y-constitucion` | **Date**: 2026-07-03 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/000-gobierno-y-constitucion/spec.md`

## Summary

Formalizar el cierre documental de Fase 0 para OraDiag/OraRCA. El plan verifica que la spec `000-gobierno-y-constitucion` quede alineada con la constitución, el Documento Rector, el roadmap agrupado por specs, CONTRIBUTING, Decision Log y la matriz de trazabilidad. El resultado es únicamente documental: plan, investigación mínima, modelo documental y guía de validación.

## Technical Context

**Language/Version**: N/A. Fase 0 no implementa código ni runtime.

**Primary Dependencies**: N/A. Solo documentos existentes de gobierno SDD.

**Storage**: N/A. No se crea persistencia ni repositorio de datos.

**Testing**: Revisión documental verificable; no hay pruebas de ejecución de código en Fase 0.

**Target Platform**: Repositorio de documentación de OraDiag/OraRCA.

**Project Type**: Gobierno documental SDD.

**Performance Goals**: N/A. No hay comportamiento ejecutable.

**Constraints**: No implementar funcionalidad de diagnóstico, no crear CLI, modelos Python, Evidence Payload, fixtures, motor RCA, reportes, conectividad Oracle, SSH, listener ni collectors. No adelantar Spec 001.

**Scale/Scope**: Una spec documental de Fase 0 y sus artefactos de planificación mínimos.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **RCA scope**: PASS. El plan preserva que OraDiag es RCA de incidentes Oracle, no health check, capacity planning, auditoría funcional, explorador de datos de negocio ni caza-problemas genérico.
- **Roadmap phase**: PASS. La feature corresponde a `000-gobierno-y-constitucion`, Fase 0: Gobierno documental. No implementa ni adelanta Fase 1 ni fases posteriores.
- **Evidence**: PASS. Para Fase 0, la evidencia es documental: constitución, spec, Documento Rector, roadmap, CONTRIBUTING, Decision Log y matriz de trazabilidad. Las conclusiones futuras siguen requiriendo evidencia positiva, evidencia negativa o limitación explícita.
- **Symptom handling**: PASS. Fase 0 no procesa síntomas. El plan preserva que el síntoma futuro es pista, no verdad causal.
- **Causal roles**: PASS. Fase 0 no emite diagnósticos. El plan preserva la separación entre causa principal, factor contribuyente, hallazgo relacionado, hallazgo incidental, hipótesis descartada, revisión no evaluada y desconocido.
- **Visible OK reviews**: PASS. Fase 0 no ejecuta revisiones técnicas. El plan conserva la obligación futura de mostrar OK relevantes cuando descarten hipótesis.
- **Causal domains**: PASS. Fase 0 no clasifica incidentes. El plan conserva los dominios aprobados y la frontera del dominio Datos.
- **No business tables**: PASS. El plan confirma que ninguna fase futura puede consultar tablas de negocio, datos funcionales ni inferir significado funcional de datos de aplicación.
- **Failures and timeouts**: PASS. Fase 0 no ejecuta conectores. El plan conserva que errores, timeouts y permisos insuficientes futuros se tratan como evidencia, limitación o no evaluado.
- **Security**: PASS. Fase 0 no gestiona secretos ni accesos. El plan mantiene mínimos privilegios y protección de secretos como obligación futura.
- **Recommendations**: PASS. Fase 0 no emite recomendaciones operativas sobre Oracle. Las recomendaciones futuras deben declarar alcance, riesgo, prerequisitos y validación humana.
- **Evidence contract**: PASS. Fase 0 no crea Evidence Payload. El plan preserva que el modelo gobierna fixtures y Evidence Payload, que JSON es el contrato formal futuro y que YAML queda limitado a escenarios humanos de laboratorio.
- **Tests**: PASS. La validación de Fase 0 es documental. Las pruebas automatizadas aplican a funcionalidades futuras según constitución.
- **Language**: PASS. El plan y artefactos están en español.
- **Deviations**: PASS. Cualquier cambio fuera de constitución, spec activa, plan aprobado o roadmap debe tratarse como `propuesta de desviación` con autorización humana explícita.

## Project Structure

### Documentation (this feature)

```text
specs/000-gobierno-y-constitucion/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
No source code changes for Fase 0.
```

**Structure Decision**: La feature es exclusivamente documental. No se crean `src/`, `tests/`, contratos ejecutables ni componentes de runtime.

## Phase 0: Research

La investigación se limita a decisiones documentales necesarias para cerrar Fase 0:

- Confirmar fuente normativa principal.
- Confirmar fuentes complementarias y su rol.
- Confirmar agrupación oficial de specs.
- Confirmar control de desviaciones.
- Confirmar ausencia de implementación funcional en Fase 0.

**Output**: [research.md](./research.md)

## Phase 1: Design & Contracts

### Data Model

El modelo es documental, no un modelo de runtime. Registra entidades de gobierno SDD como Constitución, Spec, Plan, Tareas, PR, Roadmap, Backlog, Decision Log, Matriz de Trazabilidad y Propuesta de Desviación.

**Output**: [data-model.md](./data-model.md)

### Contracts

No se generan contratos en `contracts/`. Fase 0 no expone API, CLI, formato ejecutable, Evidence Payload ni interfaz externa. Crear contratos aquí adelantaría fases futuras.

### Quickstart

La guía de validación describe pasos manuales para verificar que los documentos de gobierno están alineados y que no se introdujo funcionalidad.

**Output**: [quickstart.md](./quickstart.md)

## Post-Design Constitution Check

- **RCA scope**: PASS. Los artefactos generados son de gobierno documental y no convierten OraDiag en health check.
- **Roadmap phase**: PASS. Todos los artefactos pertenecen a `000-gobierno-y-constitucion`; no se adelantó Spec 001.
- **Evidence**: PASS. `research.md` documenta evidencia documental y decisiones; no declara conclusiones técnicas de diagnóstico.
- **Symptom handling**: PASS. No se procesa síntoma ni se define lógica diagnóstica.
- **Causal roles**: PASS. `data-model.md` documenta obligaciones futuras, no roles emitidos por runtime.
- **Visible OK reviews**: PASS. Se conserva como regla futura, sin implementar reportes.
- **No business tables**: PASS. No hay acceso, modelo ni contrato de datos de negocio.
- **Failures and timeouts**: PASS. Se conserva como regla futura, sin crear conectores.
- **Security**: PASS. No hay secretos ni credenciales; se conserva la regla de mínimos privilegios.
- **Evidence contract**: PASS. No se crea Evidence Payload; se mantiene JSON/YAML como restricción futura.
- **Tests**: PASS. `quickstart.md` define validación documental mínima.
- **Language**: PASS. Artefactos en español.
- **Deviations**: PASS. No hay desviaciones aceptadas; las contradicciones se reportan como aclaraciones requeridas.

## Complexity Tracking

No hay violaciones constitucionales ni complejidad a justificar.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Aclaraciones Requeridas

- La constitución aún conserva en su Sync Impact Report un TODO histórico sobre alinear `docs/ROADMAP.md`. El roadmap ya fue alineado en el documento actual; no se modifica la constitución en este plan porque el alcance pedido es generar el plan de la spec activa.
