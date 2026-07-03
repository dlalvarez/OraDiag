# Feature Specification: Core RCA sin conectividad real

**Feature Branch**: `001-core-rca-sin-conectividad-real`

**Created**: 2026-07-03

**Status**: Draft

**Input**: User description: "Crear la especificación SDD `001-core-rca-sin-conectividad-real` para OraDiag/OraRCA. Fase 1: CLI, configuración, perfiles, modelos base, Evidence Payload, fixtures de laboratorio y RCA engine mínimo simulado, sin conectividad real."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Diagnóstico simulado ejecutable desde CLI (Priority: P1)

Como operador técnico de OraDiag, quiero ejecutar un diagnóstico simulado contra un escenario de laboratorio para validar el flujo mínimo de entrada, perfil, síntoma, evidencia, RCA y salida sin conectarme a Oracle ni a infraestructura real.

**Why this priority**: Es el primer valor funcional verificable de OraDiag. Sin un flujo CLI mínimo, no se puede validar el contrato de evidencia, el motor RCA mínimo ni las salidas esperadas de Fase 1.

**Independent Test**: Puede probarse ejecutando `oradiag run` con un target de ejemplo, un perfil declarativo, un síntoma, un fixture de laboratorio y salida console o json; el resultado debe contener diagnóstico, evidencia, limitaciones y recomendaciones sin usar conectividad real.

**Acceptance Scenarios**:

1. **Given** una configuración YAML válida con targets de ejemplo sin credenciales reales y un fixture de laboratorio con evidencia de sesiones bloqueadas y waits compatibles con bloqueo, **When** se ejecuta `oradiag run` con síntoma de lentitud, perfil amplio y salida JSON, **Then** el diagnóstico clasifica como causa probable principal un problema de bloqueo o contención en el dominio Base de datos, con confianza adecuada, evidencia concreta, hallazgos relacionados si existen y revisiones OK relevantes.
2. **Given** un fixture donde la conexión o acceso falla por usuario bloqueado o contraseña expirada simulada, **When** se ejecuta `oradiag run`, **Then** el diagnóstico clasifica el dominio Usuario como causa probable principal o hallazgo relacionado según la evidencia disponible, e incluye limitaciones de capas no evaluadas cuando aplique.
3. **Given** un fixture con timeouts, errores o permisos insuficientes que impiden reunir evidencia suficiente, **When** se ejecuta el diagnóstico, **Then** OraDiag devuelve estado indeterminado o equivalente, confianza baja, limitaciones explícitas y no emite causa probable principal.

---

### User Story 2 - Contrato formal de evidencia validado (Priority: P1)

Como mantenedor de OraDiag, quiero que toda evidencia que llegue al motor RCA use un Evidence Payload formal, versionado, serializable a JSON y validado por modelos internos para que los providers futuros puedan reemplazar fixtures sin cambiar las reglas RCA.

**Why this priority**: El principio rector de Fase 1 es que el modelo formal manda. Si el motor depende de YAML o del formato humano de fixtures, el core queda acoplado a laboratorio y no puede evolucionar hacia collectors reales.

**Independent Test**: Puede probarse cargando un fixture YAML de laboratorio mediante un provider de fixtures y verificando que el motor RCA recibe únicamente Evidence Payload o modelos internos validados, nunca YAML crudo.

**Acceptance Scenarios**:

1. **Given** un fixture YAML con observaciones técnicas simuladas y, opcionalmente, una sección de expected output para pruebas, **When** el provider de fixtures lo carga, **Then** transforma solo la evidencia del escenario a Evidence Payload/modelos internos y no entrega conclusiones esperadas al motor RCA.
2. **Given** un Evidence Payload serializado a JSON con `schema_version`, contexto de target, observaciones, revisiones OK y limitaciones, **When** se valida contra modelos internos, **Then** se acepta si cumple el contrato y se rechaza con error controlado si viola campos obligatorios o estados permitidos.
3. **Given** una prueba automatizada que intenta pasar YAML directamente al motor RCA, **When** se ejecuta, **Then** debe fallar o demostrar que esa ruta no existe.

---

### User Story 3 - RCA mínimo determinístico y prudente (Priority: P2)

Como revisor técnico, quiero que el motor RCA mínimo clasifique causa principal, hallazgos relacionados, incidentales, contribuyentes, descartados, no evaluados y desconocidos con reglas determinísticas y explicables para evitar conclusiones inventadas o sesgadas por el síntoma.

**Why this priority**: La utilidad de OraDiag depende de separar causalidad de anomalías. Fase 1 debe validar esa disciplina aunque el análisis sea mínimo y simulado.

**Independent Test**: Puede probarse con escenarios de laboratorio controlados que cubran causa principal, evidencia insuficiente, hallazgo incidental severo, revisiones OK y frontera Aplicación/Datos.

**Acceptance Scenarios**:

1. **Given** un fixture donde existe un hallazgo severo pero no correlacionado con el síntoma ni la evidencia principal, **When** se ejecuta el diagnóstico, **Then** ese hallazgo se clasifica como incidental o relacionado, pero no como causa principal solo por severidad.
2. **Given** un fixture con revisiones OK de almacenamiento, listener o espacio simulado que ayudan a descartar hipótesis, **When** se genera la salida, **Then** esas revisiones aparecen como OK relevantes o evidencia negativa.
3. **Given** un fixture donde las revisiones técnicas simuladas están OK y no hay evidencia técnica causal, **When** el síntoma apunta a problema funcional o de aplicación, **Then** OraDiag emite una conclusión prudente hacia Aplicación o Datos como frontera, sin consultar ni modelar tablas de negocio.

---

### User Story 4 - Configuración y perfiles declarativos de laboratorio (Priority: P2)

Como mantenedor, quiero cargar configuración humana en YAML con targets de ejemplo y perfiles declarativos para validar la ergonomía operativa inicial sin introducir secretos, collectors reales ni cambios de causalidad por perfil.

**Why this priority**: La CLI necesita entradas consistentes para ejecutar escenarios de laboratorio, y los perfiles deben existir desde el diseño inicial sin alterar las reglas RCA.

**Independent Test**: Puede probarse cargando configuraciones válidas e inválidas, seleccionando un target de ejemplo y un perfil inicial como `diag_all`, y confirmando que los errores se reportan de forma controlada.

**Acceptance Scenarios**:

1. **Given** una configuración YAML válida con targets de ejemplo sin credenciales reales y perfiles declarativos, **When** se ejecuta un diagnóstico simulado, **Then** OraDiag selecciona target y perfil sin intentar conectividad real.
2. **Given** una configuración YAML inválida, incompleta o con perfil inexistente, **When** se invoca la CLI, **Then** OraDiag devuelve un error controlado, legible en español, y no ejecuta el motor RCA.
3. **Given** dos perfiles que seleccionan revisiones distintas sobre la misma evidencia simulada, **When** se ejecutan diagnósticos comparables, **Then** el perfil puede agrupar o filtrar revisiones, pero no altera las reglas de causalidad ni fabrica certeza.

---

### User Story 5 - Salidas console y JSON verificables (Priority: P3)

Como consumidor humano o automatizado de OraDiag, quiero una salida console legible en español y una salida JSON estable para pruebas para poder revisar diagnósticos iniciales y automatizar validaciones de contrato.

**Why this priority**: Las salidas cierran el flujo funcional de Fase 1 y permiten convertir escenarios de laboratorio en pruebas repetibles.

**Independent Test**: Puede probarse ejecutando los escenarios mínimos con `output=console` y `output=json`; la salida JSON debe ser estable y la salida console debe incluir los elementos RCA esenciales en español.

**Acceptance Scenarios**:

1. **Given** un diagnóstico con causa probable principal, **When** se solicita salida JSON, **Then** el resultado incluye causa probable, dominio causal, confianza, evidencias usadas, hallazgos relacionados, hallazgos incidentales, revisiones OK relevantes, limitaciones y recomendaciones iniciales.
2. **Given** un diagnóstico con evidencia insuficiente, **When** se solicita salida console, **Then** el reporte advierte claramente que no hay evidencia suficiente, muestra limitaciones y evita presentar una causa probable como certeza.
3. **Given** cualquier escenario aceptado de Fase 1, **When** se ejecutan pruebas automatizadas sobre la salida JSON, **Then** los campos esperados permanecen estables para snapshots o comparaciones estructuradas.

### Edge Cases

- Si el síntoma no se proporciona, OraDiag debe usar `unspecified` o equivalente y no fabricar causalidad.
- Si el síntoma contradice la evidencia simulada, OraDiag debe reportar la contradicción o reducir confianza, no forzar el síntoma como causa.
- Si toda la evidencia disponible está en estado `TIMEOUT`, `ERROR`, permisos insuficientes, capa no disponible o `SKIPPED`, el resultado debe ser indeterminado y con limitaciones explícitas.
- Si un fixture incluye conclusiones esperadas para pruebas, esas conclusiones no deben llegar al motor RCA.
- Si un hallazgo tiene severidad crítica pero no explica el incidente, debe clasificarse como incidental, relacionado o contribuyente según evidencia, nunca como causa principal por severidad aislada.
- Si una revisión OK descarta una hipótesis importante, debe conservarse en la salida aunque no sea un problema.
- Si la configuración contiene credenciales reales o secretos literales, la ejecución debe rechazarlas o tratarlas como error de configuración según la política de seguridad de Fase 1.
- Si se solicita un perfil avanzado futuro, OraDiag debe rechazarlo de forma controlada o marcarlo como no soportado en Fase 1.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La CLI MUST permitir identificar la herramienta y ejecutar un diagnóstico simulado desde un fixture de laboratorio.
- **FR-002**: La CLI MUST aceptar parámetros para target, profile, symptom, fixture o escenario de laboratorio, y output en console o json.
- **FR-003**: La configuración humana MUST cargarse desde YAML y validar errores de forma controlada.
- **FR-004**: La configuración MUST soportar targets de ejemplo sin credenciales reales y perfiles declarativos iniciales.
- **FR-005**: Los perfiles iniciales MUST agrupar revisiones o capas, pero MUST NOT alterar reglas de causalidad ni confianza.
- **FR-006**: Debe existir al menos un perfil amplio tipo `diag_all` o equivalente para Fase 1.
- **FR-007**: El modelo formal MUST representar escenario diagnóstico, contexto del target, capa de acceso, proveedor de evidencia, Evidence Payload, observación individual, sujeto observado, estado, severidad, dominio causal candidato, rol causal, ventana temporal, datos estructurados, limitaciones, revisión OK, hallazgo diagnóstico, evaluación causal, recomendación y resultado diagnóstico final.
- **FR-008**: Los modelos MUST soportar evidencia positiva, evidencia negativa, revisiones OK, errores controlados, timeouts, permisos insuficientes, skipped/no evaluado, unknown/evidencia insuficiente, hallazgos incidentales, hallazgos relacionados, causa probable principal, factores contribuyentes, dominios causales, confianza del diagnóstico y salida JSON estable.
- **FR-009**: Evidence Payload MUST ser el contrato formal entre providers, collectors o scanners y el motor RCA.
- **FR-010**: Evidence Payload MUST ser serializable a JSON, incluir `schema_version` y validarse contra modelos internos.
- **FR-011**: Evidence Payload MUST ser independiente del origen de la evidencia.
- **FR-012**: En Fase 1, el origen de evidencia MUST ser un provider de fixtures de laboratorio o componente equivalente, no collectors reales.
- **FR-013**: YAML MAY usarse solo como formato humano para escenarios de laboratorio y configuración humana.
- **FR-014**: Los fixtures YAML MUST NOT definir el modelo formal ni el contrato consumido por el motor RCA.
- **FR-015**: Los fixtures YAML MUST compilarse o transformarse a Evidence Payload/modelos internos antes de cualquier evaluación RCA.
- **FR-016**: El motor RCA MUST NOT consumir YAML directamente.
- **FR-017**: Los fixtures MUST representar evidencia simulada, no conclusiones resueltas para uso del motor RCA.
- **FR-018**: Cualquier sección de expected output o expected diagnosis en fixtures MAY usarse por pruebas automatizadas, pero MUST NOT ser consumida por el motor RCA.
- **FR-019**: El motor RCA mínimo MUST ser determinístico, explicable y simulado.
- **FR-020**: El motor RCA MUST consumir Evidence Payload/modelos internos, no formatos humanos ni detalles del provider.
- **FR-021**: El motor RCA MUST elegir causa probable principal solo si existe evidencia suficiente.
- **FR-022**: El motor RCA MUST poder emitir `undetermined`, `Indeterminado` o equivalente cuando no exista evidencia suficiente.
- **FR-023**: El motor RCA MUST clasificar hallazgos como causa probable principal, contribuyentes, relacionados, incidentales, descartados, no evaluados o desconocidos según evidencia.
- **FR-024**: El motor RCA MUST conservar revisiones OK relevantes como evidencia negativa cuando ayuden a descartar hipótesis.
- **FR-025**: El motor RCA MUST convertir errores, timeouts, permisos insuficientes y capas no disponibles en limitaciones o revisiones no evaluadas.
- **FR-026**: El síntoma MUST usarse como pista de priorización y contexto, no como verdad causal.
- **FR-027**: El motor RCA MUST NOT usar IA, heurísticas no explicables ni análisis avanzado de correlación multicapas en Fase 1.
- **FR-028**: La salida console MUST ser legible en español.
- **FR-029**: La salida JSON MUST ser estructurada, estable y apta para pruebas automatizadas.
- **FR-030**: Toda salida MUST incluir, como mínimo, causa probable principal si existe, dominio causal, confianza, evidencias usadas, hallazgos relacionados, hallazgos incidentales, revisiones OK relevantes, limitaciones, recomendaciones iniciales y advertencia si la evidencia es insuficiente.
- **FR-031**: Las recomendaciones MUST ser prudentes, seguras, no destructivas y no deben solicitar escalamiento automático de privilegios.
- **FR-032**: La implementación futura de esta spec MUST incluir pruebas automatizadas de CLI básica, carga de configuración, validación de modelos, transformación de fixture YAML a Evidence Payload/modelos internos, prohibición de consumo YAML por el motor RCA, salida JSON estable y salida console básica.
- **FR-033**: Las pruebas automatizadas MUST cubrir al menos los escenarios de lentitud por bloqueo/sesiones simuladas, problema de usuario/autenticación simulado, evidencia insuficiente por timeouts/errores/permisos, hallazgo severo incidental, revisiones técnicas OK que descartan hipótesis y caso técnico OK con frontera Aplicación/Datos.
- **FR-034**: Fase 1 MUST NOT implementar conexión Oracle real, SSH real, listener real, collectors reales, consultas SQL reales, lectura real de alert log, parsing real de alert log, AWR/ASH, histórico, SQLite, reportes HTML maduros, reportes Markdown maduros, RAC/ASM/Multitenant/Standby avanzado, integraciones externas, IA, consultas a tablas de negocio ni modelado de datos funcionales.
- **FR-035**: La spec MUST NOT copiar decisiones de OraHealth/OraParity por analogía ni introducir funcionalidades de fases posteriores.

### Key Entities

- **Escenario diagnóstico**: Caso de laboratorio que describe el incidente simulado, síntoma, contexto y evidencia disponible sin conectividad real.
- **Target de ejemplo**: Identificador de entorno simulado definido en configuración humana, sin secretos ni credenciales reales.
- **Perfil de ejecución**: Agrupación declarativa de revisiones o capas aplicables a Fase 1; no modifica causalidad.
- **Fuente o proveedor de evidencia**: Componente reemplazable que produce Evidence Payload; en Fase 1 corresponde a fixtures de laboratorio.
- **Fixture de laboratorio**: YAML humano que describe evidencia simulada y puede incluir expectativas solo para pruebas.
- **Evidence Payload**: Contrato formal, versionado y serializable a JSON entre providers/collectors/scanners y motor RCA.
- **Observación o evidencia individual**: Dato técnico simulado con fuente, sujeto observado, estado, severidad, ventana temporal y datos estructurados.
- **Sujeto observado**: Entidad técnica a la que aplica la evidencia, como sesión, usuario, servicio, instancia, capa de acceso, almacenamiento simulado o componente técnico.
- **Limitación**: Restricción explícita por error, timeout, permiso insuficiente, capa no disponible, datos incompletos o no aplicabilidad.
- **Revisión OK**: Resultado sin problema que conserva valor como evidencia negativa o descarte de hipótesis.
- **Hallazgo diagnóstico**: Condición relevante detectada a partir de evidencia validada.
- **Evaluación causal**: Clasificación determinística del rol causal, dominio, confianza, evidencias usadas y contradicciones o limitaciones.
- **Recomendación**: Acción inicial prudente y no destructiva basada en el resultado y sus limitaciones.
- **Resultado diagnóstico final**: Salida consolidada console/json con causa probable si existe, dominio, confianza, hallazgos, OK relevantes, limitaciones y recomendaciones.

### Expected Automated Tests

- Prueba de identificación básica de la CLI.
- Prueba de ejecución `run` con target, profile, symptom, fixture y output.
- Pruebas de carga de configuración YAML válida e inválida.
- Pruebas de perfiles declarativos y rechazo controlado de perfiles no soportados.
- Pruebas de validación de modelos internos y serialización JSON del Evidence Payload.
- Pruebas de transformación de fixture YAML a Evidence Payload/modelos internos.
- Prueba que demuestre que el motor RCA no consume YAML directamente.
- Pruebas del motor RCA mínimo para causa principal, indeterminado, hallazgo incidental, hallazgo relacionado, contribuyente, descartado, no evaluado y unknown.
- Pruebas de conservación de revisiones OK relevantes.
- Pruebas de conversión de errores, timeouts y permisos insuficientes en limitaciones.
- Pruebas de salida JSON estable y salida console básica en español.

## Constitutional Alignment *(mandatory)*

### Roadmap and Scope

- **Roadmap grouping**: `001-core-rca-sin-conectividad-real`, Fase 1: CLI, configuración, perfiles, modelos base, Evidence Payload, fixtures de laboratorio y RCA engine mínimo simulado.
- **Rector docs used**: `.specify/memory/constitution.md`, `docs/DOCUMENTO_RECTOR.md`, `docs/ARCHITECTURE.md`, `docs/RCA_MODEL.md`, `docs/EVIDENCE_MODEL.md`, `docs/CAUSAL_DOMAINS.md`, `docs/SYMPTOM_HANDLING.md`, `docs/ERROR_HANDLING_AND_TIMEOUTS.md`, `docs/SECURITY_AND_ACCESS.md`, `docs/EXECUTION_PROFILES.md`, `docs/ROADMAP.md`, `docs/BACKLOG.md`, `docs/DECISION_LOG.md`, `docs/TRACEABILITY_MATRIX.md`, `docs/CONTRIBUTING.md`, `specs/000-gobierno-y-constitucion/spec.md`, `specs/000-gobierno-y-constitucion/plan.md` y `specs/000-gobierno-y-constitucion/tasks.md`.
- **Out of scope**: Conectividad Oracle real, SSH real, listener real, collectors reales, consultas SQL reales, lectura/parsing real de alert log, AWR/ASH, histórico, SQLite, reportes HTML/Markdown maduros, topologías Oracle avanzadas, integraciones externas, IA, tablas de negocio y datos funcionales.
- **Deviation status**: Ninguna desviación aceptada. Cualquier ampliación hacia fases 2 a 14 debe tratarse como `propuesta de desviación` y no incorporarse sin autorización humana explícita.

### RCA and Evidence Rules

- **Incident/RCA focus**: Esta spec crea el primer núcleo funcional de RCA de incidentes simulados, no un health check general ni una herramienta de capacity planning.
- **Evidence required**: Toda conclusión del motor RCA mínimo debe estar soportada por evidencia positiva, evidencia negativa o limitaciones explícitas dentro del Evidence Payload validado.
- **Symptom handling**: El síntoma prioriza y contextualiza, pero no decide causalidad. Si la evidencia no soporta el síntoma, la salida debe reflejar ambigüedad, contradicción o baja confianza.
- **Causal roles**: Fase 1 debe poder emitir o representar `primary_cause`, `contributing_factor`, `related_finding`, `incidental_finding`, `ruled_out`, `not_evaluated` y `unknown`.
- **Visible OK reviews**: Las revisiones OK deben conservarse y mostrarse cuando descarten hipótesis, expliquen confianza o justifiquen que un dominio no tiene evidencia causal.
- **Causal domains**: Deben usarse los dominios Sistema Operativo, Infraestructura, Almacenamiento, Base de datos, Aplicación, Usuario, Datos e Indeterminado según evidencia simulada. Datos se mantiene como frontera y no autoriza consultas de negocio.

### Safety, Data and Error Boundaries

- **No business data**: Fase 1 no consulta, modela ni infiere tablas de negocio, datos funcionales ni significado de aplicación. El caso Aplicación/Datos solo declara una frontera prudente.
- **Failures/timeouts**: Errores, timeouts, permisos insuficientes, capas no disponibles y datos incompletos deben convertirse en limitaciones o revisiones no evaluadas.
- **Security/minimum privileges**: La configuración de Fase 1 usa targets de ejemplo sin credenciales reales. No se deben guardar ni imprimir secretos. La falta de permisos simulada se reporta como limitación, no como solicitud automática de privilegios.
- **Recommendations**: Las recomendaciones deben ser seguras, no destructivas, explícitas sobre limitaciones y orientadas a obtener evidencia adicional o escalar al equipo correcto cuando corresponda.
- **Evidence Payload/format**: JSON es el contrato formal de Evidence Payload y salida estructurada. YAML solo es formato humano para configuración y escenarios de laboratorio; el motor RCA no debe consumir YAML.
- **Language**: La documentación, salida console, mensajes principales de error y reportes humanos deben estar en español. Identificadores técnicos estables pueden mantenerse en inglés cuando sirvan al contrato JSON.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de los escenarios mínimos de aceptación definidos en esta spec pueden ejecutarse con evidencia simulada y sin conectividad real.
- **SC-002**: El 100% de los diagnósticos con causa probable principal incluyen dominio causal, confianza y al menos una evidencia trazable usada por la evaluación.
- **SC-003**: El 100% de los escenarios con evidencia insuficiente devuelven resultado indeterminado o equivalente, confianza baja y al menos una limitación explícita.
- **SC-004**: El 100% de los fixtures YAML usados por pruebas se transforman a Evidence Payload/modelos internos antes de llegar al motor RCA.
- **SC-005**: Las pruebas automatizadas verifican que no existe ruta soportada donde el motor RCA consuma YAML directamente.
- **SC-006**: La salida JSON de cada escenario mínimo contiene de forma estable los campos requeridos para causa probable, dominio, confianza, evidencias, hallazgos, OK relevantes, limitaciones y recomendaciones.
- **SC-007**: La salida console de cada escenario mínimo es legible en español e incluye advertencia explícita cuando la evidencia es insuficiente.
- **SC-008**: El 100% de errores de configuración probados se reportan de forma controlada, sin crash no explicado ni intento de conectividad real.
- **SC-009**: Ninguna prueba, fixture o salida de Fase 1 requiere Oracle real, SSH real, listener real, SQL real, alert log real, tablas de negocio, IA o integraciones externas.
- **SC-010**: La revisión documental de la spec no encuentra contradicciones con la constitución, roadmap, modelos RCA/evidencia, dominios causales, seguridad, perfiles y reglas de síntomas.

## Assumptions

- La constitución en `.specify/memory/constitution.md` ya está ratificada y gobierna esta spec.
- `docs/ROADMAP.md` ya alinea Fase 1 con CLI, configuración, perfiles, modelos base, Evidence Payload, fixtures de laboratorio, RCA engine mínimo simulado y salidas console/json.
- La implementación futura usará las tecnologías obligatorias declaradas por la constitución para Fase 1, incluyendo CLI con Typer y pruebas con pytest.
- Los fixtures de laboratorio son datos de prueba controlados, no evidencia de entornos reales.
- Los targets de ejemplo no contienen credenciales reales ni datos sensibles.
- Los escenarios de laboratorio pueden simular capas futuras, pero no habilitan collectors reales ni consultas reales.
- La salida JSON de Fase 1 funciona como contrato inicial de pruebas y puede evolucionar solo mediante cambios versionados y gobernados por specs futuras.
- La correlación RCA avanzada pertenece a fases posteriores; Fase 1 solo valida reglas mínimas determinísticas y explicables.
