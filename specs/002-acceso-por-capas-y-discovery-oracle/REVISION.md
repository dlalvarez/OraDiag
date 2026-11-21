# Revisión de la spec 002 (noviembre 2026)

**Estado**: Histórica. Superseded por `004-conexion-oracle-y-discovery`.
**Revisada contra**: constitución v2.0.0.

Se revisaron `spec.md`, `plan.md`, `data-model.md`, `research.md`,
`quickstart.md`, `tasks.md` y `contracts/`. Nunca se implementó. Este documento
registra qué se conserva como insumo para la spec 004 y qué se descarta. Los
archivos originales se conservan sin cambios, salvo un aviso al inicio de `spec.md`.

## Veredicto

Los principios de tolerancia a fallas son sólidos y se conservan: cada fuente
independiente, resultados parciales, nada de inferir lo que no se ve, el
discovery no concluye causalidad. El problema es el modelo de "acceso por
capas", que trata SSH, listener y sistema operativo como capas del núcleo. En
RDS no hay acceso al host ni al listener, y con el principio XII esas fuentes
pasan a ser adaptadores opcionales (spec 010). Además la spec no contemplaba
licenciamiento de packs, particularidades de RDS ni generación de grants.

## Se conserva para la spec 004

| Origen | Contenido | Ajuste en 004 |
|---|---|---|
| FR-004 a FR-010 | Resultado independiente por fuente; timeouts configurables; errores sin traceback; permisos como limitación sin escalamiento | Timeouts concretos: conexión y `call_timeout` de `python-oracledb` |
| FR-015 a FR-019 | Discovery con resultados parciales; no inferir topología no visible; el discovery no concluye | Se agrega edición, plataforma (RDS u on-premise) y estado de licencias |
| FR-021, FR-024 | Motor independiente de conectores; una fuente inaccesible nunca es evidencia positiva de causa | Sin cambios |
| FR-013, FR-014 | Validación con dobles antes de conexión real | Se agrega validación contra una RDS de desarrollo como criterio de cierre |
| Casos límite | Fuente parcial, todo falla, datos inconsistentes, identificadores sensibles | Sin cambios |
| `contracts/evidence-integration.md` | Discovery como contexto compatible con el payload | Se alinea al Evidence Payload v2 de la 003 |

## Se descarta

| Origen | Contenido | Motivo |
|---|---|---|
| FR-002, `contracts/layer-access.md` | Capas `os/ssh`, `listener/network`, `storage_context` en el núcleo | XII: son adaptadores opcionales (spec 010) |
| FR-015 | "Host visible técnicamente" como dato de discovery | En RDS no hay host accesible; se reporta solo lo que expone la base |
| FR-016 | ASM y listener en discovery | No visibles en RDS; se evalúan con on-premise |
| FR-028 | Prohibición de SQL real en la spec | La 004 define las consultas exactas con su grant y licencia |
| — | Sin verificación de licencias ni grants | Se agregan: declaración y verificación de packs (XIII) y generador de grants con variante `rdsadmin` |
