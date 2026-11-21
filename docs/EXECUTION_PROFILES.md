# Perfiles de ejecución

Los perfiles agrupan revisiones para distintos escenarios. No cambian las
reglas RCA, la obligación de evidencia, las reglas de licenciamiento ni la
prohibición de tablas de negocio. Un perfil puede incluir revisiones que
requieran licencia o adaptador: si no están disponibles, quedan
`not_evaluated` con la limitación correspondiente.

## Perfiles

| Perfil | Propósito | Fuentes | Spec |
|---|---|---|---|
| `diag_fast` | Incidente en curso: lo mínimo para orientar en segundos | Núcleo SQL | 005 |
| `diag_all` | Revisión amplia dentro del alcance técnico | Todas las disponibles | 009 |
| `diag_connectivity` | No se puede conectar o la conexión cuelga | Núcleo SQL + prueba de alcance de red desde el cliente | 004, 007 |
| `diag_availability` | Base o instancia no disponible | Núcleo SQL; adaptador para eventos de plataforma | 004, 010 |
| `diag_locks` | Bloqueos y contención | Núcleo SQL | 005 |
| `diag_waits` | Lentitud por esperas | Núcleo SQL; ASH si hay licencia | 005, 006 |
| `diag_past_incident` | Incidente ya ocurrido en una ventana declarada | ASH/AWR con licencia; adaptador de plataforma | 006, 010 |
| `diag_user_access` | Cuentas, expiración, intentos fallidos | Núcleo SQL | 007 |
| `diag_storage` | Espacio, TEMP, UNDO y FRA | Núcleo SQL; adaptador para el volumen | 008, 010 |
| `diag_redo` | Redo, archive y log switches | Núcleo SQL | 008 |
| `diag_infrastructure` | Host, red y plataforma gestionada | Adaptador de plataforma | 010 |
| `diag_rac`, `diag_multitenant`, `diag_standby` | Topologías avanzadas | Núcleo SQL | 011 |

ASM no tiene perfil propio en la plataforma inicial: en RDS no es visible. Se
evaluará al incorporar on-premise.

## Ejemplos

```bash
# Incidente en curso
oradiag run --target rds_core_01 --profile diag_fast --symptom slow_performance

# Incidente pasado con ventana declarada (requiere fuentes con histórico)
oradiag run --target rds_core_01 --profile diag_past_incident \
  --since "2026-11-20 14:05" --until "2026-11-20 14:40" --output json
```

La sintaxis exacta de la CLI se define en la spec 003.
