# Revisión de la spec 001 (noviembre 2026)

**Estado**: Histórica. Superseded por `003-modelo-de-evidencia-y-motor-causal`.
**Revisada contra**: constitución v2.0.0.

Se revisaron `spec.md`, `plan.md`, `data-model.md`, `research.md`,
`quickstart.md`, `tasks.md` y `contracts/`. Este documento registra qué se
conserva como insumo para la spec 003 y qué se descarta, con el motivo. Los
archivos originales se conservan sin cambios, salvo un aviso al inicio de `spec.md`.

## Veredicto

La disciplina de contrato es buena y se conserva casi completa: Evidence
Payload como único camino al motor, fixtures que no definen el modelo, salida
JSON estable, OK como evidencia negativa y errores como limitaciones. El
defecto de fondo está en el motor: FR-027 prohibía expresamente la correlación
y la spec no definía ventana del incidente, reglas causales ni cadenas de
evidencia. La implementación resultante eligió la causa sumando pesos por
severidad y estado contra un umbral, lo que contradice el principio XV.

## Se conserva para la spec 003

| Origen | Contenido | Ajuste en 003 |
|---|---|---|
| US1, US4, US5 | Diagnóstico desde CLI con fixture, configuración YAML y salidas console/JSON | Se agrega ventana del incidente (`--since/--until` o "en curso") |
| US2, FR-009 a FR-018 | Evidence Payload versionado como único contrato; YAML solo humano; expectativas de prueba nunca llegan al motor | Payload v2 con marcas de tiempo por observación y origen (`sql`, `licensed`, `platform`, `lab`) |
| FR-021 a FR-026 | Causa solo con evidencia suficiente; indeterminado explícito; OK como evidencia negativa; síntoma como pista | Sin cambios |
| FR-030 | Campos mínimos de salida | Se agrega la cadena de evidencia y el motivo de la confianza |
| Casos límite | Síntoma ausente o contradictorio; todo en error; hallazgo crítico incidental; secretos en configuración | Se agrega: hallazgo crítico fuera de la ventana |
| Pruebas esperadas | CLI, configuración, modelos, fixture -> payload, prohibición de YAML en el motor, roles causales, OK, limitaciones, JSON estable | Se agregan guardrails XII-XIV y escenarios de correlación |
| `data-model.md` | Entidades `DiagnosticScenario`, `TargetContext`, `ObservedSubject`, `Observation`, `Limitation`, `ReviewResult`, `DiagnosticFinding`, `CausalAssessment`, `Recommendation` | Punto de partida del data model v2; `AccessLayer` se elimina y se agregan ventana, hipótesis y cadena de evidencia |
| `contracts/diagnostic-result.md` | Semántica de `assessment`, listas vacías antes que campos omitidos, IDs estables | Base del contrato de salida v2 |

## Se descarta

| Origen | Contenido | Motivo |
|---|---|---|
| FR-019, FR-027 | Motor "mínimo simulado" sin correlación | Contradice XV; el motor debe correlacionar desde el inicio |
| FR-034 | Prohibición de cualquier conexión real en la fase | La 003 sigue sin conexión, pero la restricción ya no es de fase: la conexión llega en la 004 |
| `access_layers` en el payload | Capas de acceso estilo SSH/listener/storage | Reemplazado por origen de la evidencia y adaptadores (XII) |
| Dominios en inglés `undetermined` | Valor de enum | Se revisa la nomenclatura de enums en el data model de 003 |
| Referencias a OraParity y fases 2-14 | Gobierno v1 | Gobierno v2 |
| Código en `src/` y `tests/` | Implementación previa | No se reutiliza (ADR-0009) |
