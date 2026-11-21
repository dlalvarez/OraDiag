# Seguridad y acceso

OraDiag opera con mínimos privilegios, solo lectura y sin exponer secretos ni
datos sensibles. La seguridad es parte del diseño, no una mejora posterior.

## Credenciales

Métodos permitidos, en orden de preferencia:

1. Referencia a un gestor de secretos. La lectura del gestor es responsabilidad
   del adaptador de la plataforma correspondiente (por ejemplo, AWS Secrets
   Manager en el adaptador AWS RDS), para no acoplar el núcleo a un proveedor.
2. Variable de entorno referenciada en la configuración (`password_env`).
3. Prompt interactivo sin eco.

No se permite password en texto plano en archivos de configuración, ni siquiera
en laboratorio. Las conexiones SSH del adaptador on-premise usan llave y
verificación estricta de host key.

## Usuario de base de datos

- Usuario dedicado para OraDiag, nunca el usuario maestro de RDS ni `SYSTEM`.
- Privilegios: `CREATE SESSION` y `SELECT` sobre las vistas que declaran las
  revisiones habilitadas. OraDiag genera el script de grants mínimos a partir
  de esa declaración (spec 004).
- En RDS los grants sobre vistas `V$` se hacen con
  `rdsadmin.rdsadmin_util.grant_sys_object`; on-premise, con `GRANT SELECT` sobre
  la vista `V_$` correspondiente.
- No se usa `SELECT_CATALOG_ROLE` ni `SELECT ANY DICTIONARY`: incluyen vistas
  licenciadas y amplían el acceso más de lo necesario.
- Los grants sobre vistas licenciadas se otorgan solo si el target declara la
  licencia.

## Solo lectura

OraDiag ejecuta únicamente `SELECT`. No ejecuta DML, DDL, `ALTER SYSTEM`, no
crea objetos, no genera archivos en el servidor y no invoca procedimientos que
cambien estado. Una prueba automatizada verifica que no existan otras
sentencias en el código.

## Reglas de secretos

- Nunca secretos en el repositorio, logs, reportes ni fixtures.
- Los logs y reportes registran el nombre de la referencia (variable o secreto),
  nunca su valor.
- Las cadenas de conexión se registran sin password.

## Datos sensibles

- Texto de SQL y valores de bind: se recolectan solo cuando una spec lo
  justifique y se enmascaran en reportes por defecto.
- Nombres de máquina, programa y usuario de sistema operativo de las sesiones:
  datos operativos sensibles; se incluyen en reportes solo cuando son parte de
  la cadena de evidencia.
- Los reportes se escriben con permisos restringidos al usuario que ejecuta.

## Exposición a terceros

OraDiag no envía evidencia a servicios externos. Cualquier integración futura
con IA, servidores MCP, correo, chat o tickets requiere una spec propia y
aprobación de seguridad del banco.

## Prohibición de tablas de negocio

OraDiag no consulta tablas de negocio ni investiga datos funcionales. El dominio
Datos no cambia esta regla: solo permite declarar que, sin evidencia técnica, el
análisis debe continuar fuera de OraDiag.

## Mínimos privilegios ante fallas

Si faltan permisos, el resultado es una limitación `permission_denied` con el
grant exacto que falta. Nunca se escalan privilegios automáticamente.
