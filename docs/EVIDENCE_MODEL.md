# Modelo de evidencias

Toda conclusión relevante necesita evidencia. La ausencia de evidencia por falla
de acceso se registra como limitación, nunca se ignora ni se convierte en OK.
El contrato formal (Evidence Payload v2, JSON versionado validado con Pydantic)
se define en la spec 003.

## Entidades

- **Observation**: dato técnico observado. Incluye fuente, momento o intervalo
  observado, momento de recolección, alcance (`inst_id`, `con_id`, objeto),
  valor, unidad y polaridad (positiva, negativa o neutra).
- **ReviewResult**: resultado de una revisión con estado, severidad técnica,
  observaciones y limitaciones.
- **Hypothesis**: explicación candidata con dominio causante, regla que la
  generó, cadena de evidencia y rol causal asignado.
- **Diagnosis**: conclusión del motor: causa principal (si existe), roles de las
  demás hipótesis, confianza con su motivo, limitaciones y recomendaciones.
- **Limitation**: restricción con tipo, fuente afectada, motivo exacto (vista,
  código ORA- o DPY-) e impacto en la confianza.
- **Recommendation**: acción sugerida con alcance, riesgo, prerrequisitos y
  necesidad de validación humana. Nunca se ejecuta.

## Origen de la evidencia

Cada observación declara su tipo de fuente, porque afecta licenciamiento,
confianza y trazabilidad:

```text
sql          núcleo SQL (vistas no licenciadas)
licensed     ASH/AWR (requiere licencia declarada)
platform     adaptador de plataforma (aws_rds, onprem_ssh, oci)
lab          fixture de laboratorio (solo pruebas)
```

El motor RCA no decide distinto según el origen; solo lo usa para la confianza
(fuentes independientes) y el reporte.

## Estados de revisión

```text
OK          revisado, sin problema (evidencia negativa útil)
INFO        dato contextual sin juicio
WARNING     anomalía leve
PROBLEM     anomalía relevante
CRITICAL    anomalía grave
TIMEOUT     la fuente no respondió a tiempo
ERROR       fallo técnico (permiso, vista inexistente, conexión)
SKIPPED     no aplica (característica ausente, por ejemplo RAC en standalone)
UNKNOWN     no se pudo determinar responsablemente
```

## Tipos de limitación

```text
permission_denied     falta de grant (por ejemplo ORA-00942, ORA-01031)
timeout               consulta o conexión excedió su tiempo
connection_failed     no se pudo conectar (por ejemplo ORA-12170, ORA-01017)
not_licensed          fuente licenciada sin licencia declarada
license_mismatch      licencia declarada pero parámetro de la base incoherente
adapter_missing       la evidencia requiere un adaptador no configurado
not_applicable        la característica no existe en el target
unsupported_version   la vista o columna no existe en la versión
partial_data          datos incompletos o truncados
```

## Niveles

```text
severity:   info, warning, critical, blocker   (severidad técnica del hallazgo)
confidence: low, medium, high                  (confianza del diagnóstico)
```

La severidad describe el hallazgo; no determina el rol causal.

## Datos sensibles

Texto de SQL, valores de bind, nombres de máquina, programa y usuario de
sistema operativo se recolectan solo cuando la spec lo justifique y se
enmascaran en reportes por defecto. Nunca se recolectan datos de tablas de
negocio.

## Reglas

- `OK` se conserva para descartar hipótesis.
- `TIMEOUT` y `ERROR` siempre generan una limitación con motivo exacto.
- `SKIPPED` no es un hallazgo ni penaliza; se reporta para transparencia.
- `CRITICAL` no implica causa principal sin correlación.
- Una lista vacía por falta de permisos es `ERROR`, nunca `OK`.
- `UNKNOWN` se usa solo cuando el estado no puede determinarse responsablemente.
