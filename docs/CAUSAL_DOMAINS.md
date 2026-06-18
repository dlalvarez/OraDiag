# Dominios causantes

Cada diagnóstico relevante debe clasificar el dominio causante probable cuando exista evidencia suficiente.

## Sistema Operativo
- **Definición**: recursos y servicios del host que afectan Oracle.
- **Ejemplos**: CPU saturada, memoria insuficiente, procesos bloqueados, límites del sistema.
- **Evidencias típicas**: métricas OS, errores de kernel, uso de recursos, filesystem visible.
- **Limitaciones**: requiere acceso al host o logs disponibles.
- **Reglas**: clasificar aquí cuando la evidencia OS explique el incidente.

## Infraestructura
- **Definición**: red, DNS, virtualización, balanceadores o componentes externos técnicos.
- **Ejemplos**: latencia de red, fallo DNS, VIP no disponible, listener inaccesible por red.
- **Evidencias típicas**: pruebas de conectividad, errores listener, rutas y timeouts.
- **Limitaciones**: OraDiag puede ver síntomas técnicos, no toda la plataforma externa.
- **Reglas**: usar cuando la falla esté fuera de Oracle pero afecte acceso o disponibilidad.

## Almacenamiento
- **Definición**: filesystems, ASM futuro, FRA, TEMP, UNDO, I/O y espacio.
- **Ejemplos**: FRA llena, TEMP agotado, I/O lento, archive destination lleno.
- **Evidencias típicas**: uso de espacio, waits de I/O, errores de escritura, alert log.
- **Limitaciones**: no equivale a capacity planning.
- **Reglas**: clasificar aquí cuando almacenamiento cause o limite la operación.

## Base de datos
- **Definición**: estado y componentes internos Oracle bajo vistas técnicas.
- **Ejemplos**: instancia caída, ORA críticos, bloqueos, waits dominantes, redo log buffer.
- **Evidencias típicas**: alert log, vistas dinámicas, sesiones, wait_class, SQL_ID, inst_id, con_id.
- **Limitaciones**: depende de permisos y disponibilidad SQL.
- **Reglas**: usar cuando la causa esté en comportamiento técnico Oracle.

## Aplicación
- **Definición**: comportamiento técnico de clientes, módulos, servicios o patrones SQL observables.
- **Ejemplos**: tormenta de conexiones, módulo específico saturando sesiones, SQL_ID asociado a esperas.
- **Evidencias típicas**: module, service_name, client_identifier, SQL_ID, sesiones y errores de conexión.
- **Limitaciones**: no implica revisar código ni datos funcionales.
- **Reglas**: usar cuando la evidencia técnica apunte al cliente o patrón de aplicación.

## Usuario
- **Definición**: problemas técnicos de cuentas y autenticación.
- **Ejemplos**: cuenta bloqueada, password expirado, intentos fallidos, permisos insuficientes.
- **Evidencias típicas**: estado de cuenta, errores ORA de login, auditoría de sesión disponible.
- **Limitaciones**: no analiza intención ni datos de negocio del usuario.
- **Reglas**: usar cuando el incidente sea explicado por autenticación/autorización técnica.

## Datos
- **Definición**: conclusión límite para indicar que no hay evidencia técnica bajo alcance y que el problema podría estar en datos, aplicación o usuario funcional.
- **Ejemplos**: reclamo funcional sin waits, errores, bloqueos, almacenamiento, listener o sesiones anómalas bajo alcance.
- **Evidencias típicas**: revisiones técnicas OK y ausencia de evidencia causal técnica.
- **Limitaciones**: no habilita consultas a tablas de negocio ni investigación funcional.
- **Reglas**: solo usar como hipótesis límite con recomendación de escalar al equipo funcional/aplicación.

## Indeterminado
- **Definición**: evidencia insuficiente o contradictoria.
- **Ejemplos**: accesos fallidos a todas las capas, datos parciales inconclusos.
- **Evidencias típicas**: limitaciones, timeouts, errores de permisos.
- **Limitaciones**: requiere más información.
- **Reglas**: usar cuando no sea responsable asignar otro dominio.
