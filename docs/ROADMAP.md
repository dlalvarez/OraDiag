# Roadmap

Cada fase debe respetar el Documento Rector, actualizar documentación aplicable y no adelantar lógica fuera de alcance.

## Agrupación oficial de specs

- `000-gobierno-y-constitucion`: Fase 0.
- `001-core-rca-sin-conectividad-real`: Fase 1.
- `002-acceso-por-capas-y-discovery-oracle`: Fases 2 y 3.
- `003-errores-usuarios-y-autenticacion`: Fases 4 y 5.
- `004-sesiones-bloqueos-y-waits`: Fases 6 y 7.
- `005-espacio-almacenamiento-y-redo`: Fases 8 y 9.
- `006-correlacion-rca-y-reportes`: Fases 10 y 11.
- `007-topologias-oracle-avanzadas`: Fase 12.
- `008-historico-y-extensiones`: Fases 13 y 14.

## Fase 0: Gobierno documental
- **Objetivo**: crear fuente de verdad documental.
- **Alcance**: README, documentos rectores, matriz, backlog, plantilla PR y placeholders mínimos.
- **Fuera de alcance**: lógica funcional.
- **Criterios de aceptación**: documentación en español, consistente y completa.
- **Pruebas esperadas**: validación de archivos y revisión de alcance.
- **Documentación**: todos los documentos iniciales.

## Fase 1: Core RCA sin conectividad real
- **Objetivo**: esqueleto ejecutable sin conectividad real.
- **Alcance**: CLI, configuración, perfiles, modelos base, Evidence Payload, fixtures de laboratorio, RCA engine mínimo simulado y salidas console/json.
- **Fuera de alcance**: conexión Oracle real, SSH real, listener real, collectors reales, consultas SQL reales y lectura real de alert log.
- **Criterios de aceptación**: comandos mock controlados y modelos validados.
- **Pruebas esperadas**: unitarias de CLI/modelos, Evidence Payload, fixtures, RCA mínimo simulado y salidas console/json.
- **Documentación**: arquitectura, perfiles, evidencia.

## Fase 2: Conectividad por capas
- **Objetivo**: diseñar conectores con timeouts y fallas controladas.
- **Alcance**: interfaces y pruebas con dobles.
- **Fuera de alcance**: RCA avanzado.
- **Criterios de aceptación**: errores convertidos en limitaciones.
- **Pruebas esperadas**: timeouts, permisos, caídas simuladas.
- **Documentación**: seguridad y errores.

## Fase 3: Discovery Oracle
- **Objetivo**: descubrir contexto técnico Oracle disponible.
- **Alcance**: versión, instancia, CDB/PDB, RAC/ASM/standby cuando sea visible.
- **Fuera de alcance**: checks de performance.
- **Criterios de aceptación**: discovery parcial tolerante a fallas.
- **Pruebas esperadas**: mocks SQL/OS.
- **Documentación**: arquitectura y evidencia.

## Fase 4: Alert log y errores críticos
- **Objetivo**: recolectar y evaluar errores críticos recientes.
- **Alcance**: alert log, ORA críticos, timestamps y contexto.
- **Fuera de alcance**: consultas de negocio.
- **Criterios de aceptación**: errores soportados por evidencia.
- **Pruebas esperadas**: fixtures de logs.
- **Documentación**: RCA y evidencia.

## Fase 5: Usuario y autenticación
- **Objetivo**: diagnosticar problemas de acceso de usuario.
- **Alcance**: cuentas bloqueadas, expiradas, intentos fallidos y auditoría técnica disponible.
- **Fuera de alcance**: datos funcionales del usuario.
- **Criterios de aceptación**: detalles de usuario sin secretos.
- **Pruebas esperadas**: fixtures de estados y errores.
- **Documentación**: seguridad y dominios.

## Fase 6: Sesiones y bloqueos
- **Objetivo**: identificar bloqueos, sesiones relevantes y contención.
- **Alcance**: sesiones, usuarios, módulos, servicios, SQL_ID, inst_id, con_id.
- **Fuera de alcance**: tuning automático.
- **Criterios de aceptación**: bloqueador/víctima y evidencia.
- **Pruebas esperadas**: escenarios simulados.
- **Documentación**: RCA y evidencia.

## Fase 7: Wait analysis
- **Objetivo**: analizar wait events y wait_class para rendimiento.
- **Alcance**: esperas dominantes, correlación temporal y sesiones afectadas.
- **Fuera de alcance**: AWR como dependencia inicial.
- **Criterios de aceptación**: clasificación causal prudente.
- **Pruebas esperadas**: fixtures de waits.
- **Documentación**: RCA, dominios y backlog.

## Fase 8: Storage, FRA, TEMP y UNDO
- **Objetivo**: diagnosticar presión de almacenamiento técnico.
- **Alcance**: filesystem, ASM futuro, FRA, TEMP, UNDO e I/O observable.
- **Fuera de alcance**: capacity planning.
- **Criterios de aceptación**: distinguir incidente actual vs tendencia.
- **Pruebas esperadas**: umbrales y límites simulados.
- **Documentación**: dominios y seguridad.

## Fase 9: Redo, archive y log switches
- **Objetivo**: analizar redo, archive, log switches y standby relacionado.
- **Alcance**: frecuencia de switches, presión archive/FRA, waits redo.
- **Fuera de alcance**: rediseño de capacidad.
- **Criterios de aceptación**: evidencia temporal de impacto.
- **Pruebas esperadas**: fixtures de redo/archive.
- **Documentación**: RCA y dominios.

## Fase 10: RCA correlator avanzado
- **Objetivo**: ampliar la correlación RCA más allá del motor mínimo simulado de Fase 1 para correlacionar revisiones en una causa probable.
- **Alcance**: reglas determinísticas avanzadas, roles causales, confianza y correlación entre múltiples capas técnicas.
- **Fuera de alcance**: IA obligatoria.
- **Criterios de aceptación**: conclusiones sin evidencia prohibidas.
- **Pruebas esperadas**: casos RCA end-to-end simulados.
- **Documentación**: RCA, matriz y decisiones.

## Fase 11: Reportes maduros
- **Objetivo**: salidas console, json, markdown y html.
- **Alcance**: formato estable y legible.
- **Fuera de alcance**: dashboards.
- **Criterios de aceptación**: reportes incluyen OK, problemas y limitaciones.
- **Pruebas esperadas**: snapshots de salida.
- **Documentación**: arquitectura y evidencia.

## Fase 12: RAC, ASM, Multitenant y Standby avanzado
- **Objetivo**: ampliar cobertura Oracle avanzada.
- **Alcance**: instancias, disk groups, PDBs y Data Guard.
- **Fuera de alcance**: automatizar cambios productivos.
- **Criterios de aceptación**: contexto inst_id/con_id explícito.
- **Pruebas esperadas**: fixtures multiinstancia.
- **Documentación**: dominios y arquitectura.

## Fase 13: Histórico de incidentes
- **Objetivo**: registrar incidentes y resoluciones confirmadas.
- **Alcance**: store local futuro y comparación de casos.
- **Fuera de alcance**: dependencia obligatoria para diagnóstico inicial.
- **Criterios de aceptación**: trazabilidad de resolución humana.
- **Pruebas esperadas**: persistencia y migraciones.
- **Documentación**: seguridad, backlog y decisiones.

## Fase 14: Mejoras futuras y extensiones
- **Objetivo**: incorporar extensiones controladas.
- **Alcance**: IA opcional, integraciones, dashboards, AWR licenciado opcional.
- **Fuera de alcance**: romper reglas rectoras.
- **Criterios de aceptación**: extensiones opt-in y gobernadas.
- **Pruebas esperadas**: integración aislada.
- **Documentación**: backlog, decisiones y matriz.
