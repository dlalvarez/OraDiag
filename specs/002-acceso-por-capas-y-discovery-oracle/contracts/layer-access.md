# Contract: Layer Access

## Purpose

Define el contrato documental para acceso por capas en Spec 002. Este contrato gobierna cómo una capa se define, solicita, ejecuta y transforma en evidencia o limitación sin acoplar RCA a backends concretos.

## Layer IDs

Capas iniciales permitidas:

- `database/sql_access`
- `listener/network`
- `os/ssh`
- `storage_context`
- `authentication/access`

Los nombres representan capacidad de acceso/discovery, no checks de salud.

## Scope Boundaries

- `authentication/access`: solo intento técnico de acceso o limitación. No diagnostica cuentas bloqueadas, passwords expirados, auditoría de intentos fallidos ni problemas de usuario.
- `storage_context`: solo visibilidad/disponibilidad de capa. No analiza capacidad, FRA, TEMP, UNDO, redo, archive, ASM capacity ni presión de espacio.
- `listener/network`: solo accesibilidad o contexto observable. No hace troubleshooting profundo ni diagnóstico avanzado de servicios.

## Request Contract

Una solicitud de capa debe contener:

- `request_id`
- `target_id`
- `profile`
- `symptom`
- `layer_id`
- `timeout_seconds`
- `metadata` no sensible

La solicitud no puede contener:

- passwords, tokens, secrets o connection strings;
- SQL crudo;
- comandos OS o SSH;
- reglas de causalidad, scoring o confianza.

## Result Contract

Un resultado de capa debe contener:

- `result_id`
- `layer_id`
- `status`
- `available`
- `message`
- `observed_context`
- `limitations`
- `elapsed_ms`
- `source`

Estados válidos:

```text
OK
INFO
WARNING
TIMEOUT
ERROR
SKIPPED
UNKNOWN
```

## Failure Mapping

| Condition | Required status | Required limitation |
|-----------|-----------------|---------------------|
| Timeout | `TIMEOUT` | `timeout` |
| Controlled backend error | `ERROR` | `error` |
| Missing permissions | `ERROR` or `SKIPPED` | `insufficient_permissions` |
| Layer unreachable/unavailable | `ERROR` or `SKIPPED` | `layer_unavailable` |
| Not applicable to target | `SKIPPED` | `not_applicable` |
| Partial/incomplete data | `WARNING` or `UNKNOWN` | `incomplete_data` |

## Continuity Rules

- Una capa fallida no aborta capas independientes.
- Todo resultado fallido debe ser serializable y trazable.
- `available=false` requiere limitación.
- Una capa inaccesible no es evidencia positiva de causa.
- Backends deben devolver resultado controlado o ser envueltos por el orquestador en resultado controlado.

## Backend Contract

Un backend reemplazable debe:

- aceptar una solicitud normalizada;
- respetar timeout;
- devolver resultado normalizado;
- no exponer secretos;
- no entregar handles de conexión al RCA;
- no entregar SQL crudo al RCA.

Tipos aceptados para Spec 002:

- `fake`: backend determinístico para pruebas.
- `double`: backend configurable para simular estados.
- `real_future`: interfaz preparada para conectividad real futura, sin requerir implementación productiva inicial.

## Evidence Integration

El resultado de capa debe transformarse antes de RCA:

- capa OK -> `AccessLayer` y opcional `ReviewResult`;
- capa fallida -> `AccessLayer` no disponible, `ReviewResult` no evaluado y `Limitation`;
- contexto observado -> `Observation` neutral si aporta contexto trazable;
- resultado OK que descarta hipótesis -> `ReviewResult.ok_relevance`.
