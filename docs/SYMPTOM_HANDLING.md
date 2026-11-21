# Manejo de síntomas

El síntoma reportado es opcional. Sirve para priorizar revisiones, ordenar
hipótesis y presentar contexto, pero nunca decide la causa. La evidencia manda.

## Taxonomía determinística

```text
cannot_connect      no se puede establecer conexión
connection_hangs    la conexión se establece pero no responde
errors              la aplicación recibe errores ORA-
slow_performance    lentitud generalizada o puntual
partial_impact      afecta a un subconjunto (servicio, módulo, usuario)
availability_down   base o instancia no disponible
unspecified         sin síntoma declarado
```

## Datos del reporte

Además de la categoría, el reporte del incidente puede incluir:

- **Ventana**: inicio y fin aproximados, o "en curso". Es el dato más valioso
  para la correlación y se pide siempre.
- **Alcance**: servicio, módulo, usuario de base de datos o `SQL_ID` afectados,
  cuando se conozcan.
- **Errores observados**: códigos ORA- reportados por la aplicación.

Ninguno de estos datos es evidencia: son pistas que el motor contrasta con lo
observado.

## Reglas

- Sin síntoma se usa `unspecified` y el perfil guía la ejecución.
- Sin ventana declarada se asume incidente en curso ("ahora").
- Si el síntoma contradice la evidencia, se reporta la contradicción.
- El síntoma no requiere IA para interpretarse. Cualquier uso futuro de IA
  requiere una spec propia y aprobación de seguridad, y nunca reemplaza la
  evidencia técnica.

## Riesgos de sesgo

El síntoma induce anclaje: por ejemplo, asumir que la lentitud es I/O sin
revisar bloqueos o waits. Se mitiga evaluando también los dominios alternativos,
conservando los OK como evidencia negativa y declarando las limitaciones.
