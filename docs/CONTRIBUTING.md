# Contribuir a OraDiag

Toda contribución respeta `.specify/memory/constitution.md` como fuente
normativa principal, `CLAUDE.md` como guía operativa y `docs/` como
documentación rectora complementaria.

## Flujo de trabajo

1. **Planeación**: la spec se escribe completa con Spec Kit (`spec.md`,
   `plan.md`, `data-model.md`, `contracts/`, `tasks.md`) y se aprueba antes de
   implementar.
2. **Implementación**: Claude Code implementa el `tasks.md` aprobado, tarea por
   tarea, con pruebas.
3. **Revisión**: PR hacia `develop-claude` con la plantilla del repositorio.

Ramas: `develop-claude` es la rama integradora; una rama por spec
(`spec/NNN-nombre`) creada desde ella; `main` solo recibe versiones estables.

## Reglas

1. Identificar la spec a la que pertenece el cambio.
2. No implementar nada fuera de la spec activa.
3. Mantener la diferencia entre RCA, health check y capacity planning.
4. No consultar tablas de negocio.
5. Solo sentencias `SELECT`; ninguna acción que cambie estado.
6. Fuentes licenciadas solo en `sources/licensed/` y con licencia declarada.
7. Núcleo sin dependencias de proveedores cloud ni SSH.
8. Manejo controlado de errores y timeouts en toda fuente.
9. Actualizar documentación, matriz de trazabilidad y decision log cuando
   cambien reglas, modelos o decisiones.
10. Registrar ideas fuera de alcance en `docs/BACKLOG.md`.
11. Marcar como `propuesta de desviación` cualquier cambio fuera de la
    constitución, spec activa, plan aprobado o roadmap, y no implementarlo sin
    autorización humana explícita.

## Criterios antes de abrir PR

- La PR declara la spec relacionada.
- El alcance coincide con el `tasks.md` aprobado.
- El fuera de alcance fue respetado.
- La suite completa pasa (`uv run pytest -q`).
- La documentación relevante fue actualizada.
- Cualquier desviación fue declarada, justificada y autorizada.
