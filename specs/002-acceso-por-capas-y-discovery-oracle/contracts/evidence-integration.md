# Contract: Evidence Integration

## Purpose

Define cómo resultados de acceso por capas y Discovery Oracle se convierten en `EvidencePayload` o modelos compatibles antes de cualquier evaluación RCA.

## Inbound Sources

Fuentes aceptadas:

- `LayerExecutionResult`
- `OracleDiscoveryContext`
- `OracleDiscoveryField`
- `LayerLimitation`
- `DiscoverySource`

Fuentes no aceptadas por el RCA:

- backends;
- handles de conexión;
- SQL crudo;
- comandos SSH/OS;
- salida cruda de listener;
- credenciales o secretos.

## Mapping Targets

Modelos existentes de Spec 001:

- `AccessLayer`
- `ReviewResult`
- `Observation`
- `Limitation`
- `EvidencePayload`

## Mapping Rules

### AccessLayer

Crear o actualizar `AccessLayer` por cada capa evaluada:

- `name`: layer id normalizado.
- `available`: `true` si la capa es accesible; `false` si no.
- `status`: estado normalizado.
- `limitations`: limitaciones de capa.

`available=false` siempre requiere al menos una limitación.

### ReviewResult

Crear `ReviewResult` para ejecución de capa/discovery cuando el resultado debe ser visible:

- `OK` o `INFO`: contexto visible o evidencia negativa.
- `TIMEOUT`, `ERROR`, `SKIPPED`: no evaluado con limitación obligatoria.
- `UNKNOWN`: solo cuando el estado no pueda determinarse responsablemente.

### Observation

Crear `Observation` para contexto técnico descubierto cuando sea útil para trazabilidad:

- `polarity=neutral` por defecto.
- `severity=info` por defecto para contexto.
- `candidate_domain` puede indicar dominio técnico, pero no causalidad.
- `structured_data` solo contiene datos técnicos no sensibles.

Una observación de discovery no puede ser `positive` salvo que una spec futura defina evidencia causal explícita.

### Limitation

Crear `Limitation` para:

- timeout;
- error controlado;
- permisos insuficientes;
- capa no disponible;
- no aplicable;
- datos incompletos;
- skipped controlado.

Toda limitación debe incluir alcance, mensaje e impacto.

## RCA Isolation

`RCAEngine.evaluate()` debe recibir únicamente `EvidencePayload`.

Prohibido pasar al RCA:

- `LayerBackend`;
- `LayerExecutionRequest`;
- `LayerExecutionResult` sin transformar;
- `OracleDiscoveryContext` sin integrar;
- SQL;
- SSH;
- listener;
- credenciales;
- objetos de conexión.

## Reporter Rule

Reporters console/json solo serializan `DiagnosticResult`. No recalculan causalidad ni reinterpretan discovery.

## Compatibility Rules

- Fixtures existentes de Spec 001 siguen válidos.
- `FixtureEvidenceProvider` sigue transformando YAML humano a `EvidencePayload`.
- La nueva integración puede coexistir como provider compuesto/fake futuro.
- No se requiere cambiar `schema_version` en Spec 002 salvo decisión explícita posterior.

## Guardrails

- No tablas de negocio.
- No datos funcionales.
- No IA.
- No AWR/ASH.
- No alert log.
- No sesiones, bloqueos ni waits.
- No storage/FRA/redo.
- No reportes markdown/html.
- No histórico.
- No endpoints web.
