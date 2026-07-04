# Feature Specification: Acceso por capas y Discovery Oracle

**Feature Branch**: `002-acceso-por-capas-y-discovery-oracle`

**Created**: 2026-07-04

**Status**: Draft

**Input**: User description: "Crear la especificación SDD `002-acceso-por-capas-y-discovery-oracle` para OraDiag/OraRCA. Fases 2 y 3: conectividad por capas y Discovery Oracle inicial, tolerante a fallas, gobernado por evidencia y sin convertir OraDiag en health check ni collector amplio."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Acceso por capas tolerante a fallas (Priority: P1)

Como operador técnico, quiero que OraDiag evalúe las capas técnicas disponibles y reporte claramente las capas inaccesibles para obtener un diagnóstico parcial útil durante incidentes reales.

**Why this priority**: Es el primer paso para salir del laboratorio sin perder las garantías de Spec 001. Si una capa falla y tumba toda la ejecución, OraDiag no puede operar en incidentes reales donde el acceso parcial es normal.

**Independent Test**: Puede probarse con dobles o fakes de capas donde una capa responde, otra falla por timeout y otra queda inaccesible; el resultado debe conservar la evidencia disponible y registrar limitaciones para lo no evaluado sin abortar toda la ejecución.

**Acceptance Scenarios**:

1. **Given** un target con acceso disponible a una capa técnica y falla controlada en otra, **When** OraDiag ejecuta un perfil que incluye ambas capas, **Then** conserva la evidencia o contexto de la capa accesible y registra la falla de la capa inaccesible como limitación trazable.
2. **Given** una capa que excede su tiempo máximo configurado, **When** se ejecuta el diagnóstico, **Then** esa capa termina con estado de timeout, impacto diagnóstico explícito y la ejecución continúa con capas independientes.
3. **Given** una capa que devuelve permisos insuficientes, **When** OraDiag intenta evaluarla, **Then** el resultado reporta permiso insuficiente como limitación y no solicita ni simula escalamiento automático de privilegios.

---

### User Story 2 - Discovery Oracle técnico inicial (Priority: P1)

Como DBA, quiero que OraDiag descubra contexto Oracle básico disponible para que el RCA futuro entienda topología y alcance sin asumir información no comprobada.

**Why this priority**: El discovery técnico aporta contexto esencial para interpretar evidencia posterior, pero debe permanecer separado de las conclusiones RCA. Sin esta separación, el contexto podría confundirse con causalidad.

**Independent Test**: Puede probarse con dobles de discovery que devuelvan subconjuntos de contexto Oracle, como versión, nombre de base, instancia, DBID, CDB/PDB o servicios visibles; el resultado debe preservar solo lo comprobado y marcar lo no visible como desconocido, no como falla causal.

**Acceptance Scenarios**:

1. **Given** una capa de acceso técnico que permite ver versión, nombre de base e instancia, **When** se ejecuta discovery inicial, **Then** OraDiag registra ese contexto como información técnica observable sin convertirlo en causa probable.
2. **Given** un entorno donde CDB/PDB, RAC, ASM, standby o listener no son visibles por permisos o disponibilidad, **When** se ejecuta discovery, **Then** OraDiag conserva el contexto sí visible y registra limitaciones o estado no evaluado para lo no visible.
3. **Given** una señal técnica de standby visible y consistente con el alcance evaluado, **When** se construye el contexto Oracle, **Then** standby queda registrado como contexto técnico; si no es visible o no corresponde, no se infiere.

---

### User Story 3 - Conversión de errores en limitaciones (Priority: P1)

Como revisor del diagnóstico, quiero que timeouts, permisos insuficientes y errores de conexión aparezcan como limitaciones trazables, no como crashes ni como causas inventadas.

**Why this priority**: La constitución exige fallas controladas y diagnóstico parcial. Esta historia protege la confianza del reporte: lo que no pudo evaluarse debe ser visible y no debe contaminar causalidad.

**Independent Test**: Puede probarse inyectando resultados de error, timeout, permiso insuficiente y capa no disponible desde dobles de acceso; cada caso debe producir limitaciones o revisiones no evaluadas con motivo, alcance e impacto.

**Acceptance Scenarios**:

1. **Given** una capa de acceso que falla por error controlado, **When** OraDiag consolida el resultado, **Then** el error aparece como limitación con alcance, mensaje e impacto diagnóstico.
2. **Given** varias capas con estados mixtos de OK, timeout y no disponible, **When** se genera el resultado, **Then** el reporte diferencia evidencia positiva, evidencia negativa, limitaciones y revisiones no evaluadas.
3. **Given** que toda la conectividad disponible falla, **When** se ejecuta el diagnóstico, **Then** OraDiag devuelve un resultado parcial o indeterminado con limitaciones explícitas, no una causa probable fabricada.

---

### User Story 4 - Validación con dobles antes de conectividad real productiva (Priority: P2)

Como mantenedor, quiero validar conectividad por capas y discovery con dobles, fakes o mocks antes de depender de Oracle real o infraestructura real.

**Why this priority**: La spec debe permitir construir confianza contractual antes de introducir dependencias externas. Los dobles preservan pruebas determinísticas y evitan que el avance dependa de entornos reales.

**Independent Test**: Puede probarse ejecutando escenarios de acceso y discovery completamente simulados, sin Oracle real, SSH real, listener real ni archivos SQL, y verificando que los contratos de evidencia, contexto y limitaciones se cumplen.

**Acceptance Scenarios**:

1. **Given** dobles de capas que simulan disponibilidad, timeout, error y permisos insuficientes, **When** se ejecutan pruebas automatizadas, **Then** cada estado queda representado de forma estable y verificable.
2. **Given** dobles de discovery que devuelven contexto parcial, **When** se consolida el resultado, **Then** OraDiag conserva los campos descubiertos y no inventa los ausentes.
3. **Given** una prueba automatizada de Spec 002, **When** se ejecuta en un entorno sin Oracle real ni infraestructura real, **Then** debe poder validar el comportamiento de la spec sin conectividad productiva.

---

### User Story 5 - Integración con EvidencePayload (Priority: P2)

Como mantenedor, quiero que el discovery produzca evidencia o contexto compatible con el contrato formal existente, sin acoplar el RCAEngine a conectores concretos.

**Why this priority**: Spec 001 estableció que el Evidence Payload gobierna el intercambio formal. Spec 002 debe extender la entrada de evidencia sin romper la independencia del motor RCA ni introducir SQL crudo en la capa causal.

**Independent Test**: Puede probarse verificando que resultados de capas y discovery se transforman en evidencia, contexto técnico, limitaciones o revisiones no evaluadas compatibles con el contrato formal antes de llegar al motor RCA.

**Acceptance Scenarios**:

1. **Given** una capa que produce contexto Oracle observable, **When** el resultado se integra al flujo diagnóstico, **Then** queda representado como contexto técnico o evidencia estructurada validada, no como formato crudo de backend.
2. **Given** una falla de capa, **When** se transforma el resultado, **Then** se registra como limitación diagnóstica trazable en el contrato formal.
3. **Given** el RCAEngine existente, **When** recibe evidencia de Spec 002, **Then** no depende de conectores concretos, detalles de backend ni texto SQL crudo para evaluar causalidad.

### Edge Cases

- Si una capa accesible produce contexto y otra capa crítica falla, OraDiag debe reportar ambas cosas: contexto disponible y limitación por la capa fallida.
- Si un timeout ocurre en una capa, debe terminar en tiempo finito, registrar el timeout y permitir que capas independientes continúen.
- Si faltan permisos mínimos para una fuente técnica, la salida debe explicar el alcance no evaluado sin sugerir escalamiento automático.
- Si el discovery obtiene solo versión o nombre de base, ese contexto parcial debe conservarse sin inferir topología no observada.
- Si CDB/PDB, RAC, ASM, standby, listener o servicios no son visibles, deben quedar como desconocidos, no como ausentes ni como causa.
- Si una capa devuelve datos inconsistentes o incompletos, OraDiag debe registrar limitación, contradicción o baja confianza de contexto según aplique.
- Si el síntoma apunta a conectividad pero solo existe contexto técnico sin evidencia causal, OraDiag no debe convertir el síntoma ni el contexto en causa probable.
- Si todas las capas fallan, OraDiag debe producir resultado indeterminado o parcial con limitaciones y sin causa principal.
- Si un perfil incluye capas futuras fuera de Spec 002, OraDiag debe rechazarlas, omitirlas de forma controlada o marcarlas como no soportadas según el contrato vigente.
- Si una fuente técnica expone identificadores sensibles innecesarios, deben omitirse o redactarse conforme a seguridad y mínimo privilegio.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: OraDiag MUST definir acceso por capas como capacidad diagnóstica controlada, no como health check general ni framework de homologación.
- **FR-002**: OraDiag MUST representar capas evaluables de acceso/discovery, incluyendo database/sql_access, listener/network, os/ssh, storage_context y authentication/access o equivalentes de alcance técnico.
- **FR-003**: Las capas MUST tratarse como fuentes de acceso o discovery, no como checks amplios de salud ni como validaciones de performance.
- **FR-004**: Cada capa MUST tener resultado independiente para permitir diagnóstico parcial cuando otras capas fallen.
- **FR-005**: Ninguna capa, conector, backend o discovery MAY tumbar toda la ejecución por timeout, error, permiso insuficiente o inaccesibilidad si existen capas independientes evaluables.
- **FR-006**: Todo timeout, error, permiso insuficiente, capa inaccesible o dato incompleto MUST convertirse en limitación diagnóstica o revisión no evaluada.
- **FR-007**: Las limitaciones de capa MUST incluir alcance, motivo, impacto diagnóstico y trazabilidad hacia la capa o discovery afectado.
- **FR-008**: OraDiag MUST soportar timeouts configurables para capas y operaciones de discovery dentro del alcance de Spec 002.
- **FR-009**: Los errores de acceso y discovery MUST reportarse de forma controlada, legible y sin traceback como comportamiento normal de uso.
- **FR-010**: Los permisos insuficientes MUST reportarse como limitación y MUST NOT provocar escalamiento automático de privilegios.
- **FR-011**: Los perfiles MAY agrupar capas o discovery inicial, pero MUST NOT alterar reglas de causalidad, scoring ni confianza por sí mismos.
- **FR-012**: La separación entre contrato, provider/discovery y backend real o fake MUST quedar explícita para impedir acoplar RCA a implementaciones concretas.
- **FR-013**: Spec 002 MUST poder validarse con dobles, fakes o mocks antes de requerir Oracle real, SSH real o listener real.
- **FR-014**: Las pruebas de Spec 002 MUST NOT requerir conectividad productiva real ni credenciales reales.
- **FR-015**: El discovery Oracle inicial MUST registrar contexto técnico observable cuando esté disponible, incluyendo versión de base de datos, nombre de base, instancia, host visible técnicamente y DBID si está disponible.
- **FR-016**: El discovery Oracle inicial MUST registrar CDB/PDB, RAC, ASM, standby, servicios o listener solo cuando sean visibles técnicamente y correspondan al alcance evaluado.
- **FR-017**: El discovery MUST permitir resultados parciales y conservar lo descubierto aunque otras consultas o capas fallen.
- **FR-018**: El discovery MUST NOT inferir topología, rol, disponibilidad o causa cuando la información no sea visible o no esté soportada por evidencia.
- **FR-019**: El discovery MUST producir contexto técnico, evidencia estructurada, limitaciones o revisiones no evaluadas; MUST NOT producir conclusiones RCA por sí mismo.
- **FR-020**: El contexto técnico descubierto MUST ser compatible con el Evidence Payload o con modelos formales gobernados por el contrato existente.
- **FR-021**: El RCAEngine MUST permanecer independiente de conectores concretos, backends reales/fake, SQL crudo, SSH, listener o detalles de discovery.
- **FR-022**: El síntoma MAY orientar qué capas o discovery se priorizan, pero MUST NOT fabricar causalidad ni convertir información incompleta en causa probable.
- **FR-023**: Una capa accesible MAY producir evidencia positiva, evidencia negativa, contexto técnico o ausencia informativa, según lo observado.
- **FR-024**: Una capa inaccesible MUST NOT contarse como evidencia positiva de causa; solo puede aportar limitación o no evaluado.
- **FR-025**: La salida futura derivada de Spec 002 MUST mostrar contexto descubierto, capas no evaluadas, limitaciones y evidencia disponible sin recalcular causalidad en reporters.
- **FR-026**: OraDiag MUST NOT consultar tablas de negocio, datos funcionales ni significado de aplicación durante acceso por capas o discovery.
- **FR-027**: Spec 002 MUST NOT introducir checks de performance, waits, sesiones, bloqueos, alert log, storage/FRA/redo, AWR/ASH, histórico, SQLite, dashboards, endpoints web ni reportes markdown/html.
- **FR-028**: Spec 002 MUST NOT crear archivos `.sql` ni requerir SQL real en el paso de especificación.
- **FR-029**: Las recomendaciones derivadas de limitaciones MUST ser prudentes, no destructivas y orientadas a obtener evidencia adicional o validar permisos mínimos con intervención humana.
- **FR-030**: Cualquier idea fuera de Fases 2 y 3, constitución, roadmap o spec activa MUST declararse como `propuesta de desviación` y no incorporarse sin autorización humana.
- **FR-031**: La documentación y mensajes humanos asociados a esta spec MUST estar en español; identificadores técnicos estables MAY permanecer en inglés cuando formen parte del contrato.
- **FR-032**: La spec MUST preservar compatibilidad conceptual con Spec 001 y MUST NOT modificarla salvo hallazgo documental crítico reportado explícitamente.

### Key Entities

- **Capa de acceso/discovery**: Fuente técnica evaluable de forma independiente, como database/sql_access, listener/network, os/ssh, storage_context o authentication/access; representa capacidad de observación, no salud general.
- **Resultado de capa**: Estado consolidado de una capa, con disponibilidad, resultado observado, limitaciones, tiempo máximo aplicado e impacto diagnóstico.
- **Backend de capa**: Implementación reemplazable real o fake que intenta obtener información técnica; no define causalidad.
- **Provider o discovery**: Componente que coordina una o varias capas para producir contexto técnico, evidencia estructurada o limitaciones.
- **Contexto Oracle descubierto**: Datos técnicos observables como versión, nombre de base, instancia, host visible, DBID, CDB/PDB, RAC, ASM, standby, servicios o listener cuando sean visibles.
- **Limitación diagnóstica**: Registro trazable de timeout, error, permiso insuficiente, capa inaccesible, dato incompleto o no aplicabilidad.
- **Evidencia estructurada**: Información técnica validada y compatible con el contrato formal existente, apta para alimentar el RCA sin exponer detalles crudos de backend.
- **Perfil de ejecución**: Agrupación declarativa que selecciona capas o discovery inicial sin cambiar causalidad.
- **Evidence Payload**: Contrato formal, versionado y serializable que integra evidencia, contexto, revisiones y limitaciones antes de cualquier evaluación RCA.

### Expected Automated Tests

- Pruebas de capa accesible que produce contexto o evidencia estructurada.
- Pruebas de capa inaccesible que produce limitación.
- Pruebas de timeout configurable que no cuelga la ejecución.
- Pruebas de permisos insuficientes reportados como limitación.
- Pruebas de error controlado sin traceback ni aborto total.
- Pruebas de discovery parcial que conserva lo descubierto.
- Pruebas de discovery que no infiere CDB/PDB, RAC, ASM, standby, servicios o listener no visibles.
- Pruebas de integración con Evidence Payload o modelos formales existentes.
- Pruebas que demuestren que el RCAEngine no depende de conectores concretos ni SQL crudo.
- Pruebas con dobles/fakes/mocks sin Oracle real, SSH real, listener real ni credenciales reales.
- Pruebas de guardrail que impidan tablas de negocio, datos funcionales y funcionalidades de fases posteriores.

## Constitutional Alignment *(mandatory)*

### Roadmap and Scope

- **Roadmap grouping**: `002-acceso-por-capas-y-discovery-oracle`, Fases 2 y 3: conectividad por capas y Discovery Oracle.
- **Rector docs used**: `.specify/memory/constitution.md`, `docs/DOCUMENTO_RECTOR.md`, `docs/ARCHITECTURE.md`, `docs/RCA_MODEL.md`, `docs/EVIDENCE_MODEL.md`, `docs/SYMPTOM_HANDLING.md`, `docs/ERROR_HANDLING_AND_TIMEOUTS.md`, `docs/SECURITY_AND_ACCESS.md`, `docs/EXECUTION_PROFILES.md`, `docs/ROADMAP.md`, `docs/BACKLOG.md`, `docs/DECISION_LOG.md`, `docs/TRACEABILITY_MATRIX.md`, `docs/CONTRIBUTING.md` y Spec 001 como contrato funcional existente.
- **Out of scope**: Implementación de código, plan técnico, tasks, conectividad Oracle real productiva, SSH real productivo, listener real productivo, archivos `.sql`, checks de performance, waits, sesiones, bloqueos, alert log, diagnóstico funcional de usuario, storage/FRA/redo, reportes markdown/html, histórico, SQLite, AWR/ASH, dashboards, endpoints/API web, IA, tablas de negocio y datos funcionales.
- **Layer boundary clarifications**: `authentication/access` en Spec 002 representa únicamente la capacidad técnica de intentar acceso o reportar una limitación de acceso. No incluye diagnóstico de cuentas bloqueadas, passwords expirados, auditoría de intentos fallidos ni clasificación causal de problemas de usuario, que pertenecen a specs posteriores. `storage_context` representa únicamente visibilidad técnica o disponibilidad de una capa relacionada con contexto de almacenamiento. No incluye análisis de capacidad, FRA, TEMP, UNDO, redo, archive, ASM capacity ni presión de espacio. `listener/network` representa accesibilidad o contexto técnico observable. No incluye troubleshooting profundo de red/listener ni diagnóstico avanzado de servicios.
- **Deviation status**: Ninguna desviación incorporada. No se detecta `propuesta de desviación` necesaria para cubrir Fases 2 y 3 dentro del roadmap.

### RCA and Evidence Rules

- **Incident/RCA focus**: Esta spec habilita observación técnica controlada para incidentes Oracle; no define health checks generales, homologación, capacity planning ni inventario amplio.
- **Evidence required**: Todo contexto, limitación o conclusión futura debe estar soportado por evidencia positiva, evidencia negativa o limitación explícita. Discovery por sí solo no concluye causalidad.
- **Symptom handling**: El síntoma puede orientar prioridad de capas o presentación, pero no convierte contexto parcial, timeout o capa inaccesible en causa probable.
- **Causal roles**: Spec 002 no redefine roles causales. Cualquier uso futuro de `primary_cause`, `contributing_factor`, `related_finding`, `incidental_finding`, `ruled_out`, `not_evaluated` o `unknown` debe provenir del RCA con evidencia validada.
- **Visible OK reviews**: Resultados OK o accesos exitosos deben conservarse cuando sirvan como evidencia negativa, contexto o descarte de hipótesis; no deben ocultarse solo por no ser problema.
- **Causal domains**: Los dominios aprobados se mantienen. Discovery puede aportar contexto para Base de datos, Infraestructura, Sistema Operativo, Almacenamiento, Usuario o Indeterminado, pero Datos sigue siendo frontera y no autoriza datos funcionales.

### Safety, Data and Error Boundaries

- **No business data**: Spec 002 prohíbe consultar, modelar o inferir tablas de negocio, datos funcionales y significado de aplicación.
- **Failures/timeouts**: Errores, timeouts, permisos insuficientes, capas no disponibles y datos incompletos deben convertirse en limitaciones o revisiones no evaluadas con alcance e impacto.
- **Security/minimum privileges**: La falta de permisos se reporta como limitación. La spec no autoriza credenciales reales en repositorio, exposición de secretos ni escalamiento automático.
- **Recommendations**: Las recomendaciones deben ser seguras, no destructivas, explícitas sobre prerequisitos y sujetas a validación humana cuando impliquen acciones operativas.
- **Evidence Payload/format**: JSON/modelos internos siguen siendo el contrato formal. YAML puede seguir siendo configuración humana o laboratorio; no gobierna el RCA ni sustituye el contrato.
- **Language**: La documentación, reportes humanos y mensajes principales deben estar en español. Identificadores técnicos estables pueden mantenerse en inglés.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de escenarios de acceso por capas definidos para Spec 002 pueden validarse con dobles/fakes/mocks sin Oracle real, SSH real, listener real ni credenciales reales.
- **SC-002**: El 100% de timeouts, errores, permisos insuficientes y capas inaccesibles probados se convierten en limitaciones o revisiones no evaluadas, no en crashes.
- **SC-003**: El 100% de ejecuciones con al menos una capa accesible y otra fallida conservan la evidencia o contexto disponible y reportan la falla de forma trazable.
- **SC-004**: El 100% de resultados de discovery parcial conservan los campos observados y no infieren campos no visibles.
- **SC-005**: El 100% de resultados de discovery inicial se clasifican como contexto técnico, evidencia estructurada, limitación o no evaluado; ninguno emite conclusión RCA por sí mismo.
- **SC-006**: El 100% de pruebas de guardrail confirman que no se consultan tablas de negocio ni datos funcionales.
- **SC-007**: El 100% de pruebas de integración contractual demuestran que el RCAEngine no depende de conectores concretos, SQL crudo, SSH, listener ni backend real/fake.
- **SC-008**: El 100% de mensajes humanos relevantes para fallas de capa y discovery son legibles en español y no exponen secretos.
- **SC-009**: La revisión documental de Spec 002 no encuentra adelantos de Fases 4 a 14 ni cambios no autorizados a Spec 001.
- **SC-010**: Cualquier idea fuera de alcance detectada queda documentada como `propuesta de desviación` y no se incorpora a requisitos funcionales sin autorización humana.

## Assumptions

- Spec 001 ya provee CLI, configuración, perfiles, FixtureEvidenceProvider, EvidencePayload, RCAEngine mínimo y salidas console/json como base contractual.
- Spec 002 define comportamiento y contratos esperados; no implementa código, plan técnico, tasks ni conectividad real en este paso.
- Los nombres de capas son categorías de alcance diagnóstico y pueden mapearse más adelante a implementaciones reales o dobles sin cambiar reglas RCA.
- Discovery Oracle inicial se limita a contexto técnico observable y no incluye checks de performance, waits, sesiones, bloqueos, alert log, storage/FRA/redo ni AWR/ASH.
- La validación inicial debe poder hacerse completamente con dobles/fakes/mocks.
- Los perfiles existentes o futuros solo seleccionan grupos de capas o discovery; no modifican causalidad.
- El contexto Oracle ausente por falta de visibilidad se considera desconocido o no evaluado, no evidencia de ausencia.
- La seguridad por mínimo privilegio y la redacción de secretos gobiernan cualquier acceso futuro.
