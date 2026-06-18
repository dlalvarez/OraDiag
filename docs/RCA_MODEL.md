# Modelo RCA

OraDiag no debe conformarse con encontrar problemas. Debe razonar cuál evidencia explica mejor el incidente reportado, qué hallazgos solo contribuyen, qué hallazgos están relacionados, cuáles son incidentales, qué hipótesis fueron descartadas y qué no pudo evaluarse.

## Roles causales

- `primary_cause`: causa probable principal que explica el incidente con mayor soporte.
- `contributing_factor`: condición que agrava o facilita el incidente, pero no lo explica por sí sola.
- `related_finding`: hallazgo conectado al contexto del incidente sin probar causalidad directa.
- `incidental_finding`: anomalía real pero sin relación causal demostrada.
- `ruled_out`: hipótesis descartada por evidencia negativa o resultado OK.
- `not_evaluated`: revisión no ejecutada por error, permiso, timeout o no aplicabilidad.
- `unknown`: no hay evidencia suficiente para clasificar.

## Confianza

La confianza debe ser `low`, `medium` o `high` según consistencia temporal, especificidad, cantidad de fuentes independientes, ausencia de contradicciones y severidad de limitaciones. Alta confianza requiere evidencia directa y pocas limitaciones. Baja confianza debe expresarse como hipótesis, no como certeza.

## Evidencia positiva, negativa y limitaciones

La evidencia positiva soporta una causa. La evidencia negativa descarta hipótesis y debe aparecer como revisión OK o `ruled_out`. Las limitaciones explican lo no evaluado por permisos, timeouts, errores o falta de aplicabilidad.

## Múltiples problemas simultáneos

Si hay varios problemas, OraDiag debe priorizar el que mejor explica el incidente reportado. Los demás deben clasificarse como contribuyentes, relacionados o incidentales. Si dos causas compiten con evidencia similar, debe declararse ambigüedad y confianza menor.

## Prohibiciones

No se permiten conclusiones sin evidencia, recomendaciones peligrosas sin advertencia ni usar el síntoma como única prueba causal.
