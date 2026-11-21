# Modelo RCA

OraDiag no se conforma con encontrar problemas. Razona qué evidencia explica
mejor el incidente reportado en su ventana de tiempo, qué hallazgos solo
contribuyen, cuáles están relacionados, cuáles son incidentales, qué hipótesis
se descartaron y qué no pudo evaluarse. El diseño detallado del motor es
responsabilidad de la spec 003; este documento fija los conceptos.

## Roles causales

- `primary_cause`: la hipótesis que mejor explica el incidente, con cadena de evidencia completa dentro de la ventana.
- `contributing_factor`: condición que agrava o facilita el incidente pero no lo explica por sí sola.
- `related_finding`: hallazgo conectado al contexto del incidente sin causalidad demostrada.
- `incidental_finding`: anomalía real sin relación temporal o causal con el incidente.
- `ruled_out`: hipótesis descartada por evidencia negativa (un OK relevante).
- `not_evaluated`: hipótesis que no pudo evaluarse por permiso, timeout, error, falta de licencia o falta de adaptador.
- `unknown`: no hay evidencia suficiente para asignar rol.

## Conceptos del motor

- **Ventana del incidente**: intervalo `[inicio, fin]` declarado o "ahora". Toda
  observación tiene marca de tiempo o intervalo; lo que no se solapa con la
  ventana no puede ser causa principal.
- **Hipótesis causal**: explicación candidata con dominio causante (por ejemplo,
  "contención por bloqueo de fila", dominio Base de datos).
- **Regla causal**: patrón declarativo que conecta observaciones con una
  hipótesis y define qué evidencia la confirma, qué la descarta y qué la
  debilita. Las reglas son determinísticas y versionadas.
- **Cadena de evidencia**: secuencia de observaciones enlazadas que sostiene una
  hipótesis. Ejemplo: sesión bloqueadora con transacción abierta -> N sesiones
  en `enq: TX - row lock contention` -> aumento de tiempo de respuesta en la
  ventana -> síntoma `slow_performance`.
- **Explicación alternativa**: otra hipótesis con evidencia comparable. Si
  existe, la confianza baja y se declara la ambigüedad.

## Criterios de confianza

La confianza es `low`, `medium` o `high` y siempre se acompaña de su motivo.
Se evalúa con criterios explícitos, no con un puntaje opaco:

| Criterio | Sube la confianza | Baja la confianza |
|---|---|---|
| Coincidencia temporal | Evidencia dentro de la ventana y en orden causal | Evidencia fuera de la ventana o sin marca de tiempo |
| Cadena causal | Cadena completa del origen al síntoma | Eslabones faltantes |
| Fuentes independientes | Varias fuentes concuerdan | Una sola fuente |
| Alternativas | Hipótesis competidoras descartadas con OK | Alternativas sin evaluar o con evidencia similar |
| Limitaciones | Dominios relevantes evaluados | Dominios relevantes en `not_evaluated` |

`high` exige cadena completa, coincidencia temporal y alternativas descartadas.
`low` se expresa como hipótesis, nunca como certeza.

## Evidencia positiva, negativa y limitaciones

La evidencia positiva soporta una hipótesis. La evidencia negativa la descarta
y aparece como OK relevante o `ruled_out`. Las limitaciones explican lo no
evaluado y su impacto en la confianza.

## Múltiples problemas simultáneos

Se prioriza la hipótesis que mejor explica el incidente reportado en su ventana.
Las demás se clasifican como contribuyentes, relacionadas o incidentales. Si dos
hipótesis compiten con evidencia equivalente, se reportan ambas, se declara la
ambigüedad y la confianza no puede ser `high`.

## Prohibiciones

- Elegir la causa principal por severidad o por cantidad de hallazgos.
- Concluir sin evidencia o usando el síntoma como única prueba.
- Recomendar acciones peligrosas sin advertencia ni validación humana.
- Ocultar limitaciones que afectan la confianza.
