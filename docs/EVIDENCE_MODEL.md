# Modelo de evidencias

Toda conclusión relevante debe tener evidencia. La ausencia de evidencia por falla de acceso debe registrarse como limitación, no ignorarse.

## Entidades

- **Evidence**: dato técnico observado, con fuente, timestamp, alcance, valor y relación con una revisión.
- **ReviewResult**: resultado de una revisión con estado, severidad, evidencia, limitaciones y datos detallados.
- **Diagnosis**: conclusión RCA con dominio, rol causal, confianza, evidencias y recomendaciones.
- **Limitation**: restricción por error, timeout, permisos, no aplicabilidad o datos incompletos.
- **Recommendation**: acción sugerida segura, con riesgo, prerequisitos y validación humana si aplica.
- **DetailedData**: datos puntuales como sesiones, usuarios, módulos, servicios, SQL_ID, wait events, wait_class, inst_id y con_id.

## Estados de revisión

```text
OK
INFO
WARNING
PROBLEM
CRITICAL
TIMEOUT
ERROR
SKIPPED
UNKNOWN
```

## Niveles

```text
severity: info, warning, critical, blocker
confidence: low, medium, high
```

## Reglas

- `OK` debe conservarse para descartar hipótesis.
- `TIMEOUT`, `ERROR` y `SKIPPED` deben alimentar limitaciones.
- `CRITICAL` no implica causa principal sin correlación.
- `UNKNOWN` debe usarse solo cuando el estado no pueda determinarse responsablemente.
