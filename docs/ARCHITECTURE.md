# Arquitectura

La arquitectura separa recolección, evaluación, correlación y reporte, para que
ninguna fuente de evidencia determine conclusiones RCA sin contexto. Desde la
constitución v2.0.0 se organiza en un núcleo independiente de plataforma y
adaptadores opcionales.

## Capas

| Capa | Contenido | Dependencias permitidas | ¿Obligatoria? |
|---|---|---|---|
| Núcleo de dominio | Modelos, Evidence Payload, motor causal, reglas, reporters | Python estándar, Pydantic | Sí |
| Fuente SQL | Conexión Oracle, preflight, discovery, collectors SQL por dominio | `python-oracledb` (thin) | Sí, salvo modo laboratorio |
| Fuentes licenciadas | ASH y AWR | Fuente SQL + declaración de licencia | No, apagada por defecto |
| Adaptadores de plataforma | AWS RDS, on-premise (SSH), OCI | SDK del proveedor, como `extra` opcional | No |
| CLI | Comandos, carga de configuración y perfiles | Typer, PyYAML | Sí |

Regla de dependencias: las flechas solo apuntan hacia el núcleo. El núcleo no
importa la fuente SQL, ni las fuentes licenciadas, ni los adaptadores. Una
prueba automatizada lo verifica.

## Flujo de un diagnóstico

1. La CLI carga el target, el perfil, el síntoma opcional y la ventana del
   incidente (por defecto, "ahora" para incidentes en curso).
2. La fuente SQL conecta con timeout, ejecuta el discovery y el preflight de las
   vistas que pide el perfil. Lo inaccesible se registra como limitación.
3. Los collectors de cada dominio recolectan observaciones con marca de tiempo.
   Las fuentes licenciadas solo participan si el target declara la licencia y
   el parámetro `control_management_pack_access` es coherente.
4. Los adaptadores de plataforma configurados agregan observaciones propias.
5. Todo se normaliza en un Evidence Payload versionado (JSON).
6. El motor causal construye hipótesis, las correlaciona con la ventana del
   incidente y entre sí, y asigna roles causales y confianza con su cadena de
   evidencia.
7. Los reporters emiten console y JSON (markdown y HTML a partir de la spec 009).

## Árbol objetivo

```text
src/oradiag/
  domain/        modelos, enums, Evidence Payload, resultados
  engine/        motor causal, reglas, confianza
  sources/
    sql/         conexión, preflight, discovery, collectors por dominio
    licensed/    ASH y AWR (aislado y protegido por licencia)
    lab/         proveedor de fixtures de laboratorio
  adapters/
    aws_rds/     extra opcional
    onprem_ssh/  extra opcional
  reports/       console, json (markdown/html en 009)
  cli/
  config/
```

## Particularidades de Amazon RDS for Oracle

- No hay acceso a `SYS` ni `SYSDBA`; los permisos sobre vistas `V$` se otorgan
  con `rdsadmin.rdsadmin_util.grant_sys_object`.
- No hay acceso al host: la evidencia de sistema operativo dentro del núcleo
  proviene de `V$OSSTAT` y `V$SYSMETRIC_HISTORY`; el detalle de host, volumen y
  eventos de plataforma requiere el adaptador AWS RDS (spec 010).
- El alert log se lee por SQL; la vía exacta se valida en la spec 007.
- Enterprise Edition en RDS usa licencia propia (BYOL): la licencia de los packs
  depende del contrato del banco con Oracle.
