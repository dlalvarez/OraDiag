# Manejo de síntomas

El síntoma reportado es opcional. Sirve para priorizar revisiones, ordenar hipótesis y presentar contexto, pero nunca decide la causa por sí mismo. La evidencia manda sobre el síntoma.

## Taxonomía inicial determinística

```text
cannot_connect
connection_hangs
errors
slow_performance
partial_impact
availability_down
unspecified
```

## Reglas

- Si no hay síntoma, se usa `unspecified` y el perfil elegido guía la ejecución.
- Si el síntoma contradice la evidencia, se reporta la contradicción.
- No se requiere IA para interpretar síntomas en fases iniciales.
- La IA podrá considerarse como ayuda opcional futura, nunca como fuente de verdad sin evidencia técnica.

## Riesgos de sesgo

Un síntoma puede inducir anclaje: por ejemplo, asumir que lentitud es I/O sin revisar locks o waits. OraDiag debe mitigar el sesgo manteniendo revisiones OK, evidencia negativa, dominios alternativos y limitaciones explícitas.
