# Research: Gobierno y Constitución SDD

## Decision: La constitución es la fuente normativa principal

**Rationale**: `.specify/memory/constitution.md` gobierna specs, planes, tareas, implementaciones y pull requests. `docs/CONTRIBUTING.md` también la reconoce como fuente normativa principal.

**Alternatives considered**:
- Usar solo `docs/DOCUMENTO_RECTOR.md`: rechazado porque la constitución ratificada establece reglas SDD, versionado, desviaciones y checks de planificación.
- Usar documentos por igual sin jerarquía: rechazado porque dificultaría resolver tensiones documentales.

## Decision: El Documento Rector es fuente complementaria

**Rationale**: `docs/DOCUMENTO_RECTOR.md` define propósito, alcance, fuera de alcance y principios no negociables de OraDiag. Complementa la constitución sin reemplazarla.

**Alternatives considered**:
- Duplicar el Documento Rector dentro de la spec: rechazado para evitar divergencia documental.
- Ignorarlo por existir constitución: rechazado porque sigue siendo fuente rectora del dominio OraDiag.

## Decision: El roadmap agrupado por specs gobierna la secuencia de trabajo

**Rationale**: `docs/ROADMAP.md` contiene la agrupación oficial de specs `000` a `008` y conserva Fase 0 como gobierno documental. Esto permite validar que futuras specs no adelanten fases.

**Alternatives considered**:
- Crear una agrupación nueva: rechazado porque agregaría alcance no autorizado.
- Usar fases sin specs: rechazado porque la constitución exige trazabilidad por spec y fase.

## Decision: Fase 0 no implementa funcionalidad

**Rationale**: La spec y el roadmap definen Fase 0 como gobierno documental. Implementar CLI, modelos, Evidence Payload, fixtures, RCA engine, reportes o conectividad adelantaría Spec 001 o fases posteriores.

**Alternatives considered**:
- Crear validadores automáticos ahora: rechazado porque sería funcionalidad futura y no parte de Fase 0.
- Crear contratos de Evidence Payload ahora: rechazado porque adelanta el alcance de Spec 001.

## Decision: Las validaciones de cierre son documentales

**Rationale**: El cierre de Fase 0 se verifica revisando consistencia entre constitución, spec, roadmap, CONTRIBUTING, Decision Log y matriz de trazabilidad. No hay runtime que ejecutar.

**Alternatives considered**:
- Exigir pruebas automatizadas en Fase 0: rechazado porque no hay código ni comportamiento ejecutable.
- Omitir validación: rechazado porque la constitución exige trazabilidad y control de desviaciones.

## Decision: No se generan contratos externos

**Rationale**: Fase 0 no expone API, CLI, JSON de evidencia ni interfaz de integración. Generar contratos sería diseño de fases futuras.

**Alternatives considered**:
- Crear un contrato de PR o spec: rechazado porque las reglas ya están en la constitución, spec y plan; un contrato formal podría confundirse con interfaz ejecutable.

## Aclaraciones requeridas

- La constitución conserva un TODO histórico en su Sync Impact Report sobre alinear `docs/ROADMAP.md`. El roadmap actual ya contiene la agrupación oficial y Fase 1 alineada, pero este plan no modifica la constitución por estar fuera del alcance solicitado.
