# Roadmap

Roadmap vigente desde la constitución v2.0.0. Cada spec se planea y aprueba
completa (spec, plan, modelo de datos, contratos y tareas) antes de
implementarse con Claude Code. Solo la spec activa y la siguiente se detallan al
máximo; las posteriores se refinan al cerrar la anterior, con lo aprendido.

Principios transversales que toda spec debe respetar: núcleo SQL independiente
de plataforma (XII), packs licenciados deshabilitados por defecto (XIII), solo
lectura estricta (XIV) y correlación causal (XV).

## Mapa de dependencias

```text
003 modelo y motor causal
 └─ 004 conexión Oracle y discovery
     ├─ 005 sesiones, bloqueos y waits ──┐
     ├─ 006 fuentes licenciadas ASH/AWR ─┤
     ├─ 007 alert log y autenticación ───┼─ 009 correlación avanzada y reportes
     └─ 008 almacenamiento y redo ───────┘        │
                                                   ├─ 010 adaptadores de plataforma
                                                   ├─ 011 topologías avanzadas
                                                   └─ 012 histórico y extensiones
```

006, 007 y 008 dependen solo de 004 y pueden ejecutarse en cualquier orden.

## Specs históricas

- `000-gobierno-y-constitucion`: gobierno documental v1. Vigente en lo que no
  contradiga la constitución v2.0.0.
- `001-core-rca-sin-conectividad-real`: superseded por 003. Su código no se
  reutiliza.
- `002-acceso-por-capas-y-discovery-oracle`: superseded por 004. Su modelo de
  capas con SSH obligatorio se reemplaza por núcleo SQL + adaptadores.

## 003 — Modelo de evidencia y motor causal

- **Objetivo**: definir el contrato de evidencia y un motor RCA determinístico
  que correlacione, en lugar de sumar severidades.
- **Alcance**: Evidence Payload v2 (observaciones con marca de tiempo, ventana
  del incidente, fuente, polaridad y limitaciones); modelo de hipótesis causales
  y cadenas de evidencia; reglas causales declarativas; cálculo de confianza
  explicable; fixtures de laboratorio; CLI (`run`, `validate`, `version`);
  salidas console y JSON.
- **Fuera de alcance**: conexión Oracle, consultas SQL, adaptadores de
  plataforma, reportes markdown/html.
- **Criterios de aceptación**: cada escenario de laboratorio produce la causa
  esperada con su cadena de evidencia; un hallazgo grave fuera de la ventana
  temporal queda como incidental; sin evidencia suficiente el resultado es
  `unknown` o `Indeterminado`; JSON estable y versionado.
- **Pruebas esperadas**: unitarias de modelos y reglas, escenarios end-to-end
  con fixtures, snapshot de salida JSON, prueba de que el núcleo no importa SDKs
  cloud ni SSH.

## 004 — Conexión Oracle y discovery

- **Objetivo**: conectar de forma segura y tolerante a fallas, y conocer qué se
  puede evaluar en el target.
- **Alcance**: conexión `python-oracledb` thin con `call_timeout`; credenciales
  por variable de entorno o gestor de secretos referenciado; preflight de vistas
  (`select 1 from <vista> where 1 = 0`); discovery de versión, edición,
  CDB/PDB, RAC, rol Data Guard y plataforma (RDS u on-premise); declaración y
  verificación de licencias de packs; generador del script de grants mínimos,
  con variante `rdsadmin.rdsadmin_util.grant_sys_object` para RDS.
- **Fuera de alcance**: revisiones de diagnóstico por dominio.
- **Criterios de aceptación**: sin permisos o sin conexión, el resultado es un
  diagnóstico parcial con limitaciones exactas (vista + ORA-), nunca un crash;
  inconsistencia de licencia detectada y reportada.
- **Pruebas esperadas**: dobles de conexión (timeout, ORA-01017, ORA-00942,
  ORA-12170), discovery parcial, guardrail de licencias y guardrail de solo
  lectura.

## 005 — Sesiones, bloqueos y waits

- **Objetivo**: diagnosticar incidentes en curso de lentitud, cuelgues y
  contención usando solo vistas no licenciadas.
- **Alcance**: `V$SESSION`, `V$SESSION_WAIT`, `V$LOCK` y cadenas de bloqueo,
  `V$SYSTEM_EVENT` por deltas, `V$EVENT_HISTOGRAM`, `V$SYSMETRIC_HISTORY`
  (última hora), `V$OSSTAT`, `V$SQL` acotado por `SQL_ID`; vistas `GV$` cuando
  aplique.
- **Validación previa**: confirmar en *Database Licensing Information* de la
  versión objetivo que ninguna vista usada pertenece a un pack.
- **Fuera de alcance**: ASH/AWR, tuning automático.
- **Criterios de aceptación**: bloqueador -> víctimas -> síntoma correlacionado
  como cadena causal; métricas de la última hora usadas como baseline reciente.

## 006 — Fuentes licenciadas ASH y AWR

- **Objetivo**: RCA de incidentes ya ocurridos por ventana temporal.
- **Alcance**: `V$ACTIVE_SESSION_HISTORY` y `DBA_HIST_*` en módulo aislado,
  habilitado solo con `diagnostic_pack: licensed` y parámetro coherente;
  comparación contra una ventana de referencia.
- **Fuera de alcance**: generación de reportes AWR/ADDM en el servidor (prohibido
  por XIV), Tuning Pack salvo spec aprobada.
- **Bloqueo**: no se ejecuta contra bases reales hasta confirmar licencia.

## 007 — Errores, alert log y autenticación

- **Alcance**: alert log por SQL (`V$DIAG_ALERT_EXT`; en RDS validar el grant o
  usar `rdsadmin.rds_file_util` en modo lectura); ORA- críticos en la ventana;
  `DBA_USERS` (estado, expiración, perfil); auditoría de logins si está
  disponible.
- **Fuera de alcance**: datos funcionales del usuario.

## 008 — Almacenamiento, redo, TEMP y UNDO

- **Alcance**: tablespaces y autoextend, TEMP y UNDO en uso, FRA, redo log
  switches, archive y waits de redo/I/O.
- **Fuera de alcance**: capacity planning; espacio del volumen en RDS (lo cubre
  el adaptador de 010).

## 009 — Correlación avanzada y reportes

- **Alcance**: correlación entre dominios (por ejemplo, I/O lento + log file
  sync + switches frecuentes), reportes markdown y HTML con cadenas de evidencia
  visibles.

## 010 — Adaptadores de plataforma

- **Alcance**: adaptador AWS RDS opcional (métricas CloudWatch, Enhanced
  Monitoring, eventos RDS, logs) y adaptador on-premise opcional (SSH con
  verificación de host key). OCI cuando se requiera.
- **Regla**: el núcleo funciona sin ellos; aportan evidencia a los dominios
  Sistema Operativo, Infraestructura y Almacenamiento.

## 011 — Topologías avanzadas

- **Alcance**: RAC (`inst_id`), Multitenant (`con_id`) y Data Guard
  (transport/apply lag) desde la perspectiva de RCA.

## 012 — Histórico y extensiones

- **Alcance**: registro de incidentes y resoluciones confirmadas; extensiones
  opt-in. Cualquier integración con IA o MCP requiere spec propia y aprobación
  de seguridad.
