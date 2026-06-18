# Contribuir a OraDiag

Toda contribución debe respetar `docs/DOCUMENTO_RECTOR.md` como fuente de verdad.

## Reglas de contribución

1. Identificar la fase del roadmap a la que pertenece el cambio.
2. No implementar funcionalidad fuera de fase.
3. Mantener la diferencia entre RCA, health check y capacity planning.
4. No consultar tablas de negocio.
5. Actualizar documentación cuando cambien reglas, modelos o decisiones.
6. Registrar decisiones importantes en `docs/DECISION_LOG.md`.
7. Registrar ideas fuera de alcance en `docs/BACKLOG.md`.
8. Agregar o actualizar pruebas según criterios de aceptación de la fase.
9. Mantener manejo controlado de errores, timeouts y fallas parciales cuando aplique.
10. Preservar evidencia obligatoria y trazabilidad.

## Criterios antes de abrir PR

- La PR declara fase relacionada.
- El alcance implementado coincide con el roadmap.
- El fuera de alcance fue respetado.
- La documentación relevante fue actualizada.
- Las pruebas o validaciones esperadas fueron ejecutadas o justificadas.
