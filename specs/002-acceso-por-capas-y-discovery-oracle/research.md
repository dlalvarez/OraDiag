# Research: Acceso por capas y Discovery Oracle

## Decision: Contratos y fakes antes de conectividad real

**Decision**: Spec 002 debe implementar primero contratos, modelos intermedios y backends fake/double determinísticos. Los backends reales quedan preparados por interfaz, pero no son requisito para validar la spec.

**Rationale**: La constitución exige pruebas automatizadas, fallas controladas y mínimo privilegio. Fakes permiten probar timeouts, errores, permisos insuficientes y discovery parcial sin Oracle real, SSH real, listener real, secretos ni conectividad productiva.

**Alternatives considered**:

- Implementar conexión Oracle real primero: rechazado porque introduce infraestructura, credenciales y errores externos antes de fijar contrato.
- Seguir usando solo fixtures YAML: rechazado porque no modela capa/backend/timeout como responsabilidades separadas.

## Decision: Discovery no produce causa RCA

**Decision**: Discovery Oracle inicial produce contexto técnico observable, evidencia neutral, revisiones OK, limitaciones o no evaluado. No emite `primary_cause` ni cambia scoring.

**Rationale**: Versión, instancia, DBID, CDB/PDB, RAC, ASM, standby o listener son contexto de alcance. Por sí solos no prueban causalidad. La causalidad sigue en el RCA sobre `EvidencePayload` validado.

**Alternatives considered**:

- Crear hallazgos RCA desde discovery: rechazado porque confunde contexto con causa.
- Ocultar discovery del EvidencePayload: rechazado porque el RCA futuro necesita trazabilidad de contexto y limitaciones.

## Decision: Modelos intermedios compatibles con EvidencePayload

**Decision**: Diseñar `LayerExecutionResult`, `OracleDiscoveryContext` y `EvidenceIntegrationRecord` como modelos intermedios, y mapearlos hacia `AccessLayer`, `ReviewResult`, `Observation` y `Limitation`.

**Rationale**: Spec 001 ya define `EvidencePayload` como contrato formal del RCA. Modelos intermedios evitan acoplar backends a RCA y permiten evolucionar discovery sin romper fixtures existentes.

**Alternatives considered**:

- Extender directamente `EvidencePayload` con campos específicos de Oracle: rechazado para evitar acoplamiento temprano y cambios de contrato innecesarios.
- Pasar resultados de backend directamente al RCAEngine: rechazado por violar aislamiento del motor.

## Decision: Reutilizar estados y tipos existentes

**Decision**: Reutilizar `ReviewStatus` para estados de capa (`OK`, `INFO`, `WARNING`, `TIMEOUT`, `ERROR`, `SKIPPED`, `UNKNOWN`) y `LimitationType` para timeout, error, permisos insuficientes, capa no disponible, no aplicable e incompleto.

**Rationale**: Mantiene consistencia con Spec 001, reduce nuevos enums y permite que reporters/RCA ya entiendan limitaciones y no evaluados.

**Alternatives considered**:

- Crear un enum de estados de capa separado: rechazado salvo que tareas futuras encuentren una necesidad real; duplicaría semántica existente.
- Representar permisos insuficientes como `ERROR` sin tipo específico: rechazado porque perdería trazabilidad operativa.

## Decision: No crear archivos `.sql`

**Decision**: Spec 002 no crea `.sql`. Cualquier consulta futura debe quedar encapsulada en backends y documentada como intención técnica, nunca como archivo SQL ni texto crudo que llegue al RCA.

**Rationale**: El alcance del plan es diseño y validación con fakes. Además, la constitución prohíbe adelantar conectividad real y exige que el RCA no consuma SQL crudo.

**Alternatives considered**:

- Documentar consultas SQL iniciales en archivos: rechazado por adelantar implementación y aumentar riesgo de alcance.
- Incluir SQL en fixtures: rechazado porque los fixtures no gobiernan el contrato formal.

## Decision: Fronteras explícitas de capas con nombres sensibles

**Decision**: `authentication/access`, `storage_context` y `listener/network` se mantienen como capacidades de acceso/discovery, no como diagnósticos de specs posteriores.

**Rationale**: Sus nombres se solapan con fases futuras. La frontera explícita evita implementar diagnósticos de usuario, almacenamiento, listener/red profundo o servicios avanzados antes de tiempo.

**Alternatives considered**:

- Eliminar esas capas de Spec 002: rechazado porque el acceso parcial necesita representarlas como disponibilidad/limitación técnica.
- Implementarlas como checks completos: rechazado por violar roadmap.

## Decision: Síntoma solo prioriza, no decide

**Decision**: El síntoma puede orientar orden o selección de capas en perfiles, pero no cambia mapeo causal ni convierte capa inaccesible/contexto parcial en evidencia positiva.

**Rationale**: Evita sesgo de anclaje. El síntoma es pista, no verdad.

**Alternatives considered**:

- Crear reglas de causalidad por síntoma en discovery: rechazado porque adelanta correlación y viola Spec 002.

## Decision: CLI compatible con Spec 001

**Decision**: Mantener `oradiag run --fixture` y diseñar la ruta Spec 002 como extensión compatible mediante provider fake/double o configuración declarativa futura, sin remover opciones existentes.

**Rationale**: Spec 001 está cerrada y validada. La compatibilidad permite que pruebas y fixtures existentes sigan pasando.

**Alternatives considered**:

- Reemplazar fixture por conectividad por defecto: rechazado porque rompería contrato existente y exigiría infraestructura real.

## Decision: Sin desviaciones

**Decision**: No se requiere `propuesta de desviación`.

**Rationale**: Todo el diseño queda dentro de Fases 2 y 3 y respeta constitución, roadmap y Spec 002.

**Alternatives considered**:

- Incluir conectividad real productiva o diagnósticos de fases futuras: rechazado por fuera de alcance.
