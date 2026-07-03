# Quickstart: Validación documental de Fase 0

Esta guía valida la spec `000-gobierno-y-constitucion` sin ejecutar código ni crear funcionalidad de diagnóstico.

## Prerrequisitos

- Existe `.specify/memory/constitution.md`.
- Existe `specs/000-gobierno-y-constitucion/spec.md`.
- Existe `specs/000-gobierno-y-constitucion/plan.md`.
- Existen los documentos rectores mínimos: `docs/DOCUMENTO_RECTOR.md`, `docs/ROADMAP.md`, `docs/CONTRIBUTING.md`, `docs/DECISION_LOG.md` y `docs/TRACEABILITY_MATRIX.md`.

## Validación 1: Fuente normativa

1. Revisar `.specify/memory/constitution.md`.
2. Confirmar que gobierna specs, planes, tareas, implementaciones y PRs.
3. Revisar `docs/CONTRIBUTING.md`.
4. Confirmar que declara la constitución como fuente normativa principal y `docs/DOCUMENTO_RECTOR.md` como fuente complementaria.

**Resultado esperado**: La jerarquía documental queda clara y no hay otra fuente declarada como superior a la constitución.

## Validación 2: Roadmap agrupado por specs

1. Revisar `docs/ROADMAP.md`.
2. Confirmar que existe la agrupación oficial `000` a `008`.
3. Confirmar que `000-gobierno-y-constitucion` corresponde a Fase 0.
4. Confirmar que Fase 0 declara fuera de alcance la lógica funcional.

**Resultado esperado**: El roadmap permite ubicar esta spec sin agregar fases ni adelantar fases futuras.

## Validación 3: Spec de gobierno

1. Revisar `specs/000-gobierno-y-constitucion/spec.md`.
2. Confirmar que referencia todas las fuentes rectoras obligatorias.
3. Confirmar que define reglas mínimas para futuras specs, planes, tareas y PRs.
4. Confirmar que incluye control explícito de `propuesta de desviación`.
5. Confirmar que declara que Fase 0 no implementa funcionalidad de diagnóstico.

**Resultado esperado**: La spec cumple sus criterios de aceptación documentales.

## Validación 4: Constitution Check del plan

1. Revisar `specs/000-gobierno-y-constitucion/plan.md`.
2. Confirmar que el Constitution Check marca PASS para RCA vs health check, evidencia, síntoma, causalidad, OK visibles, tablas de negocio, errores/timeouts, seguridad, modelo/Evidence Payload, JSON/YAML, desviaciones y ausencia de funcionalidad diagnóstica en Fase 0.
3. Confirmar que el Post-Design Constitution Check también queda en PASS.

**Resultado esperado**: El plan no introduce violaciones constitucionales.

## Validación 5: Sin implementación

1. Confirmar que esta feature solo agrega artefactos documentales bajo `specs/000-gobierno-y-constitucion/`.
2. Confirmar que no se crearon CLI, modelos Python, Evidence Payload, fixtures, motor RCA, reportes, conectividad Oracle, SSH, listener ni collectors.
3. Confirmar que no se ejecutaron tareas ni implementación.

**Resultado esperado**: Fase 0 permanece documental y no adelanta Spec 001.

## Validación 6: Aclaraciones requeridas

1. Revisar la sección de aclaraciones en `plan.md` y `research.md`.
2. Confirmar que las tensiones documentales se reportan sin inventar alcance nuevo.

**Resultado esperado**: Cualquier pendiente queda declarado y no resuelto por cambios fuera de alcance.
