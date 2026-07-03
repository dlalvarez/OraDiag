# Data Model: Gobierno y Constitución SDD

Este modelo es documental. No define clases Python, esquemas de base de datos ni Evidence Payload.

## Entidades

### Constitución SDD

- **Propósito**: Fuente normativa principal de OraDiag/OraRCA.
- **Campos documentales**: versión, principios, restricciones técnicas, proceso SDD, agrupación de specs, governance, asuntos pendientes.
- **Reglas de validación**:
  - Debe gobernar specs, planes, tareas, implementaciones y PRs.
  - Debe mantener control de desviaciones.
  - Debe preservar que OraDiag es RCA, no health check.

### Documento Rector

- **Propósito**: Fuente complementaria de propósito, alcance, fuera de alcance y principios no negociables.
- **Campos documentales**: definición formal, alcance, fuera de alcance, principios, RCA vs health check, errores/timeouts, evidencia, recomendaciones.
- **Reglas de validación**:
  - No reemplaza la constitución.
  - Debe mantenerse consistente con el foco RCA.

### Roadmap Agrupado

- **Propósito**: Secuencia oficial de specs y fases.
- **Campos documentales**: agrupación `000` a `008`, fases, alcance, fuera de alcance, criterios de aceptación, pruebas esperadas.
- **Reglas de validación**:
  - No debe agregar fases sin autorización constitucional.
  - Debe impedir adelantar fases futuras.

### Spec SDD

- **Propósito**: Definir qué se quiere lograr y por qué para una fase o agrupación concreta.
- **Campos mínimos**: fase o agrupación, fuentes rectoras, alcance, fuera de alcance, criterios de evidencia, manejo de errores/timeouts, seguridad, pruebas, trazabilidad, desviaciones.
- **Reglas de validación**:
  - Debe respetar constitución y roadmap.
  - Debe declarar explícitamente cualquier `propuesta de desviación`.

### Plan SDD

- **Propósito**: Definir cómo se verificará y organizará el trabajo autorizado por una spec.
- **Campos mínimos**: resumen, contexto, Constitution Check, estructura de artefactos, investigación, diseño aplicable, validación.
- **Reglas de validación**:
  - Debe incluir Constitution Check explícito.
  - No debe introducir alcance fuera de la spec.

### Lista de Tareas

- **Propósito**: Convertir plan y spec en trabajo verificable.
- **Campos mínimos**: ID, descripción, archivo objetivo, dependencia, historia asociada cuando aplique, criterio de completitud.
- **Reglas de validación**:
  - Las tareas deben ser pequeñas y verificables.
  - Las tareas no deben adelantar fases futuras.

### Pull Request

- **Propósito**: Unidad revisable de cambio.
- **Campos mínimos**: spec/fase relacionada, cumplimiento constitucional, pruebas ejecutadas, documentación actualizada, desviaciones autorizadas.
- **Reglas de validación**:
  - No debe mezclar cambios fuera de alcance sin autorización.
  - Debe declarar documentación y pruebas relevantes.

### Backlog

- **Propósito**: Registro de ideas futuras.
- **Campos documentales**: idea, fase probable, restricciones, dependencia de spec/plan/tareas.
- **Reglas de validación**:
  - No autoriza implementación por sí mismo.
  - Las ideas requieren spec, plan y tareas antes de implementarse.

### Decision Log

- **Propósito**: Registro de decisiones relevantes y consecuencias.
- **Campos documentales**: ID, estado, decisión, consecuencia.
- **Reglas de validación**:
  - Debe registrar decisiones importantes o desviaciones aceptadas cuando corresponda.

### Matriz de Trazabilidad

- **Propósito**: Vincular principios, documentos, fases y pruebas futuras.
- **Campos documentales**: principio rector, archivo fuente, fases relacionadas, pruebas futuras.
- **Reglas de validación**:
  - Debe permitir auditar que una fase respeta los principios aplicables.

### Propuesta de Desviación

- **Propósito**: Marcar cambios fuera de constitución, spec activa, plan aprobado o roadmap.
- **Campos mínimos**: descripción, motivo, impacto, alternativa, autorización humana explícita.
- **Reglas de validación**:
  - No debe implementarse sin autorización humana explícita.
  - No puede justificarse por preferencia, facilidad o analogía con OraHealth/OraParity.

## Relaciones

- La Constitución SDD gobierna todos los artefactos.
- El Documento Rector complementa la Constitución SDD.
- El Roadmap Agrupado limita Specs SDD por fase.
- Una Spec SDD produce un Plan SDD.
- Un Plan SDD habilita una Lista de Tareas.
- Un Pull Request debe referenciar spec/fase y tareas aplicables.
- El Backlog registra ideas, pero no habilita implementación.
- El Decision Log registra decisiones y desviaciones aceptadas cuando corresponda.
- La Matriz de Trazabilidad enlaza principios con fases y pruebas futuras.

## State Transitions

```text
Idea futura -> Backlog -> Spec SDD -> Plan SDD -> Tasks -> Pull Request -> Revisión -> Aceptado/Rechazado
```

```text
Cambio fuera de alcance -> Propuesta de Desviación -> Autorización humana -> Plan/Spec actualizados -> Tareas
```

Sin autorización humana explícita, una `propuesta de desviación` permanece fuera de alcance.
