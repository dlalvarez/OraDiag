# Manejo de errores y timeouts

Todo conector, consulta y collector futuro debe tener timeout. Ninguna capa debe quedar colgada indefinidamente.

## Reglas

- Todo connector debe tener timeout configurable.
- Toda consulta debe tener timeout configurable.
- Todo collector debe fallar de forma controlada.
- Un timeout es evidencia o limitación, no un crash.
- El diagnóstico parcial es preferible a quedarse colgado.
- Los estados `TIMEOUT`, `ERROR` y `SKIPPED` deben registrarse y reportarse.
- Una capa fallida no debe impedir revisar otras capas independientes.

## Continuidad por capas

Si SSH falla, se puede intentar SQL si hay ruta disponible. Si SQL falla, se pueden analizar logs o sistema operativo si existen accesos. Si la base está caída, OraDiag debe explicar qué pudo y no pudo evaluar.

## Reporte

El reporte debe mostrar revisiones no evaluadas, motivo, impacto en confianza y acciones seguras para obtener evidencia adicional.
