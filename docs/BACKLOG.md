# Backlog

Ideas identificadas que no forman parte de ninguna spec vigente. Incorporar
cualquiera requiere decisión explícita y su ubicación en el roadmap.

## Candidatas

- Histórico local de incidentes con resolución confirmada por humano (base de
  la spec 012).
- Comparación de incidentes similares a partir del histórico.
- Knowledge base de recomendaciones seguras por hipótesis causal.
- Reportes enriquecidos con línea de tiempo y anexos.
- Perfiles personalizados definidos por archivo de configuración.
- Adaptador OCI (Base DB, Exadata y Autonomous), cuando haya bases en OCI.
- Integraciones de notificación o tickets (n8n, correo, chat). Requieren
  aprobación de seguridad.
- Exponer OraDiag como servidor MCP para asistentes de IA. Requiere spec propia
  y aprobación de seguridad por la exposición de evidencia a modelos externos.
- IA opcional para resumir evidencia, sin reemplazar reglas determinísticas.

## Descartadas por ahora

- **Statspack** como fuente de histórico sin packs: descartado por decisión del
  responsable del proyecto (ADR-0011). Se reconsidera si se confirma que no hay
  licencia de Diagnostics Pack.
- **Muestreo propio de `V$SESSION`** (ASH casero): convertiría a OraDiag en un
  agente permanente con overhead y almacenamiento propios.
- **Performance Insights / Database Insights como fuente base**: acoplaría el
  núcleo a AWS (ADR-0010). Puede evaluarse dentro del adaptador AWS RDS.

## Incorporadas a specs vigentes

- Integración con AWR licenciado: spec 006.
- Validadores de que no existan consultas a tablas de negocio, de solo lectura y
  de vistas licenciadas: guardrails de la constitución, se implementan desde la
  spec 003.
- Soporte RAC, Multitenant y Standby: spec 011.
