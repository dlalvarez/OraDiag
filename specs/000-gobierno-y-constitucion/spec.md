# Spec 000: Gobierno y constitución

**Estado**: Aprobada (v2, 2026-11-21) | **Versión anterior**: v1, 2026-07-03

**Constitución**: v2.0.0

## Propósito

Fijar cómo se gobierna OraDiag: qué documentos mandan, en qué orden, y qué
debe contener cada artefacto SDD (spec, plan, tareas y PR) para que la
implementación con Claude Code sea trazable y no salga del alcance. Esta spec
no produce código.

## Cambios frente a la v1

La v1 (generada en julio de 2026) documentaba el gobierno de la constitución
1.0.0 en siete artefactos (spec, plan, research, data-model, quickstart, tasks
y checklist), la mayoría dedicados a verificar la existencia de otros
documentos. La v2:

- Se alinea con la constitución 2.0.0 (principios XII a XV, RDS como plataforma
  inicial, specs 001 y 002 históricas, agrupación 003-012).
- Concentra el gobierno en esta spec y en `plan.md`; las reglas operativas
  viven en la constitución, `CLAUDE.md`, `docs/CONTRIBUTING.md` y las plantillas
  de Spec Kit, que son las que se usan en el día a día.
- Retira `research.md`, `data-model.md`, `quickstart.md`, `tasks.md` y el
  checklist de la v1, que verificaban documentos sin aportar reglas nuevas.
  Quedan en el historial de Git.

## Jerarquía documental

1. `.specify/memory/constitution.md`: fuente normativa principal.
2. Spec activa en `specs/NNN-*/`.
3. `CLAUDE.md`: guía operativa para la implementación con Claude Code.
4. `docs/`: documentación rectora complementaria. Si contradice la
   constitución, prevalece la constitución y el documento se corrige.

## Requisitos para artefactos SDD

- **GOV-001 Spec**: declara agrupación del roadmap, fuentes rectoras, alcance y
  fuera de alcance, vistas Oracle con su grant normal y su equivalente en RDS,
  clasificación de licenciamiento de cada fuente, criterios de evidencia,
  manejo de errores y timeouts, riesgos de seguridad, pruebas esperadas y
  trazabilidad. Lo garantiza `.specify/templates/spec-template.md`.
- **GOV-002 Plan**: incluye un Constitution Check verificable de los
  principios I a XV, antes del diseño y después de él. Lo garantiza
  `.specify/templates/plan-template.md`.
- **GOV-003 Tareas**: pequeñas, verificables, con ruta de archivo, sin
  adelantar specs futuras, e incluyen pruebas, trazabilidad y actualización
  documental cuando aplique. Lo garantiza `.specify/templates/tasks-template.md`.
- **GOV-004 PR**: declara spec y tareas cubiertas, cumplimiento constitucional,
  pruebas ejecutadas, documentación actualizada y desviaciones aceptadas. Lo
  garantiza `.github/pull_request_template.md`.
- **GOV-005 Desviaciones**: todo cambio fuera de la constitución, spec activa,
  plan aprobado o roadmap se marca como `propuesta de desviación` y no se
  implementa sin autorización humana explícita.
- **GOV-006 Flujo**: la planeación completa de una spec se aprueba antes de su
  implementación; Claude Code implementa el `tasks.md` aprobado; si una tarea
  revela que la spec es incorrecta, se detiene y se ajusta la spec.
- **GOV-007 Ramas**: `develop-claude` integra; una rama por spec
  (`spec/NNN-nombre`); `main` solo recibe versiones estables.
- **GOV-008 Idioma**: artefactos SDD, documentación, reportes y mensajes en
  español; identificadores técnicos pueden ir en inglés.

## Casos límite

- Propuesta que no corresponde a ninguna spec del roadmap: `propuesta de
  desviación`.
- Spec que consulte tablas de negocio, use fuentes licenciadas sin protección,
  ejecute algo distinto de `SELECT` o acople el núcleo a un proveedor: se
  rechaza por contradicción constitucional.
- Decisión copiada de OraHealth por analogía: se corrige o se declara como
  desviación.
- Tensión entre un documento de `docs/` y una spec: se registra como aclaración
  requerida y se resuelve antes de implementar.

## Criterios de aceptación

- La constitución, el roadmap y `docs/` no se contradicen entre sí.
- Las plantillas de Spec Kit exigen GOV-001 a GOV-003.
- La plantilla de PR exige GOV-004.
- Spec Kit está configurado para Claude Code.
- No quedan referencias vigentes a la agrupación `000-008` de la v1 ni a
  conectividad por SSH como requisito del núcleo.
