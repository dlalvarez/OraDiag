# Implementation Plan: Acceso por capas y Discovery Oracle

**Branch**: `002-acceso-por-capas-y-discovery-oracle` | **Date**: 2026-07-04 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-acceso-por-capas-y-discovery-oracle/spec.md`

## Summary

Spec 002 diseña la incorporación incremental de acceso por capas y Discovery Oracle inicial para OraDiag/OraRCA. La implementación futura debe introducir modelos intermedios de capas/discovery, backends fake/double para pruebas, mapeo validado hacia `EvidencePayload` y una ruta CLI/config/perfiles compatible con Spec 001.

El diseño mantiene al `RCAEngine` aislado: el motor seguirá recibiendo únicamente `EvidencePayload` o modelos internos validados, nunca conectores concretos, SQL crudo, SSH, listener ni detalles de backend. Discovery produce contexto técnico, evidencia estructurada, limitaciones o revisiones no evaluadas; no produce causalidad por sí mismo.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: Typer para CLI, PyYAML para configuración humana, Pydantic para modelos/validación, pytest para pruebas.

**Storage**: N/A. Spec 002 no introduce SQLite, histórico, caché persistente ni store local.

**Testing**: pytest con unit, integration y contract tests.

**Target Platform**: CLI local de OraDiag ejecutada con `uv run`, sin dependencia de Oracle real para pruebas de Spec 002.

**Project Type**: Python package + CLI.

**Performance Goals**: Cada capa y operación de discovery debe terminar en tiempo finito mediante timeout configurable; el diagnóstico parcial debe continuar cuando capas independientes fallen.

**Constraints**: Sin Oracle real productivo, SSH real productivo, listener real productivo, archivos `.sql`, SQL crudo en RCA, tablas de negocio, datos funcionales, IA, AWR/ASH, alert log, sesiones/bloqueos/waits, storage/FRA/redo, endpoints web, dashboards, histórico ni reportes markdown/html.

**Scale/Scope**: Fases 2 y 3 únicamente: interfaces/modelos de acceso por capas, backends fake/double, Discovery Oracle inicial y transformación hacia EvidencePayload.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **RCA scope**: PASS. El diseño soporta incidentes Oracle con contexto técnico observable; no define health check general, homologación, capacity planning, auditoría funcional ni inventario amplio.
- **Roadmap phase**: PASS. Corresponde a `002-acceso-por-capas-y-discovery-oracle`, Fases 2 y 3. No implementa fases 4 a 14.
- **Evidence**: PASS. Toda salida de capa/discovery se transforma en evidencia estructurada, evidencia negativa, contexto neutral, limitación o revisión no evaluada antes de llegar al RCA.
- **Symptom handling**: PASS. El síntoma puede priorizar selección/presentación de capas, pero no cambia causalidad ni convierte contexto incompleto en causa.
- **Causal roles**: PASS. Spec 002 no redefine roles. `primary_cause`, `contributing_factor`, `related_finding`, `incidental_finding`, `ruled_out`, `not_evaluated` y `unknown` siguen siendo responsabilidad del RCA sobre evidencia validada.
- **Visible OK reviews**: PASS. Capas exitosas y descubrimientos OK deben conservarse cuando sirvan como evidencia negativa, contexto o descarte de hipótesis.
- **Causal domains**: PASS. Se mantienen Sistema Operativo, Infraestructura, Almacenamiento, Base de datos, Aplicación, Usuario, Datos e Indeterminado. Datos sigue siendo frontera, no permiso para inspeccionar negocio.
- **No business tables**: PASS. No se consultan, modelan ni infieren tablas de negocio, datos funcionales ni significado de aplicación.
- **Failures and timeouts**: PASS. Timeouts, errores, permisos insuficientes, capa no disponible y datos incompletos se convierten en `Limitation`, `ReviewResult` no evaluado o `AccessLayer` no disponible.
- **Security**: PASS. Configuración declarativa sin secretos; cualquier credencial futura debe ser referencia segura, no valor literal en repo, logs o reportes.
- **Recommendations**: PASS. Spec 002 no agrega acciones destructivas. Recomendaciones derivadas de limitaciones se orientan a obtener evidencia o validar permisos mínimos con intervención humana.
- **Evidence contract**: PASS. `EvidencePayload` permanece JSON-serializable, versionado y validado. YAML queda como configuración humana/laboratorio.
- **Tests**: PASS. El plan exige pruebas de fakes/doubles, limitaciones, discovery parcial, no negocio, no SQL crudo en RCA, aislamiento del RCAEngine y compatibilidad con Spec 001.
- **Language**: PASS. Documentación y mensajes humanos deben estar en español; identificadores técnicos estables pueden mantenerse en inglés.
- **Deviations**: PASS. No se incorpora ninguna `propuesta de desviación`; cualquier ampliación fuera de Fases 2 y 3 debe declararse y aprobarse antes.
- **No OraHealth/OraParity by analogy**: PASS. El diseño se basa en la constitución, roadmap, Spec 001 y Spec 002, no en analogías automáticas con otros proyectos.

## Project Structure

### Documentation (this feature)

```text
specs/002-acceso-por-capas-y-discovery-oracle/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── evidence-integration.md
│   ├── layer-access.md
│   └── oracle-discovery.md
└── checklists/
    └── requirements.md
```

`tasks.md` se generará únicamente con `speckit-tasks`; no forma parte de este paso.

### Source Code (repository root)

```text
src/oradiag/
├── cli/                 # Mantener oradiag run/version; integrar selección futura sin romper Spec 001
├── config/              # Extender perfiles/timeouts declarativos sin secretos ni comandos
├── discovery/           # Nuevo espacio futuro para Discovery Oracle inicial
├── layers/              # Nuevo espacio futuro para contratos/backends de capa
├── models/              # Extender modelos Pydantic intermedios y mapeo EvidencePayload
├── providers/           # Agregar provider compuesto/fake que produzca EvidencePayload
├── rca/                 # Sin dependencia de capas, discovery, SQL, SSH o listener
└── reports/             # Serializar DiagnosticResult sin recalcular causalidad

tests/
├── contract/            # Contratos de layer access, discovery e integración EvidencePayload
├── integration/         # CLI/config/perfiles con fakes sin infraestructura real
└── unit/                # Modelos, mapeos, fakes, timeouts y guardrails
```

**Structure Decision**: Se mantiene un único paquete Python. Se agregan espacios conceptuales `layers` y `discovery` para separar acceso/discovery de providers, RCA y reportes. El motor RCA y reporters no reciben dependencias nuevas.

## Design Overview

### Acceso por capas

La implementación futura debe representar cada capa como definición declarativa y ejecutar solicitudes mediante backend reemplazable. Las capas iniciales bajo Spec 002 son:

- `database/sql_access`: capacidad técnica de acceso SQL o limitación, sin SQL crudo en RCA.
- `listener/network`: accesibilidad o contexto técnico observable, sin troubleshooting profundo de red/listener ni diagnóstico avanzado de servicios.
- `os/ssh`: capacidad técnica de acceso OS o limitación, sin SSH real productivo requerido para pruebas.
- `storage_context`: visibilidad técnica/disponibilidad de capa, sin análisis de capacidad, FRA, TEMP, UNDO, redo, archive, ASM capacity ni presión de espacio.
- `authentication/access`: intento técnico de acceso o limitación, sin cuentas bloqueadas, passwords expirados, auditoría de intentos fallidos ni clasificación causal de usuario.

### Discovery Oracle inicial

Discovery debe producir contexto técnico observable y parcial:

- versión de base de datos;
- nombre de base;
- instancia;
- host visible técnicamente;
- DBID si está disponible;
- CDB/PDB cuando sea visible;
- RAC cuando sea visible;
- ASM cuando sea visible;
- standby solo si es visible y corresponde al alcance evaluado;
- servicios o listener solo como contexto observable.

Campos no visibles deben quedar `unknown`, `not_evaluated`, omitidos con limitación explícita o representados como fuente no disponible. No se infiere topología.

### Integración con EvidencePayload

Los resultados intermedios se transforman antes de entrar al RCA:

- `LayerExecutionResult` exitoso -> `AccessLayer(status=OK|INFO, available=True)` y opcional `ReviewResult`.
- Capa fallida -> `AccessLayer(available=False, status=ERROR|TIMEOUT|SKIPPED)` con `Limitation`.
- Discovery visible -> `Observation(polarity=neutral, severity=info, structured_data={...})` o `ReviewResult(status=OK|INFO)`.
- Discovery no visible por error/timeout/permisos -> `ReviewResult(status=TIMEOUT|ERROR|SKIPPED)` con `Limitation`.
- Contexto que descarta hipótesis técnica -> `ReviewResult(status=OK, ok_relevance=...)` cuando aplique.

El `RCAEngine` no recibe `LayerBackend`, `LayerExecutionRequest`, handles de conexión, SQL, comandos OS ni datos crudos de listener.

### CLI, configuración y perfiles

Spec 001 conserva `oradiag run --fixture`. Spec 002 debe añadir una ruta compatible para ejecutar providers fake/double o integrar discovery simulado sin eliminar fixtures existentes. La configuración humana puede extender perfiles con capas y timeouts declarativos, pero no puede contener SQL, comandos OS ni secretos.

Los perfiles seleccionan grupos de capas/discovery; no alteran scoring, causalidad ni confianza. Perfiles de fases futuras pueden existir como nombres declarativos solo si no activan comportamiento fuera de Spec 002.

## Phase 0 Research Output

Ver [research.md](./research.md).

## Phase 1 Design Output

- [data-model.md](./data-model.md)
- [contracts/layer-access.md](./contracts/layer-access.md)
- [contracts/oracle-discovery.md](./contracts/oracle-discovery.md)
- [contracts/evidence-integration.md](./contracts/evidence-integration.md)
- [quickstart.md](./quickstart.md)

## Post-Design Constitution Check

- **RCA vs health check**: PASS. Contratos limitan capas a acceso/discovery y prohíben checks amplios.
- **Evidencia y síntoma**: PASS. Discovery se mapea a contexto/evidencia/limitaciones; síntoma no fabrica causalidad.
- **Separación causal**: PASS. No se modifica RCAEngine ni roles causales.
- **OK visibles**: PASS. El mapeo conserva OK relevantes como `ReviewResult`.
- **Datos y seguridad**: PASS. No tablas de negocio, no datos funcionales, no secretos, no escalamiento automático.
- **Fallas controladas**: PASS. Timeouts, errores, permisos y no disponible tienen rutas de limitación.
- **Trazabilidad y roadmap**: PASS. Artefactos cubren solo Fases 2 y 3; no hay desviaciones.

## Complexity Tracking

No hay violaciones constitucionales que justificar.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
