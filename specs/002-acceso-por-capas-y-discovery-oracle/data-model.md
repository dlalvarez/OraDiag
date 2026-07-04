# Data Model: Acceso por capas y Discovery Oracle

## Overview

Spec 002 introduce modelos conceptuales intermedios para acceso por capas y Discovery Oracle. Estos modelos no sustituyen `EvidencePayload`: lo alimentan mediante una transformación validada.

Regla central: ningún backend, handle de conexión, SQL crudo, comando SSH o detalle de listener llega al `RCAEngine`.

## Entity: AccessLayerDefinition

Representa una capa técnica que puede evaluarse de forma independiente.

### Fields

- `id`: identificador estable, por ejemplo `database/sql_access`.
- `name`: nombre humano en español.
- `description`: propósito de acceso/discovery.
- `domain_hint`: dominio causal candidato solo como contexto, no causalidad.
- `default_timeout_seconds`: timeout por defecto.
- `enabled_by_profiles`: perfiles que pueden seleccionarla.
- `scope_boundary`: texto obligatorio para capas con riesgo de adelantar fases.

### Validation Rules

- `id` debe ser declarativo y no contener SQL, comandos OS, hosts ni secretos.
- `default_timeout_seconds` debe ser positivo.
- `scope_boundary` es obligatorio para `authentication/access`, `storage_context` y `listener/network`.

## Entity: LayerExecutionRequest

Solicitud de ejecución de una capa para un target/perfil.

### Fields

- `request_id`: identificador de ejecución.
- `target_id`: target configurado.
- `profile`: perfil seleccionado.
- `symptom`: síntoma efectivo o `unspecified`.
- `layer_id`: referencia a `AccessLayerDefinition`.
- `timeout_seconds`: timeout efectivo.
- `metadata`: datos no sensibles necesarios para fake/double o backend futuro.

### Validation Rules

- No puede contener passwords, tokens, connection strings ni comandos.
- `timeout_seconds` debe venir de configuración validada o default de capa.
- El síntoma no puede alterar reglas de causalidad.

## Entity: LayerBackend

Contrato conceptual para un backend reemplazable.

### Responsibilities

- Recibir `LayerExecutionRequest`.
- Devolver `LayerExecutionResult`.
- Respetar timeout.
- No lanzar errores no controlados hacia la orquestación.

### Backend Types

- `fake`: determinístico para pruebas.
- `double`: configurable para simular estados.
- `real_future`: reservado para conectividad real futura, fuera de implementación productiva inicial.

## Entity: LayerExecutionResult

Resultado normalizado de una capa.

### Fields

- `result_id`: identificador trazable.
- `layer_id`: capa evaluada.
- `status`: `OK`, `INFO`, `WARNING`, `TIMEOUT`, `ERROR`, `SKIPPED` o `UNKNOWN`.
- `available`: booleano de disponibilidad técnica.
- `message`: explicación humana.
- `observed_context`: datos técnicos observables, sin secretos.
- `limitations`: lista de `LayerLimitation`.
- `elapsed_ms`: duración observada.
- `source`: backend o discovery que produjo el resultado.

### State Rules

- `TIMEOUT`, `ERROR` y `SKIPPED` requieren al menos una limitación.
- `available=false` requiere limitación.
- `UNKNOWN` solo se usa cuando no puede determinarse responsablemente el estado.
- `OK` puede generar evidencia negativa o contexto visible, no causa directa.

## Entity: LayerLimitation

Limitación específica de capa.

### Fields

- `id`: identificador estable.
- `type`: `timeout`, `error`, `insufficient_permissions`, `layer_unavailable`, `not_applicable`, `incomplete_data` o `skipped`.
- `scope`: capa, operación o discovery afectado.
- `message`: descripción en español.
- `impact`: impacto diagnóstico.
- `recoverability`: `retry_possible`, `needs_permissions`, `not_applicable` o `unknown`.

### Mapping

`LayerLimitation` se transforma a `Limitation` existente antes de entrar al RCA.

## Entity: OracleDiscoveryContext

Contexto Oracle técnico observable.

### Fields

- `database_version`: campo visible o unknown.
- `database_name`: campo visible o unknown.
- `instance_name`: campo visible o unknown.
- `host_name`: campo visible técnicamente o unknown.
- `dbid`: campo visible o unknown.
- `cdb`: visible/unknown.
- `pdbs`: lista visible o unknown/not_evaluated.
- `rac`: visible/unknown.
- `asm`: visible/unknown.
- `standby`: visible solo si corresponde; unknown si no se puede comprobar.
- `services`: servicios visibles o unknown/not_evaluated.
- `listener`: contexto listener visible o unknown/not_evaluated.
- `sources`: lista de `DiscoverySource`.
- `limitations`: limitaciones de discovery.

### Validation Rules

- Campo no visible no se infiere.
- Standby no se usa como DR genérico ni Data Guard avanzado.
- ASM visible no habilita análisis de capacidad.
- Servicios/listener visibles no habilitan troubleshooting avanzado.

## Entity: OracleDiscoveryField

Representa un campo de discovery con trazabilidad.

### Fields

- `name`: nombre del campo.
- `value`: valor serializable y no sensible, si está visible.
- `visibility`: `visible`, `unknown`, `not_evaluated` o `not_applicable`.
- `source_id`: fuente que lo observó.
- `limitation_id`: limitación asociada si aplica.

### Validation Rules

- `value` solo se permite cuando `visibility=visible`.
- `unknown` y `not_evaluated` no deben serializar valores inventados.

## Entity: DiscoverySource

Fuente técnica usada por discovery.

### Fields

- `id`: identificador de fuente.
- `layer_id`: capa que habilitó la fuente.
- `source_type`: `fake`, `sql_access`, `listener_context`, `os_context` o equivalente futuro.
- `status`: estado normalizado.
- `limitations`: limitaciones de la fuente.

### Validation Rules

- `source_type` no puede implicar tablas de negocio ni datos funcionales.
- Fuentes reales futuras deben ocultar detalles de conexión y SQL crudo.

## Entity: EvidenceIntegrationRecord

Registro de transformación hacia EvidencePayload.

### Fields

- `source_result_id`: resultado de capa o discovery de origen.
- `target_model`: `AccessLayer`, `ReviewResult`, `Observation` o `Limitation`.
- `target_id`: identificador del modelo generado.
- `polarity`: `neutral`, `negative` o `positive` cuando aplique.
- `notes`: explicación de mapeo.

### Validation Rules

- Discovery contextual usa `polarity=neutral` por defecto.
- Una capa inaccesible no puede mapearse a evidencia positiva.
- SQL crudo, comandos OS y secretos no pueden aparecer en `notes` ni `structured_data`.

## Entity: ProfileLayerSelection

Selección declarativa de capas/discovery desde perfil.

### Fields

- `profile_name`: nombre del perfil.
- `layers`: lista de capas permitidas.
- `discovery_groups`: grupos de discovery inicial.
- `timeouts`: overrides declarativos por capa.
- `disabled_layers`: capas omitidas de forma controlada.

### Validation Rules

- No puede contener reglas de causalidad, scoring ni confianza.
- No puede contener SQL, comandos OS, hosts sensibles ni secretos.
- Perfiles de fases futuras no activan comportamiento fuera de Spec 002.

## Transformation To EvidencePayload

| Source | EvidencePayload target | Rule |
|--------|------------------------|------|
| `LayerExecutionResult(status=OK, available=true)` | `AccessLayer` + optional `ReviewResult` | Contexto disponible o evidencia negativa si descarta una hipótesis técnica. |
| `LayerExecutionResult(status=TIMEOUT)` | `AccessLayer` + `ReviewResult` + `Limitation` | No evaluado por timeout; ejecución continúa. |
| `LayerExecutionResult(status=ERROR)` | `AccessLayer` + `ReviewResult` + `Limitation` | Error controlado; no causa principal por sí mismo. |
| `insufficient_permissions` | `Limitation` | No solicita escalamiento automático. |
| `OracleDiscoveryField(visible)` | `Observation` or `ReviewResult` | Contexto técnico neutral salvo evidencia negativa explícita. |
| `OracleDiscoveryField(unknown/not_evaluated)` | `Limitation` or omitted with source status | No inferir valor. |

## Compatibility With Spec 001

- `EvidencePayload.schema_version` permanece `1.0` salvo decisión futura explícita.
- Fixtures existentes siguen válidos.
- `FixtureEvidenceProvider` no cambia de responsabilidad.
- `RCAEngine.evaluate()` sigue aceptando solo `EvidencePayload`.
- Reporters siguen derivando salida desde `DiagnosticResult`.
