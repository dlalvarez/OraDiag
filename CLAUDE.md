# CLAUDE.md — OraDiag

Guía para Claude Code en este repositorio. Léela completa antes de cambiar nada.

## Qué es

OraDiag es un framework Python para RCA (análisis de causa raíz) de incidentes
Oracle ya reportados o en curso. Lo usa un DBA en un banco: **una conclusión
sin evidencia es peor que un "no sé"**. No es un health check (eso es
OraHealth), ni capacity planning, ni un buscador de anomalías.

Plataforma inicial: Amazon RDS for Oracle Enterprise Edition. Después:
on-premise y OCI con el mismo núcleo.

## Fuentes rectoras (en orden de prioridad)

1. `.specify/memory/constitution.md` (v2.0.0): manda sobre todo lo demás.
2. La spec activa en `specs/NNN-*/` (`spec.md`, `plan.md`, `tasks.md`).
3. `docs/` (arquitectura, modelo RCA, evidencia, dominios, roadmap, decisiones).

Si algo de `docs/` contradice la constitución, prevalece la constitución y se
reporta la contradicción. Las specs 001 y 002 son históricas: no las
implementes ni copies su código.

## Cómo se trabaja

- La planeación (specs, planes, tareas) se hace y aprueba **antes** de
  implementar. Tu trabajo aquí es implementar el `tasks.md` de la spec activa.
- Implementa solo lo que pide la tarea. Si encuentras algo que invalida la
  spec, **detente** y propón el ajuste a la spec; no improvises en código.
- Cualquier idea fuera de la spec se marca como `propuesta de desviación` y no
  se implementa sin autorización.
- Pruebas primero cuando la tarea lo permita. Toda la suite en verde antes de
  cada commit.
- Ramas: `develop-claude` es la rama integradora. Una rama por spec desde ella
  (`spec/NNN-nombre`), PR hacia `develop-claude`. `main` solo recibe versiones
  estables.
- PRs: spec relacionada, cumplimiento constitucional, pruebas ejecutadas,
  documentación actualizada y desviaciones aceptadas.

## Reglas no negociables

1. **Núcleo SQL independiente de plataforma (XII).** `domain/`, `engine/`,
   `reports/` y `sources/sql/` no importan boto3, SDKs de OCI, paramiko ni
   nada específico de un proveedor. Los adaptadores son `extras` opcionales.
2. **Packs deshabilitados por defecto (XIII).** Nunca consultes
   `V$ACTIVE_SESSION_HISTORY`, `DBA_HIST_*`, `DBA_ADDM_*`, `DBA_ADVISOR_*`,
   `V$SQL_MONITOR`, `V$SQL_PLAN_MONITOR` ni paquetes `DBMS_WORKLOAD_REPOSITORY`,
   `DBMS_ADDM`, `DBMS_SQLTUNE` fuera de `sources/licensed/`, y solo con la
   licencia declarada en el target. No infieras la licencia de un parámetro.
3. **Solo lectura (XIV).** Solo `SELECT`. Nada de DML, DDL, `ALTER SYSTEM`,
   crear objetos, generar archivos en el servidor ni procedimientos de
   `rdsadmin` que escriban reportes.
4. **Sin dato confiable no hay conclusión (II, VIII).** Si una consulta falla o
   una vista no es accesible, el resultado es una limitación con el motivo
   exacto (vista + ORA-), nunca un OK por "lista vacía". No inventes valores.
5. **Correlación, no suma de severidades (XV).** La causa principal sale de una
   cadena de evidencia correlacionada con la ventana del incidente. Una
   severidad alta fuera de la ventana o sin relación causal es incidental.
6. **Timeouts en todo (VIII).** `call_timeout` en cada consulta; ninguna fuente
   puede colgar el diagnóstico.
7. **Sin datos de negocio (VII).** Nunca consultes tablas de aplicación. Texto
   de SQL y valores de bind se tratan como sensibles y se enmascaran en reportes.
8. **Secretos (IX).** Credenciales solo por variable de entorno o gestor de
   secretos referenciado. Nunca en el repo, logs, reportes ni fixtures.
9. **Idioma.** Todo texto visible (mensajes, reportes, docs) en español.
   Identificadores, enums y claves JSON pueden ir en inglés.
10. **Particularidades de RDS.** No hay `SYS` ni acceso al host. Cada vista
    nueva documenta su grant normal y su equivalente
    `rdsadmin.rdsadmin_util.grant_sys_object`.

## Stack

Python 3.12+, `uv`, Typer, Pydantic, PyYAML, pytest y `python-oracledb` en modo
thin (sin Oracle Client).

```bash
uv sync                    # dependencias
uv run pytest -q           # suite completa; debe pasar antes de cada commit
uv run oradiag --help
```

## Pruebas obligatorias por tipo de cambio

- Regla causal nueva: caso con causa, caso incidental fuera de ventana, caso
  sin evidencia suficiente.
- Fuente SQL nueva: caso sano, caso con hallazgo, sin privilegios (limitación),
  timeout (limitación) y vista no existente en la versión.
- Fuente licenciada: sin licencia declarada no se ejecuta ninguna consulta.
- Guardrails permanentes: imports del núcleo, vistas licenciadas fuera de
  `sources/licensed/`, sentencias que no sean `SELECT`.

## Estado

Constitución v2.0.0 aprobada; roadmap reescrito (`docs/ROADMAP.md`). Siguiente
paso: planeación completa de la spec `003-modelo-de-evidencia-y-motor-causal`.
El código en `src/` y `tests/` pertenece a la implementación anterior y se
retirará en un commit explícito antes de implementar la 003.
