# Perfiles de ejecución

Los perfiles agrupan revisiones para distintos escenarios, pero no cambian las reglas RCA, la obligación de evidencia ni la prohibición de tablas de negocio.

## Perfiles iniciales

```text
diag_all
diag_fast
diag_connectivity
diag_availability
diag_waits
diag_locks
diag_storage
diag_redo
diag_user_access
diag_infrastructure
diag_rac
diag_asm
diag_multitenant
diag_standby
```

## Descripción resumida

- `diag_all`: revisión amplia dentro del alcance técnico.
- `diag_fast`: revisión rápida para incidentes activos.
- `diag_connectivity`: capas de acceso y listener.
- `diag_availability`: disponibilidad de instancia/base.
- `diag_waits`: wait events y wait_class.
- `diag_locks`: sesiones y bloqueos.
- `diag_storage`: filesystem, FRA, TEMP y UNDO.
- `diag_redo`: redo, archive y log switches.
- `diag_user_access`: cuentas, passwords, intentos fallidos y auditoría técnica.
- `diag_infrastructure`: red, DNS, listener y plataforma visible.
- `diag_rac`, `diag_asm`, `diag_multitenant`, `diag_standby`: componentes avanzados futuros.

## Ejemplos futuros

```bash
oradiag run --target prod_orcl_01 --profile diag_all --output console
oradiag run --target prod_orcl_01 --profile diag_waits --output json
```
