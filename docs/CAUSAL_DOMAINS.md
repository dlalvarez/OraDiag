# Dominios causantes

Cada diagnóstico clasifica el dominio causante probable cuando existe evidencia
suficiente. El dominio orienta al equipo que debe actuar. Para cada dominio se
indica qué evidencia aporta el núcleo SQL (disponible en cualquier plataforma)
y qué requiere un adaptador de plataforma.

## Sistema Operativo

- **Definición**: recursos del host que afectan a Oracle.
- **Ejemplos**: CPU saturada, presión de memoria, swapping, límites del sistema.
- **Núcleo SQL**: `V$OSSTAT` (CPU, load, memoria) y `V$SYSMETRIC_HISTORY`
  (consumo de CPU de host y base en la última hora).
- **Adaptador**: Enhanced Monitoring en RDS; comandos del sistema vía SSH
  on-premise.
- **Limitación**: en RDS no hay acceso al host; sin adaptador, la evidencia es
  la que la base expone de sí misma.
- **Regla**: clasificar aquí cuando la evidencia del host explique el incidente.

## Infraestructura

- **Definición**: red, DNS, balanceadores y la plataforma gestionada (RDS, OCI
  u on-premise virtualizado).
- **Ejemplos**: failover Multi-AZ, mantenimiento o reinicio de RDS, latencia de
  red, fallo de resolución, servicio no alcanzable.
- **Núcleo SQL**: `startup_time` de la instancia, errores de conexión de
  OraDiag, alert log.
- **Adaptador**: eventos y estado de la instancia en RDS; pruebas de red
  on-premise.
- **Regla**: usar cuando la falla esté fuera de Oracle pero afecte acceso o
  disponibilidad.

## Almacenamiento

- **Definición**: espacio e I/O: tablespaces, TEMP, UNDO, FRA, archive y el
  volumen subyacente.
- **Ejemplos**: TEMP agotado, FRA llena, archive sin espacio, latencia de I/O,
  throttling de IOPS del volumen.
- **Núcleo SQL**: uso de tablespaces, TEMP y UNDO, `V$RECOVERY_AREA_USAGE`,
  waits e histogramas de I/O, alert log.
- **Adaptador**: espacio libre, IOPS, throughput y latencia del volumen
  (CloudWatch en RDS; filesystem vía SSH on-premise).
- **Limitación**: la base ve síntomas de I/O, no la causa en el volumen; sin
  adaptador, el throttling del volumen queda como hipótesis de baja confianza.
- **Regla**: no equivale a capacity planning; clasificar aquí cuando el
  almacenamiento cause o limite la operación en la ventana.

## Base de datos

- **Definición**: comportamiento técnico de Oracle observable en vistas.
- **Ejemplos**: bloqueos, waits dominantes, ORA- críticos, contención de redo,
  latches o mutex, instancia en estado anómalo.
- **Núcleo SQL**: sesiones, bloqueos, waits, métricas, alert log, `SQL_ID`,
  `inst_id`, `con_id`. ASH y AWR si hay licencia.
- **Regla**: usar cuando la causa esté en el comportamiento técnico de Oracle.

## Aplicación

- **Definición**: comportamiento técnico de clientes, módulos, servicios o
  patrones SQL observables.
- **Ejemplos**: tormenta de conexiones, módulo saturando sesiones, un `SQL_ID`
  concentrando la carga, transacciones sin commit que bloquean.
- **Núcleo SQL**: `module`, `action`, `service_name`, `client_identifier`,
  `SQL_ID`, sesiones y errores de conexión.
- **Limitación**: no implica revisar código ni datos funcionales.
- **Regla**: usar cuando la evidencia técnica apunte al cliente o a un patrón
  de aplicación.

## Usuario

- **Definición**: problemas técnicos de cuentas y autenticación.
- **Ejemplos**: cuenta bloqueada, password expirado, intentos fallidos,
  privilegios insuficientes.
- **Núcleo SQL**: `DBA_USERS`, perfiles, auditoría de logins disponible.
- **Limitación**: no analiza intención ni datos de negocio del usuario.
- **Regla**: usar cuando el incidente se explique por autenticación o
  autorización técnica.

## Datos

- **Definición**: conclusión límite: sin evidencia técnica bajo alcance, el
  problema podría estar en datos, aplicación o uso funcional.
- **Ejemplos**: reclamo funcional sin waits, errores, bloqueos, presión de
  almacenamiento ni sesiones anómalas en la ventana.
- **Evidencia típica**: revisiones técnicas OK relevantes y ausencia de
  evidencia causal técnica.
- **Limitación**: no habilita consultas a tablas de negocio.
- **Regla**: solo como hipótesis límite, con recomendación de escalar al equipo
  funcional o de aplicación. Requiere que los dominios técnicos relevantes
  estén evaluados; si hay dominios en `not_evaluated`, corresponde
  Indeterminado.

## Indeterminado

- **Definición**: evidencia insuficiente o contradictoria.
- **Ejemplos**: sin acceso a ninguna fuente, dominios relevantes no evaluados,
  hipótesis competidoras sin desempate.
- **Evidencia típica**: limitaciones, timeouts, errores de permisos.
- **Regla**: usar cuando no sea responsable asignar otro dominio, indicando qué
  evidencia faltante permitiría concluir.
